import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ==========================================
# 1. DATA RECONSTRUCTION
# ==========================================
# We manually reconstruct your results into DataFrames
# based on the data you provided.

# --- Syntax Data ---
data_syntax = {
    'Category': ['Embedded', 'Fragment', 'Standalone'],
    'Canonical': [4.95, 0.00, 95.05],
    'Metathesized': [0.00, 1.04, 98.96]
}
df_syntax = pd.DataFrame(data_syntax)

# --- Tone Data ---
data_tone = {
    'Category': ['Gloating', 'Humorous/Meme', 'Serious/Narrative'],
    'Canonical': [31.68, 60.40, 7.92],
    'Metathesized': [12.50, 84.38, 3.12]
}
df_tone = pd.DataFrame(data_tone)

# --- Context Data ---
data_context = {
    'Category': ['Fandom/TV', 'Finance/Crypto', 'Gaming', 'General', 
                 'Personal/Rel.', 'Politics', 'Sports'],
    'Canonical': [9.90, 1.98, 26.73, 38.61, 4.95, 9.90, 7.92],
    'Metathesized': [16.67, 3.12, 14.58, 35.42, 5.21, 13.54, 11.46]
}
df_context = pd.DataFrame(data_context)

# ==========================================
# 2. PLOTTING CONFIGURATION
# ==========================================
# Set a professional academic theme
sns.set_theme(style="whitegrid")
palette = ["#34495e", "#e74c3c"] # Dark Blue (Canonical) vs Red (Metathesized)

def create_chart(df, title, filename, figure_size=(10, 6)):
    """
    Generates a grouped bar chart with data labels.
    """
    # Convert from "Wide" to "Long" format for Seaborn
    df_melted = df.melt(id_vars='Category', var_name='Phrase Type', value_name='Percentage')
    
    plt.figure(figsize=figure_size)
    
    # Create the Bar Plot
    ax = sns.barplot(
        data=df_melted, 
        x='Category', 
        y='Percentage', 
        hue='Phrase Type',
        palette=palette,
        edgecolor="black" # Adds a crisp border
    )
    
    # Add Titles and Labels
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.ylabel("Frequency (%)", fontsize=12)
    plt.xlabel("", fontsize=12)
    plt.ylim(0, 105) # Give space for top labels
    
    # Add Percentage Labels on top of bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3, fontsize=10)
    
    # Adjust Layout
    plt.legend(title='Phrase Type', loc='upper right')
    plt.tight_layout()
    
    # Save
    plt.savefig(filename, dpi=300)
    print(f"Generated: {filename}")
    plt.show()

# ==========================================
# 3. GENERATE PLOTS
# ==========================================

print("--- Generating Visualizations ---")

# 1. Syntax Distribution
create_chart(
    df_syntax, 
    "Syntactic Distribution: Canonical vs. Metathesized", 
    "graph_syntax.png"
)

# 2. Tone Distribution
create_chart(
    df_tone, 
    "Semantic Tone: The Shift to Humor", 
    "graph_tone.png"
)

# 3. Context Distribution
# (Slightly larger size to fit the many categories)
create_chart(
    df_context, 
    "Contextual Domain Distribution", 
    "graph_context.png",
    figure_size=(12, 6)
)