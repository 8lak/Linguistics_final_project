import feedparser
import pandas as pd
import time

# ==========================================
# CONFIGURATION
# ==========================================
PHRASES = {
    "Canonical": '"how the tables have turned"',
    "Metathesized": '"how the turn tables"'
}

# We will attack the search from these different angles
SORTS = [
    {'sort': 'new', 't': 'all'},
    {'sort': 'relevance', 't': 'all'},
    {'sort': 'top', 't': 'all'},   # Best of all time
    {'sort': 'top', 't': 'year'},  # Best of this year
    {'sort': 'top', 't': 'month'}, # Best of this month
    {'sort': 'comments', 't': 'all'} # Most discussed
]

OUTPUT_FILENAME = 'turn_tables_corpus_complete.csv'

# ==========================================
# LOGIC
# ==========================================
def collect_rss_data():
    dataset = []
    seen_urls = set() # To prevent duplicates across different sort methods
    
    print(f"--- Starting Multi-Angle RSS Extraction ---")

    for label, query in PHRASES.items():
        print(f"\n[Target: {label}]")
        
        # URL Encode the query: "how the turn tables" -> "how+the+turn+tables"
        encoded_query = query.replace(' ', '+').replace('"', '%22')
        
        for sort_option in SORTS:
            # Construct specific URL for this sort method
            rss_url = (
                f"https://www.reddit.com/search.rss?"
                f"q={encoded_query}&"
                f"sort={sort_option['sort']}&"
                f"t={sort_option['t']}"
            )
            
            try:
                # Fetch feed
                feed = feedparser.parse(rss_url)
                new_items = 0
                
                for entry in feed.entries:
                    # DEDUPLICATION CHECK
                    # RSS often repeats content across 'new' and 'relevance'
                    if entry.link in seen_urls:
                        continue
                    
                    # Schema Mapping
                    data_point = {
                        'ID': entry.id, 
                        'Source': entry.category if 'category' in entry else 'r/Reddit',
                        'Date': entry.updated, # RSS format date
                        'Phrase_Type': label,
                        'Full_Text': entry.title, # In RSS, the title is usually the cleanest text
                        'URL': entry.link
                    }
                    
                    dataset.append(data_point)
                    seen_urls.add(entry.link)
                    new_items += 1
                
                print(f"   -> Mode [{sort_option['sort']:<9}]: Found {new_items} new unique entries.")
                
                # IMPORTANT: Sleep prevents Reddit from blocking your IP
                time.sleep(3) 
                
            except Exception as e:
                print(f"   -> Error fetching {sort_option['sort']}: {e}")

    return dataset

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    data = collect_rss_data()
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    if not df.empty:
        df = df[['ID', 'Source', 'Date', 'Phrase_Type', 'Full_Text', 'URL']]
        df.to_csv(OUTPUT_FILENAME, index=False)
        
        print(f"\n========================================")
        print(f"TOTAL UNIQUE RECORDS: {len(df)}")
        print(f"Saved to: {OUTPUT_FILENAME}")
        print("Breakdown:")
        print(df['Phrase_Type'].value_counts())
        print(f"========================================")
        
        # Check if we met the goal
        counts = df['Phrase_Type'].value_counts()
        if counts.get('Canonical', 0) >= 75 and counts.get('Metathesized', 0) >= 75:
            print("SUCCESS: You have reached the target of 150!")
        else:
            print("STATUS: You are close. Check the breakdown above.")
    else:
        print("No data found. Reddit might be rate-limiting. Try again in 5 minutes.")