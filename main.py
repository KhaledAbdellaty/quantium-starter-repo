import csv
from collections import defaultdict
import glob
from pathlib import Path

def main():
    # Use glob to get all CSV files in the data directory
    data_dir = 'data'
    csv_files = glob.glob(f'{data_dir}/daily_sales_data_*.csv')
    
    # We'll collect all the processed data in this list
    all_data = []
    
    # For summary statistics
    total_records = 0
    total_sales = 0
    sales_by_region = defaultdict(float)
    
    # Process each file
    for file_path in csv_files:
        print(f"Processing {file_path}...")
        
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Process each row
            for row in reader:
                # Filter for pink morsels only (case-insensitive)
                if row['product'].lower() != 'pink morsel':
                    continue
                
                # Calculate sales
                price = float(row['price'].replace('$', ''))
                quantity = int(row['quantity'])
                sales = price * quantity
                
                # Create a new row with only the required fields
                processed_row = {
                    'sales': sales,
                    'date': row['date'],
                    'region': row['region']
                }
                
                # Add to our collection
                all_data.append(processed_row)
                
                # Update statistics
                total_records += 1
                total_sales += sales
                sales_by_region[row['region']] += sales
    
    # Create output directory if it doesn't exist
    Path('output').mkdir(exist_ok=True)
    
    # Write to CSV
    output_path = 'output/pink_morsels_sales.csv'
    
    if all_data:
        with open(output_path, 'w', newline='') as csvfile:
            # Define the fieldnames in the order we want
            fieldnames = ['sales', 'date', 'region']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header and rows using dictionary writer
            writer.writeheader()
            writer.writerows(all_data)

        # Sort regions by sales amount
        sorted_regions = sorted(sales_by_region.items(), key=lambda x: x[1], reverse=True)

    else:
        print("No data was processed. Check that your CSV files contain 'pink morsel' products.")

if __name__ == "__main__":
    main()
