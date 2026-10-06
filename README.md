# Causal Inference Study

A learning repository for understanding causal inference through Python experiments.
Daily notes live in `docs/`, and experiment code lives in `src/`.
MkDocs Material builds the notes into a website hosted on GitHub Pages.

## Getting started

Install uv using the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/),
then run these commands from the repository root. Python 3.12 is pinned in `.python-version`.

```bash
uv sync --locked
uv run mkdocs serve
```

`uv sync` creates `.venv` and installs the experiment, documentation, and development dependencies.
Preview the notes at <http://127.0.0.1:8000>.
Commit `uv.lock` alongside `pyproject.toml` to keep dependency versions reproducible.

## JupyterLab

Register the project kernel and start JupyterLab from the repository root:

```bash
uv run python -m ipykernel install --sys-prefix --name causal-learning --display-name "Python (Causal .venv)" --env VIRTUAL_ENV "$PWD/.venv"
uv run jupyter lab
```

Register the kernel when setting up the project for the first time or after recreating `.venv`.
In the Launcher, select **Python (Causal .venv)** to create a notebook using the project's
NumPy, pandas, and Matplotlib installation.
For an existing notebook, select **Kernel → Change Kernel → Python (Causal .venv)**.
Run `import sys; print(sys.executable)` in a notebook to check the kernel's Python path.

Save notebooks alongside the experiment code in `src/day_XX_topic/`.
To stop JupyterLab, press `Ctrl+C` in its terminal and confirm shutdown.

JupyterLab and `ipykernel` are development dependencies, so `uv sync --locked`
also installs them on another machine.
See the [uv and Jupyter guide](https://docs.astral.sh/uv/guides/integration/jupyter/).

## Project structure

```text
.
├── docs/
│   ├── index.md                   # Study index
│   ├── guide.md                   # Writing guide
│   ├── day-01/index.md            # Average treatment effect
│   ├── day-02/index.md            # Confounding and stratification
│   └── assets/javascripts/        # Math rendering configuration
├── src/
│   ├── day_01_ate/
│   │   └── simulate_ate.py
│   └── day_02_confounder/
│       └── confounder.py
├── templates/
│   └── day.md                    # Template for new study notes
├── .github/workflows/pages.yml   # Documentation build and deployment
├── .python-version
├── mkdocs.yml
├── pyproject.toml
└── uv.lock
```

Use `day-01` for documentation folders and `day_01_ate` for Python experiment folders.
The root `main.py` is the initial sample; learning experiments live in `src/`.

## Study notes

- [Day 01 · ATE](docs/day-01/index.md): estimate an average treatment effect in a randomized experiment.
- [Day 02 · Confounding and Stratification](docs/day-02/index.md): compare outcomes within confounder strata and combine the estimates.

## Adding another day

```bash
mkdir -p docs/day-03 src/day_03_topic
cp templates/day.md docs/day-03/index.md
```

1. Write the notes in `docs/day-03/index.md`.
2. Add the experiment scripts to `src/day_03_topic/`.
3. Add the page under `nav → Study notes` in `mkdocs.yml`.
4. Add its link to the study index in `docs/index.md`.

See the [writing guide](docs/guide.md) for the note format.

## Validation

```bash
uv run ruff check src
uv run ruff format --check src
uv run mkdocs build --strict
```

Run each experiment you change and check that its documented results match the output.

## GitHub Pages deployment

1. Push the changes to the repository's `main` branch.
2. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**.
3. For the first deployment, select `main` under **Actions → Build and deploy docs → Run workflow**.

After setup, each push to `main` builds and deploys the notes. Pull requests only run validation.
The published site is <https://karim-moon.github.io/Causal/>.

References: [uv with GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/),
[GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
