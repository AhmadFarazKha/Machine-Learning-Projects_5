import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Sample wait time data (replace with your actual data)
np.random.seed(42)  # for reproducibility
num_patients = 500
wait_times = np.concatenate([
    np.random.exponential(15, 400),  # Most patients have shorter waits (exponential distribution)
    np.random.normal(60, 20, 100)  # Some patients have longer waits (normal distribution, representing more complex cases)
])
wait_times = np.clip(wait_times, 0, 200) # Ensure no negative wait times and cap at 200 minutes
arrival_times = pd.to_datetime(['2024-01-01 00:00:00'] * num_patients) + pd.to_timedelta(np.random.randint(0, 365*24*60, num_patients), unit='m') #random arrival times

df = pd.DataFrame({'WaitTime': wait_times, 'ArrivalTime': arrival_times})

# Add Emergency Severity (simulated)
emergency_types = ['Minor', 'Moderate', 'Severe']
df['EmergencyType'] = np.random.choice(emergency_types, num_patients, p=[0.6, 0.3, 0.1]) #Simulate more minor cases

# Save to CSV
df.to_csv('hospital_wait_times.csv', index=False)

# Load from CSV
df = pd.read_csv('hospital_wait_times.csv', parse_dates=['ArrivalTime'])

# --- Analysis ---
print("\n--- Overall Wait Time Analysis ---")

mean_wait = df['WaitTime'].mean()
median_wait = df['WaitTime'].median()
try:
    mode_wait = stats.mode(df['WaitTime'])[0][0]
except IndexError:
    mode_wait = None
std_dev_wait = df['WaitTime'].std()

print(f"Mean Wait Time: {mean_wait:.2f} minutes")
print(f"Median Wait Time: {median_wait:.2f} minutes")
print(f"Mode Wait Time: {mode_wait:.2f}" if mode_wait is not None else "No unique mode found")
print(f"Standard Deviation of Wait Times: {std_dev_wait:.2f} minutes")

# Percentiles
percentiles = [25, 50, 75, 90, 95, 99]
for p in percentiles:
    print(f"{p}th Percentile Wait Time: {np.percentile(df['WaitTime'], p):.2f} minutes")

# Peak Hours Analysis
df['HourOfDay'] = df['ArrivalTime'].dt.hour
peak_hours = df['HourOfDay'].value_counts().sort_index()
print("\nPeak Hours:")
print(peak_hours)

plt.figure(figsize=(10, 6))
sns.countplot(x='HourOfDay', data=df)
plt.title("Patient Arrivals by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Patients")
plt.show()

# Wait times by emergency type:
print("\nWait Times by Emergency Type:")
print(df.groupby('EmergencyType')['WaitTime'].describe())

plt.figure(figsize=(8, 6))
sns.boxplot(x='EmergencyType', y='WaitTime', data=df)
plt.title("Wait Times by Emergency Type")
plt.show()

# --- Answers to Key Considerations ---
print("\n--- Answers to Key Considerations ---")

print("1. Why might median wait time be more useful than mean?")
print("   - Wait times are often skewed (some patients have very long waits). The mean is sensitive to these extreme values, while the median (the middle value) is not. The median gives a better representation of the 'typical' wait time experienced by most patients.")

print("\n2. How can percentiles help in setting service level agreements?")
print("   - Percentiles can be used to define service level targets. For example:\n"
      "     - '90% of patients will be seen within X minutes' (using the 90th percentile).\n"
      "     - '99% of patients will be seen within Y minutes' (using the 99th percentile).\n"
      "   This allows the hospital to set targets based on different levels of urgency and allocate resources accordingly.")

print("\n3. What does the standard deviation of wait times indicate about service consistency?")
print("   - A high standard deviation indicates high variability in wait times, meaning the service is inconsistent. Some patients wait much longer than others. A low standard deviation indicates more consistent wait times.")

print("\n4. How would you identify and account for different types of emergencies?")
print("   - Categorize emergencies by severity (e.g., minor, moderate, severe). Analyze wait times separately for each category. This allows you to identify if certain types of emergencies are experiencing disproportionately long waits. Different service level targets can be set for different emergency types (e.g., shorter wait times for severe emergencies). This is demonstrated in the code using simulated emergency types.")