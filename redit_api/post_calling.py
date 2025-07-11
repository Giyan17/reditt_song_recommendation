import praw

# Initialize Reddit client
reddit = praw.Reddit(
    client_id='_oecUO_wyvTDSdi8GdPl7g',
    client_secret='YXeILXnViKM-dk4QTXd0gikH8eZaKA',
    user_agent='script:subreddit_scraper:v1.0 (by u/Weird_Desk_9199)'
)

# Choose the subreddit
subreddit = reddit.subreddit('BollyBlindsNGossip')  # e.g., 'python', 'technology'

# Search all of Reddit (you can also do reddit.subreddit('music') or others) 
query = "Similar songs like Tum Hi Ho"

# Fetch search results (max 1000, default is relevance sort)
for post in reddit.subreddit("all").search(query, sort="relevance", time_filter="all", limit=10000):
# for post in subreddit.search(query, sort="relevance", time_filter="all", limit=10000):
    print({
        "title": post.title,
        "subreddit": post.subreddit.display_name,
        "url": post.url,
        "score": post.score,
        "author": str(post.author),
        "created_utc": post.created_utc,
        "selftext": post.selftext[:200]  # trim long text
    })

