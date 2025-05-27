import yaml
import pandas as pd
import glob

def yaml_to_csv(yaml_dir_path, csv_file_path):
    yaml_files = glob.glob(yaml_dir_path + '/*.yaml')

    dfs = []
    for file in yaml_files:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
            df = pd.DataFrame(data)
            dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    combined_df.to_csv(csv_file_path, index=False)

yaml_dir_path = r'C:\Users\admin\Music\Guvi\Data-Driven Stock Analysis\Data\data\2024-11'
csv_file_path = '2024-11.csv'

yaml_to_csv(yaml_dir_path, csv_file_path)
