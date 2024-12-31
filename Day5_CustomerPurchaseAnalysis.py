import pandas as pd
import numpy as np
from scipy import stats

# Sample purchase data (replace with your actual data)
purchase_data = {
    'CustomerID': range(1, 101),  # 100 customers
    'PurchaseAmount': np.concatenate([
        np.random.normal(50, 15, 80),  # Most customers spend around 50
        np.random.normal(200, 50, 10), # Some high spenders
        np.random.normal(10, 5, 10)   # Few very low spenders
    ])
}

df = pd.DataFrame(purchase_data)

# Save to CSV
df.to_csv('customer_purchases.csv', index=False)

# Load from CSV (for demonstration)
df = pd.read_csv('customer_purchases.csv')

# --- Analysis ---
mean_purchase = df['PurchaseAmount'].mean()
median_purchase = df['PurchaseAmount'].median()

# Improved mode handling
try:
    mode_purchase = stats.mode(df['PurchaseAmount'])[0][0]  # Try to get the first mode
except IndexError:
    # If there's no mode (tie for most frequent values), print a message
    print("There is no single most frequent purchase amount (multiple modes).")
    mode_purchase = None  # Set mode to None to indicate no unique mode

std_dev_purchase = df['PurchaseAmount'].std()

print(f"Mean Purchase Amount: {mean_purchase:.2f}")
print(f"Median Purchase Amount: {median_purchase:.2f}")
print(f"Mode Purchase Amount: {mode_purchase:.2f}" if mode_purchase else "No single mode found.")
print(f"Standard Deviation of Purchase Amounts: {std_dev_purchase:.2f}")

# --- Outlier Identification (using IQR) ---
Q1 = df['PurchaseAmount'].quantile(0.25)
Q3 = df['PurchaseAmount'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['PurchaseAmount'] < (Q1 - 1.5 * IQR)) | (df['PurchaseAmount'] > (Q3 + 1.5 * IQR))]

print(f"\nNumber of Outliers: {len(outliers)}")
print("\nOutliers:")
print(outliers)

# --- Spending Categories ---
df['SpendingCategory'] = pd.cut(df['PurchaseAmount'],
                                bins=[0, 30, 70, 100, float('inf')],
                                labels=['Low Spender', 'Moderate Spender', 'High Spender', 'Very High Spender'])

print("\nSpending Categories:")
print(df['SpendingCategory'].value_counts())

# --- Answers to Questions ---

print("\n--- Answers to Questions ---")

print("1. Why might the mean purchase amount be significantly different from the median?")
print("   - The mean is sensitive to extreme values (outliers). If there are a few very large purchases, they will pull the mean upwards, while the median (the middle value) is not affected as much. In our example, the presence of few high spenders and few very low spenders is causing the mean to be higher than the median.")

print("\n2. How would outliers affect each measure of central tendency?")
print("   - Mean: Significantly affected; outliers pull the mean towards their value.\n   - Median: Less affected; outliers have minimal impact if they are not numerous enough to change the middle position.\n   - Mode: Not directly affected; outliers do not change the most frequent value unless they themselves become the most frequent value (which is unlikely).")

print("\n3. What insights can standard deviation provide about customer spending patterns?")
print("   - Standard deviation measures the spread or dispersion of the data. A high standard deviation indicates that purchase amounts are widely spread out (high variability in spending), while a low standard deviation indicates that most purchases are close to the mean (consistent spending). In our example, a relatively high standard deviation shows that there's considerable variation in customer spending.")