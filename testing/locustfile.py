from locust import HttpUser, task, between
import random
import string
import json
from faker import Faker

fake = Faker()
registered_users = []
tokens = ["internal_testing"]
devices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def test_register(self):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        
        response = self.client.put("/api/login", json={
            "user_full_name": username,
            "user_given_name": username,
            "user_email": email,
            "user_phone": ''.join(random.choices(string.digits, k=9)),
            "user_city": fake.city(),
            "user_address": fake.address(),
            "user_password": password
        })
        
        if response.status_code == 200:
            registered_users.append({"email": email, "password": password})
    
    @task(2)
    def test_login(self):
        if registered_users:
            user = random.choice(registered_users)
            response = self.client.post("/api/login", json={
                "user_email": user["email"],
                "user_password": user["password"]
            })
            if response.status_code == 200:
                print("True", response)
                tokens.append(response.json().get('token'))
            else:
                print("False", response)  


    @task(3)
    def test_user_get(self):
        token = random.choice(tokens)
        self.client.get("/api/user", json={'token': token})

    @task(3)
    def test_auth_get(self):
        token = random.choice(tokens)
        self.client.get("/api/auth", json={'token': token})

    @task(1)
    def test_auth_delete(self):
        token = random.choice(tokens)
        self.client.delete("/api/auth", json={'token': token})

    @task(1)
    def test_connection_post(self):
        token = random.choice(tokens)
        device = random.choice(devices)
        self.client.post("/api/connection", json={
            "device_id": device,
            "token": token,
            "options": {
                "option1": ''.join(random.choices(string.digits, k=2)),
                "option2": ''.join(random.choices(string.digits, k=2)),
                "option3": ''.join(random.choices(string.digits, k=2)),
            }
        })

    @task(1)
    def test_connection_delete(self):
        token = random.choice(tokens)
        device = random.choice(devices)
        self.client.delete("/api/connection", json={
            "device_id": fake.uuid4(),
            "token": token
        })

    @task(3)
    def test_connection_get(self):
        token = random.choice(tokens)
        device = random.choice(devices)
        self.client.get("/api/connection", json={'token': token})