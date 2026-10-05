import tempfile
import unittest
from pathlib import Path
from app import StudentManager


class StudentManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = Path(self.temp_dir.name) / "test.db"
        self.manager = StudentManager(self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_student(self):
        sid = self.manager.add_student("Asha Rao", "asha@example.com", "Computing", 1)
        rows = self.manager.list_students()
        self.assertEqual(sid, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Asha Rao")

    def test_search_student(self):
        self.manager.add_student("Ravi Kumar", "ravi@example.com", "Cybersecurity", 2)
        rows = self.manager.search_students("Cyber")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Ravi Kumar")

    def test_update_student(self):
        sid = self.manager.add_student("Meera Shah", "meera@example.com", "Computing", 1)
        self.manager.update_student(sid, "Meera Patel", "meera.p@example.com", "Software", 2)
        row = self.manager.list_students()[0]
        self.assertEqual(row[1:], ("Meera Patel", "meera.p@example.com", "Software", 2))

    def test_delete_student(self):
        sid = self.manager.add_student("John Lee", "john@example.com", "Computing", 3)
        self.manager.delete_student(sid)
        self.assertEqual(self.manager.list_students(), [])

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.manager.add_student("Test User", "not-an-email", "Computing", 1)

    def test_invalid_year(self):
        with self.assertRaises(ValueError):
            self.manager.add_student("Test User", "test@example.com", "Computing", 7)

    def test_duplicate_email(self):
        self.manager.add_student("First", "same@example.com", "Computing", 1)
        with self.assertRaises(ValueError):
            self.manager.add_student("Second", "same@example.com", "Computing", 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
