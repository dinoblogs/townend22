from flask import Flask, render_template, request, redirect, session

from flask_sqlalchemy import SQLAlchemy
from fileinput import filename
import requests

from datetime import datetime




app = Flask(__name__)
app.secret_key = "krishna4704"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product.db"
db = SQLAlchemy(app)


class Product(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(800), nullable=False)
    SP = db.Column(db.String(100), nullable=False)
    MRP = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(400), nullable=False)
    rank = db.Column(db.Integer(), default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno}, {self.title},{self.MRP},{self.SP}, {self.img_url}'
    

@app.route('/')
def home():
    # product = Product(title="Vivo 11", desc="4GB Ram", img_url="http://tou.com", SP='12,000',MRP='15,000', rank=10)
    # db.session.add(product)
    # db.session.commit()

    dbms = Product.query.all()
    print(dbms)
    #db.session.commit()
    n = []
    if dbms == n or dbms == '':
        return render_template('index.html',error = 'Sorry No Items Available...😢', dbms=dbms , heading = 'Dino Phons' , title="Dino Phones", email="none@gmail.com", phone="8279692610", add="none", desc="This is my site")
    

    return render_template('index.html',error="Our Latest Products...", dbms=dbms , heading = 'Dino Phons' , title="Dino Phones", email="none@gmail.com", phone="8279692610", add="none", desc="This is my site")



@app.route('/contact')
def all_product():
    return render_template('contact.html')

@app.route('/add')
def create():
    return render_template('add_item.html')

# Post Request
@app.route('/create', methods=['POST'])
def handle_post():
    f = request.files['img']
    name1 = str(datetime.now())
    name1 = name1.replace("-", "")
    name1 = name1.replace(" ", "")
    name1 = name1.replace(":", "")
    name1 = name1.replace(".", "")
    f.save(f'static/{name1}.png')  
    #file
    title = request.form['name']
    sp = request.form['sp']
    rank = request.form['rank']
    mrp = request.form['mrp']
    desc = request.form['desc']
    product = Product(title=title, desc=desc, img_url=f'static/{name1}.png',rank = rank, SP=sp,MRP=mrp)
    db.session.add(product)
    db.session.commit()
    return redirect('/add')

@app.route('/del', methods=['GET'])
def del_phone():
    if request.method == 'GET':
        sno = request.args['sno']
        Product.query.filter_by(sno=sno).delete()
        db.session.commit()
        return redirect('/admin')
    else:
        return 'Error With Server!'

@app.route('/item/')
def red():
    return redirect('/')
@app.route('/item/<name>')
def items(name):
    dbms = Product.query.all()
    for i in dbms:
        sno = str(i.sno)
        name = str(name)
        if sno == name:
            print("found")
            return render_template('item.html',color=None, name = i.title ,url = i.img_url, desc = i.desc, MRP = i.MRP, SP=i.SP, rank = i.rank)
            break

        else:
            pass

    return redirect("/")


@app.route("/edit/<name1>")
def edit(name1):
    i  = Product.query.filter_by(sno=name1).first()
    return render_template("edit.html", site=name1,name = i.title ,url = i.img_url, desc = i.desc, MRP = i.MRP, SP=i.SP, rank = i.rank)
    # n.title = "Iphone"
    # db.session.commit()
@app.route("/change/<name>", methods=['POST'])
def change(name):
        #file
    title = request.form['name']
    sp = request.form['sp']
    rank = request.form['rank']
    mrp = request.form['mrp']
    desc = request.form['desc']
    i  = Product.query.filter_by(sno=name).first()
    i.title = title
    i.SP = sp
    i.MRP = mrp
    i.desc = desc
    i.rank = rank

    db.session.commit()

    return redirect('/add')

@app.route("/admin", methods=['GET'])
def admin():
    flag=request.args.get('flag') 
    if 'username' in session:
        if session['username'] == 'admin':
            if session['password'] == 'kanha0003':
                return render_template('/dashboard')
            else:
                pass

            
    else:
        return render_template('admin-login.html', flag = flag)

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        if session['username'] == 'admin':
            if session['password'] == 'kanha0003':
                dbms = Product.query.all()
                if dbms == []:
                    return render_template("dashboard.html" , dbms = dbms,error='No Item!!!')
                else:
                    return render_template("dashboard.html" , dbms = dbms)
    else:
        return render_template('admin-login.html')
@app.route("/auth" , methods=['POST'])
def auth():
    session['username'] = request.form["username"]
    session['password'] = request.form["password"]
    if session['username'] != "admin" or session['password'] != 'kanha0003':
        return redirect('/admin?flag=false')
    else:
        return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.pop('username',None)  
    session.pop('password',None)
    return redirect("/admin")  

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

