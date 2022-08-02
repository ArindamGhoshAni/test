from flask  import   Flask , render_template, request
import numpy as np
import jsonify
import pickle
import pymongo
from pymongo import MongoClient
from pymongo import collection
import os

app = Flask(__name__)

picFolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picFolder

client = MongoClient("mongodb+srv://Arin:Arindam@insurance.lx7vz.mongodb.net/?retryWrites=true&w=majority")
db = client["storedata"]
collection = db["user"]

model = pickle.load(open('insurance_predict_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'pic1.jpg')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'],'pic2.jpg')
    return render_template('home.html',user_image = pic1)

@app.route('/index',methods=['GET'])
def hello():
    return render_template('index.html')
    
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['a'])
        sex = request.form['sex']
        bmi = float(request.form['c'])
        child = int(request.form['d'])
        smoker = request.form['smoker']
        region = request.form['region']
        prediction = model.predict([[age , sex, bmi, child, smoker, region]])
        output=round(prediction[0],2)
        collection.insert_one({"age" : age, "sex": sex,"bmi":bmi,"child":child,"smoker":smoker,"region":region,"Predicted Price":output})
        return render_template('index.html',prediction_text="Your predicted premium is : {}".format(output))
    else:
        return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True)