"""Read-only workspace checks; run from any directory with Python's standard library."""

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
DIRECTORIES = (
    'src', 'tests', 'docs', 'scripts', 'memory', 'skills', 'data/raw/private',
    'outputs', 'logs', 'notebooks', 'notebooks/reference', 'docs/references/private', 'labs',
)
REQUIRED_FILES = (
    'README.md', 'AGENTS.md', 'PLAN.md', '.gitignore', 'docs/project-brief.md',
    'memory/README.md', 'memory/decisions.md', 'memory/course-baseline.md',
    'memory/data-audit.md', 'skills/README.md',
    'data/raw/private/student_data.csv', 'notebooks/datamining1.ipynb',
    'notebooks/reference/datamining1.ipynb',
    'docs/references/private/Project_DMI_2026_2027.pdf',
    'docs/references/private/Missing Values Analyses.docx',
)
IGNORE_ENTRIES = (
    '.env', '.env.*', '!.env.example', '__pycache__/', '*.pyc', '.venv/',
    'node_modules/', '.DS_Store', 'logs/*.log', 'data/raw/private/', '*.sqlite3',
    '.ipynb_checkpoints/', '/docs/references/private/', '/labs/', '/outputs/',
)


def main():
    problems = []
    for relative in DIRECTORIES:
        if not (ROOT / relative).is_dir():
            problems.append(f'Missing directory: {relative}')
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            problems.append(f'Missing file: {relative}')
    ignore = ROOT / '.gitignore'
    rules = set(ignore.read_text(encoding='utf-8').splitlines()) if ignore.exists() else set()
    for entry in IGNORE_ENTRIES:
        if entry not in rules:
            problems.append(f'Missing ignore entry: {entry}')
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if path.suffix != '.md' or not path.exists():
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            destination = path.parent / target.split('#', 1)[0]
            if not destination.exists():
                problems.append(f'Broken link in {relative}: {target}')
    originals = [ROOT / path for path in (
        'notebooks/datamining1.ipynb', 'notebooks/reference/datamining1.ipynb',
    )]
    expected = 'a6eaac9fed21f86808f15ff7ad4f0f4fbcb9e01f10100821bfb22edd54d9710f'
    for path in originals:
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            problems.append(f'Protected original changed: {path.relative_to(ROOT)}')
    if problems:
        print('\n'.join(problems))
        return 1
    print('PASS: workspace folders, required files, document links, minimum ignore entries, and original notebooks.')
    print('Notebook execution, environments, analysis correctness, and current Git tracking were not tested.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
