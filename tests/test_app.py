import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app as project


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        project.DB_PATH = Path(self.temp_dir.name) / "test.db"
        project.app.config["TESTING"] = True
        self.client = project.app.test_client()
        project.init_db()

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("app.notify_class_representatives")
    def test_registration_is_saved(self, notify):
        response = self.client.post("/register", data={
            "full_name": "Иванов Иван",
            "group_name": "ИС-21",
            "email": "ivanov@example.com",
            "competition_name": "Студенческий проект"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Заявка успешно зарегистрирована".encode(), response.data)
        notify.assert_called_once()

        with project.get_connection() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM registrations"
            ).fetchone()[0]
        self.assertEqual(count, 1)

    def test_empty_form_is_rejected(self):
        response = self.client.post("/register", data={}, follow_redirects=True)
        self.assertIn("заполните все поля".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
