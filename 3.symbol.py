import pandas as pd
import os

def split_tickers_to_csv(csv_file_path, output_dir_path):
    try:
        data = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"file not found: {csv_file_path}")
        return
    
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    
    tickers = data['Ticker'].unique()
    
    for ticker in tickers:
        ticker_data = data[data['Ticker'] == ticker]

        ticker_data['date'] = pd.to_datetime(ticker_data['date']) 
        ticker_data = ticker_data.sort_values(by='date')
        
        output_file_name = f"{ticker}.csv"
        output_file_path = os.path.join(output_dir_path, output_file_name)
        
        ticker_data.to_csv(output_file_path, index=False)
        
        print(f"{ticker} file saved: {output_file_path}")

csv_file_path = r'C:\Users\admin\Music\Guvi\Data-Driven Stock Analysis\Data\data\merged_and_sorted.csv'

output_dir_path = r'C:\Users\admin\Music\Guvi\Data-Driven Stock Analysis\Data\data\tickers'

split_tickers_to_csv(csv_file_path, output_dir_path)
