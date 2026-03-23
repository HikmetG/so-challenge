import pandas as pd
import requests
import os
import time
from datetime import datetime, timezone
from calendar import monthrange
from requests.exceptions import RequestException

def fetch_data(cache_path=None, retries=3, delay=5.0, start_year=2008, end_year=2024):
    """
    Fetch historical StackOverflow question counts from the real API (resumable).
    Uses annual requests to maximize quota efficiency and reliability.
    """
    df = pd.DataFrame(columns=["year_month", "question_count"])
    if cache_path and os.path.exists(cache_path):
        try:
            df = pd.read_csv(cache_path)
        except Exception:
            pass

    required_years = []
    now = datetime.now(timezone.utc)
    
    for year in range(start_year, end_year + 1):
        # We store as YYYY-01 for simplicity in the cache/plot
        ym = f"{year}-01"
        if ym not in df['year_month'].values:
            # Skip future years
            if year > now.year: continue
            required_years.append((year, ym))

    if not required_years:
        return df.sort_values("year_month")

    print(f"Fetching {len(required_years)} years from Stack Exchange API (Resumable)...")
    
    # Common filters for 'total' only counts
    filters = ["!nKzpxGz_Vn", "!0W9jN9U_A8.r1", "total"]
    
    for year, ym in required_years:
        start_date = datetime(year, 1, 1, tzinfo=timezone.utc)
        # End of the year
        end_date = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        if year == 2008:
            # SO launched in late 2008
            start_date = datetime(2008, 8, 1, tzinfo=timezone.utc)
        
        if end_date > now: end_date = now
            
        fromdate = int(start_date.timestamp())
        todate = int(end_date.timestamp())
        
        success = False
        for f_idx, current_filter in enumerate(filters):
            if success: break
            
            url = (f"https://api.stackexchange.com/2.3/questions?site=stackoverflow"
                   f"&fromdate={fromdate}&todate={todate}&filter={current_filter}")
            
            for attempt in range(retries):
                try:
                    response = requests.get(url)
                    
                    if response.status_code == 429:
                        wait_time = (attempt + 1) * 60
                        print(f"Rate limited. Sleeping for {wait_time}s...")
                        time.sleep(wait_time)
                        continue

                    data = response.json()
                    
                    if "error_id" in data:
                        # Try next filter if this one is invalid
                        print(f"Filter {current_filter} failed (Error {data.get('error_id')})")
                        break
                    
                    response.raise_for_status()
                    total = data.get("total", 0)
                    
                    # If total is 0 but has items, it might be a filter issue
                    if total == 0 and "items" in data and len(data["items"]) > 0:
                        total = len(data["items"]) # Fallback if filter didn't produce total
                    
                    new_row = pd.DataFrame([{"year_month": ym, "question_count": int(total)}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    
                    if cache_path: df.to_csv(cache_path, index=False)
                    print(f"Fetched {year}: {total} questions")
                    time.sleep(delay)
                    success = True
                    break
                except Exception as e:
                    print(f"Attempt {attempt+1} for {year} failed: {e}")
                    time.sleep(10)
        
        if not success:
            print(f"Skipping year {year} after all filters and retries failed.")

    return df.sort_values("year_month")
