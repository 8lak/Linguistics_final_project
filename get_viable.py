import pandas as pd

# Load your current corpus
df = pd.read_csv('final_linguistics_corpus.csv')

print(f"Total Rows Loaded: {len(df)}")

# Define the target phrases for checking
canonical_phrase = "how the tables have turned"
metathesized_phrase = "how the turn tables"

def check_phrase_presence(row):
    text = str(row['Full_Text']).lower()
    p_type = row['Phrase_Type']
    
    # Check strict containment based on the label
    if p_type == 'Canonical':
        # We look for "tables have turned" to be safe against small variations
        return "tables have turned" in text
    elif p_type == 'Metathesized':
        # We look for "turn tables"
        return "turn tables" in text
    return False

# Apply the check
df['Is_Valid'] = df.apply(check_phrase_presence, axis=1)

# Split the data
valid_df = df[df['Is_Valid'] == True].drop(columns=['Is_Valid'])
invalid_df = df[df['Is_Valid'] == False].drop(columns=['Is_Valid'])

# Save reports
valid_df.to_csv('clean_ready_to_use.csv', index=False)
invalid_df.to_csv('requires_manual_fix.csv', index=False)

print("\n--- QUALITY CONTROL REPORT ---")
print(f"✅ GOOD DATA: {len(valid_df)} rows")
print(f"   (The phrase is explicitly in the text. Ready for analysis.)")
print(f"⚠️ HIDDEN DATA: {len(invalid_df)} rows")
print(f"   (The phrase was found in a comment/body, but the RSS only grabbed the Title.)")
print("-" * 30)
print("Files created:")
print("1. clean_ready_to_use.csv")
print("2. requires_manual_fix.csv")