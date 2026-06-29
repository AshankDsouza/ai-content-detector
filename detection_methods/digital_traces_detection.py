"""
Digital Traces AI Detection
Based on: AIDetection — Buschmann (2025)
"A Generative AI Detection Tool for Educators Using Syntactic Matching of
Common ASCII Characters As Potential 'AI Traces' Within Users' Internet Browser"

Replicates the js-script.js behavior exactly:
  - PDF  : pypdf page-by-page, each text item joined with a space, then trimmed
           (mirrors pdfjsLib getTextContent → items.forEach item.str + ' ' → trim)
  - DOCX : mammoth.extract_raw_text → .value
           (same mammoth library used in the JS)
  - Date : files with lastModified < 2022-11-22 are skipped (JS creationThresholdDate)
  - Type : only PDF and wordprocessingml (docx/doc) accepted; others are skipped

Usage:
    python digital_traces.py --file essay.pdf
    python digital_traces.py --file essay.docx
    python digital_traces.py --text "raw text to analyse directly"
"""

import re
import argparse
import os
from datetime import datetime, timezone


# JS creationThresholdDate = new Date('2022-11-22').getTime()
_THRESHOLD_TS = datetime(2022, 11, 22, tzinfo=timezone.utc).timestamp()


def read_pdf(path: str) -> str:
    """
    Replicates JS readPDF:
        pdfjsLib.getDocument({data}) → for each page → getTextContent()
        → items.forEach(item => text += (item.str || '') + ' ')
        → text.trim()
    """
    from pypdf import PdfReader
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        # extract_text() with space separator replicates item.str + ' ' per token
        page_text = page.extract_text(extraction_mode="plain") or ""
        # Append a space after each page's content, mirroring the per-item space
        text += page_text + " "
    return text.strip()


def read_docx(path: str) -> str:
    """
    Replicates JS readDocx:
        mammoth.extractRawText({arrayBuffer}) → result.value
    Python mammoth is the same library — output is identical.
    """
    import mammoth
    with open(path, "rb") as fh:
        result = mammoth.extract_raw_text(fh)
    return result.value


def read_file(path: str) -> str | None:
    """
    Replicates the JS processFiles() file-handling logic:
      - Skips files with lastModified < 2022-11-22  (returns None)
      - Dispatches to read_pdf or read_docx by type
      - Raises ValueError for unsupported types
    """
    mtime = os.path.getmtime(path)
    if mtime < _THRESHOLD_TS:
        return None  # JS: skip with "was created before Nov 22 2022" message

    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext in (".docx", ".doc"):
        return read_docx(path)
    elif ext == ".txt":
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}  (JS also skips these)")


# ─────────────────────────────────────────────────────────────────────────────
# Detection — matches js-script.js lines 75-99 exactly
# ─────────────────────────────────────────────────────────────────────────────

# JS: text.match(/['"]/g)  — ASCII straight single (U+0027) and double (U+0022)
_ASCII_QUOTES = re.compile(r'[\'\"]')

# JS: text.match(/[""'']/g) — exactly these 4 curly/typographic characters:
#   " U+201C  " U+201D  ' U+2018  ' U+2019
_CURLY_QUOTES = re.compile(r'[""'']')

# JS tool patterns — same 6 regexes, same flags
AI_TOOLS = {
    "ChatGPT":    re.compile(r'(?:\bchat[\s-]?gpt\b|chatgpt\b|chat\s+gpt\b)', re.IGNORECASE),
    "Grammarly":  re.compile(r'\bgrammarly\b(?=\s|[.,;:\/\-]|$)', re.IGNORECASE),
    "Claude":     re.compile(r'\bclaude\b(?=\s|[.,;:\/\-]|$)', re.IGNORECASE),
    "Gemini":     re.compile(r'\bgemini\b(?=\s|[.,;:\/\-]|$)', re.IGNORECASE),
    "Llama/Meta": re.compile(r'\b(llama|meta)\b(?=\s|[.,;:\/\-]|$)', re.IGNORECASE),
    "Copilot":    re.compile(r'\bcopilot\b(?=\s|[.,;:\/\-]|$)', re.IGNORECASE),
}


def analyze(text: str) -> dict:
    """
    Mirrors JS lines 75-99:
      _0x4db0b4 = (text.match(/['"]/g)  || []).length   → ascii_traces
      _0x2d5442 = (text.match(/[""'']/g) || []).length  → regular_traces
      tool detections → any_ai_mentioned
      verdict: red / yellow / green
    """
    ascii_traces   = len(_ASCII_QUOTES.findall(text))
    regular_traces = len(_CURLY_QUOTES.findall(text))

    mentioned        = {t: bool(p.search(text)) for t, p in AI_TOOLS.items()}
    any_ai_mentioned = any(mentioned.values())

    # JS:
    #   if (aiTraces > 0 && noAiMentioned && regularTraces == 0) → red
    #   else if (aiTraces > 0 && noAiMentioned)                  → yellow
    #   else                                                      → green
    if ascii_traces > 0 and not any_ai_mentioned and regular_traces == 0:
        verdict = "red"
    elif ascii_traces > 0 and not any_ai_mentioned:
        verdict = "yellow"
    else:
        verdict = "green"

    return {
        "ascii_traces":       ascii_traces,
        "regular_traces":     regular_traces,
        "ai_tools_mentioned": mentioned,
        "any_ai_mentioned":   any_ai_mentioned,
        "verdict":            verdict,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Report / CLI
# ─────────────────────────────────────────────────────────────────────────────

_VERDICT_LABEL = {
    "red":    "Likely AI-generated — unacknowledged (all-ASCII quotes)",
    "yellow": "Possibly AI-generated — ambiguous (mixed ASCII/curly quotes)",
    "green":  "No strong AI trace signal (or AI use acknowledged)",
}
_VERDICT_COLOR = {"red": "\033[31m", "yellow": "\033[33m", "green": "\033[32m"}
_RESET = "\033[0m"


def print_report(result: dict, label: str = "input") -> None:
    v     = result["verdict"]
    color = _VERDICT_COLOR[v]
    print(f"\n-- Digital Traces ({label})")
    print(f"  ASCII straight quotes : {result['ascii_traces']:>5}   <- potential AI traces")
    print(f"  Curly/typographic     : {result['regular_traces']:>5}   <- human/word-processor")
    print()
    for tool, detected in result["ai_tools_mentioned"].items():
        print(f"  {tool:20s}: {'Yes' if detected else 'No'}")
    print()
    print(f"  Verdict: {color}{_VERDICT_LABEL[v]}{_RESET}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Digital-traces heuristic AI detector (Buschmann 2025)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Raw text string to analyse")
    group.add_argument("--file", type=str, help="Path to a .pdf, .docx, .doc, or .txt file")
    args = parser.parse_args()

    if args.text:
        text  = args.text
        label = "stdin"
    else:
        label = os.path.basename(args.file)
        text  = read_file(args.file)
        if text is None:
            print(f"  Skipped: {label} was last modified before 2022-11-22 (pre-ChatGPT).")
            return

    if not text.strip():
        raise ValueError("Input text is empty.")

    print_report(analyze(text), label)


if __name__ == "__main__":
    main()
