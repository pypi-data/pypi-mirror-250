# gitaddnb

If you want to add a Jupyter Notebook to the git stage:

- ensuring all code cells ran consecutively
- without outputs
- without execution order
- leave the cell outputs on disk as is

## Pre-Commit

You can use this repository as a [pre-commit](https://pre-commit.com/) hook:

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

```bash
pipx install gitaddnb
```

### Usage

```bash
gitaddnb notebook1.ipynb notebook2.ipynb
```
