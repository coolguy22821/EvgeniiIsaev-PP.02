import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import app

class Week2Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); app.DB_PATH=Path(self.tmp.name)/"test.db"
  app.app.config["TESTING"]=True; self.client=app.app.test_client(); app.init_db()
 def tearDown(self): self.tmp.cleanup()
 @patch("app.send_registration_notification")
 def test_registration_writes_notification_log(self,notify):
  notify.return_value={"status":"demo","details":"test"}
  r=self.client.post("/register",data={"full_name":"Анна","group_name":"ПИ-22","email":"a@example.com","competition_name":"Проекты"},follow_redirects=True)
  self.assertEqual(r.status_code,200); notify.assert_called_once()
  with app.db() as con: self.assertEqual(con.execute("SELECT COUNT(*) FROM notification_log").fetchone()[0],1)
 def test_notifications_page(self): self.assertEqual(self.client.get("/notifications").status_code,200)

if __name__=="__main__": unittest.main()
