import pandas as pd
import pickle
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import boto3


# Method to save stuffs on AWS S3
def save_to_s3(bucket_name, key_name, data):
    s3 = boto3.resource('s3', region_name='us-east-1')
    if isinstance(data, bytes):
        s3.Bucket(bucket_name).put_object(Key=key_name, Body=data)
    else:
        s3.Object(bucket_name, key_name).put(Body=data)
    s3.ObjectAcl(bucket_name, key_name).put(ACL='public-read')


def train_heart_attack_model():
    df = pd.read_csv('https://diabetesprojectfinal.s3.amazonaws.com/dataset/heart.csv')
    new_column_names = {
        'age': 'Age',
        'sex': 'Sex',
        'cp': 'Chest Pain Type',
        'trtbps': 'Resting Blood Pressure',
        'chol': 'Cholesterol',
        'fbs': 'Fasting Blood Sugar',
        'restecg': 'Rest ECG',
        'thalachh': 'Max Heart Rate',
        'exng': 'Exercise Induced Angina',
        'oldpeak': 'ST Depression',
        'slp': 'Slope',
        'caa': 'Num Major Vessels',
        'thall': 'Thalassemia',
        'output': 'Target'
    }
    df = df.rename(columns=new_column_names)

    plt.figure(figsize=(10, 5))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')

    # Save the plot as a PNG file in memory
    png_buffer = BytesIO()
    plt.savefig(png_buffer, format='png')
    png_buffer.seek(0)

    # Upload the plot to S3 as an object
    object_key = 'plot/heatmap_heart.png'
    png_file = png_buffer.read()
    save_to_s3('diabetesprojectfinal', object_key, png_file)

    plt.close()

    X = df.drop('Target', axis=1)
    y = df['Target']

    X.columns = X.columns.astype(str)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Has to put max iteration big, otherwise it will raise an error
    model = LogisticRegression(max_iter=100000)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print('Accuracy:', accuracy)

    # Save the trained model as a pickle file
    with open('model/heart_attack_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Save the model to S3 as a pickle file
    s3 = boto3.client('s3')
    with open('model/heart_attack_model.pkl', "rb") as f:
        s3.upload_fileobj(f, 'diabetesprojectfinal', 'model/heart_attack_model.pkl')


if __name__ == "__main__":
    train_heart_attack_model()
