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

---

## Quick Start (Step by Step)

### Step 1: Install

```bash
pip install reportlab
```

Or clone this repo and install from requirements:

```bash
git clone https://github.com/gabrielmeir53/cold-call-ready.git
cd cold-call-ready
pip install -r requirements.txt
```

### Step 2: Set up your font

cold-call-ready uses Palatino. Set the path as an environment variable or pass it directly.

**macOS** (Palatino ships with the system):
```bash
export NOTE_GEN_FONT_PATH="/System/Library/Fonts/Palatino.ttc"
```

**Linux** (install Palatino or use another `.ttc`/`.ttf`):
```bash
# Install via your package manager or download, then:
export NOTE_GEN_FONT_PATH="/usr/share/fonts/truetype/Palatino.ttc"
```

**Windows:**
```powershell
$env:NOTE_GEN_FONT_PATH = "C:\Windows\Fonts\pala.ttf"
```

Or skip the env var and pass the path directly in your script:
```python
nb = NoteBuilder(..., font_path="/path/to/Palatino.ttc")
```

### Step 3: Write your script

Create a file (e.g., `my_notes.py`):

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
    [
        ("Posture.", "Defendant's wife made statements to police ..."),
        ("Holding.", "Testimonial statements require confrontation ..."),
        ("Reasoning.", [
            "The Confrontation Clause bars admission of testimonial hearsay unless the declarant is unavailable and was previously cross-examined.",
            "The Roberts reliability test gave courts too much discretion.",
        ]),
    ]
)

nb.add_cold_call("COLD-CALL POINTS -- Crawford", [
    ("What did Crawford change?", [
        "Replaced the Roberts reliability test with a bright-line rule: testimonial statements require prior cross-examination.",
        "Shifted the focus from judicial reliability assessments to the original constitutional guarantee.",
    ]),
    ("What counts as 'testimonial'?", [
        "Statements made during police interrogation, affidavits, prior testimony, and similar formal declarations.",
        "The Court left the precise boundaries for future cases.",
    ]),
])

nb.add_problem("8.1", "The Neighbor's Account",
    "A neighbor told police she saw the defendant leave the house carrying a bag. "
    "The neighbor is now unavailable. The prosecution wants to introduce her statement.",
    "Is the neighbor's statement admissible under the Confrontation Clause after Crawford?",
    [
        "NO -- this is a testimonial statement (made during police interrogation).",
        "Under Crawford, testimonial hearsay requires that the declarant be unavailable AND that the defendant had a prior opportunity to cross-examine.",
        "Here, even though the declarant is unavailable, there was no prior cross-examination.",
        "The statement must be excluded regardless of its reliability.",
    ]
)

nb.add_confidence_score([
    ["Crawford", "95%", "Strong coverage of the holding and reasoning."],
    ["Problem 8.1", "92%", "Clear application of the Crawford rule."],
    ["OVERALL", "93%", "Review the forfeiture-by-wrongdoing exception."],
])

nb.build()
```

### Step 4: Run it

```bash
python my_notes.py
```

### Step 5: Review

Open `my_notes.pdf` and check:
- [ ] Every case has a full brief with cold-call points
- [ ] Every problem is answered with talking points
- [ ] Bookmarks work in the PDF sidebar
- [ ] No content is split across pages
- [ ] Confidence score is at the end

---

## AI-Powered Workflow

The included [`PROMPT_TEMPLATE.md`](PROMPT_TEMPLATE.md) is a universal prompt you can paste into Claude (or any LLM) alongside your reading materials. It instructs the AI to:

1. Read all problems first, then cases, then answer problems
2. Generate detailed case summaries with cold-call talking points
3. Output a Python script using this library that produces a print-ready PDF

**How to use it:**

1. Upload your casebook pages (PDF or DOCX) to Claude
2. Copy the Master Prompt from `PROMPT_TEMPLATE.md`
3. Fill in the `[BRACKETED PLACEHOLDERS]` (class name, pages, font path)
4. Optionally paste a class-specific instruction block (Evidence, Immigration Law, Internet Law, WTE, or write your own)
5. Send the prompt and say **"Run it."**

Pre-built class-specific instruction blocks are included for:

| Class | Key emphasis |
|---|---|
| **Evidence** | Problems first, admissibility verdicts with FRE subsections, amendment tracking |
| **Immigration Law** | Step-by-step walkthroughs, all visa types/INA sections, doctrinal timelines |
| **Internet Law** | Full case summaries with judge names, dissents at full depth, policy Qs |
| **Wills, Trusts & Estates** | Heavy charts/diagrams, financial data tables, statutory cross-references |

---

## API Reference

| Method | Description |
|---|---|
| `NoteBuilder(output_path, class_name, topic_title, page_range, font_path=None, semester=None)` | Create a new PDF builder |
| `.add_title_page(subtitle, page_ref, toc_data, why_title, why_text)` | Title + TOC + "Why" box |
| `.add_section(title)` | Maroon section header with bookmark |
| `.add_subsection(title)` | Teal subsection header with bookmark |
| `.add_text(text)` | Body paragraph (supports `<b>`, `<i>` HTML) |
| `.add_case_brief(title, citation, fields)` | Bordered case brief; `fields` = list of `(label, content_or_bullet_list)` |
| `.add_cold_call(title, qa_pairs)` | Cold-call Q&A box; `qa_pairs` = list of `(question, [answer_bullets])` |
| `.add_problem(number, title, facts, question, answer_bullets)` | Problem with answer |
| `.add_table(headers, rows, col_widths=None)` | Colored info table |
| `.add_rule_box(rule_title, rule_text_parts)` | Styled rule/statute box |
| `.add_info_box(title, text)` | Bordered info box |
| `.add_confidence_score(rows)` | Confidence score table; `rows` = list of `[component, score, notes]` |
| `.add_page_break()` | Insert page break |
| `.add_spacer(height=6)` | Vertical spacer |
| `.build()` | Build the PDF with bookmarks; returns output path |

All `add_*` methods return `self` for fluent chaining:

```python
nb.add_section("A. Intro").add_text("...").add_page_break()
```

---

## Colors

| Name | Hex | Usage |
|---|---|---|
| Navy | `#1B2A4A` | Header bar, title text |
| Teal | `#2E6B62` | Subsection headers, table headers |
| Maroon | `#8B1A1A` | Section headers, cold-call titles |
| Cream | `#FDF8F0` | Case brief backgrounds |
| Teal Light | `#E8F4F2` | Alternating table rows |

Access them programmatically:

```python
from note_generator import COLORS
print(COLORS["NAVY"])  # HexColor('#1B2A4A')
```

---

## Contributing

PRs welcome. If you add a new component (e.g., `add_flowchart()`, `add_timeline()`), follow the existing pattern: return a ReportLab `Flowable`, accept an optional `content_w` parameter, and add a corresponding `NoteBuilder` method that appends it to the story.

## License

[MIT](LICENSE)
