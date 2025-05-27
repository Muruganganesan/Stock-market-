import pandas as pd
import glob

def merge_and_sort_csv(csv_dir_path, output_csv_path):
    csv_files = glob.glob(csv_dir_path + '/*.csv')
    
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    combined_df = combined_df.sort_values(by='Ticker', ascending=True)
    
    combined_df.to_csv(output_csv_path, index=False)

csv_dir_path = r'C:\Users\admin\Music\Guvi\Data-Driven Stock Analysis\Data\data\CSV monthwise'
output_csv_path = 'merged_and_sorted.csv'

merge_and_sort_csv(csv_dir_path, output_csv_path)
