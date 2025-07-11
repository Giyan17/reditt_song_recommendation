import ast
import json
from ollama import Client

# Ask user for the target song
target_song = input("Enter the song name to match posts against: ").strip()

# File containing Reddit posts
file_path = "post_calling.txt"

# Initialize the Ollama client
client = Client(host="http://localhost:11434")

# Function to check if post is relevant to the song
def is_similar_to_song(post, song):
    content = f"Title: {post.get('title', '')}\nText: {post.get('selftext', '')}"
    
    prompt = f"""
You are a music expert assistant.
Check if the following Reddit post is asking for or discussing Hindi songs that are similar in vibe, lyrics, or emotion to the song titled "{song}".
Respond only with "Yes" or "No".

Post:
{content}
"""
    try:
        response = client.generate(
            model="llama3.1",
            prompt=prompt,
            system="You are a helpful assistant.",
        )
        result = response.get("response", "")
        return "yes" in result.lower()
    except Exception as e:
        print(f"Error calling Ollama model: {e}")
        return False

# Store matching posts
matching_posts = []

# Read and process the posts
with open(file_path, "r") as file:
    for line in file:
        try:
            post = ast.literal_eval(line.strip())
            if is_similar_to_song(post, target_song):
                matching_posts.append(post)
        except Exception as e:
            print(f"Error parsing line:\n{line}\n{e}")

# Output results
print(f"\n Posts similar to '{target_song}':\n")
for post in matching_posts:
    print(json.dumps(post, indent=2))
