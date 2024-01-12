import os
import random

BACKEND_BASE_URL = (
    'http://localhost:8001'
    if os.environ.get('GS_DEV', '').lower() == 'true'
    else 'https://backend.goldenset.io'
)

GOLD_COLOR = (252, 168, 37)

ADJECTIVES = [
    "happy",
    "sad",
    "excited",
    "tired",
    "energetic",
    "beautiful",
    "ugly",
    "smart",
    "dumb",
    "funny",
    "serious",
    "kind",
    "mean",
    "friendly",
    "hostile",
    "generous",
    "selfish",
    "brave",
    "cowardly",
    "strong",
    "weak",
    "tall",
    "short",
    "old",
    "young",
    "wise",
    "foolish",
    "honest",
    "dishonest",
    "calm",
    "anxious",
    "quiet",
    "loud",
    "clean",
    "dirty",
    "gentle",
    "rough",
    "smooth",
    "rough",
    "soft",
]
NOUNS = [
    "apple",
    "banana",
    "car",
    "dog",
    "cat",
    "book",
    "computer",
    "house",
    "tree",
    "flower",
    "sun",
    "moon",
    "star",
    "friend",
    "family",
    "bird",
    "river",
    "mountain",
    "ocean",
    "city",
    "country",
    "pen",
    "pencil",
    "phone",
    "chair",
    "table",
    "shoe",
    "hat",
    "shirt",
    "pants",
    "sock",
    "guitar",
    "piano",
    "movie",
    "song",
    "school",
    "teacher",
    "student",
    "cake",
    "coffee",
]


def get_random_name() -> str:
    """Returns a random name in the form of <adjective>-<noun>"""
    return random.choice(ADJECTIVES) + '-' + random.choice(NOUNS)
