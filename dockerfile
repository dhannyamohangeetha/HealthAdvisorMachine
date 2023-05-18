# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN apt-get update \
    && apt-get install -y build-essential libssl-dev libffi-dev python3-dev
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install kafka-python
RUN pip install awscli

# Set environment variables
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    SPARK_HOME=/opt/spark \
    JAVA_HOME=/usr/lib/jvm/default-java \
    KAFKA_HOME=/opt/kafka \
    PATH=${PATH}:${SPARK_HOME}/bin:${KAFKA_HOME}/bin


# Install Java, Spark, and Kafka
RUN apt-get update && \
    apt-get install -y default-jre wget && \
    wget -q https://dlcdn.apache.org/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz && \
    tar -xzf spark-3.4.0-bin-hadoop3.tgz && \
    mv spark-3.4.0-bin-hadoop3 ${SPARK_HOME} && \
    rm spark-3.4.0-bin-hadoop3.tgz && \
    wget -q https://downloads.apache.org/kafka/3.4.0/kafka_2.13-3.4.0.tgz && \
    tar -xzf kafka_2.13-3.4.0.tgz && \
    mv kafka_2.13-3.4.0 ${KAFKA_HOME} && \
    rm kafka_2.13-3.4.0.tgz && \
    apt-get remove -y wget && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the environment variables for Kafka
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092
ENV KAFKA_GROUP_ID=mygroup
ENV KAFKA_TOPIC=mytopic


# Expose port 6060 for the Flask app to listen on
EXPOSE 6060
EXPOSE 9092
EXPOSE 2181

# Copy the rest of the application code into the container
COPY . /

# Start the Flask app
RUN chmod +x starting.sh
CMD ["sh", "starting.sh"]
