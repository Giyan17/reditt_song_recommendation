import praw
import sys
import json

song_name = sys.argv[1]
# Initialize Reddit client
reddit = praw.Reddit(
    client_id='_oecUO_wyvTDSdi8GdPl7g',
    client_secret='YXeILXnViKM-dk4QTXd0gikH8eZaKA',
    user_agent='script:subreddit_scraper:v1.0 (by u/Weird_Desk_9199)'
)

# Choose the subreddit
# subreddit = reddit.subreddit('BollyBlindsNGossip')  # e.g., 'python', 'technology'

# # Search all of Reddit (you can also do reddit.subreddit('music') or others) 
# query = "Songs with similar vibe to Tum Hi Ho"

# # Fetch search results (max 1000, default is relevance sort)
# for post in reddit.subreddit("all").search(query, sort="relevance", time_filter="all", limit=100):
# # for post in subreddit.search(query, sort="relevance", time_filter="all", limit=10000):
#     print({
#         "title": post.title,
#         "subreddit": post.subreddit.display_name,
#         "url": post.url,
#         "score": post.score,
#         "author": str(post.author),
#         "created_utc": post.created_utc,
#         "selftext": post.selftext[:200]  # trim long text
#     })

subreddits_to_search = [
    "BollyBlindsNGossip",
    "IndianMusic",
    "BollywoodMusic",
    "music",
    "AskReddit"
    "LetsTalkMusic"
    "IndianHipHopHeads"
    "MusicIndia"
    "bollywood"
    "punjabimusic"
    "IndianCinema"
]

query = "Songs suggestions with similar vibe to {song_name}"

list_of_post = []

for subreddit_name in subreddits_to_search:
    subreddit = reddit.subreddit(subreddit_name)
    print(f"\n🔍 Results from r/{subreddit_name}:\n")

    try:
        results = subreddit.search(query, sort="relevance", time_filter="all", limit=20)
        for post in results:
            output_post = {
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "author": str(post.author),
                "created_utc": post.created_utc,
                "selftext": post.selftext[:200]  # preview first 200 chars
            }
            list_of_post.append(output_post)
            print(output_post)
    except Exception as e:
        print(f"⚠️ Error searching r/{subreddit_name}: {e}")

file_path = f"posts_data_from_reditt_{song_name}.json"

with open(file_path, "w") as f:
    json.dump(list_of_post, f, indent=2) 

