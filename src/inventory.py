def inventory_logic(df):
    lead_time = 5
    service_level = 1.65

    std_dev = df['predicted_sales'].std()

    df['safety_stock'] = service_level * std_dev
    df['reorder_point'] = (df['predicted_sales'] * lead_time) + df['safety_stock']

    # NEW LOGIC
    mean = df['predicted_sales'].mean()

    df['stock_risk'] = df['predicted_sales'].apply(
        lambda x: "HIGH" if x > mean*1.25 else ("LOW" if x < mean*0.75 else "NORMAL")
    )

    df['demand_level'] = df['predicted_sales'].apply(
        lambda x: "HIGH" if x > mean*1.2 else ("LOW" if x < mean*0.8 else "MEDIUM")
    )
    df['action'] = df.apply(lambda row:
    "REORDER NOW" if row['predicted_sales'] > row['reorder_point']*0.85
    else "STABLE", axis=1)

    return df