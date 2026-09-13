import requests
import time
import json
import os
from datetime import datetime


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}

MAX_STORIES_PER_CATEGORY = 25
NUMBER_OF_TOP_STORIES = 1000


# ---------------------------------------------------------
# Category keywords
# ---------------------------------------------------------

CATEGORIES = {
    "technology": [
        "AI",
        "software",
        "tech",
        "computer",
        "data",
        "cloud",
        "API",
        "GPU",
        "LLM",
        "programming",
        "developer",
        "Microsoft",
        "Google",
        "Apple",
        "OpenAI",
        "robot",
        "technology"
    ],

    "worldnews": [
        "war",
        "government",
        "country",
        "president",
        "election",
        "climate",
        "attack",
        "global",
        "China",
        "India",
        "Russia",
        "Ukraine",
        "Israel",
        "Europe",
        "United States",
        "UK",
        "politics"
    ],

    "sports": [
        "NFL",
        "NBA",
        "FIFA",
        "sport",
        "sports",
        "team",
        "player",
        "league",
        "championship",
        "football",
        "soccer",
        "basketball",
        "baseball",
        "tennis",
        "Olympics",
        "World Cup",
        "athlete",
        "match",
        "tournament",
        "coach",
        "goal",
        "game",
        "race",
        "racing",
        "cricket",
        "Formula 1",
        "F1",
        "golf",
        "hockey",
        "rugby",
        "boxing",
        "MMA",
        "medal",
        "final",
        "playoffs",
        "playoff"
    ],

    "science": [
        "research",
        "study",
        "space",
        "physics",
        "biology",
        "discovery",
        "NASA",
        "genome",
        "scientist",
        "science",
        "medical",
        "health",
        "planet",
        "earth",
        "astronomy",
        "experiment"
    ],

    "entertainment": [
        "movie",
        "film",
        "music",
        "Netflix",
        "book",
        "show",
        "award",
        "streaming",
        "actor",
        "actress",
        "TV",
        "television",
        "album",
        "song",
        "Hollywood"
    ]
}

# ---------------------------------------------------------
# Step 1 - Get the top Hacker News story IDs
# ---------------------------------------------------------

def get_top_story_ids():
    """
    Get the first 500 top stories and then collect additional
    story IDs if needed.

    The first 500 come from the official Hacker News
    topstories endpoint.
    """

    try:
        # Get the top story IDs
        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        top_story_ids = response.json()

        print(
            f"Retrieved {len(top_story_ids)} top story IDs."
        )

        # The HN API provides up to 500 top stories.
        # Keep those first.
        story_ids = top_story_ids[:500]

        # If we need more stories, walk backwards from maxitem.
        if len(story_ids) < 1000:

            print("Fetching additional Hacker News stories...")

            max_response = requests.get(
                "https://hacker-news.firebaseio.com/v0/maxitem.json",
                headers=HEADERS,
                timeout=10
            )

            max_response.raise_for_status()

            max_item_id = max_response.json()

            # Add older story IDs until we have enough IDs
            # to search for at least 100 matching stories.
            current_id = max_item_id

            while len(story_ids) < 1500 and current_id > 0:

                current_id -= 1

                # Avoid downloading every item here.
                # We only store the ID for later processing.
                if current_id not in story_ids:
                    story_ids.append(current_id)

        print(
            f"Total story IDs available for searching: "
            f"{len(story_ids)}"
        )

        return story_ids

    except requests.RequestException as error:

        print(
            f"Failed to fetch Hacker News story IDs: {error}"
        )

        return []


# ---------------------------------------------------------
# Step 1 - Get one story's details
# ---------------------------------------------------------

