# Train a demo model from data/historical.csv and save model.pkl
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

# If you don't have utils/features.py yet, comment these out or define inside
try:
    from utils.features import add_time_features, add_lags_rolls, FEATURES
except ImportError:
    # fallback demo functions
    def add_time_features(df):
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['dayofweek'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        return df
    
    def add_lags_rolls(df, col, lags=[1, 2, 3], windows=[3]):
        for lag in lags:
            df[f'{col}_lag{lag}'] = df[col].shift(lag)
        for w in windows:
            df[f'{col}_roll{w}'] = df[col].rolling(w).mean()
        return df
    
    FEATURES = ['water_level_m', 'hour', 'dayofweek',
                'water_level_m_lag1', 'water_level_m_lag2', 'water_level_m_lag3',
                'water_level_m_roll3']

BASELINE = 0.8  # meters (demo)

if __name__ == '__main__':
    # === Load historical data ===
    df = pd.read_csv('data/historical.csv')

    # === Feature engineering ===
    df = add_time_features(df)
    df = add_lags_rolls(df, 'water_level_m')

    # === Label encoding: severity levels ===
    lvl = df['water_level_m']
    conditions = [
        (lvl <= BASELINE + 0.3),
        (lvl <= BASELINE + 0.6),
        (lvl <= BASELINE + 1.0),
    ]
    choices = [0, 1, 2]  # 0=Safe, 1=Moderate, 2=High, else 3=Extreme
    df['severity'] = np.select(conditions, choices, default=3)

    # === Drop missing values (from lag/roll features) ===
    train = df.dropna().copy()
    X = train[FEATURES]
    y = train['severity']

    # === Train/test split ===
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    # === Train model ===
    model = GradientBoostingClassifier()
    model.fit(Xtr, ytr)

    print('✅ Holdout accuracy:', model.score(Xte, yte))

    # === Save trained model ===
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print('✅ Saved model.pkl')
