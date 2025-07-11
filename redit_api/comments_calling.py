import ast
import json
import praw

# File with Reddit posts (each post is a JSON object per line)
file_path = "filter_post.txt"

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
            "parent_id": comment.parent_id
        } for comment in comments]
    except Exception as e:
        print(f"❌ Error fetching comments for URL: {url}\n{e}")
        return []

# Read posts and process each one
with open(file_path, "r") as file:
    buffer = ""
    for line in file:
        line = line.strip()
        if line.startswith("{") and buffer:
            # Process the last buffered JSON block
            try:
                post = json.loads(buffer)
                url = post.get("url")
                if url:
                    print(f"\n📥 Fetching comments for post: {url}")
                    comments = fetch_comments_from_url(url)
                    print(f"🗨️  {len(comments)} comments fetched.")
                    for comment in comments:
                        print(json.dumps(comment, indent=2))
            except Exception as e:
                print(f"⚠️  Failed to parse or fetch comments: {e}")
            buffer = line  # start new JSON object
        else:
            buffer += line

    # Don't forget the last object
    if buffer:
        try:
            post = json.loads(buffer)
            url = post.get("url")
            if url:
                print(f"\n📥 Fetching comments for post: {url}")
                comments = fetch_comments_from_url(url)
                print(f"🗨️  {len(comments)} comments fetched.")
                for comment in comments:
                    print(json.dumps(comment, indent=2))
        except Exception as e:
            print(f"⚠️  Failed to parse or fetch comments: {e}")
