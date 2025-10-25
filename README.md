# Decommentor

A Python utility to clean Python source code by removing comments, docstrings, and type hints.

## Overview

Decommentor provides two variants for cleaning Python code:

- **decommentor_1**: Removes comments and docstrings only
- **decommentor_2**: Removes comments, docstrings, AND type hints

Both tools process individual files or entire directory trees, with flexible options for output and selective file/directory exclusion.

## Features

### decommentor_1

- ✅ Removes module-level docstrings
- ✅ Removes class docstrings
- ✅ Removes function/method docstrings
- ✅ Removes inline comments (`# comment`)
- ✅ Removes standalone comment lines
- ✅ Preserves code functionality

### decommentor_2 (All features of decommentor_1, plus:)

- ✅ Removes function return type hints (`-> Type`)
- ✅ Removes function parameter type hints (`param: Type`)
- ✅ Removes variable type annotations (`var: Type = value`)
- ✅ Removes type-only annotations (`var: Type`)

### Common Features

- 🔄 Process single files or entire directories recursively
- 📁 Ignore specific directories (venv, **pycache**, etc.)
- 📄 Ignore specific files or file patterns (wildcards supported)
- 💾 In-place modification or create cleaned copies
- 🎯 Custom output directory support
- ⚡ Batch processing with progress reporting

## Installation

No external dependencies required! Uses only Python standard library.

**Requirements:**

- Python 3.9 or higher (for `ast.unparse()`)

**Setup:**

```bash
# Clone or download the scripts
git clone <repository-url>
cd decommentor

# Make scripts executable (optional)
chmod +x decommentor_1.py
chmod +x decommentor_2.py
```

## Usage

### Basic Usage

```bash
# Process a single file (creates .cleaned.py)
python decommentor_1.py input.py
python decommentor_2.py input.py

# Process entire directory
python decommentor_1.py my_project/
python decommentor_2.py my_project/
```

### Output Options

```bash
# Create cleaned copies in a specific output directory
python decommentor_1.py my_project/ -o cleaned_project/
python decommentor_2.py my_project/ -o cleaned_project/

# Modify files in-place (WARNING: overwrites originals)
python decommentor_1.py my_project/ --in-place
python decommentor_2.py my_project/ --in-place
```

### Ignoring Files and Directories

```bash
# Ignore specific directories
python decommentor_1.py project/ --ignore tests venv __pycache__ docs

# Ignore specific file patterns
python decommentor_2.py project/ --ignore-files __init__.py setup.py test_*.py

# Combine both
python decommentor_2.py project/ \
  --ignore tests venv \
  --ignore-files __init__.py *_pb2.py test_*.py
```

### Command-Line Options

| Option           | Short | Description                                            |
| ---------------- | ----- | ------------------------------------------------------ |
| `path`           | -     | Path to Python file or directory to process (required) |
| `--output`       | `-o`  | Output directory for cleaned files                     |
| `--in-place`     | `-i`  | Modify files in place (overwrites originals)           |
| `--ignore`       | -     | Directory names to ignore (space-separated)            |
| `--ignore-files` | -     | File patterns to ignore (supports wildcards)           |

**Default ignored directories:**

- `venv`
- `__pycache__`
- `.git`
- `.tox`
- `node_modules`
- `.pytest_cache`

## Examples

### Example 1: Clean a Single File

**Input file (`example.py`):**

```python
"""Module for calculations."""

from typing import List

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b  # Return sum

numbers: List[int] = [1, 2, 3]
```

**Command:**

```bash
python decommentor_1.py example.py
```

**Output (`example.cleaned.py`):**

```python
from typing import List

def add(a: int, b: int) -> int:
    return a + b

numbers: List[int] = [1, 2, 3]
```

**Command:**

```bash
python decommentor_2.py example.py
```

**Output (`example.cleaned.py`):**

```python
from typing import List

def add(a, b):
    return a + b

numbers = [1, 2, 3]
```

### Example 2: Process Project Directory

```bash
# Clean entire project, output to new directory
python decommentor_2.py ./my_project -o ./my_project_cleaned

# Clean project, ignore tests and __init__.py files
python decommentor_2.py ./my_project \
  -o ./my_project_cleaned \
  --ignore tests docs \
  --ignore-files __init__.py
```

### Example 3: In-Place Modification

```bash
# WARNING: This overwrites original files!
python decommentor_2.py ./my_project --in-place
```

The script will prompt for confirmation:

```
WARNING: This will modify files in place. Continue? (yes/no):
```

## Use Cases

### 1. Code Obfuscation

Remove documentation and type hints before distributing code where you want to minimize information exposure.

### 2. Size Reduction

Reduce file size for deployment in constrained environments.

### 3. Legacy Compatibility

Remove type hints for compatibility with older Python versions or tools that don't support them.

### 4. Educational Purposes

Create "skeleton" code for students to document themselves.

### 5. Code Analysis

Remove comments to focus purely on code structure during analysis.

## File Patterns (Wildcards)

The `--ignore-files` option supports Unix shell-style wildcards:

| Pattern       | Matches                         |
| ------------- | ------------------------------- |
| `*.py`        | All Python files                |
| `test_*.py`   | Files starting with "test\_"    |
| `*_test.py`   | Files ending with "\_test.py"   |
| `__init__.py` | Exact filename match            |
| `*_pb2.py`    | Protocol buffer generated files |
| `*config*.py` | Files containing "config"       |

## Error Handling

- **Syntax errors:** Files with syntax errors are skipped and reported
- **Missing files:** Non-existent paths are caught and reported
- **Permission errors:** Files without read/write permissions are skipped
- **Encoding issues:** Assumes UTF-8 encoding; other encodings may cause errors

## Limitations

1. **Preserves imports:** Type hint imports (e.g., `from typing import List`) are NOT removed
2. **String literals:** Comments inside strings (e.g., `"# not a comment"`) are preserved correctly
3. **Python version:** Requires Python 3.9+ for `ast.unparse()`
4. **Formatting:** Output formatting may differ from original (uses `ast.unparse()` formatting)

## Project Structure

```
decommentor/
├── README.md
├── decommentor_1.py    # Removes comments and docstrings
└── decommentor_2.py    # Removes comments, docstrings, and type hints
```

## Contributing

Contributions are welcome! Areas for improvement:

- Support for preserving specific docstrings (e.g., `__doc__`)
- Option to also remove type hint imports
- Support for stub files (`.pyi`)
- Custom formatting options
- Configuration file support

## Safety Tips

1. **Always backup your code** before using `--in-place`
2. **Test on a small subset** before processing large projects
3. **Use version control** (Git) to easily revert changes
4. **Review output** before deploying cleaned code
5. **Keep original files** when unsure - use output directory instead of in-place

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the project repository.

---
