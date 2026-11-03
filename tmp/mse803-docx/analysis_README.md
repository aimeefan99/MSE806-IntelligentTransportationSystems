# Assessment 1 Task 1 Analysis

This folder contains the reproducible analysis for the Avon River dataset.
The source workbook is read without being modified.

## Run

From the repository root:

```bash
python Assessment/analysis/assessment1_analysis.py
```

Install the packages in `requirements.txt` in an isolated environment when
they are not already available. Generated CSV files, the analysis report, and
the two figures are written to `outputs/`.

## Method

The workflow follows the course exercises:

1. extract and inspect the two source tables;
2. audit exact duplicates, missing values, dates, and implausible values;
3. preserve excluded records with explicit reasons;
4. aggregate distinct water-quality replicates by site and date;
5. merge water quality with species-level fish observations;
6. calculate descriptive statistics and Pearson correlations;
7. perform a one-way ANOVA and chi-square test using the classroom hypothesis-testing sequence; and
8. generate two static, colourblind-safe figures.

The statistical outputs describe observational associations. They do not
establish that water quality caused differences in fish populations.
