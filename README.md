# cold-call-ready

**Beautiful, bookmarked PDF class notes with one Python script.**

A ReportLab-based toolkit for generating polished, color-coded study guides with case briefs, cold-call Q&A boxes, problem answers, rule text, and confidence scores -- all in Palatino on letter-sized pages with PDF bookmarks.

Built for law school, works for any class.

## Features

- **Case Brief Boxes** -- structured briefs with posture, facts, holding, reasoning
- **Cold-Call Q&A** -- italic questions with bullet-point answers, ready to recite
- **Problem Boxes** -- restate the facts, state the question, deliver the answer
- **Rule Boxes** -- styled containers for statutes, FRE rules, constitutional text
- **Colored Tables** -- teal headers, alternating row shading, auto-width columns
- **Section Headers** -- maroon (major) and teal (sub) headers with PDF bookmarks
- **Header/Footer Bars** -- navy top bar with class/topic info, gray footer with page numbers
- **Confidence Scores** -- rate your coverage section by section
- **Palatino Typography** -- register all four variants (roman, italic, bold, bold-italic)
- **No Page Splits** -- `KeepTogether` wraps every logical block

## Quick Start

### 1. Install

```bash
pip install reportlab
```

### 2. Set up your font

cold-call-ready uses Palatino. On macOS it ships with the system:

```bash
export NOTE_GEN_FONT_PATH="/System/Library/Fonts/Palatino.ttc"
```

Or pass the path directly:

```python
nb = NoteBuilder(..., font_path="/path/to/Palatino.ttc")
```

### 3. Build a PDF

```python
from note_generator import NoteBuilder

nb = NoteBuilder(
    output_path="my_notes.pdf",
    class_name="Evidence",
    topic_title="Hearsay Exceptions",
    page_range="pp. 400-430",
    semester="Fall 2025"
)

nb.add_title_page(
    subtitle="Exceptions to the Rule Against Hearsay",
    page_ref="Casebook pp. 400-430 | FRE 803, 804",
    toc_data=[["A", "Present Sense Impression", "What makes it reliable?"]],
    why_title="Why You're Reading These Cases",
    why_text="<b>Big Picture.</b> This unit covers ..."
)

nb.add_section("A. Present Sense Impression")
nb.add_text("Under FRE 803(1), a statement describing an event ...")

nb.add_case_brief(
    "Crawford v. Washington",
    "541 U.S. 36 (2004) -- Scalia, J.",
    [("Holding.", "Testimonial statements require confrontation ...")]
)

nb.add_cold_call("COLD-CALL POINTS -- Crawford", [
    ("What did Crawford change?", [
        "Replaced the Roberts reliability test with a bright-line rule ...",
    ])
])

nb.add_confidence_score([
    ["Crawford", "95%", "Strong coverage of the holding and reasoning."],
    ["OVERALL", "93%", "Review the forfeiture-by-wrongdoing exception."],
])

nb.build()
```

## API Reference

| Method | Description |
|---|---|
| `NoteBuilder(output_path, class_name, topic_title, page_range, font_path=None, semester=None)` | Create a new PDF builder |
| `.add_title_page(subtitle, page_ref, toc_data, why_title, why_text)` | Title + TOC + "Why" box |
| `.add_section(title)` | Maroon section header with bookmark |
| `.add_subsection(title)` | Teal subsection header with bookmark |
| `.add_text(text)` | Body paragraph (supports `<b>`, `<i>` HTML) |
| `.add_case_brief(title, citation, fields)` | Bordered case brief box |
| `.add_cold_call(title, qa_pairs)` | Cold-call Q&A box |
| `.add_problem(number, title, facts, question, answer_bullets)` | Problem with answer |
| `.add_table(headers, rows, col_widths=None)` | Colored info table |
| `.add_rule_box(rule_title, rule_text_parts)` | Styled rule/statute box |
| `.add_info_box(title, text)` | Bordered info box |
| `.add_confidence_score(rows)` | Confidence score table |
| `.add_page_break()` | Insert page break |
| `.add_spacer(height=6)` | Vertical spacer |
| `.build()` | Build the PDF with bookmarks |

All `add_*` methods return `self` for fluent chaining.

## AI-Powered Workflow

The included [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md) is a universal prompt you can paste into Claude (or any LLM) alongside your reading materials. It instructs the AI to:

1. Read all problems first, then cases, then answer problems
2. Generate detailed case summaries with cold-call talking points
3. Output a Python script using this library that produces a print-ready PDF

Just upload your casebook pages, paste the prompt, and say "Run it."

## Colors

| Name | Hex | Usage |
|---|---|---|
| Navy | `#1B2A4A` | Header bar, title text |
| Teal | `#2E6B62` | Subsection headers, table headers |
| Maroon | `#8B1A1A` | Section headers, cold-call titles |
| Cream | `#FDF8F0` | Case brief backgrounds |
| Teal Light | `#E8F4F2` | Alternating table rows |

## License

[MIT](LICENSE)
