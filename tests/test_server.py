#!/usr/bin/env python3
"""Unit tests for the Docker laboratory application."""

import unittest

from app.server import load_student_info, parse_port, render_student_info


class StudentApplicationTests(unittest.TestCase):
    def test_default_student_information(self) -> None:
        student = load_student_info({})
        self.assertEqual(
            student,
            {
                "Name": "Zhanibek",
                "Surname": "Taubakul",
                "Group": "IT2-2302",
                "Student ID": "37650",
            },
        )

    def test_environment_overrides(self) -> None:
        student = load_student_info(
            {
                "STUDENT_NAME": "Test",
                "STUDENT_SURNAME": "Student",
                "STUDENT_GROUP": "QA-0001",
                "STUDENT_ID": "99999",
            }
        )
        self.assertIn("Name: Test", render_student_info(student))
        self.assertIn("Student ID: 99999", render_student_info(student))

    def test_empty_required_value_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "STUDENT_NAME must not be empty"):
            load_student_info({"STUDENT_NAME": "   "})

    def test_line_break_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not contain line breaks"):
            load_student_info({"STUDENT_GROUP": "IT2-2302\nforged"})

    def test_required_output(self) -> None:
        output = render_student_info(load_student_info({}))
        self.assertIn("DevOps Student Application", output)
        self.assertIn("Name: Zhanibek", output)
        self.assertIn("Surname: Taubakul", output)
        self.assertIn("Group: IT2-2302", output)
        self.assertIn("Student ID: 37650", output)
        self.assertIn("Application is running successfully!", output)

    def test_port_validation(self) -> None:
        self.assertEqual(parse_port({}), 8080)
        self.assertEqual(parse_port({"PORT": "9090"}), 9090)
        with self.assertRaisesRegex(ValueError, "PORT must be between"):
            parse_port({"PORT": "0"})
        with self.assertRaisesRegex(ValueError, "PORT must be an integer"):
            parse_port({"PORT": "invalid"})


if __name__ == "__main__":
    unittest.main()
