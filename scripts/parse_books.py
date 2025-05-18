#!/usr/bin/env python3

import os
import yaml
import re
from datetime import datetime
from pathlib import Path

class BookReviewParser:
    def __init__(self, vault_path):
        self.vault_path = vault_path;
        self.books = []

    def parse_book_review(self, file_path):
        """Parse a single book review file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter if it exists
        frontmatter = {}
        if content.startswith('---'):
            _, frontmatter_str, content = content.split('---', 2)
            try:
                frontmatter = yaml.safe_load(frontmatter_str)
            except yaml.YAMLError:
                print(f"Warning: Could not parse frontmatter in {file_path}")

        # Extract book information
        title = f.name.split('/')[-1].removesuffix(".md")
        completed = frontmatter.get('completed', '')
        started = frontmatter.get('started', '')
        review_created = datetime.fromtimestamp(os.path.getctime(file_path)) 
        date_read = (completed or started or review_created).strftime('%Y-%m-%d')
        review = content.split('# Review')[1].split('\n\n')[0].strip()  if '# Review' in content else ''
        book_info = {
            'title': title,
            'author': frontmatter.get('author', ''),
            'date_read': date_read,
            'rating': frontmatter.get('rating', 0),
            'review': review,
            'ideas': frontmatter.get('ideas', []),
            'genre': frontmatter.get('genre', [])
        }

        return book_info

    def find_book_reviews(self):
        """Find all book review files in the Books/Reviews directory."""
        reviews_path = self.vault_path / 'Books' / 'Reviews'
        if not reviews_path.exists():
            return []
        return list(reviews_path.glob('**/*.md'))

    def generate_yaml(self, output_path):
        """Generate YAML file from book reviews."""
        book_files = self.find_book_reviews()
        
        for file_path in book_files:
            try:
                book_info = self.parse_book_review(file_path)
                if book_info['title']:  # Only add if we have at least a title
                    self.books.append(book_info)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        # Sort books by date_read (most recent first)
        self.books.sort(key=lambda x: x.get('date_read', ''), reverse=True)

        # Write to YAML file
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.books, f, allow_unicode=True, sort_keys=False, width=float('inf'))

def main():
    # Get Obsidian vault path from environment variable or use default
    # vault_path = os.getenv('OBSIDIAN_VAULT_PATH', os.path.expanduser('~/Documents/Obsidian'))
    vault_path = Path("/Users/robrob/Library/Mobile Documents/iCloud~md~obsidian/Documents/Spaghetti/")
    
    # Output path for the YAML file
    output_path = Path('.') / '_data' / 'books.yml'
    
    # Create _data directory if it doesn't exist
    output_path.parent.mkdir(exist_ok=True)
    
    parser = BookReviewParser(vault_path)
    parser.generate_yaml(output_path)
    print(f"Generated book reviews YAML at: {output_path}")

if __name__ == '__main__':
    main() 