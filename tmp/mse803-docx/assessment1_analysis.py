"""Reproducible analysis for MSE803 Assessment 1 Task 1.

The script preserves the supplied workbook, audits both side-by-side source
tables, applies explicit cleaning rules, creates analysis-ready CSV files,
performs descriptive and inferential analysis, and produces two static figures.

It intentionally uses the same core workflow practised in Weeks 1, 3, and 4:
schema inspection, duplicate and missing-value checks, documented outlier
review, descriptive statistics, correlation, regression, and visualisation.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent
ASSESSMENT_DIR = BASE_DIR.parent
SOURCE_FILE = ASSESSMENT_DIR / "Data_Set_Assignmnet_1 - 0426.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"

RANDOM_SEED = 803
ALPHA = 0.05

WATER_COLUMNS = ["site_id", "date", "temperature_c", "ph", "dissolved_oxygen_mg_l"]
FISH_COLUMNS = ["site_id", "date", "species", "count", "average_size_cm"]
WATER_KEY = ["site_id", "date"]

FONT_REGULAR = Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_output_directory() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_source_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read the two adjacent tables without changing the source workbook."""
    worksheet = openpyxl.load_workbook(SOURCE_FILE, data_only=True).active
    rows = list(worksheet.iter_rows(min_row=3, values_only=True))

    water = pd.DataFrame([row[:5] for row in rows], columns=WATER_COLUMNS).dropna(how="all")
    fish = pd.DataFrame([row[6:11] for row in rows], columns=FISH_COLUMNS).dropna(how="all")
    water.insert(0, "source_row", np.arange(3, 3 + len(water)))
    fish.insert(0, "source_row", np.arange(3, 3 + len(fish)))
    return water.reset_index(drop=True), fish.reset_index(drop=True)


