# Word counts need normalisation because Python treats "AI", "ai" and "AI,"
# as three different strings even though a human reads them as the same word.
# Lower-casing and stripping punctuation collapses these variants into one key.
#
# set_a - set_b only pulls out items that belong to set_a alone, and doing it
# the other way round gives a different answer, so each direction has to be
# computed separately if we want to know which platform a user came from.
# set_a ^ set_b skips that distinction and just lumps everyone who is in
# exactly one of the two sets into a single result.

import string


def build_word_counts(text):
    """Return a dictionary of word frequencies from a paragraph of text."""
    word_counts = {}
    for raw_word in text.split():
        cleaned_word = raw_word.lower().strip(string.punctuation)
        if not cleaned_word:
            continue
        word_counts.setdefault(cleaned_word, 0)
        word_counts[cleaned_word] += 1
    return word_counts


def compare_followers(platform_a_followers, platform_b_followers):
    """Compare two follower lists and return overlap and unique members."""
    set_a = set(platform_a_followers)
    set_b = set(platform_b_followers)

    both_platforms = set_a & set_b
    only_a = set_a - set_b
    only_b = set_b - set_a
    either_only = set_a ^ set_b

    return both_platforms, only_a, only_b, either_only


def print_word_counts(word_counts):
    for word in sorted(word_counts):
        print(f"{word}: {word_counts[word]}")


def main():
    text = ("AI is changing the world. ai is powering new tools, and AI is "
            "helping researchers learn faster. The world loves AI, and the "
            "world depends on it more each year.")

    print("Word Frequency Counter")
    print("-----------------------")
    word_counts = build_word_counts(text)
    print_word_counts(word_counts)

    platform_a_followers = ["u101", "u102", "u103", "u104", "u105"]
    platform_b_followers = ["u103", "u104", "u106", "u107"]

    print()
    print("Follower Deduplicator")
    print("-----------------------")
    both_platforms, only_a, only_b, either_only = compare_followers(
        platform_a_followers, platform_b_followers)

    print("Follows on both platforms:", both_platforms)
    print("Unique to Platform A:", only_a)
    print("Unique to Platform B:", only_b)
    print("Unique to exactly one platform:", either_only)

    # empty paragraph edge case
    empty_counts = build_word_counts("")
    print()
    print("Empty paragraph test:", empty_counts)

    # punctuation-only token edge case
    dash_counts = build_word_counts("AI is great -- truly.")
    print("Punctuation-only token test:", dash_counts)

    # identical follower lists edge case
    same_both, same_only_a, same_only_b, same_either = compare_followers(
        platform_a_followers, platform_a_followers)
    print("Identical lists test - both:", same_both)
    print("Identical lists test - only_a:", same_only_a)
    print("Identical lists test - only_b:", same_only_b)

main()
