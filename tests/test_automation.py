"""Tests for automation utilities."""
import shutil
import tempfile
import unittest
from pathlib import Path

from automation.backup import create_backup
from automation.file_organizer import organize


class TestBackup(unittest.TestCase):
    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()
        # Create some test files
        Path(self.source_dir, "file1.txt").write_text("test content")
        Path(self.source_dir, "file2.txt").write_text("more content")
    
    def tearDown(self):
        shutil.rmtree(self.source_dir, ignore_errors=True)
        shutil.rmtree(self.dest_dir, ignore_errors=True)
    
    def test_create_backup(self):
        archive_path = create_backup(self.source_dir, self.dest_dir)
        self.assertTrue(archive_path.exists())
        self.assertTrue(str(archive_path).endswith(".zip"))


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create test files with different extensions
        Path(self.test_dir, "document.txt").write_text("doc")
        Path(self.test_dir, "image.png").write_text("img")
        Path(self.test_dir, "script.py").write_text("code")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_organize_dry_run(self):
        moves = organize(self.test_dir, dry_run=True)
        # Verify dry-run doesn't actually move files
        self.assertTrue(Path(self.test_dir, "document.txt").exists())
        self.assertEqual(len(moves), 3)
    
    def test_organize_actual(self):
        moves = organize(self.test_dir, dry_run=False)
        # Verify files were moved
        self.assertTrue(Path(self.test_dir, "txt", "document.txt").exists())
        self.assertTrue(Path(self.test_dir, "png", "image.png").exists())
        self.assertTrue(Path(self.test_dir, "py", "script.py").exists())
        self.assertEqual(len(moves), 3)


if __name__ == "__main__":
    unittest.main()
