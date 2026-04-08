import pandas as pd
import numpy as np

# 1. Generate the Mock Data (50+ listings)
np.random.seed(42)

# Create a list of common items
items = ['Milk (1L)', 'Bread', 'Eggs (12)', 'Chips', 'Soda (2L)', 'Chicken Biryani', 'Pizza', 'Burger', 'Pasta', 'Coffee'] * 6

# Create data for Quick Commerce (e.g., Swiggy Instamart / Zepto)
quick_commerce = pd.DataFrame({
    'Item': items[:30],
    'Category': ['Groceries/Snacks'] * 30,
    'Model': 'Quick Commerce (10-min)',
    'Base_Price_INR': np.random.uniform(40, 150, 30),
    'Delivery_Fee_INR': np.random.uniform(15, 35, 30),
    'Platform_Fee_INR': np.full(30, 5),
    'Surge_Pricing_Multiplier': np.random.choice([1.0, 1.2, 1.5], 30, p=[0.7, 0.2, 0.1])
})

# Create data for Standard Food Delivery (e.g., Swiggy Food / Zomato)
standard_delivery = pd.DataFrame({
    'Item': items[30:60],
    'Category': ['Restaurant Meals'] * 30,
    'Model': 'Standard Delivery (45-min)',
    'Base_Price_INR': np.random.uniform(150, 400, 30),
    'Delivery_Fee_INR': np.random.uniform(30, 80, 30),
    'Platform_Fee_INR': np.full(30, 5),
    'Surge_Pricing_Multiplier': np.random.choice([1.0, 1.2], 30, p=[0.8, 0.2])
})

# Combine datasets
df = pd.concat([quick_commerce, standard_delivery], ignore_index=True)

# 2. Perform the Benchmarking Analysis

# Calculate Total Consumer Cost
df['Total_Cost'] = (df['Base_Price_INR'] * df['Surge_Pricing_Multiplier']) + df['Delivery_Fee_INR'] + df['Platform_Fee_INR']

# Calculate the "Delivery Premium" (Percentage of the total cost that goes to fees, not the food)
df['Fee_Percentage'] = ((df['Delivery_Fee_INR'] + df['Platform_Fee_INR']) / df['Total_Cost']) * 100

print("--- E-Commerce Pricing Benchmarking Results ---")

# Group by Model to find profitability gaps
summary = df.groupby('Model').agg({
    'Base_Price_INR': 'mean',
    'Delivery_Fee_INR': 'mean',
    'Total_Cost': 'mean',
    'Fee_Percentage': 'mean'
}).round(2)

print("\nAverage Metrics by Delivery Model:")
print(summary)

# Identify Profitability Gaps (Where users pay a massive premium for small items)
high_markup_items = df[df['Fee_Percentage'] > 30].sort_values(by='Fee_Percentage', ascending=False)
print("\nItems with highest fee-to-item-price ratio (Potential Profitability Optimization Areas):")
print(high_markup_items[['Item', 'Model', 'Base_Price_INR', 'Fee_Percentage']].head())
