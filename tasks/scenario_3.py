import pandas as pd
import numpy as np

# Sample dataset
df = pd.DataFrame({
    "income": [1000, None, 2000, 3000, None, 4000, 5000]
})

#Calculate mean and median
mean_value = df["income"].mean()
median_value = df["income"].median()

# Check difference between mean and median
if abs(mean_value - median_value) < (0.1 * median_value):
    fill_value = median_value
    print("Data is normal → Filling with MEDIAN")
else:
    fill_value = df["income"].mode()[0]
    print("Data is skewed → Filling with MODE")

# Fill missing values
df["income"] = df["income"].fillna(fill_value)

print(df)
