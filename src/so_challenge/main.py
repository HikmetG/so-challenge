import matplotlib.pyplot as plt
from so_challenge.data_fetcher import fetch_data
from so_challenge.milestones import get_milestones
from so_challenge.plotter import plot_questions

def main():
    """Main entry point for the so-challenge project."""
    print("Fetching StackOverflow data...")
    cache_path = "so_questions_cache.csv"
    
    try:
        # Note: fetch_data currently uses a placeholder API call.
        # In a complete implementation, this would handle the 2008-2024 range.
        df = fetch_data(cache_path=cache_path)
        
        if df.empty:
            print("No data fetched or DataFrame is empty. Exiting.")
            return
            
        print(f"Successfully processed {len(df)} records.")
        
        print("Loading AI milestones...")
        milestones = get_milestones()
        
        print("Generating visualization...")
        fig, ax = plot_questions(df, milestones)
        
        output_file = "so_questions_plot.png"
        fig.savefig(output_file)
        print(f"Visualization saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()
