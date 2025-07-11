import json
from ollama import Client
import sys

# Get the target song name from command-line argument
song_name = sys.argv[1]

# JSON file containing Reddit posts
file_path = f"./posts_data_from_reditt_{song_name}.json"

# Output file to store matching posts
output_file = f"filtered_posts_for_{song_name}.json"

# Initialize the Ollama client
client = Client(host="http://localhost:11434")

# Function to check if post is relevant to the song
def is_similar_to_song(post, song):
    content = f"Title: {post.get('title', '')}\nText: {post.get('selftext', '')}"

    prompt = f'''
You are a music expert assistant.
Check if the following Reddit post is asking for or discussing Hindi songs that are similar in vibe, lyrics, or emotion to the song titled "{song}".
Respond only with "Yes" or "No".

Post:
{content}
'''

    try:
        response = client.generate(
            model="llama3.1",
            prompt=prompt,
            system="You are a helpful assistant."
        )
        result = response.get("response", "")
        return "yes" in result.lower()
    except Exception as e:
        print(f"Error calling Ollama model: {e}")
        return False

# List to store matching posts
matching_posts = []

# Read JSON file and filter matching posts
try:
    with open(file_path, "r") as file:
        posts = json.load(file)
        for post in posts:
            if is_similar_to_song(post, song_name):
                matching_posts.append(post)
except Exception as e:
    print(f"Error reading or parsing file: {e}")

# Output matching posts
print(f"\nPosts similar to '{song_name}':\n")
for post in matching_posts:
    print(json.dumps(post, indent=2))

# Dump results to a new JSON file
with open(output_file, "w") as f:
    json.dump(matching_posts, f, indent=2)

print(f"\n✅ Matching posts saved to {output_file}")
