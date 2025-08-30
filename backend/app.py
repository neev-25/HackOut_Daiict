# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd, numpy as np, json, pickle
# from utils.impact import choose_effects, affected_features
# from utils.features import add_time_features, add_lags_rolls, FEATURES

# app = Flask(__name__)
# CORS(app)

# # Load model + areas
# MODEL = pickle.load(open('model.pkl', 'rb'))

# try:
#     AREAS = json.load(open('data/areas.geojson', 'r'))  # FeatureCollection
# except FileNotFoundError:
#     AREAS = {"type": "FeatureCollection", "features": []}

# @app.route('/')
# def health():
#     return jsonify({"ok": True, "service": "tideguard-api"})

# @app.route('/predict', methods=['POST'])
# def predict():
#     body = request.get_json(force=True)
#     # Expect body with latest readings
#     rec = {
#         'timestamp': body.get('timestamp'),
#         'water_level_m': float(body.get('water_level_m', 0.9)),
#         'wind_speed_mps': float(body.get('wind_speed_mps', 4.0)),
#         'pressure_hpa': float(body.get('pressure_hpa', 1008.0)),
#         'tide_predicted_m': float(body.get('tide_predicted_m', 0.85)),
#     }
#     df = pd.DataFrame([rec])
#     df = add_time_features(df)
#     df = add_lags_rolls(df, 'water_level_m').fillna(method='bfill').fillna(0)
#     X = df[FEATURES]
#     sev = int(MODEL.predict(X)[0])

#     # Effects + affected polygons
#     feats = affected_features(AREAS['features'], sev)
#     out_geo = {"type": "FeatureCollection", "features": feats}

#     return jsonify({
#         'severity': sev,
#         'effects': choose_effects(sev),
#         'affected_areas': out_geo,
#         'confidence': 0.7  # demo constant
#     })

# @app.route('/timeseries', methods=['GET'])
# def timeseries():
#     # Serve last N points from historical for charts (demo)
#     df = pd.read_csv('data/historical.csv').tail(200)
#     return df.to_json(orient='records')

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os
import joblib
import json

# Local utils
from utils.features import add_time_features, add_lags_rolls, FEATURES
from utils.impact import choose_effects, affected_features

# Initialize app
app = Flask(__name__)

# Load trained model if available
MODEL_PATH = "model.pkl"
MODEL = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

# Load area polygons (GeoJSON)
AREAS_PATH = "areas.geojson"
AREAS = {}
if os.path.exists(AREAS_PATH):
    with open(AREAS_PATH, "r") as f:
        AREAS = json.load(f)

# Historical data path
HIST_PATH = "historical.csv"


@app.route('/')
def health():
    return jsonify({"ok": True, "service": "tideguard-api"})


@app.route('/predict', methods=['POST'])
def predict():
    body = request.get_json(force=True)

    rec = {
        'timestamp': body.get('timestamp'),
        'water_level_m': float(body.get('water_level_m', 0.9)),
        'wind_speed_mps': float(body.get('wind_speed_mps', 4.0)),
        'pressure_hpa': float(body.get('pressure_hpa', 1008.0)),
        'tide_predicted_m': float(body.get('tide_predicted_m', 0.85)),
    }

    df = pd.DataFrame([rec])
    df = add_time_features(df)
    df = add_lags_rolls(df, 'water_level_m').fillna(method='bfill').fillna(0)
    X = df[FEATURES]

    if MODEL is None:
        # fallback: simple rule-based severity
        lvl = rec['water_level_m']
        baseline = 0.8
        if lvl <= baseline + 0.3:
            sev = 0
        elif lvl <= baseline + 0.6:
            sev = 1
        elif lvl <= baseline + 1.0:
            sev = 2
        else:
            sev = 3
        confidence = 0.5
    else:
        pred = MODEL.predict_proba(X)
        pred_cls = np.argmax(pred, axis=1)[0]
        sev = int(pred_cls)
        confidence = float(np.max(pred))

    feats = affected_features(AREAS.get('features', []), sev)
    out_geo = {"type": "FeatureCollection", "features": feats}

    return jsonify({
        'severity': sev,
        'effects': choose_effects(sev),
        'affected_areas': out_geo,
        'confidence': confidence
    })


@app.route('/timeseries', methods=['GET'])
def timeseries():
    if os.path.exists(HIST_PATH):
        df = pd.read_csv(HIST_PATH).tail(200)
        return df.to_json(orient='records')
    else:
        return jsonify([])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
