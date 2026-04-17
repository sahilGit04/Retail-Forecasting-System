import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range(start="2026-01-01", end="2026-01-30")

stores = ["Mumbai", "Pune", "Delhi", "Bangalore"]

products = {
    "cereals": "Grocery",
    "herbs": "Grocery",
    "fruits": "Grocery",
    "veggies": "Grocery",
    "Milk": "Dairy",
    "Cheese": "Dairy",
    "Butter Milk": "Dairy",
    "Chips": "Snacks",
    "Nuts": "Snacks",
    "Cheetos": "Snacks",
    "M&M'S": "Snacks",
    "Soft Drinks" : "Beverages",
    "Energy Drinks" : "Beverages",
    "coffee&tea": "Beverages",
    "Shampoo" : "Personal Care",
    "Lotion" : "Personal Care",
    "Soap" : "Personal Care",
    "Face Wash" : "Personal Care"
}

data = []

for date in dates:
    for store in stores:
        for product, category in products.items():

            base = {
    "cereals": 120,
    "herbs": 80,
    "fruits": 150,
    "veggies": 100,

    "Milk": 200,
    "Cheese": 90,
    "Butter Milk": 110,

    "Chips": 150,
    "Nuts": 140,
    "Cheetos": 130,
    "M&M'S": 120,

    "Soft Drinks": 180,
    "Energy Drinks": 160,
    "coffee&tea": 140,

    "Shampoo": 90,
    "Lotion": 80,
    "Soap": 70,
    "Face Wash": 60
}[product]

            # Weekend spike
            if date.weekday() >= 5:
                base *= 1.3

            # Seasonal spike (summer drinks)
            if date.month in [3] and product == "Soft Drinks":
                base *= 1.6

            # Festival spike (simulate random big days)
            if np.random.rand() < 0.05:
                base *= 2

            # Low demand days (random dips)
            if np.random.rand() < 0.05:
                base *= 0.5

            noise = np.random.randint(-40, 40)

            sales = max(10, int(base + noise))

            data.append([date, store, product, category, sales])

df = pd.DataFrame(data, columns=["date","store","product","category","sales"])

df.to_csv("data/raw/sales.csv", index=False)

print("✅ Realistic dataset generated")