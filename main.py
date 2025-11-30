import praw
import pandas as pd
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
# Replace these with the keys you generated in Part 1
CLIENT_ID = 'YOUR_CLIENT_ID_HERE'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE'
USER_AGENT = 'python:CorpusBuilder:v1.0 (by /u/YourRedditUsername)'

# Target Definition
TARGETS = {
    "Canonical": {
        "query": '"how the tables have turned"',
        "limit": 75
    },
    "Metathesized": {
        "query": '"how the turn tables"',
        "limit": 75
    }
}

OUTPUT_FILENAME = 'turn_tables_corpus.csv'

# ==========================================
# INITIALIZATION
# ==========================================
def init_reddit():
    """Initialize PRAW instance."""
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )

def collect_data():
    reddit = init_reddit()
    dataset = []
    
    # Safety Check: Set to track unique IDs to prevent duplicates
    # Reddit IDs are globally unique (e.g., "t3_x5y6z")
    unique_ids = set()

    print(f"--- Starting Extraction for Project: How the Turn Tables ---")

    for label, config in TARGETS.items():
        print(f"\nProcessing Phrase Type: {label} ({config['query']})")
        count = 0
        
        # We search "all" subreddits to get the widest discourse
        # sort='new' gets the most recent discourse
        search_results = reddit.subreddit("all").search(
            config['query'], 
            sort='relevance', 
            limit=None,
            syntax='plain' # Ensures we look for the exact string phrase
        )

        for submission in search_results:
            if count >= config['limit']:
                break
            
            # 1. Safety Check: Duplicate Detection
            if submission.id in unique_ids:
                continue

            # 2. Context Construction
            # We combine Title and Selftext to ensure we capture the phrase
            # regardless of where it appears in the post.
            full_text = f"{submission.title} \n {submission.selftext}"
            
            # Simple check to ensure the phrase is actually in the text 
            # (Search sometimes returns fuzzy matches)
            clean_query = config['query'].replace('"', '').lower()
            if clean_query not in full_text.lower():
                continue

            # 3. Data Schema Mapping
            entry = {
                'ID': submission.id,
                'Source': f"r/{submission.subreddit.display_name}",
                'Date': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'Phrase_Type': label,
                'Full_Text': full_text.strip(),
                'URL': f"https://www.reddit.com{submission.permalink}"
            }

            dataset.append(entry)
            unique_ids.add(submission.id)
            count += 1
            
            if count % 10 == 0:
                print(f"  -> Collected {count}/{config['limit']} instances...")

    return dataset

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    try:
        data = collect_data()
        
        # Convert to DataFrame and Save
        df = pd.DataFrame(data)
        
        # Reordering columns to match your exact schema requirement
        df = df[['ID', 'Source', 'Date', 'Phrase_Type', 'Full_Text', 'URL']]
        
        df.to_csv(OUTPUT_FILENAME, index=False)
        
        print(f"\nSUCCESS: Corpus built with {len(df)} total records.")
        print(f"Data saved to: {OUTPUT_FILENAME}")
        
        # Verification of counts
        print("\nDistribution:")
        print(df['Phrase_Type'].value_counts())
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        print("Please check your API credentials and internet connection.")