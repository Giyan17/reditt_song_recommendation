import json
import sys

song_name = sys.argv[1]
# Input file with full JSON array
file_path = f"filtered_music_comments_for_{song_name}.json"
output_path = f"unique_songs_output_{song_name}.json"

# Set to store unique songs while preserving order
unique_songs = []
seen = set()

# Read and parse JSON file
with open(file_path, "r") as f:
    try:
        data = json.load(f)
        for entry in data:
            songs = entry.get("analysis", {}).get("songs", [])
            for song in songs:
                if song not in seen:
                    seen.add(song)
                    unique_songs.append(song)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Write unique songs to a new JSON file
with open(output_path, "w") as f:
    json.dump(unique_songs, f, indent=2)

print(f"\n✅ {len(unique_songs)} unique songs saved to '{output_path}'")
