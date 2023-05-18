import time
import boto3
import numpy as np
import pickle
from flask import Flask, request, render_template, redirect, url_for, flash
from kafka import KafkaProducer, KafkaConsumer
import threading

app = Flask(__name__)
app.secret_key = 'HEALTH ADVISOR'

# Load Pickles diabetes Logistic Regression model
with open('model/diabetes_model.pkl', 'rb') as f:
    model1 = pickle.load(f)

# Heart attack Random Forest model
with open('model/heart_attack_model.pkl', 'rb') as file:
    model2 = pickle.load(file)


# Route to index home page
@app.route('/')
def index():
    return render_template('index.html')


# Route to diabetes form
@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


# Route to diabetes results page after click on predict button
@app.route('/diabetes_results', methods=['POST'])
def diabetes_results():
    # Get form data from user input
    global no_info, never, current, former, ever
    gender = int(request.form['gender'])
    if gender == 0:
        female = 1
        male = 0
    else:
        male = 1
        female = 0
    smoking_history = int(request.form['smoking_history'])
    if smoking_history == 0:
        never = 1
        no_info = 0
        current = 0
        former = 0
        ever = 0
    elif smoking_history == 1:
        never = 0
        no_info = 1
        current = 0
        former = 0
        ever = 0
    elif smoking_history == 2:
        never = 0
        no_info = 0
        current = 1
        former = 0
        ever = 0
    elif smoking_history == 3:
        never = 0
        no_info = 0
        current = 0
        former = 1
        ever = 0
    elif smoking_history == 4:
        never = 0
        no_info = 0
        current = 0
        former = 0
        ever = 1
    age = int(request.form['age'])
    hypertension = int(request.form['hypertension'])
    heart_disease = int(request.form['heart_disease'])
    feet = int(request.form['feet'])
    inches = int(request.form['inches'])
    weight = int(request.form['weight'])
    # calculate BMI
    height_m = (feet * 0.3048) + (inches * 0.0254)
    weight_kg = weight * 0.45359237
    bmi = round(weight_kg / (height_m ** 2), 1)
    hba1c_level = float(request.form['HbA1c_level'])
    blood_glucose_level = int(request.form['blood_glucose_level'])
    # Important to check feature's orders
    form_data = np.array([[female, male, never, no_info, current, former, ever, age,
                           hypertension, heart_disease, bmi, hba1c_level, blood_glucose_level]])
    # Model1 will expect 13 values from the numpy array
    prediction = model1.predict(form_data)
    probability = model1.predict_proba(form_data)[0, 1]

    return render_template('diabetes_results.html', prediction=prediction[0], probability=probability)


# Route to heart attack form
@app.route('/heart_attack')
def heart_attack():
    return render_template('heart_attack.html')


# Route to heart attack results after click on predict button
@app.route('/heart_attack_results', methods=['POST'])
def heart_attack_results():
    # Get form data from user input
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    cp = int(request.form['cp'])
    trtbps = int(request.form['trtbps'])
    chol = int(request.form['chol'])
    fbs = int(request.form['fbs'])
    restecg = int(request.form['restecg'])
    thalachh = int(request.form['thalachh'])
    exng = int(request.form['exng'])
    oldpeak = float(request.form['oldpeak'])
    slp = int(request.form['slp'])
    caa = int(request.form['caa'])
    thall = int(request.form['thall'])

    form_data = np.array([[age, sex, cp, trtbps, chol, fbs, restecg, thalachh,
                           exng, oldpeak, slp, caa, thall]])

    prediction1 = model2.predict(form_data)
    probability1 = model2.predict_proba(form_data)[0, 1]

    return render_template('heart_attack_results.html', prediction=prediction1[0], probability=probability1)


# Route to depression form, but we don't do predict because accuracy rate is too low.
@app.route('/depression')
def depression():
    return render_template('depression.html')


# To start feed back page, where all feedback will be saved to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'final_comments'
# COMMAND IN CLI TO DOWNLOAD FROM DYNAMODB
# aws dynamodb scan --table-name comments --output json --query "Items[*]" > json/comments.json

