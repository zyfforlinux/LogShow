from flask import Flask,url_for,redirect,render_template,Blueprint
from flask import request,session,flash,abort
import chartkick
import os
from form import LoginForm
app = Flask(__name__)
#Load chartkick
ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")
#Load configure file
app.config.from_object("cmd")
app.secret_key=app.config['SECERT_KEY']
#show chart
@app.route("/show")
def index():
    #view sesson info
    if not session.get("login_in"):
        abort(401)
    count = 1
    #storage data
    datalist=[]
    while True:
        tmplist=[]
        #set config variable
        CMD="CMD"+str(count)
        TYPE = "GRAPHTYPE"+str(count)
        TITLE= "TITLE" + str(count)
        #Get config value
        if CMD in app.config.keys() or TYPE in app.config.keys():
            #Deal With Data
            #execute shell command
            result = os.popen(app.config[CMD])
            #get result
            result = result.read()
            #split result
            result = result.split("\n")[0:-1]
            data=[]
            #iterates result
            for i in result:
                i = i.split()
                data.append(i)
            #story result
            tmplist.append(app.config[TYPE])
            tmplist.append(data)
            tmplist.append(app.config[TITLE])
            count = count + 1
            datalist.append(tmplist)
        else:
            break
    #if not cmmand it will show error.html
    if count == 1:
        return render_template("error.html")
    else:
        return render_template("charts.html",datalist=datalist,title=app.config['TITLE1'])
#Set login
@app.route("/",methods=['post','get'])
@app.route("/index",methods=['post','get'])
def login():
    error=None
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == app.config['USERNAME'] and form.password.data == app.config['PASSWORD']:
            session["login_in"] = True
            flash("You were login")
            return redirect(url_for("index"))
        else:
            if form.username.data != app.config['USERNAME']:
                error="Invalid username"
            else:
                error="Invalid password"
            return render_template('login.html',form=form,error=error)
    return render_template('login.html',form=form)

#Set logout
@app.route("/logout")
def logout():
    session.pop("login_in",None)
    flash("You were logged out")
    return redirect(url_for('login'))

#this is a custome a filter function,but don't use.
#this function you can't to see
def filter_type(type):
    if type == 1:
        return "line_chart"
    elif type == 2:
        return "pie_char"
    elif type == 3:
        return "column_chart"
    else:
        return "bar_chart"
app.jinja_env.filters['switchtype'] = filter_type

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")
