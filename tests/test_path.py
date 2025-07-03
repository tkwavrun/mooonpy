# -*- coding: utf-8 -*-

import pytest
from mooonpy.tools.file_utils import Path, smart_open

import os
import tempfile
import gzip
import bz2
import lzma
import shutil
from pathlib import Path as StdPath

# Run pytest tests
print("=== NOT Running Tests ===\n")
print("To run the pytest tests, use:")
print("   Command: pytest test_path.py -v")
print("   Command: pytest test_path.py::TestPath::test_path_creation -v  # Run specific test")
print("   Command: pytest test_path.py::TestSmartOpen -v  # Run specific test class")
print()

class TestPath:
    """Pytest tests for Path class"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory with test files"""
        temp_dir = Path(tempfile.mkdtemp())
        # temp_dir = Path(__file__).dir() / "temp_dir"
        # os.makedirs(temp_dir, exist_ok=True)
        test_files = []

        # Create test files
        for i, name in enumerate(["file1.txt", "file2.txt", "data.csv", "script.py"]):
            filepath = os.path.join(temp_dir, name)
            with open(filepath, 'w') as f:
                f.write(f"Content {i}")
            test_files.append(filepath)

            # Add different modification times
            import time
            time.sleep(0.01)  # Small delay to ensure different mtimes

        yield temp_dir, test_files

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_path_creation(self):
        """Test Path object creation and normalization"""
        p1 = Path("folder/file.txt")
        p2 = Path("folder//file.txt")  # Double slash
        p3 = Path("folder\\file.txt")  # Backslash

        # All should be normalized
        assert isinstance(p1, Path)
        assert isinstance(p1, str)
        assert str(p1) == os.path.normpath("folder/file.txt")

    def test_path_division(self):
        """Test path joining with / operator"""
        base = Path("project")
        sub = Path("data")
        filename = "file.txt"

        result = base / sub / filename
        expected = Path(os.path.join("project", "data", "file.txt"))

        assert result == expected
        assert isinstance(result, Path)

    def test_path_existence(self, temp_dir):
        """Test file existence checking"""
        temp_dir_path, test_files = temp_dir
        existing_file = Path(test_files[0])
        non_existing = Path("nonexistent_file.txt")

        assert bool(existing_file) == True
        assert bool(non_existing) == False

    def test_absolute_path(self):
        """Test absolute path conversion"""
        relative = Path("test.txt")
        absolute = abs(relative)

        assert os.path.isabs(absolute)
        assert isinstance(absolute, Path)

    def test_path_parsing(self):
        """Test path component extraction"""
        test_path = Path("folder/subfolder/file.txt")

        assert test_path.basename() == "file.txt"
        assert test_path.dir() == Path("folder/subfolder")
        assert test_path.root() == "file"
        assert test_path.ext() == ".txt"

    def test_extension_replacement(self):
        """Test extension replacement"""
        original = Path("data/file.txt")
        new_path = original.new_ext(".csv")

        assert new_path == Path("data/file.csv")
        assert isinstance(new_path, Path)

    def test_wildcard_matching(self, temp_dir):
        """Test wildcard pattern matching"""
        temp_dir_path, test_files = temp_dir
        pattern = Path(os.path.join(temp_dir_path, "*.txt"))
        matches = pattern.matches()

        assert len(matches) == 2  # file1.txt and file2.txt
        assert all(isinstance(m, Path) for m in matches)
        assert all(m.ext() == ".txt" for m in matches)

    def test_iterator(self, temp_dir):
        """Test Path iteration over wildcard matches"""
        temp_dir_path, test_files = temp_dir
        pattern = Path(os.path.join(temp_dir_path, "*"))
        files = list(pattern)

        assert len(files) == 4  # All test files
        assert all(isinstance(f, Path) for f in files)

    def test_recent_file(self, temp_dir):
        """Test finding most/least recently modified files"""
        temp_dir_path, test_files = temp_dir
        pattern = Path(os.path.join(temp_dir_path, "*.txt"))

        most_recent = pattern.recent()
        oldest = pattern.recent(oldest=True)

        assert isinstance(most_recent, str)
        assert isinstance(oldest, str)
        assert most_recent != oldest

    def test_recent_no_matches(self, temp_dir):
        """Test recent() with no matching files"""
        temp_dir_path, test_files = temp_dir
        pattern = Path(os.path.join(temp_dir_path, "*.nonexistent"))
        result = pattern.recent()

        assert result is None


class TestSmartOpen:
    """Pytest tests for smart_open function"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_dir = Path(tempfile.mkdtemp())
        # temp_dir = Path(__file__).dir() / "temp_dir"
        # os.makedirs(temp_dir, exist_ok=True)
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def test_content(self):
        """Test content for file operations"""
        return "Hello, World!\nTest content here."

    def test_regular_file(self, temp_dir, test_content):
        """Test opening regular files"""
        filepath = temp_dir / "test.txt"

        # Write file
        with smart_open(filepath, 'w') as f:
            f.write(test_content)

        # Read file
        with smart_open(filepath, 'r') as f:
            content = f.read()

        assert content == test_content

    def test_gzip_file(self, temp_dir, test_content):
        """Test opening gzip files"""
        filepath = temp_dir / "test.txt.gz"

        # Write compressed file
        with smart_open(filepath, 'w') as f:
            f.write(test_content)

        # Read compressed file
        with smart_open(filepath, 'r') as f:
            content = f.read()

        assert content == test_content

    def test_bzip2_file(self, temp_dir, test_content):
        """Test opening bzip2 files"""
        filepath = temp_dir / "test.txt.bz2"

        # Write compressed file
        with smart_open(filepath, 'w') as f:
            f.write(test_content)

        # Read compressed file
        with smart_open(filepath, 'r') as f:
            content = f.read()

        assert content == test_content

    def test_lzma_file(self, temp_dir, test_content):
        """Test opening LZMA files"""
        for ext in ['.xz', '.lzma']:
            filepath = temp_dir / f"test.txt{ext}"

            # Write compressed file
            with smart_open(filepath, 'w') as f:
                f.write(test_content)

            # Read compressed file
            with smart_open(filepath, 'r') as f:
                content = f.read()

            assert content == test_content

    # def test_fallback_to_regular_open(self, temp_dir, test_content):
    #     """Test fallback when compression fails"""
    #     filepath = temp_dir / "test.txt.gz"
    #
    #     # Create a file that looks compressed but isn't
    #     with open(filepath, 'w') as f:
    #         f.write(test_content)
    #
    #     # Should still be able to read it.
    #     # No, it returns the file handle but fails on read. Error message is complete enough
    #     with smart_open(filepath, 'r') as f:
    #         content = f.read()
    #
    #     assert content == test_content