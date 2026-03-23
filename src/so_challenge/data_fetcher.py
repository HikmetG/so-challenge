import pandas as pd
import requests
import os
import time
from requests.exceptions import RequestException

def fetch_data(cache_path=None, retries=3, delay=1):
    """
    Fetch monthly StackOverflow question counts.
    
    Args:
        cache_path (str): Path to local CSV cache.
        retries (int): Number of retries for network errors.
        delay (int): Delay between retries in seconds.
        
    Returns:
        pd.DataFrame: DataFrame with year_month and question_count columns.
    """
    if cache_path and os.path.exists(cache_path):
        return pd.read_csv(cache_path)

    # Note: In a real implementation, we would construct the API query for 2008-2024.
    # The Stack Exchange API requires a 'site' parameter.
    url = "https://api.stackexchange.com/2.3/questions?site=stackoverflow"
    
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame(data.get("items", []))
            
            # If we're hitting the real API, we need to transform creation_date to year_month
            if not df.empty and 'creation_date' in df.columns:
                df['year_month'] = pd.to_datetime(df['creation_date'], unit='s').dt.to_period('M').astype(str)
                df = df.groupby('year_month').size().reset_index(name='question_count')
            
            # Final column check
            for col in ['year_month', 'question_count']:
                if col not in df.columns:
                    df[col] = pd.Series(dtype='object')
            
            if cache_path:
                df.to_csv(cache_path, index=False)
            
            return df
            if cache_path:
                df.to_csv(cache_path, index=False)
            
            return df
        except RequestException as e:
            if i < retries - 1:
                time.sleep(delay)
                continue
            raise e
            
    return pd.DataFrame(columns=["year_month", "question_count"])
