import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Read the data from CSV file
data = pd.read_csv('https://data.cdc.gov/api/views/3rge-nu2a/rows.csv')

# Filter the data to include only 'case' and 'death' outcomes
filtered_data = data[data['outcome'].isin(['case', 'death'])]

# Group the data by 'Age group', 'month', and 'outcome'
grouped = filtered_data.groupby(['Age group', 'month', 'outcome']).sum().reset_index()

# Calculate the rate of the outcome with vaccinated and unvaccinated
grouped['rate_vaccinated'] = grouped['Vaccinated with outcome'] / grouped['Fully vaccinated population']
grouped['rate_unvaccinated'] = grouped['Unvaccinated with outcome'] / grouped['Unvaccinated population']

# Pivot the data to have separate columns for 'case' and 'death'
pivoted_data = grouped.pivot(index=['Age group', 'month'], columns='outcome', values=['rate_vaccinated', 'rate_unvaccinated'])
pivoted_data = pivoted_data.reset_index()

# Plot the graphs for each age group
age_groups = pivoted_data['Age group'].unique()
for age_group in age_groups:
    age_group_data = pivoted_data[pivoted_data['Age group'] == age_group]
    months = age_group_data['month']
    
    # Plot the graph for 'Vaccinated - Case' and 'Unvaccinated - Case'
    plt.figure(figsize=(10, 6))
    plt.plot(months, age_group_data[('rate_vaccinated', 'case')], marker='o', label='Vaccinated - Case')
    plt.plot(months, age_group_data[('rate_unvaccinated', 'case')], marker='o', label='Unvaccinated - Case')
    plt.title(f'Effectiveness of Vaccination with Symptoms - {age_group} (Case)')
    plt.xlabel('Month')
    plt.ylabel('Rate (%)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 0.008)
    
    # Format y-axis tick labels as percentage
    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(1))
    
    plt.savefig(f'effectiveness_{age_group}_case.png')
    plt.close()
    
    # Plot the graph for 'Vaccinated - Death' and 'Unvaccinated - Death'
    plt.figure(figsize=(10, 6))
    plt.plot(months, age_group_data[('rate_vaccinated', 'death')], marker='o', color='r', label='Vaccinated - Death')
    plt.plot(months, age_group_data[('rate_unvaccinated', 'death')], marker='o', color='m', label='Unvaccinated - Death')
    plt.title(f'Effectiveness of Vaccination with Symptoms - {age_group} (Death)')
    plt.xlabel('Month')
    plt.ylabel('Rate (%)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 0.0005)
    
    # Format y-axis tick labels as percentage
    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(1))
    
    plt.savefig(f'effectiveness_{age_group}_death.png')
    plt.close()

# Call a main function
def main():
    plt.savefig(f'effectiveness_{age_group}_case.png')
    plt.savefig(f'effectiveness_{age_group}_death.png')
    plt.show()

if __name__ == "__main__":
    main()

