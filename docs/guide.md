# Writing Guide

## Folder conventions

Keep each day's notes and figures in `docs/day-XX/`.
Keep its experiment scripts and notebooks in `src/day_XX_topic/`.

```text
docs/day-04/
├── index.md
└── figures/
    └── result.png

src/day_04_topic/
└── experiment.py
```

Link a figure from the notes using a relative path such as `![Experiment result](figures/result.png)`.
Store figures intended for publication in that day's `figures/` folder.
Store temporary experiment output in the root `outputs/` folder, which Git ignores.

For a causal DAG, include every direct relationship in the generating model,
label the treatment, outcome, confounders, and mediators, and explain which paths
the adjustment set blocks. SVG figures stay sharp on the website and in GitHub previews.
See [Day 03](day-03/index.md) for an example.

## Creating another day's notes

```bash
mkdir -p docs/day-04 src/day_04_topic
cp templates/day.md docs/day-04/index.md
```

Replace the template's day number and title, and add the experiment script.
Register the page in `mkdocs.yml`, using the same indentation as the existing days:

```yaml
nav:
  - Home: index.md
  - Study notes:
      - Day 01 · ATE: day-01/index.md
      - Day 02 · Confounding and Stratification: day-02/index.md
      - Day 03 · DAGs and Backdoor Adjustment: day-03/index.md
      - Day 04 · Your topic: day-04/index.md
  - Writing guide: guide.md
```

Add a link to the table in `docs/index.md`.
Use GitHub code URLs when linking to experiment scripts from the published notes.
The documentation website includes `docs/`; it does not include `src/`,
so links such as `../../src/...` will not work there.

## Note format

Write each note in this order: **Today's question → Key concepts → Python experiment → Interpreting the results → Open questions**.

Distinguish the observed results, the assumptions needed for a causal interpretation,
and the questions that remain.
Record the books, papers, or lectures you used, including the relevant sections.

Use `$Y(1)$` for inline math and `$$ ... $$` for display math.
Specify a language when writing fenced code blocks.

## Checking and publishing

```bash
uv run mkdocs serve
uv run mkdocs build --strict
uv run ruff check src
uv run ruff format --check src
```

Run the relevant Python experiments before committing.
After GitHub Pages is configured, a push to `main` updates the website.
