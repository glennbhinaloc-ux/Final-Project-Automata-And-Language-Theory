"""
Gender Neutral Language Recognizer
Automata and Language Theory - Machine Problem

Reads a .txt file, finds predefined gender-specific terms using regular
expressions, and suggests gender-neutral alternatives (for review only).

Usage:  python gender_neutral_recognizer.py path/to/file.txt
"""

import os
import re
import sys


GENDER_TERMS = {
    "chairman": "chairperson",
    "chairmen": "chairpersons",
    "policeman": "police officer",
    "policemen": "police officers",
    "fireman": "firefighter",
    "firemen": "firefighters",
    "stewardess": "flight attendant",
    "mankind": "humankind",
    "mailman": "mail carrier",
    "businessman": "businessperson",
    "spokesman": "spokesperson",
    "manpower": "workforce",
    "manhole": "maintenance hole",
    "man-made": "artificial / human-made",
}

SUPPORTED_EXTENSION = ".txt"
EMPTY_MESSAGE = "The file is empty. Please select a file with text content."
NO_RESULTS_MESSAGE = "No predefined gender-specific terms were detected."
NOTE = "Note: Suggestions are for review; the appropriate replacement depends on context."


def load_text(file_path):
    """Read a .txt file and return its text.
    Raises ValueError with a clear message if the file cannot be used."""
    if os.path.splitext(file_path)[1].lower() != SUPPORTED_EXTENSION:
        raise ValueError("Unsupported file format. Please select a .txt file.")

    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    for encoding in ("utf-8", "latin-1"):
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue 
        except OSError as error:
            raise ValueError(f"The file could not be opened: {error}")

    raise ValueError("The file could not be read (unsupported text encoding).")


def build_patterns(terms):
    """Build one compiled regex per term, programmatically from the term list."""
    patterns = {}
    for term in terms:
        words = re.split(r"[\s-]+", term)
        body = r"[\s-]+".join(re.escape(word) for word in words)
        patterns[term] = re.compile(r"\b" + body + r"\b", re.IGNORECASE)
    return patterns


def detect_terms(text, patterns):
    """Count every occurrence of each term. Returns only terms that were found."""
    counts = {}
    for term, pattern in patterns.items():
        total = sum(1 for _ in pattern.finditer(text))
        if total > 0:
            counts[term] = total
    return counts


def format_results(counts, terms):
    """Return the results as a plain-text table (or the 'none found' message)."""
    if not counts:
        return NO_RESULTS_MESSAGE

    headers = ("Detected Term", "Number of Occurrences", "Suggested Alternative")
    rows = [(term, str(count), terms[term]) for term, count in counts.items()]

    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(3)]

    def line(cells):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    separator = "-+-".join("-" * w for w in widths)
    output = [line(headers), separator] + [line(row) for row in rows]
    output += ["", NOTE]
    return "\n".join(output)


def main():
    """Entry point: get the file path, run detection, print the results."""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path of the .txt file: ").strip().strip('"')

    try:
        text = load_text(file_path)
    except ValueError as error:
        print(error)
        return

    if text.strip() == "":
        print(EMPTY_MESSAGE)
        return

    patterns = build_patterns(GENDER_TERMS)
    counts = detect_terms(text, patterns)
    print(format_results(counts, GENDER_TERMS))


if __name__ == "__main__":
    main()
