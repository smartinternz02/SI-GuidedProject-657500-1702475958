import numpy as np
import os
from platformdirs import user_documents_dir, user_documents_path, user_downloads_dir
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, redirect,render_template,request, url_for

app=Flask(__name__)

model=load_model("C:/Users/JAYARAMU/Downloads/Flask/Flask/updated-xception-diabetic-retinopathy.h5")
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/')
def register():
    return render_template("register.html")

@app.route('/')
@app.route('/afterreg',methods=['POST'])
def afterreg():
    x = [x for x in request.form.values()]
    print(x)
    data = {
        '_id' : x[1],
        'name' : x[0],
        'psw' : x[2]
    }
    print(data)

    query = {'_id' : {'Seq' : data['_id']}}

    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if((len(docs.all())) == 0):
        url = my_database.create_document(data)
        return render_template('register.html', pred="Register Success")
    else:
        return render_template('register.html', pred="Already a Member")
    
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/')
@app.route('/afterlogin',methods=['POST'])
def afterlogin():
    user = request.form['_id']
    passw = request.form['psw']
    print(user,passw)
    query({'_id' : {'Seq' : user}})

    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if(len(docs.all()) == 0):
        return render_template('login.html', pred="Invalid")
    else:
        user_downloads_dir == docs.all()[0]
        if user == user_documents_dir['_id'] and passw==user_documents_path['psw']:
            return redirect(url_for('prediction'))
        else:
            return render_template('login.html', pred="Invalid credentials")

@app.route('/')
def logout():
    return render_template('logout.html')

@app.route('/')
def prediction():
    return render_template('prediction.html')
    

@app.route('/')
@app.route('/result',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        img=image.load_img(filepath,target_size=(299,299))
        x=image.img_to_array(img)
        x=np.expand_dims(x,axis=0)
        pred=np.argmax(model.predict(x),axis=1)
        index=['No Diabetic Retinopathy','Mild DR','Moderate DR','Severe DR','Proliferative DR']
        text="The Classified Retinopathy is : " +str(index[pred[0]])
    return text

if __name__=='__main__':
    app.run(debug=True)