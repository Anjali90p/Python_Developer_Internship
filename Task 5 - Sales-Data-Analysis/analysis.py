import pandas as pd
import matplotlib.pyplot as plt

# 1. Load CSV using Pandas
print("Loading sales data...")
df = pd.read_csv('sales_data.csv')

print("\nData Preview:")
print(df.head())

# 2. Basic Data Insights
print("\nOverall Summary:")
print(f"Total Sales: ${df['Sales'].sum()}")
print(f"Total Profit: ${df['Profit'].sum()}")

# 3. Group by Region and Sum Sales
print("\nGrouping by Region:")
region_sales = df.groupby('Region')['Sales'].sum()
print(region_sales)

# 4. Group by Product and Sum Sales
product_sales = df.groupby('Product')['Sales'].sum()

# 5. Plot the data
plt.figure(figsize=(10, 5))

# Subplot 1: Sales by Region
plt.subplot(1, 2, 1)
region_sales.plot(kind='bar', color='skyblue')
plt.title('Total Sales by Region')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)

# Subplot 2: Sales by Product
plt.subplot(1, 2, 2)
product_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'orange', 'lightcoral'])
plt.title('Sales Distribution by Product')
plt.ylabel('')

plt.tight_layout()

# Save the chart
plt.savefig('sales_analysis_chart.png')
print("\nCharts have been generated and saved to 'sales_analysis_chart.png'")
