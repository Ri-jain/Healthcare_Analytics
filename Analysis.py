#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 21:12:46 2025

@author: rishabhjain
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv('hospital_inpatient_discharges_totalhipreplacement.csv')



##treating nulls

df.isnull().sum()
df['zip_code_3_digits'].isnull().sum()
df['zip_code_3_digits'].value_counts(dropna=False)

most_common_zip = df['zip_code_3_digits'].mode()[0]
df['zip_code_3_digits'].fillna(most_common_zip, inplace=True)

df.isnull().sum()

### checking dtypes

df.dtypes

df.select_dtypes(include='number').dtypes
df.select_dtypes(include='object').dtypes

### dropping columns

df.drop(columns=[
    'facility_id',
    'operating_certificate_number',
    'ccs_diagnosis_code',
    'ccs_procedure_code',
    'apr_drg_code',
    'apr_mdc_code',
    'apr_severity_of_illness_code',
    'attending_provider_license_number',
    'operating_provider_license_number'
], inplace=True)


df.dtypes

## Hospitlas
df['facility_name'].value_counts().nunique()

revenue_by_facility = df.groupby('facility_name')['total_charges'].sum().sort_values(ascending=False)
## to change the formatting of the scientific notaions
revenue_formatted = revenue_by_facility.apply(lambda x: f"${round(x):,}")

print(revenue_formatted.head(10))

# Get top 10 hospitals and unformatted values for plotting
top_10_unformatted = revenue_by_facility.head(10)
top_10_formatted = revenue_formatted.head(10)


costs_by_hospital = df.groupby('facility_name')['total_costs'].mean().round().sort_values(ascending=False)

print(costs_by_hospital.head(10))

#####Matplotlib needs raw numbers (like 307654399) to size the bars.
##If you give it a string like "$307,654,399", it won’t know how to plot it — it'll break or behave weirdly.


##Visualizing Charges
#plt
plt.figure(figsize=(12, 6))
bars = plt.barh(top_10_unformatted.index, top_10_unformatted.values, color='steelblue')
plt.gca().invert_yaxis()
plt.title('Top 10 Hospitals by Total Charges', fontsize=14)
plt.xlabel('Total Charges ($)', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.5)

##label
for bar, label in zip(bars, top_10_formatted):
    plt.text(bar.get_width() + 1e6, bar.get_y() + bar.get_height()/2, label, va='center')

plt.tight_layout()
plt.show()



