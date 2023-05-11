import pickle
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import boto3


df = pd.read_csv('https://diabetesprojectfinal.s3.amazonaws.com/dataset/diabetes_prediction_dataset.csv')

plt.figure(figsize=(10,5))
sns.heatmap(df.corr(),annot=True,cmap='coolwarm')

# Save the processed data to an S3 bucket
s3 = boto3.resource('s3', region_name='us-east-1')
bucket_name = 'diabetesprojectfinal'

# Save the plot as a PNG file in memory
png_buffer = BytesIO()
plt.savefig(png_buffer, format='png')
png_buffer.seek(0)

# Upload the plot to S3 as an object
object_key = f'plot/heatmap.png'
s3.Bucket(bucket_name).put_object(Key=object_key, Body=png_buffer)
s3.ObjectAcl(bucket_name, object_key).put(ACL='public-read')

# Close the plot to free up memory
plt.close()


#Machine learning model
encoder = OneHotEncoder(drop='first')
X_cat = encoder.fit_transform(df[['gender', 'smoking_history']])
X_num = df[['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']]
X = pd.concat([pd.DataFrame(X_cat.toarray()), X_num], axis=1)
y = df['diabetes']

X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print('Accuracy:', accuracy)

with open('../model/diabetes_model.pkl', 'wb') as f:
    pickle.dump(model,f)
#Uploading pickle file to s3
s3 = boto3.client('s3')
bucket_name = 'diabetesprojectfinal'
key_name = 'model/diabetes_model.pkl'
model_pickle = pickle.dumps(model)
response = s3.put_object(Bucket=bucket_name, Key=key_name, Body=model_pickle)