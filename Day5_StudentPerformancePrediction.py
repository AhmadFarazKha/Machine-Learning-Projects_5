import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Sample student data (replace with your actual data)
np.random.seed(42)  # for reproducibility
num_students = 100
subjects = ['Math', 'Science', 'English', 'History']
student_data = {
    'StudentID': range(1, num_students + 1)
}
for subject in subjects:
    student_data[subject] = np.random.normal(75, 10, num_students) # Mean 75, std dev 10
df = pd.DataFrame(student_data)

# Save to CSV
df.to_csv('student_performance.csv', index=False)

# Load from CSV
df = pd.read_csv('student_performance.csv')

# --- Analysis ---
for subject in subjects:
    print(f"\n--- {subject} Analysis ---")

    # Percentiles
    percentiles = [25, 50, 75, 90]
    for p in percentiles:
        print(f"{p}th Percentile: {np.percentile(df[subject], p):.2f}")

    # Standard Deviation
    std_dev = df[subject].std()
    print(f"Standard Deviation: {std_dev:.2f}")

    # Grade Distribution (Histogram and Density Plot)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    sns.histplot(df[subject], kde=False)
    plt.title(f"{subject} Grade Distribution (Histogram)")

    plt.subplot(1, 2, 2)
    sns.kdeplot(df[subject])
    plt.title(f"{subject} Grade Distribution (Density Plot)")
    plt.show()
    
    #Normality Test
    stat, p = stats.shapiro(df[subject])
    print(f"Shapiro-Wilk Test: Statistics={stat:.3f}, p={p:.3f}")
    alpha = 0.05
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
    else:
        print('Sample does not look Gaussian (reject H0)')
    
    print("----------------------------")

# --- Answers to Key Questions ---
print("\n--- Answers to Key Questions ---")

print("1. How would you use percentiles to categorize student performance?")
print("   - Percentiles divide the data into 100 equal parts. For example:\n"
      "     - Students below the 25th percentile: Need significant support.\n"
      "     - Students between 25th and 50th percentile: Need monitoring and potential support.\n"
      "     - Students between 50th and 75th percentile: Performing as expected.\n"
      "     - Students above the 75th percentile: High performers.")

print("\n2. What role does standard deviation play in identifying unusual performance patterns?")
print("   - Standard deviation measures the spread of grades. A high standard deviation indicates a wider range of performance, possibly suggesting diverse learning paces or teaching effectiveness. A low standard deviation suggests more consistent performance. Students far from the mean (e.g., more than 2 standard deviations below) might need attention.")

print("\n3. How can you determine if the grade distribution is normal?")
print("   - Visually: Histograms and density plots can give a visual indication. A bell-shaped curve suggests a normal distribution.\n"
      "   - Statistical Tests: The Shapiro-Wilk test is a common test for normality. A p-value greater than 0.05 suggests that the data is likely normally distributed.")

print("\n4. At what percentile would you set intervention triggers?")
print("   - This depends on the institution's policies and resources. A common approach is to set the trigger at the 25th percentile or lower. This means students in the bottom 25% of performance in a subject would receive intervention. You could also use a combination of percentile and standard deviation (e.g., students more than 1.5 standard deviations below the mean and below the 30th percentile).")