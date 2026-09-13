import pandas as pd


# Load the JSON file created in Task 1
df = pd.read_json("data/trends_20260913.json")

# Print the number of rows loaded
print(f"Loaded {len(df)} stories from data/trends_20260913.json")

# Remove duplicate rows based on post_id
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")

# Remove rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")

# Make score and num_comments integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# Remove stories with a score less than 5
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")

# Remove extra spaces from the beginning and end of titles
df["title"] = df["title"].str.strip()

# Save the cleaned DataFrame as a CSV file
output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")

# Print the number of stories in each category
print("\nStories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")