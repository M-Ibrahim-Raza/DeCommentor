#!/usr/bin/env python3
"""
Python Comment and Docstring Remover
Removes comments, docstrings, and inline comments from Python files.
"""

import ast
import argparse
import os
import sys
from pathlib import Path
from typing import List, Set


class CommentDocstringRemover(ast.NodeTransformer):
    """AST transformer to remove docstrings from Python code."""
    
    def visit_Module(self, node):
        # Remove module-level docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            node.body = node.body[1:]
        self.generic_visit(node)
        return node
    
    def visit_FunctionDef(self, node):
        # Remove function docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            node.body = node.body[1:]
        self.generic_visit(node)
        return node
    
    def visit_AsyncFunctionDef(self, node):
        # Remove async function docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            node.body = node.body[1:]
        self.generic_visit(node)
        return node
    
    def visit_ClassDef(self, node):
        # Remove class docstring
        if (node.body and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            node.body = node.body[1:]
        self.generic_visit(node)
        return node


def remove_comments_and_docstrings(source_code: str) -> str:
    """
    Remove comments, docstrings, and inline comments from Python source code.
    
    Args:
        source_code: Python source code as string
        
    Returns:
        Cleaned source code without comments and docstrings
    """
    try:
        # Parse the source code into AST
        tree = ast.parse(source_code)
        
        # Remove docstrings using AST transformer
        transformer = CommentDocstringRemover()
        tree = transformer.visit(tree)
        
        # Unparse back to source code
        cleaned_code = ast.unparse(tree)
        
        # Remove inline and standalone comments
        lines = []
        for line in cleaned_code.split('\n'):
            # Check if line has a comment
            if '#' in line:
                # Handle string literals that might contain #
                in_string = False
                quote_char = None
                escaped = False
                comment_pos = -1
                
                for i, char in enumerate(line):
                    if escaped:
                        escaped = False
                        continue
                    
                    if char == '\\':
                        escaped = True
                        continue
                    
                    if char in ('"', "'") and not in_string:
                        in_string = True
                        quote_char = char
                    elif char == quote_char and in_string:
                        in_string = False
                        quote_char = None
                    elif char == '#' and not in_string:
                        comment_pos = i
                        break
                
                if comment_pos >= 0:
                    line = line[:comment_pos].rstrip()
            
            # Only add non-empty lines or lines with meaningful content
            if line.strip():
                lines.append(line)
        
        return '\n'.join(lines)
    
    except SyntaxError as e:
        print(f"Syntax error in file: {e}")
        return source_code


def should_ignore_path(path: Path, ignore_dirs: Set[str]) -> bool:
    """
    Check if a path should be ignored based on ignore directories.
    
    Args:
        path: Path to check
        ignore_dirs: Set of directory names to ignore
        
    Returns:
        True if path should be ignored, False otherwise
    """
    parts = path.parts
    for part in parts:
        if part in ignore_dirs:
            return True
    return False


def process_file(file_path: Path, output_dir: Path = None, in_place: bool = False) -> bool:
    """
    Process a single Python file to remove comments and docstrings.
    
    Args:
        file_path: Path to the Python file
        output_dir: Output directory for cleaned files
        in_place: If True, modify files in place
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        cleaned_code = remove_comments_and_docstrings(source_code)
        
        if in_place:
            output_path = file_path
        else:
            if output_dir:
                relative_path = file_path.relative_to(file_path.parents[len(file_path.parents) - 1])
                output_path = output_dir / relative_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = file_path.with_suffix('.cleaned.py')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_code)
        
        print(f"Processed: {file_path}")
        return True
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def process_directory(
    directory: Path,
    ignore_dirs: Set[str],
    output_dir: Path = None,
    in_place: bool = False
) -> tuple:
    """
    Process all Python files in a directory recursively.
    
    Args:
        directory: Root directory to process
        ignore_dirs: Set of directory names to ignore
        output_dir: Output directory for cleaned files
        in_place: If True, modify files in place
        
    Returns:
        Tuple of (successful_count, failed_count)
    """
    success_count = 0
    fail_count = 0
    
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        
        # Remove ignored directories from traversal
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        if should_ignore_path(root_path, ignore_dirs):
            continue
        
        for file in files:
            if file.endswith('.py'):
                file_path = root_path / file
                
                if process_file(file_path, output_dir, in_place):
                    success_count += 1
                else:
                    fail_count += 1
    
    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(
        description='Remove comments, docstrings, and inline comments from Python files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single file (creates .cleaned.py)
  python script.py input.py
  
  # Process directory with output directory
  python script.py project/ -o cleaned_project/
  
  # Process in-place (modifies original files)
  python script.py project/ --in-place
  
  # Ignore specific directories
  python script.py project/ --ignore tests venv __pycache__
        """
    )
    
    parser.add_argument(
        'path',
        type=str,
        help='Path to Python file or directory to process'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output directory for cleaned files (default: creates .cleaned.py files)'
    )
    
    parser.add_argument(
        '-i', '--in-place',
        action='store_true',
        help='Modify files in place (WARNING: overwrites original files)'
    )
    
    parser.add_argument(
        '--ignore',
        nargs='+',
        default=['venv', '__pycache__', '.git', '.tox', 'node_modules', '.pytest_cache'],
        help='Directory names to ignore (default: venv __pycache__ .git .tox node_modules .pytest_cache)'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.path)
    output_dir = Path(args.output) if args.output else None
    ignore_dirs = set(args.ignore)
    
    if not input_path.exists():
        print(f"Error: Path '{input_path}' does not exist")
        sys.exit(1)
    
    if args.in_place and args.output:
        print("Error: Cannot use both --in-place and --output")
        sys.exit(1)
    
    if args.in_place:
        response = input("WARNING: This will modify files in place. Continue? (yes/no): ")
        if response.lower() not in ('yes', 'y'):
            print("Aborted.")
            sys.exit(0)
    
    print(f"Ignoring directories: {', '.join(sorted(ignore_dirs))}")
    print()
    
    if input_path.is_file():
        if input_path.suffix != '.py':
            print("Error: File must be a Python file (.py)")
            sys.exit(1)
        
        success = process_file(input_path, output_dir, args.in_place)
        if success:
            print("\nSuccessfully processed 1 file")
        else:
            print("\nFailed to process file")
            sys.exit(1)
    
    elif input_path.is_dir():
        print(f"Processing directory: {input_path}")
        success_count, fail_count = process_directory(
            input_path,
            ignore_dirs,
            output_dir,
            args.in_place
        )
        
        print(f"\nCompleted:")
        print(f"  Successfully processed: {success_count} files")
        print(f"  Failed: {fail_count} files")
        
        if fail_count > 0:
            sys.exit(1)
    
    else:
        print(f"Error: '{input_path}' is neither a file nor directory")
        sys.exit(1)


if __name__ == '__main__':
    main()