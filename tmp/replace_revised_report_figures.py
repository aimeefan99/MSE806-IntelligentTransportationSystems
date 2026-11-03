from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path("/Users/fanfan/Documents/GitHub/MSE806-ITS")
DOCX = ROOT / "Assessment/MSE806_Assessment1_Report_Template_Final.docx"
FIGURE_DIR = ROOT / "Assessment/Analysis_Output"

REPLACEMENTS = {
    "word/media/image2.png": FIGURE_DIR / "figure_2_dublin_bus_its_timeline.png",
    "word/media/image3.png": FIGURE_DIR / "figure_3_end_to_end_communications_architecture.png",
    "word/media/image7.png": FIGURE_DIR / "figure_7_conditional_tsp_process.png",
    "word/media/image8.png": FIGURE_DIR / "figure_8_five_year_its_ai_roadmap.png",
}


def main():
    payloads = {target: source.read_bytes() for target, source in REPLACEMENTS.items()}
    found = set()

    with NamedTemporaryFile(
        dir=DOCX.parent, prefix="revised_figures_", suffix=".docx", delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    try:
        with ZipFile(DOCX, "r") as source, ZipFile(
            temporary_path, "w", compression=ZIP_DEFLATED
        ) as destination:
            for item in source.infolist():
                payload = source.read(item.filename)
                if item.filename in payloads:
                    payload = payloads[item.filename]
                    found.add(item.filename)
                destination.writestr(item, payload)

        missing = set(REPLACEMENTS) - found
        if missing:
            raise RuntimeError(f"Missing DOCX media entries: {sorted(missing)}")
        temporary_path.replace(DOCX)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    print(f"Replaced {len(found)} revised figures in {DOCX}")


if __name__ == "__main__":
    main()
