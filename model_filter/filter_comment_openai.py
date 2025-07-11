import json
from ollama import Client
import sys

# Accept song name from command-line argument
song_name = sys.argv[1]

# Initialize the Ollama client
client = Client(host="http://localhost:11434")

# File containing Reddit comments
comments_file = f"./comments_data_from_reditt_{song_name}.json"
output_file = f"filtered_music_comments_for_{song_name}.json"

# Function to check if a comment contains music-related content
def analyze_comment_for_music(comment_text):
    prompt = f'''
You are a music content detector. Your task is to analyze a Reddit comment and determine if it contains music-related information. Look for:

1. Music platform links (YouTube, Spotify, etc.)
2. Song names
3. Artist names
4. Album names
5. Music genres
6. Any music-related content like recommendations

If in any comment you find this song name {song_name} or any movie name, dont include it in the response

If music-related content is found, extract it.

Format your response as JSON with this structure:
{{
  "has_music": true/false,
  "extracted_info": "relevant music information found",
  "links": ["array of any URLs found"],
  "songs": ["array of song names found"],
  "artists": ["array of artist names found"]
}}

If no music content is found, return:
{{
  "has_music": false,
  "extracted_info": "",
  "links": [],
  "songs": [],
  "artists": []
}}

Comment:
{comment_text}
'''
    try:
        response = client.generate(
            model="llama3.1",
            prompt=prompt,
            system="You are a helpful assistant."
        )
        result = response.get("response", "")
        return json.loads(result)
    except Exception as e:
        print(f"Error analyzing comment: {e}")
        return None

# Read all comments from the file
with open(comments_file, "r") as file:
    try:
        comments = json.load(file)[:20]
    except Exception as e:
        print(f"Failed to read or parse input JSON: {e}")
        comments = []

# Analyze comments and collect music-related ones
filtered_results = []
for comment in comments:
    body = comment.get("body", "")
    analysis = analyze_comment_for_music(body)
    if analysis and analysis.get("has_music"):
        print(f"\n🎵 Music-related comment found:")
        print(json.dumps({"comment": comment, "analysis": analysis}, indent=2), flush=True)
        filtered_results.append({"comment": comment, "analysis": analysis})

# Write filtered results to output file
with open(output_file, "w") as outfile:
    json.dump(filtered_results, outfile, indent=2)

print(f"\n✅ Music-related comments saved to {output_file}")