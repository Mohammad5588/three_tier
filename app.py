from flask import Flask, render_template, request
from utils import model_predict
import mysql.connector

app = Flask(__name__)

# Database connection
db_connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='sql321',
    port='3306',
    database='email_classifier'
)
cursor = db_connection.cursor()

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    email = request.form.get('content')
    prediction = model_predict(email)
    insert_into_database(email,prediction)
    return render_template("index.html", prediction=prediction, email=email)

def insert_into_database(email, prediction):
    sql = "INSERT INTO emails (content, prediction) VALUES (%s, %s)"
    val = (email, prediction)
    cursor.execute(sql, val)
    db_connection.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)





