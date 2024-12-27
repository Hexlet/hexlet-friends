from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def load_test(self):
        self.client.get("/")
