from flask import Flask,request,render_template,redirect,url_for
import mysql.connector
app=Flask(__name__)

mysql=mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='password',
    database='baza'
)
@app.route('/',methods=['GET','POST'])
def start():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.cursor()
        cursor.execute('insert into accounts value(%s,%s)',params=(username,password,))
        mysql.commit()
        cursor.close()
        return redirect(url_for('yes',username=username, password=password))
    return render_template('index.html')
@app.route('/welcome')
def yes():
    username=request.args['username']
    password=request.args['password']
    return f"Hi {username} ,your password is:{password}"
@app.route('/login',methods=['GET','POST'])
def go():
    if request.method=='POST':
        message=False
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.cursor()
        cursor.execute('select username,password from accounts where username=%s and password=%s',params=(username,password,))
        data=cursor.fetchall()
        cursor.close()
        if data:
            return redirect(url_for('yes',username=username, password=password))
        else:
            return render_template('login.html',message=True)
    else:
        return render_template('login.html')
app.run()