import pandas as pd

def create_features(df):
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.weekday

    import pandas as pd

def create_features(df):
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.weekday

    # Create encoded version (DO NOT overwrite original df)
    df_encoded = pd.get_dummies(df, columns=['store','product'], drop_first=True)

    return df, df_encoded
    return df  