# Check if table already exists
existing_tables = list(dynamodb.tables.all())
if any(table.name == table_name for table in existing_tables):
    table = dynamodb.Table(table_name)
else:
    # Create comments table
    # DynamoDB is NoSQL, we cannot use SQL to create table
    # These standard code create table in DynamoDB, following Key-Value and Hash function
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'comment_id',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'comment_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Wait for table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)


# This end the block of creating table one DynamoDB if it's not there


# This route to feedback page, get method
@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')


# This also route to feedback page, post method
@app.route('/feedback', methods=['POST'])
def add_feedback():
    name = request.form['name']
    rating = request.form['rating']
    comment = request.form['comment']

    # Add comment to DynamoDB table
    table.put_item(
        Item={
            'comment_id': str(time.time()),
            'name': name,
            'rating': rating,
            'comment': comment
        }
    )
    flash('Thank you for your comment! It was saved on DynamoDB')
    return render_template('feedback.html')


# Route to craziness page
@app.route('/craziness')
def craziness():
    return render_template("craziness.html")


@app.route('/craziness', methods=['POST'])
def craziness_results():
    choice = request.form['developer']
    if choice == "0":
        message = "YOU ARE CRAZY! ----- DEVELOPERS ARE CRAZY!"
    else:
        message = "Select the correct answer. It's supposed to be 'Yes'"

    return render_template("craziness.html", message=message)


# These are the route to navigation bar links where we can find the project details.
@app.route('/project')
def project():
    return render_template("project.html")


@app.route('/about')
def about():
    return render_template("about.html")


# create Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
# create Kafka consumer
consumer = KafkaConsumer('my_topic', bootstrap_servers=['localhost:9092'], auto_offset_reset='latest')

#  messages will be saved to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_message = 'final_message'
# COMMAND IN CLI TO DOWNLOAD FROM DYNAMODB
# aws dynamodb scan --table-name comments --output json --query "Items[*]" > json/comments.json

# Check if table already exists
existing_tables = list(dynamodb.tables.all())
if any(table1.name == table_message for table1 in existing_tables):
    table1 = dynamodb.Table(table_message)
else:
    # Create comments table
    # DynamoDB is NoSQL, we cannot use SQL to create table
    # These standard code create table in DynamoDB, following Key-Value and Hash function
    table1 = dynamodb.create_table(
        TableName=table_message,
        KeySchema=[
            {
                'AttributeName': 'message_id',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'message_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Wait for table to be created
    table1.meta.client.get_waiter('table_exists').wait(TableName=table_message)


# This end the block of creating table one DynamoDB if it's not there


# thread to constantly check for new messages from Kafka consumer
def kafka_consumer_thread():
    for message in consumer:
        # add message to a list to be rendered on the template
        app.config['MESSAGES'].append(message.value.decode())

        # Add message to DynamoDB table
        table1.put_item(
            Item={
                'message_id': str(time.time()),
                'message': message
            })


# create a list to store flask messages
app.config['MESSAGES'] = []

# start Kafka consumer thread to receive the messages
kafka_consumer = threading.Thread(target=kafka_consumer_thread)
kafka_consumer.start()


# route to the chat window
@app.route('/user1')
def page1():
    return render_template('page1.html', messages=app.config['MESSAGES'])


# route to handle user input and send it to Kafka producer
@app.route('/send_message1', methods=['POST'])
def send_message1():
    message = request.form['message']
    producer.send('my_topic', message.encode())
    return redirect(url_for('page1'))


# route to chat window 2 for professionals
@app.route('/user2')
def page2():
    return render_template('page2.html', messages=app.config['MESSAGES'])


# route to handle the user input message and sending it to producer.
@app.route('/send_message2', methods=['POST'])
def send_message2():
    message = request.form['message']
    producer.send('my_topic', message.encode())
    return redirect(url_for('page2'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060, debug=True)
