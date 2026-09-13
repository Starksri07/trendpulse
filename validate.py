import os
import json
import glob


REQUIRED_FIELDS = [
    "post_id",
    "title",
    "category",
    "score",
    "num_comments",
    "author",
    "collected_at"
]

MAX_PER_CATEGORY = 25
MIN_TOTAL_STORIES = 100


def validate_json():
    files = glob.glob("data/trends_*.json")

    if not files:
        print("ERROR: No JSON file found.")
        return

    # Select the newest JSON file
    filename = max(files, key=os.path.getmtime)

    print(f"Validating: {filename}")

    with open(filename, "r", encoding="utf-8") as file:
        stories = json.load(file)

    print("=" * 50)
    print("JSON VALIDATION")
    print("=" * 50)

    # Check total stories
    total = len(stories)

    print(f"Total stories: {total}")

    if total >= 100:
        print("PASS: At least 100 stories collected.")
    else:
        print("FAIL: Less than 100 stories.")

    # Count stories in each category
    category_counts = {}

    for story in stories:
        category = story.get("category")

        if category not in category_counts:
            category_counts[category] = 0

        category_counts[category] += 1

    print("\nCategory counts:")

    for category, count in category_counts.items():

        print(f"{category}: {count}")

        if count <= 25:
            print(
                f"  PASS: {category} is within 25-story limit."
            )
        else:
            print(
                f"  FAIL: {category} exceeds 25 stories."
            )

    # Check all 7 required fields
    print("\nChecking required fields...")

    required_fields = [
        "post_id",
        "title",
        "category",
        "score",
        "num_comments",
        "author",
        "collected_at"
    ]

    all_fields_present = True

    for index, story in enumerate(stories, start=1):

        for field in required_fields:

            if field not in story:
                print(
                    f"FAIL: Story {index} is missing "
                    f"'{field}'."
                )

                all_fields_present = False

    if all_fields_present:
        print(
            "PASS: All stories contain all 7 required fields."
        )

    print("\n" + "=" * 50)
    print("VALIDATION FINISHED")
    print("=" * 50)


if __name__ == "__main__":
    validate_json()