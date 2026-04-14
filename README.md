# cold-call-ready

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![ReportLab](https://img.shields.io/badge/requires-reportlab%20%E2%89%A54.0-green.svg)](https://pypi.org/project/reportlab/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**Never get caught flat-footed in class again.**

Upload your casebook reading to Claude. Paste a prompt. Get a polished, color-coded PDF with every case briefed, every problem answered, and cold-call Q&A boxes telling you exactly what to say when the professor points at you.

No coding required. Built for law school.

---

## What You Get

A 20+ page PDF for each reading assignment:

<p align="center">
  <img src="assets/sample-title.png" alt="Title page with table of contents" width="380"/>
  &nbsp;&nbsp;
  <img src="assets/sample-case-brief.png" alt="Case brief with structured analysis" width="380"/>
</p>
<p align="center">
  <em>Left: Title page with TOC and "Why You're Reading" box. Right: Full case brief with facts, holding, and reasoning.</em>
</p>

<p align="center">
  <img src="assets/sample-cold-call.png" alt="Cold-call Q&A and problem answer" width="380"/>
</p>
<p align="center">
  <em>Cold-call Q&A box with professor questions and bullet-point answers you can say out loud.</em>
</p>

Every PDF includes:

- **Case briefs** -- facts, holding, reasoning, key quotes, all in a styled box
- **Cold-call Q&A** -- likely professor questions with bullet-point answers ready to recite
- **Problem answers** -- every textbook question answered with talking points
- **Rule text** -- FRE rules, statutes, constitutional provisions in highlighted boxes
- **Comparison tables** -- majority vs. dissent, old rule vs. new rule, element breakdowns
- **Confidence score** -- tells you how well-covered you are section by section
- **PDF bookmarks** -- jump to any case or section from the sidebar

All in Palatino on letter-sized pages. Nothing splits awkwardly across pages.

---

## How to Use It

### One-time setup (5 minutes)

**1. Make sure you have Python.**

<table>
<tr><td><strong>Mac</strong></td><td>Open <strong>Terminal</strong> and type <code>python3 --version</code>. If you see a version number, you're good.</td></tr>
<tr><td><strong>Windows</strong></td><td>Open <strong>Command Prompt</strong> or <strong>PowerShell</strong> and type <code>python --version</code>. If you see a version number, you're good.</td></tr>
</table>

If Python isn't installed, download it from [python.org/downloads](https://www.python.org/downloads/). **Windows users:** check "Add Python to PATH" during installation.

**2. Install one library.**

```bash
pip install reportlab
```

(On Mac, use `pip3` if `pip` doesn't work.)

**3. Download this repo.**

If you have Git installed:
```bash
git clone https://github.com/gabrielmeir53/cold-call-ready.git
```

If you don't have Git: click the green **Code** button at the top of [this page](https://github.com/gabrielmeir53/cold-call-ready), then **Download ZIP**. Unzip it wherever you like.

**4. Font (automatic).**

Palatino is auto-detected on your system:
- **Mac** -- already installed at `/System/Library/Fonts/Palatino.ttc`. Nothing to do.
- **Windows** -- auto-detected if Palatino is in `C:\Windows\Fonts`. If not installed, it falls back to **Times** automatically. Your notes will still look great.
- **Linux** -- checks common font directories. Falls back to Times if not found.

No font configuration is required. It just works.

---

### Before each class (~5 minutes)

**1. Open Claude** at [claude.ai](https://claude.ai).

**2. Upload your reading.** Attach the PDF of the casebook pages your professor assigned.

**3. Open `PROMPT_TEMPLATE.md`** from the repo you downloaded. Copy everything under **"Master Prompt"** (the big block inside the triple backticks).

**4. Paste it into Claude.** Replace three things:

| Replace this | With this |
|---|---|
| `[CLASS NAME]` | Your course -- e.g., `Evidence` |
| `[PAGES/FILE DESCRIPTION]` | What you uploaded -- e.g., `the attached PDF, pp. 747-755` |
| `[CLASS-SPECIFIC INSTRUCTIONS]` | A block from the bottom of `PROMPT_TEMPLATE.md` for your class *(optional but recommended)* |

Delete the `[PALATINO FONT PATH]` line entirely -- it auto-detects.

**5. Send it.** Claude reads your casebook pages, analyzes every case and problem, and writes a Python script that generates the PDF.

**6. Say "Run it."** Claude runs the script. A PDF appears.

**7. Open the PDF.** You're ready for class.

---

### Class-specific prompts

At the bottom of `PROMPT_TEMPLATE.md`, there are pre-built instruction blocks you can paste into `[CLASS-SPECIFIC INSTRUCTIONS]` to tailor the output:

| Class | What it adds |
|---|---|
| **Evidence** | Reads problems first, gives admissibility verdicts with FRE subsections, tracks 2000/2023 amendments |
| **Immigration Law** | Step-by-step logical walkthroughs, covers all visa types and INA sections, builds doctrinal timelines |
| **Internet Law** | Full case summaries with judge names, dissents at equal depth, policy-oriented cold-call questions |
| **Wills, Trusts & Estates** | Extra charts and diagrams, financial data tables, UTC/UPIA/UPC cross-references |
| **Custom** | Blank template with guiding questions to build your own |

---

## FAQ

**Do I need to know Python?**
No. Claude writes and runs the script for you. You just paste a prompt.

**Does it work on Windows?**
Yes. Python + ReportLab work on Windows. The font auto-detects Palatino if installed, otherwise falls back to Times.

**Can I use it for non-law classes?**
Yes. The components (case briefs, tables, Q&A boxes) work for any subject. Write your own class-specific instruction block.

**What if I want to tweak the output?**
You can ask Claude to adjust anything -- colors, layout, content. Or see the [API Reference](#for-developers) below to write scripts by hand.

**How much does it cost?**
This repo is free (MIT license). You need a Claude account to use the AI workflow.

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'reportlab'"**
You haven't installed the library yet. Run `pip install reportlab` (or `pip3 install reportlab` on Mac).

**"No such file or directory" when running the script**
Make sure the script and `note_generator.py` are in the same folder. If you downloaded the ZIP, `cd` into the unzipped folder first.

**The PDF has wrong fonts / looks different than the screenshots**
Palatino wasn't found on your system, so it fell back to Times. This is fine -- Times still looks professional. If you want Palatino on Windows, install it from a font provider or copy `Palatino.ttc` from a Mac.

**Claude generated a script but it errors out**
Ask Claude to fix it -- paste the error message back into the chat. Common causes: a typo in the generated script, or a ReportLab version mismatch. Make sure you have `reportlab >= 4.0` (`pip install --upgrade reportlab`).

**The PDF is blank or has only one page**
The script probably errored silently. Run it in Terminal/Command Prompt directly (`python my_notes.py`) instead of through Claude to see the full error output.

**Content is split across pages**
This shouldn't happen -- `KeepTogether` prevents it. If it does, ask Claude to wrap the offending section in a `KeepTogether` block, or reduce the content length so it fits on one page.

**"WARNING: Palatino font not found -- using Times as fallback"**
Not an error -- just informational. Your PDF will use Times instead of Palatino. To suppress: install Palatino or set `NOTE_GEN_FONT_PATH` to your font file.

---

## For Developers

<details>
<summary><strong>API Reference</strong> -- click to expand</summary>

### Manual Usage

If you prefer to write the script by hand, use the `NoteBuilder` API directly:

```python
from note_generator import NoteBuilder

nb = NoteBuilder(
    output_path="my_notes.pdf",
    class_name="Evidence",
    topic_title="Hearsay Exceptions",
    page_range="pp. 400-430",
    semester="Fall 2025"
)

nb.add_section("A. Present Sense Impression")
nb.add_text("Under FRE 803(1), a statement describing an event ...")

nb.add_case_brief(
    "Crawford v. Washington",
    "541 U.S. 36 (2004) -- Scalia, J.",
    [
        ("Holding.", "Testimonial statements require confrontation ..."),
        ("Reasoning.", [
            "The Roberts reliability test gave courts too much discretion.",
        ]),
    ]
)

nb.add_cold_call("COLD-CALL POINTS -- Crawford", [
    ("What did Crawford change?", [
        "Replaced Roberts with a bright-line confrontation rule.",
    ]),
])

nb.add_confidence_score([
    ["OVERALL", "93%", "Review forfeiture-by-wrongdoing."],
])

nb.build()
```

### Methods

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
| `.add_page_break()` | Page break |
| `.add_spacer(height=6)` | Vertical spacer |
| `.build()` | Build the PDF with bookmarks |

All methods return `self` for chaining: `nb.add_section("A").add_text("...").add_page_break()`

### Font Configuration

Palatino is auto-detected in this order:
1. `NOTE_GEN_FONT_PATH` environment variable
2. macOS: `/System/Library/Fonts/Palatino.ttc`
3. Linux: `/usr/share/fonts/truetype/Palatino.ttc` and common alternatives
4. Windows: `C:\Windows\Fonts\pala.ttf`
5. Fallback: Times-Roman (built into ReportLab)

### Colors

| Name | Hex | Usage |
|---|---|---|
| Navy | `#1B2A4A` | Header bar, title text |
| Teal | `#2E6B62` | Subsection headers, table headers |
| Maroon | `#8B1A1A` | Section headers, cold-call titles |
| Cream | `#FDF8F0` | Case brief backgrounds |
| Teal Light | `#E8F4F2` | Alternating table rows |

```python
from note_generator import COLORS
print(COLORS["NAVY"])  # HexColor('#1B2A4A')
```

</details>

---

## Contributing

PRs welcome. If you add a new component, follow the existing pattern: return a ReportLab `Flowable`, accept an optional `content_w` parameter, and add a corresponding `NoteBuilder` method.

## License

[MIT](LICENSE)
