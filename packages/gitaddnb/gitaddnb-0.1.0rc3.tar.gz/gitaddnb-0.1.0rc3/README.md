# gitaddnb

If you want to add a Jupyter Notebook to the git stage ensuring that:

- all code cells have consecutive execution order
- all code cell outputs are clean
- all code cell execution orders are clean
- **all cell outputs on disk remain untouched**

then this package is for you.

## Pre-Commit

You can use this package as a [pre-commit](https://pre-commit.com/) hook:

```yaml
repos:
  - repo: https://github.com/pcjedi/gitaddnb
    rev: v0.1.0
    hooks:
      - id: gitaddnb
```

On the first Commit Attempt, this hook will fail due to changing the content of the staged Notebooks. The second try should then go through.

## CLI

### Installation

Install this package using pipx or pip. It comes without any dependencies.

```bash
pipx install gitaddnb
```

### Usage

After installation, add notebooks like this:

```bash
gitaddnb notebook1.ipynb notebook2.ipynb
```

The notebooks will now be in the git stage, cleaned. The files in the working directory will still have your output.
