import boto3
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier, GBTClassifier
from pyspark.ml.feature import VectorAssembler, StringIndexer, VectorIndexer, OneHotEncoder
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator


# Method to save stuffs on AWS S3
def save_to_s3(bucket_name, key_name, data):
    s3 = boto3.resource('s3', region_name='us-east-1')
    if isinstance(data, bytes):
        s3.Bucket(bucket_name).put_object(Key=key_name, Body=data)
    else:
        s3.Object(bucket_name, key_name).put(Body=data)
    s3.ObjectAcl(bucket_name, key_name).put(ACL='public-read')


def train_depression_model():
    spark = SparkSession.builder.appName('final project').getOrCreate()
    df = spark.read.csv("dataset/depression_dataset.csv", inferSchema=True, header=True)

    my_col = df.select(['sex', 'Age', 'Married', 'Number_children', 'education_level', 'total_members',
                        'gained_asset', 'durable_asset', 'save_asset', 'living_expenses', 'other_expenses',
                        'incoming_salary', 'incoming_own_farm', 'incoming_business', 'incoming_no_business',
                        'incoming_agricultural', 'farm_expenses', 'labor_primary', 'lasting_investment',
                        'no_lasting_investmen', 'depressed'])
    final_df = my_col.na.drop()
    assembler = VectorAssembler(inputCols=['sex', 'Age', 'Married', 'Number_children', 'education_level',
                                           'total_members', 'gained_asset', 'durable_asset', 'save_asset',
                                           'living_expenses', 'other_expenses', 'incoming_salary',
                                           'incoming_own_farm', 'incoming_business', 'incoming_no_business',
                                           'incoming_agricultural', 'farm_expenses', 'labor_primary',
                                           'lasting_investment', 'no_lasting_investmen'], outputCol='features')
    train, test = final_df.randomSplit([0.8, 0.2])

    dt = DecisionTreeClassifier(featuresCol='features', labelCol='depressed')
    pipeline1 = Pipeline(stages=[assembler, dt])
    dt_model = pipeline1.fit(train)
    result1 = dt_model.transform(test)
    # result1.select('prediction','depressed').show(10)

    #  eval1 = BinaryClassificationEvaluator(rawPredictionCol='rawPrediction', labelCol='depressed')
    # AUC1 = eval1.evaluate(result1)

    # Save the trained model file
    dt_model.write().overwrite().save("model/depression_model")

    # Save the model to S3 as a pickle file
    s3 = boto3.client('s3')
    with open('model/depression_model', "rb") as f:
        s3.upload_fileobj(f, 'diabetesprojectfinal', 'model/depression_model')


if __name__ == "__main__":
    train_depression_model()
