# iOS自动打包发布脚本(python版）
---
###使用方法
1、下载完成后，将autobuild.py以及exportOptions.plist文件放到你的项目跟目录下（即与xx.xcworkspace或者xx.xcworkspace在同一个目录下）  
2、打开autobuild.py，修改配置信息  
3、打开命令终端，进入项目根目录  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;a.如果你是xx.xcworkspace  
&emsp;&emsp;	`./autobuild.py -p youproject.xcodeproj`  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;b.如果你是xx.xcworkspace  
&emsp;&emsp; `./autobuild.py -w youproject.xcworkspace`  

4、等待终端回应，依据终端提示进行相关操作  
5、最终会在桌面生成带有时间戳的文件夹，含义ipa以及xcarchive文件

注：sendmail.py是发邮件脚本，若要打包发布成功后发送邮件通知某人，请在autobuild.py里引入该模块，调用即可。