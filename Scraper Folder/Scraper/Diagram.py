# Data
age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
consumption_percentage = [22, 18, 15, 12, 20, 13]

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(age_groups, consumption_percentage, color='skyblue')
plt.xlabel('Åldersgrupper')
plt.ylabel('Procentandel av Kaffekonsumtion')
plt.title('Kaffekonsumtion per Åldersgrupp')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show chart
plt.show()
