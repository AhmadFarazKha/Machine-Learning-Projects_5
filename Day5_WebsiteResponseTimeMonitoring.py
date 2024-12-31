import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import datetime

# Simulate response time data (replace with actual data)
np.random.seed(42)
num_data_points = 1000
regions = ['North', 'South', 'East', 'West']
time_periods = pd.to_datetime(['2024-01-01 00:00:00'] * num_data_points) + pd.to_timedelta(np.random.randint(0, 365*24*60, num_data_points), unit='m')
response_times = np.concatenate([
    np.random.normal(50, 10, int(num_data_points*0.8)),  # Most responses are fast
    np.random.exponential(50, int(num_data_points*0.2)) # Some slow responses
])
response_times = np.clip(response_times, 0, 500) #Clip to avoid unrealistic values

data = {
    'Region': np.random.choice(regions, num_data_points),
    'Timestamp': time_periods,
    'ResponseTime': response_times
}
df = pd.DataFrame(data)

# Simulate a performance degradation for the 'South' region after a certain time
degradation_start_time = pd.to_datetime('2024-06-01 00:00:00')
df.loc[(df['Region'] == 'South') & (df['Timestamp'] > degradation_start_time), 'ResponseTime'] += 30

# Simulate some missing data
missing_data_indices = np.random.choice(df.index, size=int(num_data_points * 0.05), replace=False)
df.loc[missing_data_indices, 'ResponseTime'] = np.nan

# Save to CSV
df.to_csv('website_response_times.csv', index=False)

# Load from CSV
df = pd.read_csv('website_response_times.csv', parse_dates=['Timestamp'])

# --- Data Cleaning (Handling Missing Data) ---
df.dropna(inplace=True)  # Remove rows with missing response times (you could impute instead)

# --- Analysis ---
print("\n--- Overall Response Time Analysis ---")

print(df['ResponseTime'].describe())

# By Region
for region in regions:
    print(f"\n--- {region} Response Time Analysis ---")
    region_df = df[df['Region'] == region]
    print(region_df['ResponseTime'].describe())
    
    # Seasonality (Monthly Analysis)
    region_df['Month'] = region_df['Timestamp'].dt.month
    monthly_data = region_df.groupby('Month')['ResponseTime'].describe()
    print("\nMonthly Response Time Statistics for " + region)
    print(monthly_data)

    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Month', y='ResponseTime', data=region_df)
    plt.title(f"Monthly Response Time Distribution for {region}")
    plt.show()

# --- Threshold Setting (Example) ---
# 95th percentile as a performance guarantee
performance_guarantee_threshold = np.percentile(df['ResponseTime'], 95)
print(f"\nPerformance Guarantee Threshold (95th percentile): {performance_guarantee_threshold:.2f} ms")

# Alerting thresholds (example):
warning_threshold = np.percentile(df['ResponseTime'], 90)
critical_threshold = np.percentile(df['ResponseTime'], 99)

print(f"Warning Threshold (90th percentile): {warning_threshold:.2f} ms")
print(f"Critical Threshold (99th percentile): {critical_threshold:.2f} ms")

# --- Answers to Analysis Questions ---
print("\n--- Answers to Analysis Questions ---")

print("1. How would you determine 'normal' response times?")
print("   - Calculate descriptive statistics (mean, median, standard deviation). Visualize the distribution (histogram, box plot). Look for typical ranges and identify outliers.")

print("\n2. What percentile should be used for performance guarantees?")
print("   - The 95th or 99th percentile are commonly used. This means that 95% or 99% of requests will be served within that time. The choice depends on the desired level of service and business requirements.")

print("\n3. How can standard deviation help identify stability issues?")
print("   - A high or increasing standard deviation indicates inconsistent response times and potential instability. It means that response times are varying widely. A stable system will have a relatively low and consistent standard deviation.")

print("\n4. What would be appropriate thresholds for different types of alerts?")
print("   - Warning Threshold: A value that triggers a warning alert when response times start to deviate from the normal range (e.g., 90th percentile). \n"
      "   - Critical Threshold: A higher value that triggers a critical alert when performance is severely degraded (e.g., 99th percentile). The thresholds should be based on business requirements and the acceptable level of performance.")

print("\n--- Addressing Common Challenges ---")
print("Handling Outliers: Use robust statistics (median, IQR) or remove/transform outliers if justified. \n"
      "Dealing with Missing Data: Imputation (filling in missing values) or removal of rows with missing data. \n"
      "Accounting for Seasonality: Analyze data by time periods (day of week, time of day, month) to identify seasonal patterns. \n"
      "Determining Appropriate Sample Sizes: Larger sample sizes provide more reliable results. \n"
      "Setting Meaningful Thresholds: Base thresholds on business requirements, historical data, and acceptable performance levels.")

print("\n--- Implementation Considerations ---")
print("Data Quality Requirements: Accurate timestamps and reliable response time measurements. \n"
      "Calculation Frequency: Depends on the needs (e.g., hourly, daily). \n"
      "Response Time Needs: How quickly do you need to react to performance issues? \n"
      "Resource Limitations: How much computing power and storage are available? \n"
      "Reporting Requirements: What kind of reports are needed (e.g., daily summaries, weekly trends)?")