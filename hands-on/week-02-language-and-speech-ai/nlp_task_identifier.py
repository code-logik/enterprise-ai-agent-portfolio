"""
Week 2 - Language and Speech AI

This program accepts a block of text and identifies AI/NLP tasks
that may be appropriate for analyzing the text.

It intentionally does not call an AI service.

The purpose is to learn how to select an AI workload before
implementing the workload with services such as Microsoft Foundry,
Azure AI Language, or a large language model.
"""

import re


SUMMARY_WORD_THRESHOLD = 40

SENTIMENT_TERMS = {
    "excellent",
    "good",
    "great",
    "happy",
    "satisfied",
    "success",
    "successful",
    "poor",
    "bad",
    "failed",
    "failure",
    "frustrated",
    "angry",
    "disappointed",
    "problem",
    "issue",
}


def read_text() -> str:
    """Read multiple lines of text from the console."""

    print("Paste or type a block of text.")
    print("Press ENTER on an empty line when finished.")
    print()

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines).strip()


def find_entity_candidates(text: str) -> list[str]:
    """
    Find simple entity-like text.

    This is only a heuristic for the lab. It is NOT named-entity
    recognition and should not be treated as an AI result.
    """

    pattern = r"\b[A-Z][A-Za-z0-9&.-]*(?:\s+[A-Z][A-Za-z0-9&.-]*)*\b"

    matches = re.findall(pattern, text)

    # Remove duplicates while preserving order.
    unique_matches = list(dict.fromkeys(matches))

    return unique_matches[:10]


def contains_sentiment_language(text: str) -> bool:
    """Look for simple words that suggest sentiment may be present."""

    words = re.findall(r"[A-Za-z']+", text.lower())

    return bool(set(words) & SENTIMENT_TERMS)


def analyze_text(text: str) -> None:
    """Identify AI tasks that may be useful for the supplied text."""

    word_count = len(text.split())
    entity_candidates = find_entity_candidates(text)
    sentiment_detected = contains_sentiment_language(text)
    summarization_recommended = word_count >= SUMMARY_WORD_THRESHOLD

    print()
    print("=" * 60)
    print("TEXT ANALYSIS PLAN")
    print("=" * 60)

    print(f"\nWord count: {word_count}")

    print("\n1. ENTITY DETECTION")

    if entity_candidates:
        print("Recommended: YES")
        print("Reason: The text contains entity-like names or terms.")
        print("Possible candidates:")

        for candidate in entity_candidates:
            print(f"  - {candidate}")
    else:
        print("Recommended: POSSIBLY")
        print(
            "Reason: No obvious entity-like text was found by the "
            "simple heuristic."
        )

    print("\nBest technology fit:")
    print(
        "Traditional NLP is a strong choice when consistent, "
        "structured entity extraction is required."
    )
    print(
        "An LLM can be useful when entities require broader context "
        "or domain-specific interpretation."
    )

    print("\n2. SENTIMENT ANALYSIS")

    if sentiment_detected:
        print("Recommended: YES")
        print("Reason: The text contains language that may express sentiment.")
    else:
        print("Recommended: POSSIBLY")
        print("Reason: No obvious sentiment language was detected.")

    print("\nBest technology fit:")
    print(
        "Traditional NLP is useful for repeatable sentiment labels "
        "or scores across large volumes of text."
    )
    print(
        "An LLM is useful when the meaning is nuanced or an explanation "
        "of the sentiment is required."
    )

    print("\n3. SUMMARIZATION")

    if summarization_recommended:
        print("Recommended: YES")
        print(
            f"Reason: The text contains at least "
            f"{SUMMARY_WORD_THRESHOLD} words."
        )
    else:
        print("Recommended: NO")
        print("Reason: The text is already relatively short.")

    print("\nBest technology fit:")
    print(
        "A generative AI model or LLM is generally the better fit "
        "for producing a natural-language summary."
    )

    print("\n4. SPEECH AI")
    print("Recommended: NO for this input.")
    print("Reason: The supplied information is already text.")
    print(
        "Speech recognition would be used if the original input were "
        "spoken audio."
    )
    print(
        "Speech synthesis would be used if the system needed to speak "
        "its response."
    )

    print("\n5. AGENTIC AI")
    print("Recommended: NO for this task.")
    print(
        "Reason: Text analysis does not require the system to select "
        "tools or perform actions."
    )

    print()
    print("=" * 60)


def main() -> None:
    """Run the Week 2 NLP task-identification exercise."""

    text = read_text()

    if not text:
        print("No text was entered.")
        return

    analyze_text(text)


if __name__ == "__main__":
    main()