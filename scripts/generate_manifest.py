"""Build the public image list; no external packages required."""
import argparse
import json
from pathlib import Path
import re

ENTRY = re.compile(r'(male|female)/(wood|fire|earth|metal|water)_\d+\.png')
REPO = Path(__file__).resolve().parents[1]


def generate(root, exclusion_file):
    excluded = json.loads(exclusion_file.read_text(encoding='utf-8'))
    if not isinstance(excluded, list) or any(not isinstance(item, str) or not ENTRY.fullmatch(item) for item in excluded):
        raise ValueError('exclusions must be a list of valid image paths')
    images = sorted({
        file.relative_to(root).as_posix()
        for gender in ('male', 'female')
        for file in (root / gender).glob('*.png')
        if file.is_file() and not file.is_symlink()
        and ENTRY.fullmatch(file.relative_to(root).as_posix())
        and file.relative_to(root).as_posix() not in excluded
    })
    content = json.dumps({'version': 1, 'images': images}, indent=2) + '\n'
    output = root / 'manifest.json'
    changed = not output.exists() or output.read_text(encoding='utf-8') != content
    if changed:
        output.write_text(content, encoding='utf-8')
    return len(images), changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=REPO / 'public/match_images')
    parser.add_argument('--exclude', type=Path, default=REPO / 'scripts/excluded_images.json')
    args = parser.parse_args()
    count, changed = generate(args.root, args.exclude)
    print(f'images={count} changed={str(changed).lower()}')
