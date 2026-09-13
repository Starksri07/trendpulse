import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the analysed data from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create the outputs folder if it does not already exist
os.makedirs("outputs", exist_ok=True)

print("Loaded", len(df), "stories from data/trends_analysed.csv")

# Chart 1: Top 10 stories by score

# Get the 10 stories with the highest scores
top_10 = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_10["short_title"] = top_10["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

# Create a horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(top_10["short_title"], top_10["score"])

# Put the highest-scoring story at the top
plt.gca().invert_yaxis()

# Add chart title and axis labels
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

# Save the chart before showing it
plt.savefig("outputs/chart1_top_stories.png", bbox_inches="tight")

plt.show()

# Chart 2: Stories per category

# Count how many stories belong to each category
category_counts = df["category"].value_counts()

# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(category_counts.index, category_counts.values)

# Add chart title and axis labels
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

# Save the chart before showing it
plt.savefig("outputs/chart2_categories.png", bbox_inches="tight")

plt.show()

# Chart 3: Score vs Comments

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Create the scatter plot
plt.figure(figsize=(10, 6))

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Non-popular"
)

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

# Add chart title and axis labels
plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

# Add legend
plt.legend()

# Save the chart before showing it
plt.savefig("outputs/chart3_scatter.png", bbox_inches="tight")

plt.show()

# Bonus: Create a dashboard containing all three charts

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Chart 1: Top 10 stories by score
axes[0, 0].barh(top_10["short_title"], top_10["score"])
axes[0, 0].invert_yaxis()
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")

# Chart 2: Stories per category
axes[0, 1].bar(category_counts.index, category_counts.values)
axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

# Chart 3: Score vs Comments
axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Non-popular"
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].legend()

# Leave the fourth dashboard area empty
axes[1, 1].axis("off")

# Add the overall dashboard title
fig.suptitle("TrendPulse Dashboard", fontsize=18)

# Adjust the layout
plt.tight_layout()

# Save the dashboard
plt.savefig("outputs/dashboard.png", bbox_inches="tight")

plt.show()