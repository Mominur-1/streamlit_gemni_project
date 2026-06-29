import re


def prepare_text_for_audio(raw_text):
    clean_txt = raw_text

    # 0a. Normalize LaTeX fractions: \frac{p}{q} → p/q
    clean_txt = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"\1/\2", clean_txt)

    # 0a2. Normalize LaTeX comparison commands BEFORE stripping $...$
    clean_txt = re.sub(r"\\geq\b", "≥", clean_txt)
    clean_txt = re.sub(r"\\leq\b", "≤", clean_txt)
    clean_txt = re.sub(r"\\neq\b", "≠", clean_txt)
    clean_txt = re.sub(r"\\ge\b", "≥", clean_txt)
    clean_txt = re.sub(r"\\le\b", "≤", clean_txt)
    clean_txt = re.sub(r"\\ne\b", "≠", clean_txt)

    # 0b. Strip inline $...$ math wrappers
    clean_txt = re.sub(r"\$([^$]+)\$", r"\1", clean_txt)

    # 0b2. Remove parentheses wrapping math-only expressions
    # "(≥ 0)" → "≥ 0",  "(q ≠ 0)" → "q ≠ 0"
    clean_txt = re.sub(r"\(\s*([a-zA-Z0-9 ]*[≠≤≥][^)]+)\)", r"\1", clean_txt)

    # 0c. Fix duplicated rendering artifacts
    clean_txt = re.sub(r"\b([a-zA-Z0-9/]{1,10})\1\b", r"\1", clean_txt)
    clean_txt = re.sub(r"([a-zA-Z])≠(\d+)\1=\2", r"\1≠\2", clean_txt)
    clean_txt = re.sub(r"([a-zA-Z0-9+\-=]{4,})\1", r"\1", clean_txt)
    clean_txt = re.sub(r"\b(\d{1,2})\1\b", r"square root of \1", clean_txt)
    clean_txt = re.sub(r"([≠≤≥<>]=?\d*)\1", r"\1", clean_txt)
    clean_txt = re.sub(r"([≠≤≥])\s*(\d+)\s*\1\s*\2", r"\1\2", clean_txt)

    # 1. Expand unicode math symbols
    clean_txt = clean_txt.replace("≠", " is not equal to ")
    clean_txt = clean_txt.replace("≤", " is less than or equal to ")
    clean_txt = clean_txt.replace("≥", " is greater than or equal to ")
    clean_txt = clean_txt.replace("×", " times ")
    clean_txt = clean_txt.replace("÷", " divided by ")
    clean_txt = clean_txt.replace("±", " plus or minus ")
    clean_txt = clean_txt.replace("∞", " infinity ")
    clean_txt = clean_txt.replace("π", " pi ")

    # 2. Expand math operators
    clean_txt = re.sub(r"([a-zA-Z0-9])\s+-\s+([a-zA-Z0-9])", r"\1 minus \2", clean_txt)
    clean_txt = re.sub(r"([a-zA-Z])-([a-zA-Z])", r"\1\2", clean_txt)
    clean_txt = re.sub(r"([a-zA-Z0-9])-(\d)", r"\1 minus \2", clean_txt)
    clean_txt = re.sub(r"(\d)-([a-zA-Z])", r"\1 minus \2", clean_txt)
    clean_txt = re.sub(r"([a-zA-Z0-9])\+([a-zA-Z0-9])", r"\1 plus \2", clean_txt)

    # 3. Contextual slash replacements
    clean_txt = re.sub(r"(\d+)/(\d+)", r"\1 divided by \2", clean_txt)
    clean_txt = re.sub(r"\b([a-zA-Z])/([a-zA-Z])\b", r"\1 over \2", clean_txt)
    clean_txt = re.sub(r"\b([a-zA-Z]{2,})/([a-zA-Z]{2,})\b", r"\1 or \2", clean_txt)

    # 4. Convert root formats into clear words
    clean_txt = clean_txt.replace(r"\sqrt", " square root of ")
    clean_txt = re.sub(r"√(\d+|[a-zA-Z]+)", r"square root of \1", clean_txt)

    # 5. Handle ASCII comparisons
    clean_txt = clean_txt.replace(">=", " greater than or equal to ")
    clean_txt = clean_txt.replace("<=", " less than or equal to ")
    clean_txt = clean_txt.replace("!=", " not equal to ")
    clean_txt = clean_txt.replace("<", " is less than ")
    clean_txt = clean_txt.replace(">", " is greater than ")
    clean_txt = re.sub(r"(?<! )=(?! )", " equals ", clean_txt)

    # 6. Common abbreviations
    clean_txt = clean_txt.replace("e.g.", "for example")
    clean_txt = clean_txt.replace("i.e.", "that is")

    # 7. Strip numbered list prefixes at line start
    clean_txt = re.sub(r"^\s*\d+\.\s+", "", clean_txt, flags=re.MULTILINE)

    # 8. Strip Markdown markup
    clean_txt = re.sub(r"#{1,6}\s+", "", clean_txt)
    clean_txt = re.sub(r"^\s*[\-\*]\s+", "", clean_txt, flags=re.MULTILINE)
    clean_txt = re.sub(r"[*_`:]+", "", clean_txt)

    # 9. Drop isolated math dollar signs, protect money values like $5
    clean_txt = re.sub(r"(?<!\d)\$(?!\d)", "", clean_txt)

    # 10. Normalize whitespace
    clean_txt = re.sub(r" {2,}", " ", clean_txt)
    clean_txt = re.sub(r"\s*\n\s*", "\n", clean_txt)
    clean_txt = re.sub(r"\n{2,}", "\n", clean_txt)
    clean_txt = clean_txt.strip()

    return clean_txt