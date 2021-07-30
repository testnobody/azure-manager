import threading
from flask import Flask, render_template, request, url_for, redirect, flash, make_response
import function
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
# 请将 xxx 替换为随机字符
app.config['SECRET_KEY'] = 'c2jf932hibfiuebvwievubheriuvberv'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)



class User(db.Model):

  account = db.Column(db.String(100),primary_key=True)
  client_id = db.Column(db.String(100))
  client_secret = db.Column(db.String(100))
  tenant_id = db.Column(db.String(100))
  subscription_id = db.Column(db.String(100))

  def __init__(self, account, client_id,client_secret,tenant_id,subscription_id):
    self.account = account
    self.client_id = client_id
    self.client_secret = client_secret
    self.tenant_id = tenant_id
    self.subscription_id = subscription_id








@app.route('/')
def index():
    # 获取cookie账号信息
    username = request.cookies.get('username')
    password = request.cookies.get('password')


    return render_template('index.html', users=User.query.all())







@app.route('/account/add', methods=['GET', 'POST'])
def accountadd():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        account = request.form.get('account')
        client_id = request.form.get('client_id')
        client_secret = request.form.get('client_secret')
        tenant_id = request.form.get('tenant_id')
        subscription_id = request.form.get('subscription_id')
        # 验证数据
        if not account or not client_id or not client_secret or not tenant_id or not subscription_id:
            flash('输入错误')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到cookie
        u = User(account, client_id,client_secret,tenant_id,subscription_id)
        db.session.add(u)
        db.session.commit()

        resp = make_response(redirect(url_for('index')))

        flash('添加管理账户成功')
        return resp

    return render_template('account.html')


@app.route('/account/delete')
def accountdel():
    account = request.args.get('account')


    dele = User.query.filter(User.account == account).first()
    db.session.delete(dele)
    db.session.commit()





    flash('删除账户成功')
    resp = make_response(redirect(url_for('index')))
    return resp


@app.route('/account/list')
def list():
    account = request.args.get('account')
    result = User.query.filter(User.account == account).all()

    client_id = result[0].client_id
    client_secret = result[0].client_secret
    tenant_id = result[0].tenant_id
    subscription_id = result[0].subscription_id

    credential = function.create_credential_object(tenant_id, client_id, client_secret)



    return render_template('list.html', dict=function.list(subscription_id, credential), account=account)


@app.route('/account/vm/create', methods=['GET', 'POST'])
def create_vm():
    account = request.args.get('account')
    print(account)

    if request.method == 'POST':
        result = User.query.filter(User.account == account).all()

        client_id = result[0].client_id
        client_secret = result[0].client_secret
        tenant_id = result[0].tenant_id
        subscription_id = result[0].subscription_id



        credential = function.create_credential_object(tenant_id, client_id, client_secret)
        tag = request.form.get('tag')
        location = request.form.get('location')
        size = request.form.get('size')
        os = request.form.get('os')
        set = request.form.get('set')
        rootpwd=request.form.get('rootpwd')
        ## 此处为VM默认登陆密码
        username = "defaultuser"
        password = "Thisisyour.password1"
        for i in range(int(set)):
            name = (tag + str(i + 1))
            function.create_resource_group(subscription_id, credential, name, location)
            threading.Thread(target=function.create_or_update_vm, args=(
            subscription_id, credential, name, location, username, password, size, os,rootpwd)).start()
        flash('创建中，请耐心等待VM创建完成，大约需要1-3分钟')



    return render_template('vm.html', account=account)


@app.route('/account/vm/delete/<string:tag>')
def delete_vm(tag):
    account = request.args.get('account')
    result = User.query.filter(User.account == account).all()

    client_id = result[0].client_id
    client_secret = result[0].client_secret
    tenant_id = result[0].tenant_id
    subscription_id = result[0].subscription_id





    credential = function.create_credential_object(tenant_id, client_id, client_secret)
    threading.Thread(target=function.delete_vm, args=(subscription_id, credential, tag)).start()
    flash("删除中，请耐心等待1-3分钟")


    #dict[account] = function.list(subscription_id, credential)
    return render_template('list.html', dict=function.list(subscription_id, credential), account=account)


@app.route('/account/vm/start/<string:tag>')
def start_vm(tag):
    account = request.args.get('account')

    result = User.query.filter(User.account == account).all()

    client_id = result[0].client_id
    client_secret = result[0].client_secret
    tenant_id = result[0].tenant_id
    subscription_id = result[0].subscription_id

    credential = function.create_credential_object(tenant_id, client_id, client_secret)
    threading.Thread(target=function.start_vm, args=(subscription_id, credential, tag)).start()
    flash("开机中，请耐心等待1-3分钟")
    #dict[account] = function.list(subscription_id, credential)
    return render_template('list.html', dict=function.list(subscription_id, credential), account=account)


@app.route('/account/vm/stop/<string:tag>')
def stop_vm(tag):
    account = request.args.get('account')

    result = User.query.filter(User.account == account).all()

    client_id = result[0].client_id
    client_secret = result[0].client_secret
    tenant_id = result[0].tenant_id
    subscription_id = result[0].subscription_id


    credential = function.create_credential_object(tenant_id, client_id, client_secret)
    threading.Thread(target=function.stop_vm, args=(subscription_id, credential, tag)).start()
    flash("关机中，请耐心等待1-3分钟")
    #dict[account] = function.list(subscription_id, credential)
    return render_template('list.html',  dict=function.list(subscription_id, credential), account=account)


@app.route('/account/vm/changeip/<string:tag>')
def changeip_vm(tag):
    account = request.args.get('account')

    result = User.query.filter(User.account == account).all()

    client_id = result[0].client_id
    client_secret = result[0].client_secret
    tenant_id = result[0].tenant_id
    subscription_id = result[0].subscription_id


    credential = function.create_credential_object(tenant_id, client_id, client_secret)
    try:
        threading.Thread(target=function.change_ip, args=(subscription_id, credential, tag)).start()
        flash("更换IP进行中，请耐心等待1-3分钟")
        return redirect(url_for('index'))
    except:
        flash("出现未知错误，请重试")


if __name__ == '__main__':
    db.create_all()
    app.run()
