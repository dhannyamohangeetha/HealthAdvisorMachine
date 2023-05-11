from pyspark.ml import PipelineModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import lit
from pyspark.sql import SparkSession


@app.route('/depression_results', methods=['POST'])
def depression_results():
    sex = 1
    age = int(request.form['age'])
    married = int(request.form['married'])
    number_children = 2
    education_level = int(request.form['education_level'])
    total_members = int(request.form['total_members'])
    gained_assets = 30000000
    durable_assets = int(request.form['durable_assets'])
    save_asset = 10000000
    living_expenses = 20000000
    other_expenses = 20000000
    incoming_salary = 0
    incoming_own_farm = 0
    incoming_business = 0
    incoming_no_business = 0
    incoming_agricultural = 0
    farm_expenses = 0
    labour_primary = int(request.form['labour_primary'])
    lasting_investment = 25000000
    no_lasting_investment = int(request.form['no_lasting_investment'])

    form_data = [(sex, age, married, number_children, education_level, total_members, gained_assets,
                  durable_assets, save_asset, living_expenses, other_expenses, incoming_salary,
                  incoming_own_farm, incoming_business, incoming_no_business, incoming_agricultural,
                  farm_expenses, labour_primary, lasting_investment, no_lasting_investment)]

    columns = ['sex', 'age', 'married', 'number_children', 'education_level', 'total_members', 'gained_assets',
               'durable_assets', 'save_asset', 'living_expenses', 'other_expenses', 'incoming_salary',
               'incoming_own_farm', 'incoming_business', 'incoming_no_business', 'incoming_agricultural',
               'farm_expenses', 'labour_primary', 'lasting_investment', 'no_lasting_investment']

    assembled_data = spark.createDataFrame(form_data, columns)
    assembled_data = assembled_data.withColumn('dummy', lit(0))

    # Apply the assembler transformation to the DataFrame
    assembled_data = assembler.transform(assembled_data)

    # Use loaded model to predict
    prediction = dt_model.transform(assembled_data)

    # Extract the predicted label and probability from the predictions DataFrame
    predicted_label = prediction.select('prediction').collect()[0][0]
    probability = prediction.select('probability').collect()[0][0][1]

    return render_template('depression_results.html', prediction=predicted_label,
                           probability=probability)