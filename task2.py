import json
import csv
import os


# Load the JSON file
with open(
    "data/trends_20260913.json",
    "r",
    encoding="utf-8"
) as file:
    stories = json.load(file)


print(f"Loaded {len(stories)} stories.")

# Clean the story data
cleaned_stories = []

for story in stories:

    # Remove stories with missing titles
    if not story.get("title"):
        continue

    # Remove stories with missing authors
    if not story.get("author"):
        continue

    # Replace missing numeric values with 0
    score = story.get("score", 0)
    num_comments = story.get("num_comments", 0)

    # Create a cleaned story
    cleaned_story = {
        "post_id": story.get("post_id"),
        "title": story.get("title").strip(),
        "category": story.get("category"),
        "score": score,
        "num_comments": num_comments,
        "author": story.get("author"),
        "collected_at": story.get("collected_at")
    }

    cleaned_stories.append(cleaned_story)


print(f"Cleaned {len(cleaned_stories)} stories.")

# Create the data folder if it doesn't exist
os.makedirs("data", exist_ok=True)


# Set the CSV output filename
csv_filename = "data/trends_20260913.csv"


# Save the cleaned stories to CSV
with open(
    csv_filename,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    # Define the CSV columns
    fieldnames = [
        "post_id",
        "title",
        "category",
        "score",
        "num_comments",
        "author",
        "collected_at"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    # Write the column headers
    writer.writeheader()

    # Write all cleaned stories
    writer.writerows(cleaned_stories)


print(f"Saved cleaned data to {csv_filename}")