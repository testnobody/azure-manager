# Azure-manager
## Manage your VM in Azure（multi users）.
## 管理你在AZURE的机器 多用户

### 8.2日更新:

### 新增windows机器选择（2012-2019），硬盘默认64GB，建议选择2012/2016配置
### 修复了一个身份验证BUG，增加安全性，但是还是很简陋，尽量保护好自己的管理网址和登录管理信息哦。

## 5.Or you can deploy in heroku!!
### 或者你可以忽略以上所有步骤，一键部署到heroku
A simple Python example application that's ready to run on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Default VM infomation:
### 开出来的机器默认登录密码
windows/linux通用默认账号密码
USERNAME : defaultuser<br>
PASSWORD : Thisisyour.password1

linux默认root密码
USERNAME : root<br>
PASSWORD : ppxwo123

## 1.Install Python 3.9.4
### 安装python 3.9.4

## 2.Install Python Library
### 安装依赖包
pip install -r requirements.txt

## 3.Set your Secret Key 
### 随便设置一个密钥（cookie相关，13行）
Set random string in app.py(line 13)

### 设置面板管理密码（app.py 7-8行;默认账号密码：admin admin123）
Set admin password in app.py(line 7-8)

## 4.RUN!! 运行
python app.py

Visit 127.0.0.1:5000 and enjoy yourself.

## 5.Or you can deploy in heroku!!
### 或者你可以忽略以上所有步骤，一键部署到heroku
A simple Python example application that's ready to run on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## notice1.面板登录的身份验证有点简陋，担心安全性的在公网慎用哦

## notice2. Azure key 获取方法
登录AZURE，在portal.azure.com右上角选择命令行bash 输入 az ad sp create-for-rbac --name randomstring

