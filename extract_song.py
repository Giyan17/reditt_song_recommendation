import json
import re

# File with music-related comment and analysis data
file_path = "filtered_songs.txt"

# List to store songs with scores
scored_songs = []

# Read the entire file content
with open(file_path, "r") as f:
    content = f.read()

# Extract all JSON blocks using regex
json_blocks = re.findall(r"\{\s*\"comment\".*?\}\s*\}", content, re.DOTALL)

# Parse and extract songs and scores
for block in json_blocks:
    try:
        data = json.loads(block)
        score = data.get("comment", {}).get("score", 0)
        songs = data.get("analysis", {}).get("songs", [])
        for song in songs:
            scored_songs.append((song, score))
    except Exception as e:
        print(f"Failed to parse block: {e}")

# Sort songs by score descending and remove duplicates while preserving order
seen = set()
sorted_songs = []
for song, score in sorted(scored_songs, key=lambda x: -x[1]):
    if song not in seen:
        seen.add(song)
        sorted_songs.append((song, score))

# Print results
print("\n🎶 Extracted Songs (sorted by score):")
for song, score in sorted_songs:
    print(f"- {song} (score: {score})")
