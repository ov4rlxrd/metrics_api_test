from locust import HttpUser, task, between
import random



class MetricsUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def add_metric(self):
        device_id = f"dev-{random.randint(1, 20)}"
        payload = {
            "device_id": device_id,
            "x": round(random.uniform(0, 100), 2),
            "y": round(random.uniform(0, 100), 2),
            "z": round(random.uniform(0, 100), 2),
        }
        self.client.post("/metrics", json=payload, name="POST /metrics")

    @task(1)
    def get_analytics(self):
        device_id = f"dev-{random.randint(1, 20)}"
        self.client.get(f"/metrics/{device_id}/analytics", name="GET /devices/{id}/analytics")