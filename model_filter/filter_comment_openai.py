import json
from ollama import Client

# Initialize the Ollama client
client = Client(host="http://localhost:11434")

# File containing Reddit comments
comments_file = "filter_comments.txt"

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
            system="You are a helpful assistant.",
        )
        result = response.get("response", "")
        return json.loads(result)
    except Exception as e:
        print(f"Error analyzing comment: {e}")
        return None

# Read and process the comments
with open(comments_file, "r") as file:
    buffer = ""
    for line in file:
        line = line.strip()

        if line.startswith("{") and buffer:
            try:
                comment = json.loads(buffer)
                body = comment.get("body", "")
                analysis = analyze_comment_for_music(body)
                if analysis and analysis.get("has_music"):
                    print(f"\n🎵 Music-related comment found:")
                    print(json.dumps({"comment": comment, "analysis": analysis}, indent=2), flush=True)
            except Exception as e:
                print(f"Failed to parse or analyze comment: {e}")
            buffer = line
        else:
            buffer += line

    # Process the last buffered comment
    if buffer:
        try:
            comment = json.loads(buffer)
            body = comment.get("body", "")
            analysis = analyze_comment_for_music(body)
            if analysis and analysis.get("has_music"):
                print(f"\n🎵 Music-related comment found:")
                print(json.dumps({"comment": comment, "analysis": analysis}, indent=2))
        except Exception as e:
            print(f"Failed to parse or analyze last comment: {e}")
