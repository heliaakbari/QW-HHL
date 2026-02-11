import pandas as pd

# Load the CSV file
df = pd.read_csv('book.csv', header=None)

# Display basic info and head
print(df.info())
print(df.head())

df = pd.read_csv('book.csv', header=None, dtype={0: str})
df.columns = ['A', 'B', 'C', 'D']

# Sum of B to see if it relates to 8160
print("Sum of B:", df['B'].sum())

# Filter out values ending with '0'
df_filtered = df[~df['A'].str.endswith('0')].copy()
# Sum of B to see if it relates to 8160
print("Sum of B:", df_filtered['B'].sum())
#df_filtered = df
# Sort by A
df_filtered = df_filtered.sort_values(by='A')

# Transform D
df_filtered['D_scaled'] = df_filtered['D'] * 8192

print(df_filtered.head())
print(df_filtered.tail())
print("Number of rows after filtering:", len(df_filtered))

import matplotlib.pyplot as plt

# Create the plot
plt.figure(figsize=(15, 7))

# Plotting Column B as a bar chart
plt.bar(df_filtered['A'], df_filtered['B'], color='skyblue', label='Column B (Count)')

# Plotting Column D * 8160 as a line chart
plt.plot(df_filtered['A'], df_filtered['D_scaled'], color='red', marker='o', linewidth=2, label='Column D * 8160 (Expected)')

# Formatting the plot
plt.xticks(rotation=90, fontsize=8)
plt.xlabel('Column A (Bitstrings)')
plt.ylabel('Value')
plt.title('Comparison of Column B and Scaled Column D')
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig('diagram.png')
plt.close()

print("Max B (filtered):", df_filtered['B'].max())
print("Max D_scaled (filtered):", df_filtered['D_scaled'].max())