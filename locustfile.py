from locust import HttpUser, between, task

class MyUser(HttpUser):
    wait_time = between(5, 15)  # Tiempo de espera entre las tareas, en segundos

    @task
    def visitar_pagina_inicio(self):
        self.client.get("/")

    @task
    def ver_descripcion(self):
        self.client.get("/description")

    @task
    def crear_nuevo_usuario(self):
        self.client.get("/new-user")

    @task
    def buscar_usuario(self):
        self.client.get("/buscar-usuario")

    @task
    def actualizar_usuario(self):
        self.client.get("/actualizar-usuario")

    @task
    def calcular_liquidacion(self):
        self.client.get("/calcular-liquidacion")

    @task
    def eliminar_usuario(self):
        self.client.get("/eliminar-usuario")