def normalise_source_types(
    water: pd.DataFrame, fish: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    water = water.copy()
    fish = fish.copy()

    for frame in (water, fish):
        frame["site_id"] = frame["site_id"].astype("string").str.strip().str.upper()
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce", format="mixed")

    fish["species"] = fish["species"].astype("string").str.strip().replace("", pd.NA)
    for column in ["temperature_c", "ph", "dissolved_oxygen_mg_l"]:
        water[column] = pd.to_numeric(water[column], errors="coerce")
    for column in ["count", "average_size_cm"]:
        fish[column] = pd.to_numeric(fish[column], errors="coerce")
    return water, fish


def exact_duplicate_mask(frame: pd.DataFrame, data_columns: list[str]) -> pd.Series:
    return frame.duplicated(subset=data_columns, keep="first")


def append_reason(existing: pd.Series, mask: pd.Series, reason: str) -> pd.Series:
    result = existing.copy()
    needs_reason = mask & ~result.fillna("").str.contains(reason, regex=False)
    was_empty = result.eq("")
    result.loc[needs_reason & was_empty] = reason
    result.loc[needs_reason & ~was_empty] = (
        result.loc[needs_reason & ~was_empty] + "; " + reason
    )
    return result


def clean_water(raw_water: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    typed, _ = normalise_source_types(raw_water, pd.DataFrame(columns=FISH_COLUMNS))
    duplicate_mask = exact_duplicate_mask(typed, WATER_COLUMNS)
    deduplicated = typed.loc[~duplicate_mask].copy()
    reasons = pd.Series("", index=deduplicated.index, dtype="string")

    reasons = append_reason(
        reasons,
        deduplicated[["site_id", "date", "temperature_c", "ph", "dissolved_oxygen_mg_l"]]
        .isna()
        .any(axis=1),
        "missing required value or invalid date",
    )
    reasons = append_reason(
        reasons,
        ~deduplicated["site_id"].isin(["AV-1", "AV-2", "AV-3"]),
        "unexpected site identifier",
    )
    reasons = append_reason(
        reasons,
        deduplicated["temperature_c"].notna()
        & ~deduplicated["temperature_c"].between(0, 35, inclusive="both"),
        "temperature outside validation range 0-35 C",
    )
    reasons = append_reason(
        reasons,
        deduplicated["ph"].notna()
        & ~deduplicated["ph"].between(0, 14, inclusive="both"),
        "pH outside physical range 0-14",
    )
    reasons = append_reason(
        reasons,
        deduplicated["dissolved_oxygen_mg_l"].notna()
        & ~deduplicated["dissolved_oxygen_mg_l"].between(0, 20, inclusive="both"),
        "dissolved oxygen outside validation range 0-20 mg/L",
    )

    excluded = deduplicated.loc[reasons.ne("")].copy()
    excluded["exclusion_reason"] = reasons.loc[excluded.index]
    cleaned = deduplicated.loc[reasons.eq("")].copy().reset_index(drop=True)

    audit = {
        "raw_records": len(raw_water),
        "exact_duplicates_removed": int(duplicate_mask.sum()),
        "records_after_deduplication": len(deduplicated),
        "records_excluded_after_deduplication": len(excluded),
        "clean_records": len(cleaned),
    }
    return cleaned, excluded, audit


def species_size_outliers(frame: pd.DataFrame) -> pd.Series:
    """Flag species-specific sizes using the Week 4 1.5 x IQR rule."""
    flags = pd.Series(False, index=frame.index)
    for _, group in frame.dropna(subset=["species", "average_size_cm"]).groupby("species"):
        values = group["average_size_cm"]
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        flags.loc[group.index] = (values < lower) | (values > upper)
    return flags


def clean_fish(raw_fish: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    _, typed = normalise_source_types(pd.DataFrame(columns=WATER_COLUMNS), raw_fish)
    duplicate_mask = exact_duplicate_mask(typed, FISH_COLUMNS)
    deduplicated = typed.loc[~duplicate_mask].copy()
    reasons = pd.Series("", index=deduplicated.index, dtype="string")

    reasons = append_reason(
        reasons,
        deduplicated[["site_id", "date", "species", "count", "average_size_cm"]]
        .isna()
        .any(axis=1),
        "missing required value or invalid date",
    )
    reasons = append_reason(
        reasons,
        ~deduplicated["site_id"].isin(["AV-1", "AV-2", "AV-3"]),
        "unexpected site identifier",
    )
    reasons = append_reason(reasons, deduplicated["count"] < 0, "negative fish count")
    reasons = append_reason(reasons, deduplicated["average_size_cm"] <= 0, "non-positive size")

    valid_counts = deduplicated["count"].dropna()
    q1, q3 = valid_counts.quantile([0.25, 0.75])
    count_upper_fence = q3 + 1.5 * (q3 - q1)
    reasons = append_reason(
        reasons,
        deduplicated["count"] > count_upper_fence,
        f"count above robust upper fence {count_upper_fence:.2f}",
    )
    excluded = deduplicated.loc[reasons.ne("")].copy()
    excluded["exclusion_reason"] = reasons.loc[excluded.index]
    cleaned = deduplicated.loc[reasons.eq("")].copy().reset_index(drop=True)
    # The Week 4 IQR rule flags potential size outliers for review. It does not
    # remove them automatically because a statistical outlier may be genuine.
    cleaned["size_iqr_flag"] = species_size_outliers(cleaned)

    audit = {
        "raw_records": len(raw_fish),
        "exact_duplicates_removed": int(duplicate_mask.sum()),
        "records_after_deduplication": len(deduplicated),
        "records_excluded_after_deduplication": len(excluded),
        "clean_records": len(cleaned),
    }
    return cleaned, excluded, audit


def aggregate_and_merge(
    water: pd.DataFrame, fish: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    water_aggregated = (
        water.groupby(WATER_KEY, as_index=False)
        .agg(
            temperature_c=("temperature_c", "mean"),
            ph=("ph", "mean"),
            dissolved_oxygen_mg_l=("dissolved_oxygen_mg_l", "mean"),
            water_records=("source_row", "size"),
        )
        .sort_values(WATER_KEY)
    )

    merged = fish.merge(water_aggregated, on=WATER_KEY, how="left", indicator=True)
    unmatched_fish = merged.loc[merged["_merge"].ne("both")].copy()
    matched = merged.loc[merged["_merge"].eq("both")].drop(columns="_merge").copy()
    matched["month"] = matched["date"].dt.strftime("%Y-%m")
    return water_aggregated, matched.reset_index(drop=True), unmatched_fish


def describe_water_by_site(water: pd.DataFrame) -> pd.DataFrame:
    summary = water.groupby("site_id").agg(
        records=("dissolved_oxygen_mg_l", "size"),
        temperature_mean_c=("temperature_c", "mean"),
        temperature_min_c=("temperature_c", "min"),
        temperature_max_c=("temperature_c", "max"),
        ph_mean=("ph", "mean"),
        ph_min=("ph", "min"),
        ph_max=("ph", "max"),
        do_mean_mg_l=("dissolved_oxygen_mg_l", "mean"),
        do_median_mg_l=("dissolved_oxygen_mg_l", "median"),
        do_min_mg_l=("dissolved_oxygen_mg_l", "min"),
        do_max_mg_l=("dissolved_oxygen_mg_l", "max"),
    )
    return summary.reset_index()


def describe_fish_by_species(merged: pd.DataFrame) -> pd.DataFrame:
    return (
        merged.groupby("species")
        .agg(
            records=("count", "size"),
            count_mean=("count", "mean"),
            count_median=("count", "median"),
            count_min=("count", "min"),
            count_max=("count", "max"),
            average_size_mean_cm=("average_size_cm", "mean"),
            do_mean_mg_l=("dissolved_oxygen_mg_l", "mean"),
        )
        .reset_index()
    )


def pearson_correlation(left: np.ndarray, right: np.ndarray) -> float:
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if len(left) < 3 or np.std(left, ddof=1) == 0 or np.std(right, ddof=1) == 0:
        return float("nan")
    return float(np.corrcoef(left, right)[0, 1])


def build_correlation_results(merged: pd.DataFrame) -> pd.DataFrame:
    predictors = ["temperature_c", "ph", "dissolved_oxygen_mg_l"]
    outcomes = ["count", "average_size_cm"]
    rows = []
    for predictor in predictors:
        for outcome in outcomes:
            pair = merged[[predictor, outcome]].dropna()
            rows.append(
                {
                    "predictor": predictor,
                    "outcome": outcome,
                    "n": len(pair),
                    "pearson_correlation": pearson_correlation(
                        pair[predictor].to_numpy(), pair[outcome].to_numpy()
                    ),
                }
            )
    return pd.DataFrame(rows)


def one_way_anova_do_by_site(water: pd.DataFrame) -> pd.DataFrame:
    """Classroom one-way ANOVA comparing mean DO across the three sites."""
    groups = [
        group["dissolved_oxygen_mg_l"].to_numpy(dtype=float)
        for _, group in water.groupby("site_id")
    ]
    all_values = np.concatenate(groups)
    grand_mean = all_values.mean()
    group_count = len(groups)
    total_count = len(all_values)
    ss_between = sum(len(group) * (group.mean() - grand_mean) ** 2 for group in groups)
    ss_within = sum(((group - group.mean()) ** 2).sum() for group in groups)
    df_between = group_count - 1
    df_within = total_count - group_count
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    f_statistic = ms_between / ms_within

    # For this design df_between = 2. The right-tail F probability has this
    # simple closed form, equivalent to Excel's F.DIST.RT result.
    if df_between != 2:
        raise ValueError("The classroom ANOVA p-value formula expects three groups")
    p_value = (df_within / (df_within + 2 * f_statistic)) ** (df_within / 2)
    decision = "Reject H0" if p_value <= ALPHA else "Fail to reject H0"
    return pd.DataFrame(
        [
            {
                "test": "One-way ANOVA: dissolved oxygen by site",
                "df_between": df_between,
                "df_within": df_within,
                "f_statistic": f_statistic,
                "p_value": p_value,
                "alpha": ALPHA,
                "decision": decision,
            }
        ]
    )


def chi_square_site_by_origin(merged: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Classroom chi-square test for site and native/introduced classification."""
    data = merged.copy()
    data["origin"] = np.where(data["species"].eq("Brown Trout"), "Introduced", "Native")
    observed = pd.crosstab(data["site_id"], data["origin"])
    values = observed.to_numpy(dtype=float)
    expected = values.sum(axis=1, keepdims=True) @ values.sum(axis=0, keepdims=True) / values.sum()
    chi_square = float(np.sum((values - expected) ** 2 / expected))
    degrees_freedom = (values.shape[0] - 1) * (values.shape[1] - 1)
    if degrees_freedom != 2:
        raise ValueError("The classroom chi-square p-value formula expects df = 2")
    p_value = math.exp(-chi_square / 2)
    decision = "Reject H0" if p_value <= ALPHA else "Fail to reject H0"
    result = pd.DataFrame(
        [
            {
                "test": "Chi-square: site and species origin",
                "chi_square": chi_square,
                "degrees_freedom": degrees_freedom,
                "minimum_expected_count": float(expected.min()),
                "p_value": p_value,
                "alpha": ALPHA,
                "decision": decision,
            }
        ]
    )
    expected_frame = pd.DataFrame(expected, index=observed.index, columns=observed.columns)
    comparison = observed.astype(float)
    comparison.columns = [f"observed_{column}" for column in comparison.columns]
    for column in expected_frame.columns:
        comparison[f"expected_{column}"] = expected_frame[column]
    return result, comparison.reset_index()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(path), size=size)


def draw_rotated_text(
    image: Image.Image, position: tuple[int, int], text: str, text_font, fill: str
) -> None:
    box = Image.new("RGBA", (500, 80), (255, 255, 255, 0))
    box_draw = ImageDraw.Draw(box)
    box_draw.text((0, 0), text, font=text_font, fill=fill)
    rotated = box.rotate(90, expand=True)
    image.alpha_composite(rotated, dest=position)


def plot_do_time_series(water: pd.DataFrame, path: Path) -> None:
    width, height = 1600, 900
    image = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(image)
    left, right, top, bottom = 150, 70, 135, 130
    plot_width, plot_height = width - left - right, height - top - bottom
    start, end = water["date"].min(), water["date"].max()
    y_min = math.floor(water["dissolved_oxygen_mg_l"].min())
    y_max = math.ceil(water["dissolved_oxygen_mg_l"].max())

    def x_position(value):
        return left + (value - start).days / max((end - start).days, 1) * plot_width

    def y_position(value):
        return top + (y_max - value) / (y_max - y_min) * plot_height

    draw.text(
        (left, 35),
        "Dissolved Oxygen Varies Episodically Across Avon River Sites",
        font=font(38, bold=True),
        fill="#111111",
    )
    draw.text(
        (left, 83),
        "Cleaned and de-duplicated observations, October-December 2023",
        font=font(25),
        fill="#444444",
    )

    for value in range(y_min, y_max + 1):
        y = y_position(value)
        draw.line((left, y, width - right, y), fill="#D9D9D9", width=2)
        draw.text((left - 65, y - 13), f"{value}", font=font(22), fill="#333333")

    tick_dates = pd.date_range(start.normalize(), end.normalize(), periods=7)
    for tick in tick_dates:
        x = x_position(tick)
        draw.line((x, top, x, top + plot_height), fill="#EEEEEE", width=1)
        label = tick.strftime("%d %b")
        draw.text((x - 35, top + plot_height + 22), label, font=font(20), fill="#333333")

    draw.line((left, top, left, top + plot_height), fill="#222222", width=3)
    draw.line((left, top + plot_height, width - right, top + plot_height), fill="#222222", width=3)
    draw.text((width // 2 - 40, height - 60), "Date", font=font(24), fill="#111111")
    draw_rotated_text(
        image,
        (25, top + plot_height // 2 - 165),
        "Dissolved oxygen (mg/L)",
        font(24),
        "#111111",
    )

    colours = {"AV-1": "#0072B2", "AV-2": "#E69F00", "AV-3": "#009E73"}
    for site, group in water.sort_values("date").groupby("site_id"):
        points = [
            (x_position(row.date), y_position(row.dissolved_oxygen_mg_l))
            for row in group.itertuples()
        ]
        if len(points) > 1:
            draw.line(points, fill=colours[site], width=4)
        for x, y in points:
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=colours[site], outline="white", width=2)

    legend_x = width - right - 340
    for index, site in enumerate(["AV-1", "AV-2", "AV-3"]):
        y = 50 + index * 35
        draw.line((legend_x, y + 10, legend_x + 45, y + 10), fill=colours[site], width=5)
        draw.text((legend_x + 58, y - 4), site, font=font(22), fill="#111111")

    image.convert("RGB").save(path, quality=95, dpi=(300, 300))


def plot_do_count_by_species(merged: pd.DataFrame, path: Path) -> None:
    width, height = 1600, 1150
    image = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text(
        (110, 28),
        "Dissolved Oxygen and Fish Count Patterns by Species",
        font=font(36, bold=True),
        fill="#111111",
    )
    draw.text(
        (110, 76),
        "Pearson correlation is descriptive and does not establish causation",
        font=font(24),
        fill="#444444",
    )

    species_order = ["Brown Trout", "Inanga", "Longfin Eel", "Shortfin Eel"]
    colours = ["#0072B2", "#E69F00", "#009E73", "#CC79A7"]
    panel_positions = [(100, 145), (830, 145), (100, 630), (830, 630)]
    panel_width, panel_height = 640, 390
    x_min = math.floor(merged["dissolved_oxygen_mg_l"].min() * 2) / 2
    x_max = math.ceil(merged["dissolved_oxygen_mg_l"].max() * 2) / 2
    y_min, y_max = 0, math.ceil(merged["count"].max() / 5) * 5

    for species, colour, (panel_left, panel_top) in zip(
        species_order, colours, panel_positions
    ):
        group = merged.loc[merged["species"].eq(species)].copy()
        chart_left = panel_left + 75
        chart_top = panel_top + 52
        chart_width = panel_width - 105
        chart_height = panel_height - 105

        def xp(value):
            return chart_left + (value - x_min) / (x_max - x_min) * chart_width

        def yp(value):
            return chart_top + (y_max - value) / (y_max - y_min) * chart_height

        draw.text((panel_left, panel_top), species, font=font(27, bold=True), fill="#111111")
        correlation = pearson_correlation(
            group["dissolved_oxygen_mg_l"].to_numpy(), group["count"].to_numpy()
        )
        draw.text(
            (panel_left + 370, panel_top + 5),
            f"n = {len(group)}, r = {correlation:.2f}",
            font=font(20),
            fill="#444444",
        )
        for value in range(0, y_max + 1, 5):
            y = yp(value)
            draw.line((chart_left, y, chart_left + chart_width, y), fill="#E5E5E5", width=1)
            draw.text((chart_left - 42, y - 11), str(value), font=font(17), fill="#444444")
        for value in np.arange(math.ceil(x_min), math.floor(x_max) + 1, 1):
            x = xp(value)
            draw.text((x - 10, chart_top + chart_height + 10), f"{value:g}", font=font(17), fill="#444444")
        draw.line((chart_left, chart_top, chart_left, chart_top + chart_height), fill="#222222", width=2)
        draw.line(
            (chart_left, chart_top + chart_height, chart_left + chart_width, chart_top + chart_height),
            fill="#222222",
            width=2,
        )

        for row in group.itertuples():
            x, y = xp(row.dissolved_oxygen_mg_l), yp(row.count)
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=colour, outline="white", width=2)

        draw.text(
            (chart_left + chart_width // 2 - 70, panel_top + panel_height - 20),
            "Dissolved oxygen (mg/L)",
            font=font(18),
            fill="#111111",
        )
        draw.text((panel_left + 8, chart_top + chart_height // 2), "Count", font=font(18), fill="#111111")

    image.convert("RGB").save(path, quality=95, dpi=(300, 300))


def format_markdown_table(frame: pd.DataFrame, decimals: int = 3) -> str:
    display = frame.copy()
    for column in display.select_dtypes(include=["number"]).columns:
        display[column] = display[column].map(
            lambda value: "" if pd.isna(value) else f"{value:.{decimals}f}"
        )
    headers = [str(column) for column in display.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in display.astype(str).itertuples(index=False, name=None):
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def build_report(
    source_hash: str,
    water_audit: dict[str, int],
    fish_audit: dict[str, int],
    water: pd.DataFrame,
    matched: pd.DataFrame,
    unmatched_fish: pd.DataFrame,
    water_summary: pd.DataFrame,
    fish_summary: pd.DataFrame,
    correlations: pd.DataFrame,
    anova_result: pd.DataFrame,
    chi_square_result: pd.DataFrame,
    chi_square_table: pd.DataFrame,
) -> str:
    do_low_count = int((water["dissolved_oxygen_mg_l"] <= 6.9).sum())
    return f"""# MSE803 Assessment 1 Task 1 Analysis

## Reproducibility

- Source workbook: `{SOURCE_FILE.name}`
- Source SHA-256: `{source_hash}`
- Significance level selected before testing: alpha = {ALPHA:.2f}
- The source workbook is read only and is not overwritten.

## Research question and hypotheses

Research question 1: does mean dissolved oxygen differ among AV-1, AV-2,
and AV-3?

- H0: mean dissolved oxygen is equal across the three sites.
- H1: at least one site has a different mean dissolved oxygen value.
- Test: one-way ANOVA at alpha = {ALPHA:.2f}.

Research question 2: is the native/introduced classification of observed fish
independent of monitoring site?

- H0: site and species origin are independent.
- H1: site and species origin are associated.
- Test: chi-square test of independence at alpha = {ALPHA:.2f}.

## Data quality audit

| Measure | Water quality | Fish population |
| --- | ---: | ---: |
| Raw records | {water_audit['raw_records']} | {fish_audit['raw_records']} |
| Exact duplicates removed | {water_audit['exact_duplicates_removed']} ({water_audit['exact_duplicates_removed']/water_audit['raw_records']:.1%}) | {fish_audit['exact_duplicates_removed']} ({fish_audit['exact_duplicates_removed']/fish_audit['raw_records']:.1%}) |
| Records after exact de-duplication | {water_audit['records_after_deduplication']} | {fish_audit['records_after_deduplication']} |
| Additional records excluded | {water_audit['records_excluded_after_deduplication']} | {fish_audit['records_excluded_after_deduplication']} |
| Clean records | {water_audit['clean_records']} | {fish_audit['clean_records']} |

Distinct water-quality records sharing a site and date are aggregated by their
mean because the workbook has no sample-time or replicate identifier. Fish rows
for different species at the same site and date remain separate. The merge
produced {len(matched)} matched fish observations and {len(unmatched_fish)}
unmatched fish observations.

## Descriptive findings

There are {do_low_count} cleaned water-quality observations at or below 6.9
mg/L dissolved oxygen. These are described as comparatively lower observations,
not automatic regulatory breaches or universal biological thresholds.

### Water quality by site

{format_markdown_table(water_summary, 2)}

### Fish outcomes by species

{format_markdown_table(fish_summary, 2)}

## Pearson correlations

Pearson correlations describe the direction and strength of linear association.
They are not interpreted as hypothesis tests or evidence of causation.

{format_markdown_table(correlations, 4)}

## One-way ANOVA

{format_markdown_table(anova_result, 4)}

## Chi-square test of independence

{format_markdown_table(chi_square_result, 4)}

### Observed and expected counts

{format_markdown_table(chi_square_table, 3)}

For both tests, p > alpha is reported as fail to reject H0. It is not described
as accepting or proving H0. Pearson correlation remains descriptive because the
coursework analysis does not add a separate correlation significance test.

## Visualisations

- `figure1_dissolved_oxygen_by_site.png`: time-ordered dissolved oxygen observations by site; no universal threshold line is imposed.
- `figure2_do_fish_count_by_species.png`: species-faceted dissolved oxygen and count observations with descriptive Pearson coefficients.
"""


def save_outputs(
    raw_water: pd.DataFrame,
    raw_fish: pd.DataFrame,
    clean_water_frame: pd.DataFrame,
    clean_fish_frame: pd.DataFrame,
    excluded_water: pd.DataFrame,
    excluded_fish: pd.DataFrame,
    water_aggregated: pd.DataFrame,
    matched: pd.DataFrame,
    unmatched_fish: pd.DataFrame,
    water_summary: pd.DataFrame,
    fish_summary: pd.DataFrame,
    correlations: pd.DataFrame,
    anova_result: pd.DataFrame,
    chi_square_result: pd.DataFrame,
    chi_square_table: pd.DataFrame,
    water_audit: dict[str, int],
    fish_audit: dict[str, int],
    source_hash: str,
) -> None:
    raw_water.to_csv(OUTPUT_DIR / "water_quality_raw_extracted.csv", index=False)
    raw_fish.to_csv(OUTPUT_DIR / "fish_population_raw_extracted.csv", index=False)
    clean_water_frame.to_csv(OUTPUT_DIR / "water_quality_cleaned.csv", index=False)
    clean_fish_frame.to_csv(OUTPUT_DIR / "fish_population_cleaned.csv", index=False)
    excluded_water.to_csv(OUTPUT_DIR / "water_quality_excluded_records.csv", index=False)
    excluded_fish.to_csv(OUTPUT_DIR / "fish_population_excluded_records.csv", index=False)
    water_aggregated.to_csv(OUTPUT_DIR / "water_quality_site_date_aggregated.csv", index=False)
    matched.to_csv(OUTPUT_DIR / "analysis_merged.csv", index=False)
    unmatched_fish.to_csv(OUTPUT_DIR / "unmatched_fish_records.csv", index=False)
    water_summary.to_csv(OUTPUT_DIR / "water_quality_summary_by_site.csv", index=False)
    fish_summary.to_csv(OUTPUT_DIR / "fish_summary_by_species.csv", index=False)
    correlations.to_csv(OUTPUT_DIR / "correlation_results.csv", index=False)
    anova_result.to_csv(OUTPUT_DIR / "anova_dissolved_oxygen_by_site.csv", index=False)
    chi_square_result.to_csv(OUTPUT_DIR / "chi_square_site_by_origin.csv", index=False)
    chi_square_table.to_csv(OUTPUT_DIR / "chi_square_observed_expected.csv", index=False)

    # Remove outputs from the earlier advanced-model prototype. They are not
    # part of the classroom-aligned final analysis.
    for obsolete_name in ["quasi_poisson_regression.csv", "regression_diagnostics.csv"]:
        (OUTPUT_DIR / obsolete_name).unlink(missing_ok=True)

    plot_do_time_series(water_aggregated, OUTPUT_DIR / "figure1_dissolved_oxygen_by_site.png")
    plot_do_count_by_species(matched, OUTPUT_DIR / "figure2_do_fish_count_by_species.png")

    report = build_report(
        source_hash,
        water_audit,
        fish_audit,
        water_aggregated,
        matched,
        unmatched_fish,
        water_summary,
        fish_summary,
        correlations,
        anova_result,
        chi_square_result,
        chi_square_table,
    )
    (OUTPUT_DIR / "analysis_report.md").write_text(report, encoding="utf-8")


def validate_outputs(
    source_hash_before: str,
    water_audit: dict[str, int],
    fish_audit: dict[str, int],
    water: pd.DataFrame,
    fish: pd.DataFrame,
    matched: pd.DataFrame,
    anova_result: pd.DataFrame,
    chi_square_result: pd.DataFrame,
) -> None:
    assert sha256(SOURCE_FILE) == source_hash_before, "Source workbook changed during analysis"
    assert water_audit == {
        "raw_records": 100,
        "exact_duplicates_removed": 25,
        "records_after_deduplication": 75,
        "records_excluded_after_deduplication": 4,
        "clean_records": 71,
    }
    assert fish_audit == {
        "raw_records": 90,
        "exact_duplicates_removed": 16,
        "records_after_deduplication": 74,
        "records_excluded_after_deduplication": 4,
        "clean_records": 70,
    }
    assert not water.duplicated(WATER_COLUMNS).any()
    assert not fish.duplicated(FISH_COLUMNS).any()
    assert len(matched) == 68
    assert matched[["temperature_c", "ph", "dissolved_oxygen_mg_l", "count", "average_size_cm"]].notna().all().all()
    assert anova_result.iloc[0]["decision"] in ["Reject H0", "Fail to reject H0"]
    assert chi_square_result.iloc[0]["minimum_expected_count"] >= 5
    required_files = [
        "analysis_report.md",
        "analysis_merged.csv",
        "correlation_results.csv",
        "anova_dissolved_oxygen_by_site.csv",
        "chi_square_site_by_origin.csv",
        "figure1_dissolved_oxygen_by_site.png",
        "figure2_do_fish_count_by_species.png",
    ]
    for name in required_files:
        path = OUTPUT_DIR / name
        assert path.exists() and path.stat().st_size > 0, f"Missing output: {name}"


def main() -> None:
    ensure_output_directory()
    source_hash_before = sha256(SOURCE_FILE)
    raw_water, raw_fish = load_source_tables()
    clean_water_frame, excluded_water, water_audit = clean_water(raw_water)
    clean_fish_frame, excluded_fish, fish_audit = clean_fish(raw_fish)
    water_aggregated, matched, unmatched_fish = aggregate_and_merge(
        clean_water_frame, clean_fish_frame
    )
    # Use one aggregated record per site-date for summaries so days with
    # multiple water samples do not receive disproportionate weight.
    water_summary = describe_water_by_site(water_aggregated)
    fish_summary = describe_fish_by_species(matched)
    correlations = build_correlation_results(matched)
    anova_result = one_way_anova_do_by_site(water_aggregated)
    chi_square_result, chi_square_table = chi_square_site_by_origin(matched)

    save_outputs(
        raw_water,
        raw_fish,
        clean_water_frame,
        clean_fish_frame,
        excluded_water,
        excluded_fish,
        water_aggregated,
        matched,
        unmatched_fish,
        water_summary,
        fish_summary,
        correlations,
        anova_result,
        chi_square_result,
        chi_square_table,
        water_audit,
        fish_audit,
        source_hash_before,
    )
    validate_outputs(
        source_hash_before,
        water_audit,
        fish_audit,
        clean_water_frame,
        clean_fish_frame,
        matched,
        anova_result,
        chi_square_result,
    )
    print(f"Analysis complete. Outputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