#visualizing Costs
plt.figure(figsize=(12, 6))
bars_1 = plt.bar(costs_by_hospital.index[:10], costs_by_hospital.values[:10], color='grey')
plt.title('Top 10 Hospitals by Average Total Cost per Patient', fontsize=14)
plt.xlabel('Hospital Name', fontsize=12)
plt.ylabel('Average Total Cost ($)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Add labels
for bar in bars_1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1000, f"${int(height):,}", 
             ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


## Feature engineering: Cost per day
df['total_costs'] = pd.to_numeric(df['total_costs'], errors='coerce')
df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce')
df['length_of_stay'] = pd.to_numeric(df['length_of_stay'], errors='coerce')


df['cost_per_day'] = df['total_costs'] / df['length_of_stay']


## feature 2: profit
df['profit'] = df['total_charges'] - df['total_costs']

# feature 3: revenue
df['revenue_per_day'] = df['total_charges'] / df['length_of_stay']

#Feature - Length of Stay Category
df['los_category'] = pd.cut(df['length_of_stay'],
                            bins=[0, 2, 5, df['length_of_stay'].max()],
                            labels=['Short', 'Medium', 'Long'])



df['los_category'].value_counts()


## profit analysis by hospital

profit_by_facility= df.groupby('facility_name')['profit'].sum().sort_values(ascending=False)
profit_formatted= profit_by_facility.apply(lambda x: f"${round(x):,}")

top_10_profit_unformatted = profit_by_facility.head(10)
top_10_profit_formatted = profit_formatted.head(10)

plt.figure(figsize=(12, 6))
bars = plt.barh(top_10_profit_unformatted.index, top_10_profit_unformatted.values, color='seagreen')
plt.gca().invert_yaxis()
plt.title('Top 10 Hospitals by Total Profit', fontsize=14)
plt.xlabel('Total Profit ($)', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Add text labels
for bar, label in zip(bars, top_10_profit_formatted):
    plt.text(bar.get_width() + 1e6, bar.get_y() + bar.get_height()/2, label, va='center')

plt.tight_layout()
plt.show()

## cost vs revenue

avg_costs = df.groupby('facility_name')['total_costs'].mean()
avg_revenue = df.groupby('facility_name')['total_charges'].mean()

# Combine into one DataFrame
cost_vs_revenue = pd.DataFrame({
    'avg_cost_per_patient': avg_costs,
    'avg_revenue_per_patient': avg_revenue
})

# Sort by revenue (or cost)
top10 = cost_vs_revenue.head(10)
bar_width = 0.35
x = range(len(top10))

plt.figure(figsize=(14, 6))
bars1 = plt.bar(x, top10['avg_cost_per_patient'], width=bar_width, label='Avg Cost per Patient', color='gray')
bars2 = plt.bar([i + bar_width for i in x], top10['avg_revenue_per_patient'], width=bar_width, label='Avg Revenue per Patient', color='steelblue')

plt.xticks([i + bar_width/2 for i in x], top10.index, rotation=45, ha='right')
plt.xlabel('Hospital Name')
plt.ylabel('Amount ($)')
plt.title('Top 10 Hospitals: Average Cost vs Revenue per Patient')
plt.legend()
plt.tight_layout()

# Add value labels to both sets of bars
for bar in bars1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1000, f"${int(height):,}", ha='center', va='bottom', fontsize=9)
for bar in bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1000, f"${int(height):,}", ha='center', va='bottom', fontsize=9)

plt.show()


##scatter plot

# First, aggregate by hospital and LOS category
cost_rev_los = df.groupby(['facility_name', 'los_category']).agg({
    'total_costs': 'mean',
    'total_charges': 'mean'
}).reset_index()

plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=cost_rev_los,
    x='total_costs',
    y='total_charges',
    hue='los_category',
    palette='Set2',
    s=120,
    alpha=0.8
)
plt.xlabel('Average Cost per Patient ($)')
plt.ylabel('Average Revenue per Patient ($)')
plt.title('Hospital Avg Cost vs Revenue per Patient by LOS Category')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


## detecting outliers

cost_vs_revenue['profit_per_patient'] = cost_vs_revenue['avg_revenue_per_patient'] - cost_vs_revenue['avg_cost_per_patient']
outliers = cost_vs_revenue[(cost_vs_revenue['profit_per_patient'] < 0) | 
                           (cost_vs_revenue['profit_per_patient'] > cost_vs_revenue['profit_per_patient'].quantile(0.95))]

print(outliers)

sns.boxplot(data=df, x='los_category', y='profit')
plt.title('Profit Distribution by LOS Category')
plt.show()


efficient = cost_vs_revenue.sort_values(by='profit_per_patient', ascending=False).head(5)
inefficient = cost_vs_revenue.sort_values(by='profit_per_patient').head(5)

print("Most efficient:\n", efficient)
print("Least efficient:\n", inefficient)


sns.heatmap(df[['cost_per_day','revenue_per_day','profit','length_of_stay']].corr(), annot=True)
plt.title('Correlation Matrix')
plt.show()

##payer analysis


# Calculate average length of stay and total costs by payer
payer_stats = df.groupby('payment_typology_1').agg({
    'length_of_stay': 'mean',
    'total_costs': 'mean',
    'total_charges': 'mean'
}).round(2).sort_values('length_of_stay', ascending=False)

print(payer_stats)







