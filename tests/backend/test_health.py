import unittest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestHealthAndRootEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "FloodLens AI")
        self.assertIn("health", data)

    def test_health_check_endpoint(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("environment", data)
        self.assertIn("version", data)
        self.assertIn("timestamp", data)


if __name__ == "__main__":
    unittest.main()
