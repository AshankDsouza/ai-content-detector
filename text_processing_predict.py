"""
text_processing_predict.py

Checks text for AI traces using two methods:
  1. Digital traces  — ASCII quote/apostrophe analysis + AI tool mention detection
                       (based on digital_traces_of_ai_content.pdf)
  2. Stylometric     — surface-level writing pattern heuristics

Usage:
    python text_processing_predict.py --text "Your text here"
    python text_processing_predict.py --file my_essay.txt
"""

import re
import argparse
import statistics

from digital_traces import analyze as digital_traces


# ─────────────────────────────────────────────────────────────────────────────
# METHOD 2: Stylometric Patterns
# Heuristic checks on surface-level writing style.
# ─────────────────────────────────────────────────────────────────────────────

# Phrases that appear far more often in AI-generated text than human writing
_AI_PHRASES = [
    r'\bit(?:\'s)? worth noting\b',
    r'\bin conclusion\b',
    r'\bin summary\b',
    r'\bto summarize\b',
    r'\bfurthermore\b',
    r'\badditionally\b',
    r'\bmoreover\b',
    r'\bnevertheless\b',
    r'\bin other words\b',
    r'\boverall\b',
    r'\bit is important to note\b',
    r'\bthis is particularly\b',
    r'\bplays a crucial role\b',
    r'\bit is worth mentioning\b',
    r'\bsignificantly\b',
    r'\bultimately\b',
    r'\bdelve into\b',
    r'\btailored to\b',
    r'\bin the realm of\b',
    r'\ba testament to\b',
]

_AI_PHRASE_RE = [re.compile(p, re.IGNORECASE) for p in _AI_PHRASES]


def _sentences(text: str) -> list:
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in raw if len(s.split()) >= 3]


def stylometric(text: str) -> dict:
    words      = text.split()
    word_count = len(words)

    sents        = _sentences(text)
    sent_lengths = [len(s.split()) for s in sents] if sents else [0]

    avg_sent_len   = round(statistics.mean(sent_lengths), 1)
    sent_len_stdev = round(statistics.stdev(sent_lengths), 1) if len(sent_lengths) > 1 else 0.0

    unique_words = len(set(w.lower().strip(".,!?;:\"'") for w in words))
    ttr          = round(unique_words / word_count, 3) if word_count else 0.0

    phrase_hits  = {p: bool(r.search(text)) for p, r in zip(_AI_PHRASES, _AI_PHRASE_RE)}
    phrase_count = sum(phrase_hits.values())

    # Extract the actual matched strings for display
    phrase_matches = []
    for r in _AI_PHRASE_RE:
        m = r.search(text)
        if m:
            phrase_matches.append(m.group(0))

    # Heuristic score 0–100:
    #   long, uniform sentences + low lexical diversity + AI filler phrases → higher
    score = 0

    if avg_sent_len > 25:
        score += 30
    elif avg_sent_len > 18:
        score += 15

    if sent_len_stdev < 5:
        score += 20
    elif sent_len_stdev < 10:
        score += 10

    if ttr < 0.4:
        score += 20
    elif ttr < 0.55:
        score += 10

    score += min(phrase_count * 5, 30)
    score  = min(score, 100)

    return {
        "word_count":        word_count,
        "sentence_count":    len(sents),
        "avg_sent_len":      avg_sent_len,
        "sent_len_stdev":    sent_len_stdev,
        "type_token_ratio":  ttr,
        "ai_phrase_count":   phrase_count,
        "ai_phrases_found":  phrase_matches,
        "score":             score,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────────────────────────────────────

_COLOR  = {"red": "\033[31m", "yellow": "\033[33m", "green": "\033[32m"}
_RESET  = "\033[0m"

_DT_LABEL = {
    "red":    "Likely AI-generated (unacknowledged, all-ASCII quotes)",
    "yellow": "Possibly AI-generated (mixed ASCII/curly quotes, unacknowledged)",
    "green":  "No strong digital trace signal (or AI use acknowledged)",
}


def print_report(dt: dict, st: dict) -> None:
    v     = dt["verdict"]
    color = _COLOR[v]

    print("\n== Method 1: Digital Traces =====================================")
    print(f"  ASCII straight quotes  : {dt['ascii_traces']:>5}   <- potential AI traces")
    print(f"  Curly/typographic      : {dt['regular_traces']:>5}   <- human/word-processor")
    print()
    for tool, found in dt["ai_tools_mentioned"].items():
        print(f"  {tool:20s}: {'Yes' if found else 'No'}")
    print(f"\n  Verdict: {color}{_DT_LABEL[v]}{_RESET}")

    score = st["score"]
    bar   = "X" * (score // 5) + "." * (20 - score // 5)

    print("\n== Method 2: Stylometric Patterns ===============================")
    print(f"  Words            : {st['word_count']}")
    print(f"  Sentences        : {st['sentence_count']}")
    print(f"  Avg sent length  : {st['avg_sent_len']} words")
    print(f"  Sent length stdev: {st['sent_len_stdev']}  (low = uniform -> AI)")
    print(f"  Type-token ratio : {st['type_token_ratio']}  (low = repetitive -> AI)")
    print(f"  AI phrases found : {st['ai_phrase_count']}")
    if st["ai_phrases_found"]:
        for phrase in st["ai_phrases_found"]:
            print(f"    - {phrase}")
    print(f"\n  Score: [{bar}]  {score}/100")
    print()


def analyze(text: str) -> tuple:
    return digital_traces(text), stylometric(text)



def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI text detector: digital traces + stylometric patterns"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text string to analyse")
    group.add_argument("--file", type=str, help="Path to a plain-text file")
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        with open(args.file, encoding="utf-6", errors="replace") as fh:
            text = fh.read()

    if not text.strip():
        raise ValueError("Input text is empty.")

    dt, st = analyze(text)
    print_report(dt, st)


if __name__ == "__main__":
    main()
