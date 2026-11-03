from pathlib import Path

from PIL import Image, ImageDraw


SOURCE = Path("/private/tmp/mse806_font_rules_qa2")
OUTPUT = SOURCE / "contact_sheets"
OUTPUT.mkdir(exist_ok=True)

pages = sorted(
    SOURCE.glob("page-*.png"),
    key=lambda path: int(path.stem.split("-")[1]),
)

thumb_width = 800
gap = 24
label_height = 38

for sheet_number, start in enumerate(range(0, len(pages), 4), start=1):
    batch = pages[start : start + 4]
    prepared = []
    for path in batch:
        image = Image.open(path).convert("RGB")
        height = round(image.height * thumb_width / image.width)
        image = image.resize((thumb_width, height), Image.Resampling.LANCZOS)
        prepared.append((path, image))

    cell_height = max(image.height for _, image in prepared) + label_height
    sheet = Image.new(
        "RGB",
        (thumb_width * 2 + gap * 3, cell_height * 2 + gap * 3),
        "#D8D8D8",
    )
    draw = ImageDraw.Draw(sheet)
    for index, (path, image) in enumerate(prepared):
        col = index % 2
        row = index // 2
        x = gap + col * (thumb_width + gap)
        y = gap + row * (cell_height + gap)
        sheet.paste(image, (x, y + label_height))
        draw.text((x, y + 8), path.stem, fill="black")

    sheet.save(OUTPUT / f"sheet-{sheet_number}.png", optimize=True)

print(f"Created {sheet_number} contact sheets in {OUTPUT}")
