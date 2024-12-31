import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

# Sample manufacturing data (replace with your actual data)
np.random.seed(42)  # for reproducibility
num_parts = 200
target_dimension = 50  # Example target dimension (e.g., length in mm)
std_dev_normal = 2
part_data = {
    'PartID': range(1, num_parts + 1),
    'Dimension': np.random.normal(target_dimension, std_dev_normal, num_parts)
}
df = pd.DataFrame(part_data)

# Simulate a systematic error (shift in mean) for some parts:
systematic_error_start = 150
df.loc[systematic_error_start:, 'Dimension'] += 3  # Shift the mean for the last 50 parts

# Save to CSV
df.to_csv('manufacturing_parts.csv', index=False)

# Load from CSV
df = pd.read_csv('manufacturing_parts.csv')


# --- Analysis ---
print("\n--- Overall Analysis ---")

mean_dimension = df['Dimension'].mean()
std_dev_dimension = df['Dimension'].std()

print(f"Mean Dimension: {mean_dimension:.2f}")
print(f"Standard Deviation of Dimension: {std_dev_dimension:.2f}")

# Percentiles
percentiles = [5, 25, 50, 75, 95]
for p in percentiles:
    print(f"{p}th Percentile: {np.percentile(df['Dimension'], p):.2f}")

# Distribution Visualization
plt.figure(figsize=(10, 6))
sns.histplot(df['Dimension'], kde=True)
plt.title("Distribution of Part Dimensions")
plt.xlabel("Dimension")
plt.ylabel("Frequency")
plt.show()

# Normality test
stat, p = stats.shapiro(df['Dimension'])
print(f"Shapiro-Wilk Test: Statistics={stat:.3f}, p={p:.3f}")
alpha = 0.05
if p > alpha:
    print('Sample looks Gaussian (fail to reject H0)')
else:
    print('Sample does not look Gaussian (reject H0)')

# --- Analysis before and after the systematic shift ---
df_before = df[df['PartID'] < systematic_error_start]
df_after = df[df['PartID'] >= systematic_error_start]

print("\n--- Analysis Before Systematic Error ---")
print(f"Mean Dimension: {df_before['Dimension'].mean():.2f}")
print(f"Standard Deviation of Dimension: {df_before['Dimension'].std():.2f}")

print("\n--- Analysis After Systematic Error ---")
print(f"Mean Dimension: {df_after['Dimension'].mean():.2f}")
print(f"Standard Deviation of Dimension: {df_after['Dimension'].std():.2f}")


# --- Answers to Investigation Areas ---
print("\n--- Answers to Investigation Areas ---")

print("1. How can standard deviation help in setting quality control limits?")
print("   - Quality control limits are often set based on standard deviations from the mean. For example:\n"
      "     - +/- 3 standard deviations: This captures about 99.7% of the data in a normal distribution. Parts outside this range are highly likely to be defective.\n"
      "     - +/- 2 standard deviations: This captures about 95% of the data. This could be used for less critical quality checks.")

print("\n2. What percentile range should be used for acceptable parts?")
print("   - A common approach is to use the 5th and 95th percentiles (or 2.5th and 97.5th for tighter control). Parts falling within this range are considered acceptable. Parts outside might need further inspection or rejection.")

print("\n3. How would you identify systematic errors vs random variations?")
print("   - Systematic Errors: These cause a shift in the mean of the measurements (as demonstrated in the code). Analyzing data segments (e.g., by time or batch) can reveal shifts. Control charts are very useful for this. \n"
      "   - Random Variations: These are reflected in the standard deviation. A consistently high standard deviation (without a shift in mean) suggests random issues in the manufacturing process.")

print("\n4. What metrics would indicate a need to adjust the manufacturing process?")
print("   - A significant shift in the mean (indicating a systematic error).\n"
      "   - A consistently high or increasing standard deviation (indicating increased random variation).\n"
      "   - A large number of parts falling outside the quality control limits (defined by standard deviations or percentiles).\n"
      "   - Trends or patterns in control charts (e.g., runs, cycles, or drifts).")