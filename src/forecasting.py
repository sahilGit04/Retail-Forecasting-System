from sklearn.ensemble import RandomForestRegressor


def train_model(df):
    X = df.drop(columns=['sales','date','category'])
    y = df['sales']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model


def forecast(model, df):
    X = df.drop(columns=['sales','date','category'])

    df['predicted_sales'] = model.predict(X)
    df['actual_vs_predicted_diff'] = df['sales'] - df['predicted_sales']

    return df

import pandas as pd

def future_forecast(model, df, days=7):
    # Only use training columns
    feature_cols = [col for col in df.columns if col not in [
        'sales','date','category',
        'predicted_sales','actual_vs_predicted_diff',
        'safety_stock','reorder_point',
        'stock_risk','demand_level','action'
    ]]

    future_dates = pd.date_range(start=df['date'].max(), periods=days+1)[1:]
    
    future_df = pd.DataFrame({'date': future_dates})
    
    future_df['day'] = future_df['date'].dt.day
    future_df['month'] = future_df['date'].dt.month
    future_df['weekday'] = future_df['date'].dt.weekday

    # Add missing columns (store/product dummies)
    for col in feature_cols:
        if col not in future_df.columns:
            future_df[col] = 0

    # Ensure same order
    X = future_df[feature_cols]

    future_df['predicted_sales'] = model.predict(X)

    return future_df