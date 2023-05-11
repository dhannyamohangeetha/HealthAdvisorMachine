import pickle
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import boto3


# Method to save stuffs on AWS S3
def save_to_s3(bucket_name, key_name, data):
    s3 = boto3.resource('s3', region_name='us-east-1')
    if isinstance(data, bytes):
        s3.Bucket(bucket_name).put_object(Key=key_name, Body=data)
    else:
        s3.Object(bucket_name, key_name).put(Body=data)
    # To make file public
    s3.ObjectAcl(bucket_name, key_name).put(ACL='public-read')


def train_diabetes_model():
    df = pd.read_csv('https://diabetesprojectfinal.s3.amazonaws.com/dataset/diabetes_prediction_dataset.csv')

    plt.figure(figsize=(10,5))
    sns.heatmap(df.corr(),annot=True,cmap='coolwarm')

    # Save the plot as a PNG file in memory
    png_buffer = BytesIO()
    plt.savefig(png_buffer, format='png')
    png_buffer.seek(0)

    # Upload the plot to S3 as an object
    object_key = 'plot/heatmap.png'
    png_file = png_buffer.read()
    save_to_s3('diabetesprojectfinal', object_key, png_file)

    # Close the plot to free up memory
    plt.close()

    #Machine learning model
    encoder = OneHotEncoder(drop='first')
    X_cat = encoder.fit_transform(df[['gender', 'smoking_history']])
    X_num = df[['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']]
    X = pd.concat([pd.DataFrame(X_cat.toarray()), X_num], axis=1)
    y = df['diabetes']

    # Giving error if not make them string
    X.columns = X.columns.astype(str)
    # Split train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print('Accuracy:', accuracy)

    # Save the trained model as a pickle file
    with open('model/diabetes_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Save the model to S3 as a pickle file
    s3 = boto3.client('s3')
    with open('model/diabetes_model.pkl', "rb") as f:
        s3.upload_fileobj(f, 'diabetesprojectfinal', 'model/diabetes_model.pkl')


if __name__ == "__main__":
    train_diabetes_model()