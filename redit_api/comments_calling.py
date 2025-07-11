import json
import praw
import sys

song_name = sys.argv[1]

# Input and output file paths
input_file_path = f"./filtered_posts_for_{song_name}.json"
output_file_path = f"comments_data_from_reditt_{song_name}.json"

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id='_oecUO_wyvTDSdi8GdPl7g',
    client_secret='YXeILXnViKM-dk4QTXd0gikH8eZaKA',
    user_agent='script:subreddit_scraper:v1.0 (by u/Weird_Desk_9199)'
)

# Function to fetch all comments from a Reddit post URL
def fetch_comments_from_url(url):
    try:
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        return [{
            "id": comment.id,
            "author": str(comment.author),
            "body": comment.body,
            "score": comment.score,
            "created_utc": comment.created_utc,
            "parent_id": comment.parent_id,
            "post_url": url
        } for comment in comments]
    except Exception as e:
        print(f"❌ Error fetching comments for URL: {url}\n{e}")
        return []

# Load posts and fetch comments
all_comments = []
try:
    with open(input_file_path, "r") as infile:
        posts = json.load(infile)
        for post in posts:
            url = post.get("url")
            if url:
                print(f"\n📥 Fetching comments for post: {url}")
                comments = fetch_comments_from_url(url)
                print(f"🗨️  {len(comments)} comments fetched.")
                all_comments.extend(comments)
except Exception as e:
    print(f"⚠️  Failed to read or process input file: {e}")

# Write all comments to output file
try:
    with open(output_file_path, "w") as outfile:
        json.dump(all_comments, outfile, indent=2)
    print(f"\n✅ All comments saved to: {output_file_path}")
except Exception as e:
    print(f"❌ Failed to write comments to file: {e}")
