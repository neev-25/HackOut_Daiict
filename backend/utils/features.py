import numpy as np
import pandas as pd

FEATURES = [
    'water_level_m', 'wind_speed_mps', 'pressure_hpa', 'tide_predicted_m',
    'water_level_m_lag1', 'water_level_m_lag2', 'water_level_m_lag3',
    'rolling_max_6', 'rolling_mean_6', 'hour_sin', 'hour_cos', 'month_sin', 'month_cos'
]

def add_time_features(df):
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['month'] = df['timestamp'].dt.month
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    return df

def add_lags_rolls(df, col='water_level_m'):
    df = df.sort_values('timestamp').copy()
    for k in [1, 2, 3]:
        df[f'{col}_lag{k}'] = df[col].shift(k)
    df['rolling_max_6'] = df[col].rolling(6, min_periods=1).max()
    df['rolling_mean_6'] = df[col].rolling(6, min_periods=1).mean()
    return df   # ✅ was 'dfin' before, typo fixed
