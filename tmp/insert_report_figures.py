from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph


ROOT = Path("/Users/fanfan/Documents/GitHub/MSE806-ITS")
DOCX = ROOT / "Assessment/MSE806_Assessment1_Report_Template_Final.docx"
FIGURE_DIR = ROOT / "Assessment/Analysis_Output"

FIGURES = [
    (
        "figure_1_layered_its_architecture.png",
        6.25,
        "Layered ITS and cyber-physical system architecture",
        "Note. Author-developed synthesis of the Dublin Bus ITS architecture described by World Bank Group (2011), with cyber-risk considerations informed by Avci and Koca (2024).",
    ),
    (
        "figure_2_dublin_bus_its_timeline.png",
        6.25,
        "Dublin Bus ITS development timeline",
        "Note. Author-developed timeline based on the implementation sequence reported by World Bank Group (2011).",
    ),
    (
        "figure_3_end_to_end_communications_architecture.png",
        6.25,
        "End-to-end Dublin Bus ITS and communications architecture",
        "Note. Author-developed architecture based on World Bank Group (2011); the signal-priority interface is contextualised using Smith et al. (2005).",
    ),
    (
        "figure_4_dublin_bus_network.png",
        5.15,
        "Dublin Bus scheduled route and stop network",
        "Note. Author analysis of the Transport for Ireland GTFS static feed. The map represents scheduled network coverage and used stops, not observed vehicle positions (TFI, 2026).",
    ),
    (
        "figure_5_hourly_scheduled_trips.png",
        6.25,
        "Hourly distribution of scheduled trips",
        "Note. Author analysis of the Transport for Ireland GTFS static feed for 23 and 26 September 2026. Values describe scheduled departures, not actual arrivals or delay (TFI, 2026).",
    ),
    (
        "figure_6_route_distance_duration.png",
        6.05,
        "Route distance and scheduled journey duration",
        "Note. Author analysis of Dublin Bus services in the Transport for Ireland GTFS static feed. Distances and durations are schedule-derived and do not measure realised speed or congestion (TFI, 2026).",
    ),
    (
        "figure_7_conditional_tsp_process.png",
        6.25,
        "Conditional traffic signal priority decision process",
        "Note. Author-developed decision process informed by the conditional-priority principles in Smith et al. (2005). Operational deployment would require observed vehicle and controller data beyond the supplied GTFS feeds.",
    ),
    (
        "figure_8_five_year_its_ai_roadmap.png",
        6.25,
        "Five-year ITS and AI adoption roadmap",
        "Note. Author-developed roadmap synthesising the staged implementation and governance requirements discussed by World Bank Group (2011), Fatorachian and Kazemi (2024), and Avci and Koca (2024).",
    ),
]


def clear_paragraph(paragraph):
    for child in list(paragraph._p):
        if child.tag != qn("w:pPr"):
            paragraph._p.remove(child)


def set_alt_text(inline_shape, title):
    doc_pr = inline_shape._inline.docPr
    doc_pr.set("name", title)
    doc_pr.set("descr", title)


def main():
    doc = Document(DOCX)
    placeholders = [
        p for p in doc.paragraphs if p.text.strip().startswith("[Insert figure here:")
    ]
    if len(placeholders) != len(FIGURES):
        raise RuntimeError(
            f"Expected {len(FIGURES)} figure placeholders, found {len(placeholders)}"
        )

    for number, (paragraph, spec) in enumerate(zip(placeholders, FIGURES), start=1):
        filename, width, alt_text, note_text = spec
        image_path = FIGURE_DIR / filename
        if not image_path.is_file():
            raise FileNotFoundError(image_path)

        clear_paragraph(paragraph)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_before = Pt(3)
        paragraph.paragraph_format.space_after = Pt(4)
        paragraph.paragraph_format.keep_with_next = True
        shape = paragraph.add_run().add_picture(str(image_path), width=Inches(width))
        set_alt_text(shape, f"Figure {number}. {alt_text}")

        previous = paragraph._p.getprevious()
        if previous is not None:
            previous_paragraph = Paragraph(previous, paragraph._parent)
            previous_paragraph.paragraph_format.keep_with_next = True

        note = paragraph._p.getnext()
        if note is None:
            raise RuntimeError(f"Figure {number} has no following note paragraph")
        note_paragraph = Paragraph(note, paragraph._parent)
        clear_paragraph(note_paragraph)
        note_run = note_paragraph.add_run(note_text)
        note_run.italic = True
        note_paragraph.paragraph_format.keep_with_next = False

    doc.save(DOCX)
    print(f"Inserted {len(FIGURES)} figures into {DOCX}")


if __name__ == "__main__":
    main()
