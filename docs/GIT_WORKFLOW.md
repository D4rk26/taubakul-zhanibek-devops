# Git workflow

This project uses two long-lived branches for the laboratory demonstration:

- `main` contains the reviewed and integrated state.
- `development` isolates a meaningful change before it is merged.

## Typical sequence

```bash
git switch development
git status
git add -- <specific-files>
git diff --cached --check
git commit -m "docs: describe the change"
git switch main
git merge --no-ff development
```

Files are staged explicitly so generated logs, backups, local environment files, and credentials are not accidentally committed. Before a push, inspect `git status`, the staged or outgoing diff, and the commits being sent. Force push and history rewriting are intentionally excluded from this workflow.

## Verification

```bash
git branch --verbose
git log --oneline --graph --all --decorate
git status
```

A branch lets work proceed independently from the integrated branch. A normal merge combines the development history with `main`; an explicit non-fast-forward merge also leaves a visible integration point for the laboratory demonstration.
