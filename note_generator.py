#!/usr/bin/env python3
"""
note_generator.py -- Reusable ReportLab library for generating colorful law school
class notes PDFs.

Provides:
    - NoteBuilder: a fluent API class wrapping SimpleDocTemplate for building
      richly styled PDFs with bookmarks, colored headers/footers, case briefs,
      cold-call boxes, problem boxes, rule boxes, info tables, and more.
    - Standalone component functions (section_header, sub_section_header,
      info_table, bordered_box, case_brief_box, cold_call_box, problem_box,
      rule_box, why_box) that return ReportLab Flowables directly.

Usage:
    from note_generator import NoteBuilder

    nb = NoteBuilder("output.pdf", "Evidence", "Hearsay", "pp. 100-120")
    nb.add_title_page(
        subtitle="Exceptions to the Rule Against Hearsay",
        page_ref="Casebook pp. 100-120 | FRE 803, 804",
        toc_data=[["A", "Introduction", "What is hearsay?"], ...],
        why_title="Why You're Reading These Cases",
        why_text="<b>Big Picture.</b> This chapter covers ..."
    )
    nb.add_section("A. Introduction")
    nb.add_text("Hearsay is an out-of-court statement ...")
    nb.add_case_brief("Crawford v. Washington", "541 U.S. 36 (2004)", [...])
    nb.build()
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak, HRFlowable, Flowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily


# ══════════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════════════════

# Default font path -- override via NoteBuilder(..., font_path="...") or by
# setting this module-level variable before constructing a NoteBuilder.
DEFAULT_FONT_PATH = os.environ.get("NOTE_GEN_FONT_PATH", None)
# Set this to your Palatino.ttc path, e.g.:
#   export NOTE_GEN_FONT_PATH="/path/to/Palatino.ttc"
# Or pass font_path="..." to NoteBuilder() directly.
# On macOS, Palatino is typically at /System/Library/Fonts/Palatino.ttc

# ── COLORS ──
NAVY       = HexColor("#1B2A4A")
TEAL       = HexColor("#2E6B62")
TEAL_LIGHT = HexColor("#E8F4F2")
MAROON     = HexColor("#8B1A1A")
CREAM      = HexColor("#FDF8F0")
LIGHT_GRAY = HexColor("#F2F2F2")
MED_GRAY   = HexColor("#E0E0E0")
DARK_GRAY  = HexColor("#666666")
GOLD       = HexColor("#C8A951")
RULE_BG    = HexColor("#F0EDE4")
BOX_BORDER = HexColor("#999999")

# ── PAGE DIMENSIONS ──
PAGE_W, PAGE_H = letter
MARGIN = 0.65 * inch
CONTENT_W = PAGE_W - 2 * MARGIN


# ══════════════════════════════════════════════════════════════════════
#  FONT REGISTRATION (deferred)
# ══════════════════════════════════════════════════════════════════════

_fonts_registered = False


def _register_fonts(font_path):
    """Register the Palatino font family from a .ttc collection file.

    Indices: 0=Roman, 1=Italic, 2=Bold, 3=BoldItalic.
    This is idempotent -- calling it multiple times with the same path is safe.
    """
    global _fonts_registered
    if _fonts_registered:
        return
    pdfmetrics.registerFont(TTFont("Palatino",            font_path, subfontIndex=0))
    pdfmetrics.registerFont(TTFont("Palatino-Italic",     font_path, subfontIndex=1))
    pdfmetrics.registerFont(TTFont("Palatino-Bold",       font_path, subfontIndex=2))
    pdfmetrics.registerFont(TTFont("Palatino-BoldItalic", font_path, subfontIndex=3))
    registerFontFamily(
        "Palatino",
        normal="Palatino",
        bold="Palatino-Bold",
        italic="Palatino-Italic",
        boldItalic="Palatino-BoldItalic",
    )
    _fonts_registered = True


# ══════════════════════════════════════════════════════════════════════
#  PARAGRAPH STYLES
# ══════════════════════════════════════════════════════════════════════

def _s(name, **kw):
    """Build a ParagraphStyle with Palatino defaults."""
    defaults = dict(
        fontName="Palatino", fontSize=10, leading=13,
        textColor=black, alignment=TA_JUSTIFY,
    )
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


sTitle      = _s("Title",    fontName="Palatino-Bold", fontSize=22, leading=28,
                  alignment=TA_CENTER, textColor=NAVY)
sSubtitle   = _s("Subtitle", fontName="Palatino-Italic", fontSize=13, leading=17,
                  alignment=TA_CENTER, textColor=MAROON)
sPageRef    = _s("PageRef",  fontSize=10, leading=13, alignment=TA_CENTER,
                  textColor=DARK_GRAY)
sBody       = _s("Body",     fontSize=10, leading=13.5)
sBodySmall  = _s("BodySm",  fontSize=9, leading=12)
sBold       = _s("Bold",    fontName="Palatino-Bold", fontSize=10, leading=13.5)
sItalic     = _s("Italic",  fontName="Palatino-Italic", fontSize=10, leading=13.5)
sBullet     = _s("Bullet",  fontSize=10, leading=13.5, leftIndent=18, bulletIndent=6,
                  bulletFontName="Palatino", bulletFontSize=10)
sBulletBold = _s("BulletB", fontName="Palatino", fontSize=10, leading=13.5,
                  leftIndent=18, bulletIndent=6)
sQuestion   = _s("Question", fontName="Palatino-BoldItalic", fontSize=10,
                  leading=13.5, textColor=MAROON)
sAnswer     = _s("Answer",  fontSize=10, leading=13.5, leftIndent=18, bulletIndent=6)
sTableH     = _s("TableH",  fontName="Palatino-Bold", fontSize=9, leading=12,
                  textColor=white, alignment=TA_LEFT)
sTableB     = _s("TableB",  fontSize=9, leading=12)
sTableBI    = _s("TableBI", fontName="Palatino-Italic", fontSize=9, leading=12)
sRuleTitle  = _s("RuleT",   fontName="Palatino-Bold", fontSize=11, leading=14,
                  alignment=TA_CENTER, textColor=NAVY)
sRuleText   = _s("RuleText", fontSize=9.5, leading=13)
sSectionWhy = _s("SecWhy",  fontName="Palatino-Bold", fontSize=12, leading=15,
                  textColor=MAROON)
sConfTitle  = _s("ConfT",   fontName="Palatino-Bold", fontSize=14, leading=18,
                  alignment=TA_CENTER, textColor=NAVY)
sCaseTitle  = _s("CaseT",   fontName="Palatino-Bold", fontSize=11, leading=14,
                  textColor=NAVY)
sCaseCite   = _s("CaseC",   fontName="Palatino-Italic", fontSize=9.5, leading=12,
                  textColor=DARK_GRAY)


# ══════════════════════════════════════════════════════════════════════
#  BOOKMARK FLOWABLE
# ══════════════════════════════════════════════════════════════════════

class BookmarkFlowable(Flowable):
    """Invisible flowable that registers a PDF outline bookmark when drawn.

    Args:
        title: Text that appears in the PDF bookmark/outline panel.
        level: Nesting depth (0 = top-level section, 1 = subsection, etc.).
    """

    def __init__(self, title, level=0):
        Flowable.__init__(self)
        self.title = title
        self.level = level
        self.width = 0
        self.height = 0

    def draw(self):
        key = f"BM_{id(self)}"
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(self.title, key, level=self.level)


# ══════════════════════════════════════════════════════════════════════
#  STANDALONE COMPONENT FUNCTIONS  (return Flowables)
# ══════════════════════════════════════════════════════════════════════

def sp(h=6):
    """Return a vertical Spacer of *h* points."""
    return Spacer(1, h)


def section_header(text, content_w=None):
    """Maroon-background section header spanning the full content width.

    Args:
        text: Header text (plain string).
        content_w: Available width in points.  Defaults to module-level CONTENT_W.

    Returns:
        A Table flowable styled as a maroon section header.
    """
    if content_w is None:
        content_w = CONTENT_W
    t = Table(
        [[Paragraph(
            text,
            ParagraphStyle(
                "sh", fontName="Palatino-Bold", fontSize=12, leading=15,
                textColor=white, alignment=TA_LEFT,
            ),
        )]],
        colWidths=[content_w],
        rowHeights=[24],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MAROON),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def sub_section_header(text, content_w=None):
    """Teal-background sub-section header spanning the full content width.

    Args:
        text: Header text (plain string).
        content_w: Available width in points.  Defaults to module-level CONTENT_W.

    Returns:
        A Table flowable styled as a teal sub-section header.
    """
    if content_w is None:
        content_w = CONTENT_W
    t = Table(
        [[Paragraph(
            text,
            ParagraphStyle(
                "ssh", fontName="Palatino-Bold", fontSize=11, leading=14,
                textColor=white, alignment=TA_LEFT,
            ),
        )]],
        colWidths=[content_w],
        rowHeights=[22],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def info_table(headers, rows, col_widths=None, content_w=None):
    """Colored table with a teal header row and alternating white/light-teal body rows.

    Args:
        headers: List of header strings.
        rows: List of row lists.  Each cell may be a string or a Paragraph.
        col_widths: Optional list of column widths in points.
        content_w: Total content width (defaults to module-level CONTENT_W).

    Returns:
        A styled Table flowable.
    """
    if content_w is None:
        content_w = CONTENT_W
    hdr = [Paragraph(h, sTableH) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([
            Paragraph(str(c), sTableB) if not isinstance(c, Paragraph) else c
            for c in row
        ])
    if col_widths is None:
        col_widths = [content_w / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",    (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR",     (0, 0), (-1, 0), white),
        ("FONTNAME",      (0, 0), (-1, 0), "Palatino-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID",          (0, 0), (-1, -1), 0.5, BOX_BORDER),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), TEAL_LIGHT))
        else:
            style.append(("BACKGROUND", (0, i), (-1, i), white))
    t.setStyle(TableStyle(style))
    return t


def bordered_box(content_flowables, bg=CREAM, content_w=None):
    """Wrap a list of flowables in a bordered box with a background colour.

    Args:
        content_flowables: List of Flowable objects to wrap.
        bg: Background HexColor (default CREAM).
        content_w: Total content width (defaults to module-level CONTENT_W).

    Returns:
        A styled Table flowable acting as a bordered container.
    """
    if content_w is None:
        content_w = CONTENT_W
    inner = Table([[content_flowables]], colWidths=[content_w - 12])
    inner.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([[inner]], colWidths=[content_w])
    outer.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg),
        ("BOX",           (0, 0), (-1, -1), 1, BOX_BORDER),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return outer


def case_brief_box(title, citation, fields, content_w=None):
    """Case brief in a navy-bordered box on a cream background.

    Args:
        title: Case name (string).
        citation: Full citation string.
        fields: List of ``(label, content)`` tuples.  *content* may be a plain
                 string or a list of bullet strings.
        content_w: Total content width (defaults to module-level CONTENT_W).

    Returns:
        A styled Table flowable containing the case brief.
    """
    if content_w is None:
        content_w = CONTENT_W
    elements = []
    elements.append(Paragraph(title, sCaseTitle))
    elements.append(Paragraph(citation, sCaseCite))
    elements.append(sp(4))
    for label, content in fields:
        if isinstance(content, str):
            elements.append(Paragraph(f"<b>{label}</b> {content}", sBody))
            elements.append(sp(3))
        elif isinstance(content, list):
            elements.append(Paragraph(f"<b>{label}</b>", sBold))
            elements.append(sp(2))
            for bullet in content:
                elements.append(Paragraph(f"\u2022 {bullet}", sBullet))
                elements.append(sp(1))
            elements.append(sp(2))
    inner_table = Table([[elements]], colWidths=[content_w - 16])
    inner_table.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([[inner_table]], colWidths=[content_w])
    outer.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CREAM),
        ("BOX",           (0, 0), (-1, -1), 1.2, NAVY),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return outer


def cold_call_box(title, qa_pairs, content_w=None):
    """Cold-call Q&A box with a maroon border and warm background.

    Args:
        title: Box heading (string, e.g. ``"COLD-CALL POINTS -- Crawford"``).
        qa_pairs: List of ``(question_str, [answer_bullet_str, ...])`` tuples.
        content_w: Total content width (defaults to module-level CONTENT_W).

    Returns:
        A styled Table flowable containing the Q&A content.
    """
    if content_w is None:
        content_w = CONTENT_W
    elements = []
    elements.append(Paragraph(
        f"<b>{title}</b>",
        ParagraphStyle(
            "cct", fontName="Palatino-Bold", fontSize=11, leading=14,
            textColor=MAROON,
        ),
    ))
    elements.append(sp(4))
    for q, answers in qa_pairs:
        elements.append(Paragraph(f"<i>Q: {q}</i>", sQuestion))
        elements.append(sp(2))
        for a in answers:
            elements.append(Paragraph(f"\u2022 {a}", sAnswer))
            elements.append(sp(1))
        elements.append(sp(4))
    inner = Table([[elements]], colWidths=[content_w - 16])
    inner.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([[inner]], colWidths=[content_w])
    outer.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1, MAROON),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#FFF8F0")),
    ]))
    return outer


def problem_box(number, title, facts, question, answer_bullets, content_w=None):
    """Problem with answer in a teal-bordered box.

    Args:
        number: Problem number (string or int, e.g. ``"9.1"``).
        title: Short descriptive title.
        facts: Fact pattern paragraph (string, may contain HTML markup).
        question: The question posed (string, may contain HTML markup).
        answer_bullets: List of answer/talking-point strings.
        content_w: Total content width (defaults to module-level CONTENT_W).

    Returns:
        A styled Table flowable containing the full problem layout.
    """
    if content_w is None:
        content_w = CONTENT_W
    elements = []
    hdr = Table(
        [[Paragraph(
            f"Problem {number}",
            ParagraphStyle(
                "ph", fontName="Palatino-Bold", fontSize=11, leading=14,
                textColor=white, alignment=TA_CENTER,
            ),
        )]],
        colWidths=[content_w - 2],
        rowHeights=[22],
    )
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(hdr)
    elements.append(sp(2))
    elements.append(Paragraph(
        f"<i>{title}</i>",
        ParagraphStyle(
            "pit", fontName="Palatino-Italic", fontSize=10, leading=13,
            alignment=TA_CENTER, textColor=DARK_GRAY,
        ),
    ))
    elements.append(sp(4))
    elements.append(Paragraph(facts, sBody))
    elements.append(sp(4))
    elements.append(Paragraph(f"<b>Question:</b> {question}", sBold))
    elements.append(sp(6))
    elements.append(Paragraph(
        "<b>Answer / Cold-Call Talking Points:</b>",
        ParagraphStyle(
            "ans", fontName="Palatino-Bold", fontSize=10, leading=13,
            textColor=MAROON,
        ),
    ))
    elements.append(sp(3))
    for b in answer_bullets:
        elements.append(Paragraph(f"\u2022 {b}", sBullet))
        elements.append(sp(2))

    inner = Table([[elements]], colWidths=[content_w - 12])
    inner.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([[inner]], colWidths=[content_w])
    outer.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1, TEAL),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND",    (0, 0), (-1, -1), white),
    ]))
    return outer


def rule_box(rule_title, rule_text_parts, content_w=None):
    """Federal Rule of Evidence in a navy-bordered box on a parchment background.

    Args:
        rule_title: Heading (e.g. ``"Rule 701. OPINION TESTIMONY BY LAY WITNESSES"``).
        rule_text_parts: List of strings or Flowable objects making up the rule text.
        content_w: Total content width (defaults to module-level CONTENT_W).

    Returns:
        A styled Table flowable containing the rule.
    """
    if content_w is None:
        content_w = CONTENT_W
    elements = []
    elements.append(Paragraph(rule_title, sRuleTitle))
    elements.append(sp(4))
    for part in rule_text_parts:
        if isinstance(part, str):
            elements.append(Paragraph(part, sRuleText))
            elements.append(sp(3))
        else:
            elements.append(part)
            elements.append(sp(3))
    inner = Table([[elements]], colWidths=[content_w - 16])
    inner.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([[inner]], colWidths=[content_w])
    outer.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), RULE_BG),
        ("BOX",           (0, 0), (-1, -1), 1.5, NAVY),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return outer


def why_box(title, text, content_w=None):
    """'Why You're Reading' info box with a maroon border on cream.

    Args:
        title: Box heading (string).
        text: Body text (string, may contain HTML markup).
        content_w: Total content width (defaults to module-level CONTENT_W).

    Returns:
        A styled Table flowable.
    """
    if content_w is None:
        content_w = CONTENT_W
    elements = []
    elements.append(Paragraph(f"<b>{title}</b>", sSectionWhy))
    elements.append(sp(4))
    elements.append(Paragraph(text, sBody))
    inner = Table([[elements]], colWidths=[content_w - 16])
    inner.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([[inner]], colWidths=[content_w])
    outer.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1.2, MAROON),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND",    (0, 0), (-1, -1), CREAM),
    ]))
    return outer


# ══════════════════════════════════════════════════════════════════════
#  NoteBuilder CLASS
# ══════════════════════════════════════════════════════════════════════

class NoteBuilder:
    """Fluent API for building richly styled law school class notes PDFs.

    Wraps ReportLab's SimpleDocTemplate and provides high-level methods
    for every component type used in the notes (title pages, section headers,
    case briefs, cold-call boxes, problem boxes, rule boxes, tables, etc.).

    The PDF includes a navy header bar, a grey footer bar with page numbers,
    and a full PDF outline (bookmarks) built automatically from sections,
    subsections, problems, and any explicitly bookmarked elements.

    Example::

        nb = NoteBuilder(
            output_path="my_notes.pdf",
            class_name="Evidence",
            topic_title="Hearsay",
            page_range="pp. 100-120",
        )
        nb.add_title_page(...)
        nb.add_section("A. Introduction")
        nb.add_text("Body text here ...")
        nb.build()

    Args:
        output_path: File path for the generated PDF.
        class_name: Name of the class (e.g. ``"Evidence"``).
        topic_title: Topic / chapter title shown in the header bar.
        page_range: Page range string shown in the header bar.
        font_path: Path to a Palatino .ttc font collection.  Defaults to
                    ``DEFAULT_FONT_PATH``.
        semester: Semester label shown in the header bar (default
                  ``"Spring 2026"``).
    """

    def __init__(self, output_path, class_name, topic_title, page_range,
                 font_path=None, semester="Spring 2026"):
        self._output_path = output_path
        self._class_name = class_name
        self._topic_title = topic_title
        self._page_range = page_range
        self._semester = semester
        self._font_path = font_path or DEFAULT_FONT_PATH
        self._story = []
        self._bookmark_entries = []  # [(level, title), ...]

        # Ensure fonts are registered
        _register_fonts(self._font_path)

        # Header / footer text
        self._header_left = f"{class_name.upper()} \u2022 {semester}"
        self._header_right = f"{topic_title} \u2022 {page_range}"
        self._footer_left = f"{class_name} Class Notes"

    # ------------------------------------------------------------------
    #  Internal helpers
    # ------------------------------------------------------------------

    def _add_bookmark(self, title, level=0):
        """Append a BookmarkFlowable into the story."""
        self._story.append(BookmarkFlowable(title, level=level))
        self._bookmark_entries.append((level, title))

    def _header_footer(self, canvas, doc):
        """Draw the navy header bar and grey footer bar on every page."""
        canvas.saveState()
        # Header bar
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - 32, PAGE_W, 32, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Palatino-Bold", 8)
        canvas.drawString(MARGIN, PAGE_H - 22, self._header_left)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 22, self._header_right)
        # Footer bar
        canvas.setFillColor(MED_GRAY)
        canvas.rect(0, 0, PAGE_W, 24, fill=1, stroke=0)
        canvas.setFillColor(DARK_GRAY)
        canvas.setFont("Palatino-Italic", 7.5)
        canvas.drawString(MARGIN, 9, self._footer_left)
        canvas.drawRightString(PAGE_W - MARGIN, 9, f"Page {doc.page}")
        canvas.restoreState()

    # ------------------------------------------------------------------
    #  Public API -- Title Page
    # ------------------------------------------------------------------

    def add_title_page(self, subtitle, page_ref, toc_data, why_title, why_text):
        """Add a complete title page with title, subtitle, TOC table, and a "Why" box.

        Args:
            subtitle: Italicised subtitle below the main title (string).
            page_ref: Page reference line (e.g.
                      ``"Casebook pp. 100-120 | FRE 803, 804"``).
            toc_data: List of ``[section_letter, topic, key_question]`` rows for
                      the Table of Contents table.  Individual cells may be
                      strings or pre-built Paragraph objects.
            why_title: Heading for the "Why" info box (string).
            why_text: Body for the "Why" info box (string, may contain HTML).

        Returns:
            ``self`` (for method chaining).
        """
        self._add_bookmark("Title & Table of Contents", level=0)
        self._story.append(sp(30))
        self._story.append(
            Paragraph(f"{self._class_name} \u2014 Class Notes", sTitle))
        self._story.append(sp(6))
        self._story.append(Paragraph(f"<i>{subtitle}</i>", sSubtitle))
        self._story.append(sp(4))
        self._story.append(Paragraph(page_ref, sPageRef))
        self._story.append(sp(14))

        # Build TOC table
        toc_rows = []
        for row in toc_data:
            r = []
            for i, c in enumerate(row):
                if isinstance(c, str):
                    if i == 0:
                        r.append(Paragraph(f"<b>{c}</b>", sTableB))
                    else:
                        r.append(Paragraph(c, sTableB))
                else:
                    r.append(c)  # already a Paragraph / Flowable
            toc_rows.append(r)
        self._story.append(info_table(
            ["\u00a7", "Topic", "Key Question"],
            toc_rows,
            col_widths=[0.06 * CONTENT_W, 0.38 * CONTENT_W, 0.56 * CONTENT_W],
        ))
        self._story.append(sp(12))
        self._story.append(why_box(why_title, why_text))
        self._story.append(PageBreak())
        return self

    # ------------------------------------------------------------------
    #  Public API -- Structural Elements
    # ------------------------------------------------------------------

    def add_section(self, title):
        """Add a maroon section header with a PDF bookmark.

        Args:
            title: Section heading text (string).

        Returns:
            ``self`` (for method chaining).
        """
        self._add_bookmark(title, level=0)
        self._story.append(section_header(title))
        self._story.append(sp(8))
        return self

    def add_subsection(self, title):
        """Add a teal sub-section header with a PDF bookmark.

        Args:
            title: Sub-section heading text (string).

        Returns:
            ``self`` (for method chaining).
        """
        self._add_bookmark(title, level=1)
        self._story.append(sub_section_header(title))
        self._story.append(sp(6))
        return self

    def add_text(self, text):
        """Add a body paragraph.  Supports ReportLab HTML markup
        (``<b>``, ``<i>``, ``<br/>``, etc.).

        Args:
            text: Paragraph content (string).

        Returns:
            ``self`` (for method chaining).
        """
        self._story.append(Paragraph(text, sBody))
        self._story.append(sp(6))
        return self

    def add_page_break(self):
        """Insert a page break.

        Returns:
            ``self`` (for method chaining).
        """
        self._story.append(PageBreak())
        return self

    def add_spacer(self, height=6):
        """Insert a vertical spacer.

        Args:
            height: Height in points (default 6).

        Returns:
            ``self`` (for method chaining).
        """
        self._story.append(sp(height))
        return self

    # ------------------------------------------------------------------
    #  Public API -- Content Boxes
    # ------------------------------------------------------------------

    def add_case_brief(self, title, citation, fields):
        """Add a case brief box (navy-bordered, cream background).

        Args:
            title: Case name (string).
            citation: Full citation (string).
            fields: List of ``(label, content)`` tuples.  *content* may be a
                     plain string or a list of bullet strings.

        Returns:
            ``self`` (for method chaining).
        """
        self._add_bookmark(title, level=1)
        self._story.append(case_brief_box(title, citation, fields))
        self._story.append(sp(8))
        return self

    def add_cold_call(self, title, qa_pairs):
        """Add a cold-call Q&A box (maroon-bordered).

        Args:
            title: Box heading (string, e.g. ``"COLD-CALL POINTS -- Crawford"``).
            qa_pairs: List of ``(question_str, [answer_str, ...])`` tuples.

        Returns:
            ``self`` (for method chaining).
        """
        self._story.append(cold_call_box(title, qa_pairs))
        self._story.append(sp(8))
        return self

    def add_problem(self, number, title, facts, question, answer_bullets):
        """Add a problem box (teal-bordered) with a bookmark.

        Args:
            number: Problem number (string or int).
            title: Short descriptive title.
            facts: Fact pattern paragraph (string).
            question: The question posed (string).
            answer_bullets: List of answer/talking-point strings.

        Returns:
            ``self`` (for method chaining).
        """
        self._add_bookmark(f"Problem {number}: {title}", level=1)
        self._story.append(KeepTogether([
            problem_box(number, title, facts, question, answer_bullets),
            sp(10),
        ]))
        return self

    def add_table(self, headers, rows, col_widths=None):
        """Add a coloured information table (teal header, alternating rows).

        Args:
            headers: List of header strings.
            rows: List of row lists (each cell a string or Paragraph).
            col_widths: Optional list of column widths in points.  When given
                        as floats that sum to roughly 1.0, they are treated as
                        fractions of CONTENT_W.

        Returns:
            ``self`` (for method chaining).
        """
        # Auto-detect fractional widths (all values <= 1.0 and sum ~ 1.0)
        if col_widths is not None:
            if all(isinstance(w, (int, float)) and w <= 1.0 for w in col_widths):
                total = sum(col_widths)
                if 0.95 <= total <= 1.05:
                    col_widths = [w * CONTENT_W for w in col_widths]
        self._story.append(info_table(headers, rows, col_widths=col_widths))
        self._story.append(sp(8))
        return self

    def add_rule_box(self, rule_title, rule_text_parts):
        """Add a Federal Rule box (navy-bordered, parchment background).

        Args:
            rule_title: Rule heading (string).
            rule_text_parts: List of strings or Flowable objects.

        Returns:
            ``self`` (for method chaining).
        """
        self._story.append(rule_box(rule_title, rule_text_parts))
        self._story.append(sp(8))
        return self

    def add_info_box(self, title, text):
        """Add a bordered info / "why" box (maroon border, cream background).

        Args:
            title: Box heading (string).
            text: Body text (string, may contain HTML markup).

        Returns:
            ``self`` (for method chaining).
        """
        self._story.append(why_box(title, text))
        self._story.append(sp(8))
        return self

    def add_confidence_score(self, rows):
        """Add a Confidence Score table at the end of the notes.

        Args:
            rows: List of ``[component, score, notes]`` lists.  The final
                  row is typically the overall score.

        Returns:
            ``self`` (for method chaining).
        """
        self._add_bookmark("Confidence Score", level=0)
        self._story.append(KeepTogether([
            sp(4),
            Paragraph("Confidence Score", sConfTitle),
            sp(8),
            info_table(
                ["Component", "Score", "Notes"],
                rows,
                col_widths=[0.30 * CONTENT_W, 0.08 * CONTENT_W, 0.62 * CONTENT_W],
            ),
        ]))
        self._story.append(sp(8))
        return self

    # ------------------------------------------------------------------
    #  Build
    # ------------------------------------------------------------------

    def build(self):
        """Build the PDF to ``self._output_path``.

        Creates the output directory if it does not exist, assembles the
        document with header/footer bars on every page, and writes the file.

        Returns:
            The absolute output path (string).
        """
        out_dir = os.path.dirname(self._output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        doc = SimpleDocTemplate(
            self._output_path,
            pagesize=letter,
            leftMargin=MARGIN,
            rightMargin=MARGIN,
            topMargin=MARGIN + 20,
            bottomMargin=MARGIN + 12,
        )
        doc.build(
            self._story,
            onFirstPage=self._header_footer,
            onLaterPages=self._header_footer,
        )
        print(f"PDF created ({len(self._bookmark_entries)} bookmarks): "
              f"{self._output_path}")
        return self._output_path


# ══════════════════════════════════════════════════════════════════════
#  MODULE-LEVEL CONVENIENCE EXPORTS
# ══════════════════════════════════════════════════════════════════════

# Re-export styles so advanced users can reference them directly.
STYLES = {
    "title":      sTitle,
    "subtitle":   sSubtitle,
    "page_ref":   sPageRef,
    "body":       sBody,
    "body_small": sBodySmall,
    "bold":       sBold,
    "italic":     sItalic,
    "bullet":     sBullet,
    "bullet_bold": sBulletBold,
    "question":   sQuestion,
    "answer":     sAnswer,
    "table_h":    sTableH,
    "table_b":    sTableB,
    "table_bi":   sTableBI,
    "rule_title": sRuleTitle,
    "rule_text":  sRuleText,
    "section_why": sSectionWhy,
    "conf_title": sConfTitle,
    "case_title": sCaseTitle,
    "case_cite":  sCaseCite,
}

# Re-export colours for external scripts that import the library.
COLORS = {
    "navy":       NAVY,
    "teal":       TEAL,
    "teal_light": TEAL_LIGHT,
    "maroon":     MAROON,
    "cream":      CREAM,
    "light_gray": LIGHT_GRAY,
    "med_gray":   MED_GRAY,
    "dark_gray":  DARK_GRAY,
    "gold":       GOLD,
    "rule_bg":    RULE_BG,
    "box_border": BOX_BORDER,
}
