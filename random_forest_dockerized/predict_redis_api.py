import pickle
from flask import Flask, request, jsonify
from flasgger import Swagger
import numpy as np
import pandas as pd
import redis

app = Flask(__name__)
swagger = Swagger(app)

redis_host = "redis-server"
redis_port = 6379
redis_password = ""

prediction_index = 0

@app.route('/predict')
def predict_iris():
    """Example endpoint returning a prediction of iris
    ---
    parameters:
      - name: s_length
        in: query
        type: number
        required: true
      - name: s_width
        in: query
        type: number
        required: true
      - name: p_length
        in: query
        type: number
        required: true
      - name: p_width
        in: query
        type: number
        required: true
    responses:
      200:
        description: Index of predicted class 

    """
    global prediction_index
    s_length = float(request.args.get("s_length"))
    s_width = float(request.args.get("s_width"))
    p_length = float(request.args.get("p_length"))
    p_width = float(request.args.get("p_width"))
    
    print("Predicting!")
    prediction = model.predict(np.array([[s_length, s_width, p_length, p_width]]))
    # print(prediction)

    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    r.set(str(prediction_index),str(prediction))
    prediction_index+=1
    
    print("Returning Prediction")
    return str(prediction)

@app.route('/predict_file', methods=["POST"])
def predict_iris_file():
    """Example file endpoint returning a prediction of iris
    ---
    parameters:
      - name: input_file
        in: formData
        type: file
        required: true

    responses:
      200:
        description: Indecies of predicted classes
    """
    print("loding file")
    input_data = pd.read_csv(request.files.get("input_file"), header=None)
    print("Predicting whole file!")
    prediction = model.predict(input_data)
    return str(list(prediction))

@app.route('/predict_local_file')
def predict_local_file():
    """Example file endpoint returning a prediction of iris file from docker volume"
    ---    
    parameters:
      - name: file_name
        in: query
        type: string
        required: false

    responses:
      200:
        description: Indecies of predicted classes
    """

    print("loading file")
    # load the file from docker volume
    input_data = pd.read_csv("/mnt/data/iris_data.csv", header=None)
    print(input_data)
    print("Predicting whole file from docker volume!")
    prediction = model.predict(input_data)
    return str(list(prediction))

if __name__ == '__main__':
    with open('iris_model.pkl', 'rb') as model_file:
      print("loading model file")
      model = pickle.load(model_file)
      print("Model Loaded")
    print("Starting Flask Server")
    app.run(host='0.0.0.0', port=5000)