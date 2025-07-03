# -*- coding: utf-8 -*-
"""
Examples and tests for the Path class and smart_open function.
This file demonstrates usage patterns and provides comprehensive test coverage.
"""

import os
import tempfile
import gzip
import bz2
import lzma
import pytest
import shutil
from pathlib import Path as StdPath

# from mooonpy import Path
from mooonpy.tools.file_utils import smart_open, Path

def examples():
    """
    Comprehensive examples showing Path class usage
    """
    print("=== Path Class Examples ===\n")

    # 1. Basic path operations
    print("-- Basic Path Operations --")
    print(">>> project_path = Path('Project/Data/Analysis')")
    project_path = Path("Project/Data/Analysis")
    print(">>> filename = Path('results.txt')")
    filename = Path("results.txt")
    print(">>> full_path = project_path / filename")
    full_path = project_path / filename
    print(">>> print(full_path)")
    print(full_path)
    print(">>> print(abs(full_path))")
    print(abs(full_path))
    print()

    # 2. Path parsing
    print("-- Path Parsing --")
    print(">>> sample_path = Path('experiments/run_001/data.csv.gz')")
    sample_path = Path("experiments/run_001/data.csv.gz")
    print(">>> print(sample_path.dir())")
    print(sample_path.dir())
    print(">>> print(sample_path.basename())")
    print(sample_path.basename())
    print(">>> print(sample_path.root())")
    print(sample_path.root())
    print(">>> print(sample_path.ext())")
    print(sample_path.ext())
    print()

    # 3. Extension manipulation
    print("-- Extension Manipulation --")
    print(">>> data_file = Path('analysis/results.txt')")
    data_file = Path("analysis/results.txt")
    print(">>> print(data_file.new_ext('.json'))")
    print(data_file.new_ext('.json'))
    print(">>> print(data_file.new_ext('.txt.gz'))")
    print(data_file.new_ext('.txt.gz'))
    print()

    # 4. File existence checking
    print("-- File Existence --")
    print(">>> current_file = Path(__file__)")
    current_file = Path(__file__)
    print(">>> fake_file = Path('nonexistent.txt')")
    fake_file = Path("nonexistent.txt")
    print(">>> print(bool(current_file))")
    print(bool(current_file))
    print(">>> print(bool(fake_file))")
    print(bool(fake_file))
    print()

    # 5. Working with temporary files for wildcard examples
    print("-- Wildcard Matching --")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files
        test_files = ["test1.txt", "test2.txt", "data.csv", "readme.md"]
        for fname in test_files:
            temp_path = os.path.join(temp_dir, fname)
            with open(temp_path, 'w') as f:
                f.write("test content")

        # Test wildcard matching
        txt_pattern = Path(os.path.join(temp_dir, "*.txt"))
        all_pattern = Path(os.path.join(temp_dir, "*"))

        print(">>> txt_pattern = Path('temp_dir/*.txt')")
        print(">>> print(txt_pattern.matches())")
        matches = txt_pattern.matches()
        print([os.path.basename(f) for f in matches])
        print(">>> for file in all_pattern:")
        print("...     print(file.basename())")
        for file in all_pattern:
            print(file.basename())
    print()

    # 6. Recent file finding
    print("-- Recent File Finding --")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files with different timestamps
        import time
        files = ["old_file.txt", "newer_file.txt", "newest_file.txt"]
        for i, fname in enumerate(files):
            temp_path = os.path.join(temp_dir, fname)
            with open(temp_path, 'w') as f:
                f.write(f"content {i}")
            time.sleep(0.1)  # Small delay to ensure different timestamps

        pattern = Path(os.path.join(temp_dir, "*.txt"))
        print(">>> pattern = Path('temp_dir/*.txt')")
        print(">>> print(pattern.recent())")
        recent = pattern.recent()
        if recent:
            print(os.path.basename(recent))
        print(">>> print(pattern.recent(oldest=True))")
        oldest = pattern.recent(oldest=True)
        if oldest:
            print(os.path.basename(oldest))
    print()

    # 7. Smart file opening
    print("-- Smart File Opening --")
    print(">>> mypath = Path('data.txt')")
    mypath = Path('data.txt')
    print(">>> with mypath.open('w') as f:")
    print("...     f.write('Hello World')")
    # Note: This would write to a file, showing the concept
    print("# Creates regular file")
    print(">>> compressed_path = Path('data.txt.gz')")
    compressed_path = Path('data.txt.gz')
    print(">>> # compressed_path.open() would use gzip automatically")
    print("# Would automatically handle gzip compression")
    print()

    # 8. Absolute path conversion
    print("-- Absolute Path Conversion --")
    print(">>> rel_path = Path('data/file.txt')")
    rel_path = Path('data/file.txt')
    print(">>> print(abs(rel_path))")
    print(abs(rel_path))
    print()


def test_smart_open_examples():
    """
    Examples of smart_open functionality
    """
    print("=== Smart Open Examples ===\n")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files with different compressions
        test_data = "Hello, World!\nThis is test data.\n"

        # Regular file
        regular_file = os.path.join(temp_dir, "test.txt")
        with open(regular_file, 'w') as f:
            f.write(test_data)

        # Gzip file
        gz_file = os.path.join(temp_dir, "test.txt.gz")
        with gzip.open(gz_file, 'wt') as f:
            f.write(test_data)

        # Bzip2 file
        bz2_file = os.path.join(temp_dir, "test.txt.bz2")
        with bz2.open(bz2_file, 'wt') as f:
            f.write(test_data)

        # LZMA file
        lzma_file = os.path.join(temp_dir, "test.txt.xz")
        with lzma.open(lzma_file, 'wt') as f:
            f.write(test_data)

        # Test reading with smart_open
        print("1. Reading different file types:")
        for filepath in [regular_file, gz_file, bz2_file, lzma_file]:
            print(f"   Command: smart_open('{os.path.basename(filepath)}')")
            with smart_open(filepath) as f:
                content = f.read().strip()
                print(f"   {os.path.basename(filepath)}: {content.split()[0]}...")
        print()

        # Test Path.open() method
        print("2. Using Path.open() method:")
        path_obj = Path(gz_file)
        print(f"   Command: path_obj = Path('{os.path.basename(gz_file)}')")
        print("   Command: path_obj.open()")
        with path_obj.open() as f:
            content = f.read()
            print(f"   Content from {path_obj.basename()}: {len(content)} characters")
        print()

if __name__ == "__main__":
    """Run all examples and tests"""
    print("Running Path class examples...\n")

    # Run examples
    examples()
    test_smart_open_examples()

    os.system("pause")  ## Keep popup open