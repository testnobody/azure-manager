# Azure-manager
## Manage your VM in Azure（multi users）.
## 管理你在AZURE的机器 多用户

## Default VM infomation:
# 开出来的机器默认登录密码

USERNAME : defaultuser<br>
PASSWORD : Thisisyour.password1

USERNAME : root
PASSWORD : defaultuserpassword

## 1.Install Python 3.9.4

## 2.Install Python Library
pip install -r requirements.txt

## 3.Set your Secret Key 
# 随便设置一个密钥（cookie相关，13行）
Set random string in app.py(line 13)

# 设置面板管理密码（app.py 7-8行;默认账号密码：admin admin123）
Set admin password in app.py(line 7-8)

## 4.RUN!! 运行
python app.py

Visit 127.0.0.1:5000 and enjoy yourself.

## 5.deploy in heroku!!
# 一键部署到heroku
A simple Python example application that's ready to run on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# 6.No login verification yet, do not use it on the public network 
## 还没加入登陆页面，在公网慎用