def get_top_story_ids():
    """
    Get the first 500 Hacker News top-story IDs.
    If more stories are needed, add real story IDs from
    the Hacker News newstories endpoint.
    """

    try:
        # -----------------------------------------
        # 1. Get the first 500 top stories
        # -----------------------------------------
        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        top_story_ids = response.json()[:500]

        print(
            f"Retrieved {len(top_story_ids)} top story IDs."
        )

        story_ids = list(top_story_ids)

        # -----------------------------------------
        # 2. Get additional REAL story IDs
        # -----------------------------------------
        if len(story_ids) < 1000:

            print("Fetching additional real Hacker News stories...")

            newstories_url = (
                "https://hacker-news.firebaseio.com/"
                "v0/newstories.json"
            )

            new_response = requests.get(
                newstories_url,
                headers=HEADERS,
                timeout=10
            )

            new_response.raise_for_status()

            new_story_ids = new_response.json()

            # Add new story IDs that aren't already
            # in the first 500 top stories.
            for story_id in new_story_ids:

                if story_id not in story_ids:
                    story_ids.append(story_id)

                if len(story_ids) >= 1000:
                    break

        print(
            f"Total story IDs available for searching: "
            f"{len(story_ids)}"
        )

        return story_ids

    except requests.RequestException as error:

        print(
            f"Failed to fetch Hacker News story IDs: {error}"
        )

        return []


def get_story(story_id):
    """
    Fetch one Hacker News story by its ID.
    """

    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(
            f"Failed to fetch story {story_id}: {error}"
        )
        return None
# ---------------------------------------------------------
# Determine category
# ---------------------------------------------------------

def get_category(title):
    """
    Determine the category of a story based on keywords.

    Matching is case-insensitive.

    Specific categories are checked before entertainment
    so common words do not cause incorrect classification.
    """

    title_lower = title.lower()

    # Check technology first
    for keyword in CATEGORIES["technology"]:
        if keyword.lower() in title_lower:
            return "technology"

    # Check world news
    for keyword in CATEGORIES["worldnews"]:
        if keyword.lower() in title_lower:
            return "worldnews"

    # Check sports
    for keyword in CATEGORIES["sports"]:
        if keyword.lower() in title_lower:
            return "sports"

    # Check science
    for keyword in CATEGORIES["science"]:
        if keyword.lower() in title_lower:
            return "science"

    # Check entertainment last
    for keyword in CATEGORIES["entertainment"]:
        if keyword.lower() in title_lower:
            return "entertainment"

    # No category matched
    return None

# ---------------------------------------------------------
# Extract required fields
# ---------------------------------------------------------

def extract_story_fields(story, category):
    """
    Extract the seven required fields.
    """

    return {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().isoformat()
    }


# ---------------------------------------------------------
# Collect stories
# ---------------------------------------------------------


def collect_stories(story_ids):
    """
    Collect up to 25 stories for each category.
    """

    collected_stories = []

    for category, keywords in CATEGORIES.items():

        print(f"\nCollecting {category} stories...")

        category_count = 0

        for story_id in story_ids:

            # Stop this category after 25 stories
            if category_count >= MAX_STORIES_PER_CATEGORY:
                break

            story = get_story(story_id)

            if story is None:
                continue

            # Only collect Hacker News stories
            if story.get("type") != "story":
                continue

            title = story.get("title", "")

            if not title:
                continue

            # Check this category's keywords
            title_lower = title.lower()

            matched = False

            for keyword in keywords:
                if keyword.lower() in title_lower:
                    matched = True
                    break

            if not matched:
                continue

            # Save the story
            story_data = extract_story_fields(
                story,
                category
            )

            collected_stories.append(story_data)

            category_count += 1

            print(
                f"[{category_count}/25] "
                f"{category}: {title}"
            )

        print(
            f"Collected {category_count} "
            f"{category} stories."
        )

        # Wait 2 seconds between categories
        time.sleep(2)

    return collected_stories

# ---------------------------------------------------------
# Save stories to JSON
# ---------------------------------------------------------

def save_to_json(stories):
    """
    Save collected stories to a JSON file.
    """

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Create filename using today's date
    today = datetime.now().strftime("%Y%m%d")

    filename = f"data/trends_{today}.json"

    # Save stories to JSON
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(stories, file, indent=2, ensure_ascii=False)

    # Print result
    print(
        f"Collected {len(stories)} stories. "
        f"Saved to {filename}"
    )

    return filename


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main():

    print("Step 1: Fetching top Hacker News story IDs...")

    story_ids = get_top_story_ids()

    if not story_ids:
        print("No story IDs retrieved.")
        return

    print("\nStep 2: Collecting and categorizing stories...")

    stories = collect_stories(story_ids)

    print("\nStep 3: Saving stories to JSON...")

    save_to_json(stories)


if __name__ == "__main__":
    main()