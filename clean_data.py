import pandas as pd
import html

# Load your raw RSS data
input_file = 'turn_tables_corpus_complete.csv'
output_file = 'final_linguistics_corpus.csv'

try:
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} raw rows.")

    # 1. Clean HTML Entities (e.g., &quot; -> ") in the text
    print("Cleaning text artifacts...")
    df['Full_Text'] = df['Full_Text'].apply(lambda x: html.unescape(str(x)))

    # 2. Standardize Date Format
    print("Standardizing dates...")
    # RSS dates can vary, strict=False handles mixed formats
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.strftime('%Y-MM-DD %H:%M:%S')

    # 3. Balance the Dataset (Target: 75 of each)
    print("Balancing dataset to 75/75 split...")
    
    # Split by type
    canonical = df[df['Phrase_Type'] == 'Canonical']
    metathesized = df[df['Phrase_Type'] == 'Metathesized']
    
    # Check counts
    print(f"  -> Found {len(canonical)} Canonical")
    print(f"  -> Found {len(metathesized)} Metathesized")
    
    # Sample exactly 75 of each (if available)
    # random_state=42 ensures reproducibility for your research
    final_canonical = canonical.sample(n=min(len(canonical), 75), random_state=42)
    final_metathesized = metathesized.sample(n=min(len(metathesized), 75), random_state=42)
    
    # Combine
    final_df = pd.concat([final_canonical, final_metathesized])
    
    # Shuffle the final rows so they aren't grouped by type
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # 4. Save Final
    final_df.to_csv(output_file, index=False)
    
    print(f"\nSUCCESS! Final Corpus saved to: {output_file}")
    print(f"Total Rows: {len(final_df)}")
    print("Breakdown:")
    print(final_df['Phrase_Type'].value_counts())

except Exception as e:
    print(f"Error: {e}")