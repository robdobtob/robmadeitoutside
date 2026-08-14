

## Setup
Need to have ruby installed and configured
https://jekyllrb.com/docs/installation/macos/

```
brew install jekyll bundler
```

## Book reviews

Regenerate `_data/books.yml` from the Obsidian vault (run from repo root):

```
uv run --script scripts/parse_books.py
```