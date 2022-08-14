import numpy as np
import pickle
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import sys
import json
from sklearn.preprocessing import OneHotEncoder
from model import data_prep

# Your API definition
app = Flask(__name__)

# get required pickle files
xgb_model = pickle.load(open('models/xgb_model.pickle','rb'))
scaler = pickle.load(open('models/std_scaler.pickle','rb'))
ohe = pickle.load(open('models/ohe.pickle','rb'))

@app.route('/predict', methods=['POST'])
def heart_prediction():

    patient_input = request.json
    data = pd.DataFrame(patient_input)

    # one hot encoding
    data['cp'] = data['cp'].astype(str)
    new_data = data_prep(data, ohe, False)

    #standard scaling
    new_data_std = scaler.transform(new_data)

    print(f"{new_data_std}", file=sys.stderr)
    results = xgb_model.predict(new_data_std)

    results = [str(result) for result in results]

    return jsonify({'Prediction': list(results)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)