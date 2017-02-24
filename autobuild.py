#!/usr/bin/env python
# -*- coding:utf-8 -*-

#./autobuild.py -p youproject.xcodeproj
#./autobuild.py -w youproject.xcworkspace

import argparse
import subprocess
import requests
import os
import datetime

#configuration for iOS build setting
CONFIGURATION = "Release"
EXPORT_OPTIONS_PLIST = "exportOptions.plist"

#发布版本号
VERSION = '1.0.0'
BUILD = '17021803'

#要打包的TARGET名字
TARGET = 'ULife'

#Info.plist路径
PLIST_PATH = "xxxxxx/Info.plist"

#存放路径以时间命令
DATE = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

#会在桌面创建输出ipa文件的目录
EXPORT_MAIN_DIRECTORY = "~/Desktop/" + TARGET + DATE

#xcarchive文件路径（含有dsym），后续查找BUG用途
ARCHIVEPATH = EXPORT_MAIN_DIRECTORY + "/%s%s.xcarchive" %(TARGET,VERSION)

#ipa路径
IPAPATH = EXPORT_MAIN_DIRECTORY + "/%s.ipa" %(TARGET)

#苹果开发者账号
APPLEID = 'xxxxxx'
APPLEPWD = 'xxxxx'

# configuration for pgyer
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
USER_KEY = "xxxxxx"
API_KEY = "xxxxx"
#设置从蒲公英下载应用时的密码
PYGER_PASSWORD = "xxxxx"

def cleanArchiveFile():
	cleanCmd = "rm -r %s" %(ARCHIVEPATH)
	process = subprocess.Popen(cleanCmd, shell = True)
	process.wait()
	print "cleaned archiveFile: %s" %(ARCHIVEPATH)

def uploadIpaToAppStore():
	print "iPA上传中...."
	altoolPath = "/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool"

	exportCmd = "%s --validate-app -f %s -u %s -p %s -t ios --output-format xml" % (altoolPath, IPAPATH, APPLEID,APPLEPWD)
	process = subprocess.Popen(exportCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	validateResult = process.returncode
	if validateResult == 0:
		print '~~~~~~~~~~~~~~~~iPA验证通过~~~~~~~~~~~~~~~~'
		exportCmd = "%s --upload-app -f %s -u %s -p %s -t ios --output-format normal" % (
		altoolPath, IPAPATH, APPLEID, APPLEPWD)
		process = subprocess.Popen(exportCmd, shell=True)
		(stdoutdata, stderrdata) = process.communicate()

		uploadresult = process.returncode
		if uploadresult == 0:
			print '~~~~~~~~~~~~~~~~iPA上传成功'
		else:
			print '~~~~~~~~~~~~~~~~iPA上传失败'
	else:
		print "~~~~~~~~~~~~~~~~iPA验证失败~~~~~~~~~~~~~~~~"

def parserUploadResult(jsonResult):
	resultCode = jsonResult['code']
	if resultCode == 0:
		downUrl = DOWNLOAD_BASE_URL +"/"+jsonResult['data']['appShortcutUrl']
		print "Upload Success"
		print "DownUrl is:" + downUrl
	else:
		print "Upload Fail!"
		print "Reason:"+jsonResult['message']

def uploadIpaToPgyer(ipaPath):
	print "ipaPath:"+ipaPath
	ipaPath = os.path.expanduser(ipaPath)
	ipaPath = unicode(ipaPath, "utf-8")
	files = {'file': open(ipaPath, 'rb')}
	headers = {'enctype':'multipart/form-data'}
	payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'2','isPublishToPublic':'2', 'password':PYGER_PASSWORD}
	print "uploading...."
	r = requests.post(PGYER_UPLOAD_URL, data = payload ,files=files,headers=headers)
	if r.status_code == requests.codes.ok:
		result = r.json()
		parserUploadResult(result)
	else:
		print 'HTTPError,Code:'+r.status_code

def exportArchive():
	exportCmd = "xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s" %(ARCHIVEPATH, EXPORT_MAIN_DIRECTORY, EXPORT_OPTIONS_PLIST)
	process = subprocess.Popen(exportCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	signReturnCode = process.returncode
	if signReturnCode != 0:
		print "export %s failed" %(TARGET)
		return ""
	else:
		return EXPORT_MAIN_DIRECTORY

def buildProject(project):
    archiveCmd = 'xcodebuild -project %s -scheme %s -configuration %s archive -archivePath %s -destination generic/platform=iOS' %(project, TARGET, CONFIGURATION, ARCHIVEPATH)
    process = subprocess.Popen(archiveCmd, shell=True)
    process.wait()

    archiveReturnCode = process.returncode
    if archiveReturnCode != 0:
        print "archive project %s failed" %(project)
        cleanArchiveFile()

def buildWorkspace(workspace):
	archiveCmd = 'xcodebuild -workspace %s -scheme %s -configuration %s archive -archivePath %s -destination generic/platform=iOS' %(workspace, TARGET, CONFIGURATION, ARCHIVEPATH)
	process = subprocess.Popen(archiveCmd, shell=True)
	process.wait()

	archiveReturnCode = process.returncode
	if archiveReturnCode != 0:
		print "archive workspace %s failed" %(workspace)
		cleanArchiveFile()

def xcbuild(options):
	project = options.project
	workspace = options.workspace

	if project is None and workspace is None:
		pass
	elif project is not None:
		buildProject(project)
	elif workspace is not None:
		buildWorkspace(workspace)

	#导出ipa文件
	exportarchive = exportArchive()
	print "~~~~~~~~~~~~~~~~是否上传到蒲公英~~~~~~~~~~~~~~~~"
	print "        1 不上传 (默认)"
	print "        2 上传 "
	isuploadpgyer = raw_input("您的决定：")
	if isuploadpgyer == "2" and exportarchive != "":
		uploadIpaToPgyer(IPAPATH)

	print "~~~~~~~~~~~~~~~~是否上传到AppStore~~~~~~~~~~~~~~~~"
	print "        1 不上传 (默认)"
	print "        2 上传 "
	isuploadappstore = raw_input("您的决定：")
	if isuploadappstore == '2':
		uploadIpaToAppStore()
	else:
		print "~~~~~~~~~~~~~~~~是否删除archive文件~~~~~~~~~~~~~~~~"
		print "        1 保留 (默认)"
		print "        2 删除 "
		iscleararchive = raw_input("您的决定：")
		if iscleararchive == "2":
			cleanArchiveFile()


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-w", "--workspace", help="Build the workspace name.xcworkspace.", metavar="name.xcworkspace")
	parser.add_argument("-p", "--project", help="Build the project name.xcodeproj.", metavar="name.xcodeproj")

	options = parser.parse_args()

	print "options: %s" % (options)

	os.system('/usr/libexec/PlistBuddy -c "Set:CFBundleShortVersionString %s" %s' % (VERSION,PLIST_PATH))
	os.system('/usr/libexec/PlistBuddy -c "Set:CFBundleVersion %s" %s' % (BUILD, PLIST_PATH))

	xcbuild(options)

if __name__ == '__main__':
	main()
