from locust import HttpUser, task, between
import random
import string
import json
from faker import Faker

fake = Faker()
registered_users = []
tokens = set()
connections = {}
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
            tokens.add([response.json()['token'], email])
    
    @task(2)
    def test_login(self):
        if registered_users:
            user = random.choice(registered_users)
            response = self.client.post("/api/login", json={
                "user_email": user["email"],
                "user_password": user["password"]
            })
            if response.status_code == 200:
                tokens.add([response.json()['token'], user["email"]])


    @task(3)
    def test_user_get(self):
      token_list = list(tokens)
      if token_list:
        token = random.choice(token_list)[0]
        self.client.get("/api/user", json={'token': token})

    @task(3)
    def test_auth_get(self):
      token_list = list(tokens)
      if token_list:
        token = random.choice(token_list)[0]
        self.client.get("/api/auth", json={'token': token})

    @task(1)
    def test_auth_delete(self):
      token_list = list(tokens)
      if token_list:
        token = random.choice(token_list)[0]
        response = self.client.delete("/api/auth", json={'token': token})
        if response.status_code == 200:
            tokens.discard(token)

    @task(1)
    def test_connection_post(self):
      token_list = list(tokens)
      if token_list:
        aux = random.choice(token_list)
        token = aux[0]
        device = random.choice(devices)
        response = self.client.post("/api/connection", json={
            "device_id": device,
            "token": token,
            "options": {
                "option1": ''.join(random.choices(string.digits, k=2)),
                "option2": ''.join(random.choices(string.digits, k=2)),
                "option3": ''.join(random.choices(string.digits, k=2)),
            }
        })
        if response.status_code == 200:
            if aux[1] in connections:
                connections[aux[1]].append(device)
            else:
                connections[aux[1]] = [device]

    @task(1)
    def test_connection_delete(self):
      token_list = list(tokens)
      if token_list:
        aux = random.choice(token_list)
        if aux[1] in connections:
            token = aux[0]
            device = random.choice(connections[aux[1]])
            response = self.client.delete("/api/connection", json={
                "device_id": device,
                "token": token
            })
            if response.status_code == 200:
                if len(connections[aux[1]]) == 1:
                    del connections[aux[1]]
                else:
                   connections[aux[1]] = [x for x in connections[aux[1]] if x != device]
           

    @task(3)
    def test_connection_get(self):
      token_list = list(tokens)
      if token_list:
        token = random.choice(token_list)[0]
        self.client.get("/api/connection", json={'token': token})