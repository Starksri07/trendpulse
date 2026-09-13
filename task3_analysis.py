import pandas as pd
import numpy as np

# Load the cleaned CSV file from Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print the first 5 rows
print("First 5 rows:")
print(df.head())

# Print the shape of the DataFrame
print("\nDataFrame shape:", df.shape)

# Calculate and print the average score
average_score = df["score"].mean()
print("\nAverage score:", average_score)

# Calculate and print the average number of comments
average_comments = df["num_comments"].mean()
print("Average comments:", average_comments)

# NumPy analysis

scores = df["score"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print("Mean score:", mean_score)
print("Median score:", median_score)
print("Standard deviation:", std_score)
print("Maximum score:", max_score)
print("Minimum score:", min_score)

# Find the category with the most stories
category_counts = df["category"].value_counts()
most_stories_category = category_counts.idxmax()
most_stories_count = category_counts.max()

print(
    "\nMost stories in:",
    most_stories_category,
    "(",
    most_stories_count,
    "stories)"
)

# Find the story with the most comments
most_commented = df.loc[df["num_comments"].idxmax()]

print(
    "\nMost commented story:",
    most_commented["title"],
    "-",
    most_commented["num_comments"],
    "comments"
)

# Add engagement column
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Add is_popular column
df["is_popular"] = df["score"] > average_score

# Display the new columns
print("\nNew columns added:")
print(df[["title", "engagement", "is_popular"]].head())

# Save the analysed DataFrame to a new CSV file
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")