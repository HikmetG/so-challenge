import pandas as pd
import matplotlib.pyplot as plt

def plot_questions(df, milestones):
    """
    Plot StackOverflow question volume over time with AI milestone overlays.
    
    Args:
        df (pd.DataFrame): DataFrame with year_month and question_count columns.
        milestones (list): List of dicts with date and label keys.
        
    Returns:
        tuple: (figure, axes) objects from matplotlib.
        
    Raises:
        ValueError: If the DataFrame is empty.
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Ensure year_month is datetime and sorted
    df_plot = df.copy()
    df_plot['year_month'] = pd.to_datetime(df_plot['year_month'])
    df_plot = df_plot.sort_values('year_month')
    
    # Plot question counts
    ax.plot(df_plot['year_month'], df_plot['question_count'], 
            marker='o', linestyle='-', label='Questions per Month')
    
    # Add milestone overlays
    for milestone in milestones:
        m_date = pd.to_datetime(milestone['date'])
        m_label = milestone['label']
        ax.axvline(x=m_date, color='red', linestyle='--', alpha=0.6, label=m_label)
    
    # Formatting
    ax.set_xlabel("Date")
    ax.set_ylabel("Question Count")
    ax.set_title("StackOverflow Question Volume (2008-2024) and AI Milestones")
    ax.legend(loc='best')
    plt.tight_layout()
    
    return fig, ax
