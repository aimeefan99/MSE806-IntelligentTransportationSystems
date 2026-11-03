from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path("/Users/fanfan/Documents/GitHub/MSE806-ITS")
DOCX = ROOT / "Assessment/MSE806_Assessment1_Report_Template_Final.docx"
IMAGE = ROOT / "Assessment/Analysis_Output/figure_1_layered_its_architecture.png"
TARGET = "word/media/image1.png"


def main():
    replacement = IMAGE.read_bytes()
    found = False

    with NamedTemporaryFile(
        dir=DOCX.parent, prefix="figure1_", suffix=".docx", delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    try:
        with ZipFile(DOCX, "r") as source, ZipFile(
            temporary_path, "w", compression=ZIP_DEFLATED
        ) as destination:
            for item in source.infolist():
                payload = source.read(item.filename)
                if item.filename == TARGET:
                    payload = replacement
                    found = True
                destination.writestr(item, payload)

        if not found:
            raise RuntimeError(f"Could not find {TARGET} in {DOCX}")
        temporary_path.replace(DOCX)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    print(f"Replaced {TARGET} in {DOCX}")


if __name__ == "__main__":
    main()
