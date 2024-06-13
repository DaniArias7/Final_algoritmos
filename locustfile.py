from locust import HttpUser, between, task
from faker import Faker

fake = Faker()

class MyUser(HttpUser):
    wait_time = between(0,1)  # Tiempo de espera entre las tareas, en segundos

    @task
    def visitar_pagina_inicio(self):
        self.client.get("/")

    @task
    def ver_descripcion(self):
        self.client.get("/description")

    @task
    def crear_usuario(self):
        # Genera datos aleatorios para el nuevo usuario
        nombre = fake.name()
        cedula = fake.unique.ssn()
        salario = fake.random_number(digits=6)
        dias_trabajados = fake.random_number(digits=2)
        dias_enfermedad = fake.random_number(digits=1)
        auxilio_transporte = fake.random_number(digits=5)
        horas_diurnas_extra = fake.random_number(digits=2)
        horas_nocturnas_extra = fake.random_number(digits=2)
        horas_diurnas_extra_festivo = fake.random_number(digits=2)
        horas_nocturnas_extra_festivo = fake.random_number(digits=2)
        dias_libres = fake.random_number(digits=1)
        porcentaje_seguro_salud = fake.random_number(digits=2)
        porcentaje_retiro = fake.random_number(digits=2)
        porcentaje_fondo_retiro = fake.random_number(digits=2)

        # Define los datos que se enviarán en la solicitud POST
        data = {
            "nombre": nombre,
            "cedula": cedula,
            "salario": salario,
            "Días_Trabajados": dias_trabajados,
            "Días_enfermedad": dias_enfermedad,
            "Auxilio_Trasporte": auxilio_transporte,
            "Horas_diurnas_extra": horas_diurnas_extra,
            "Horas_nocturnas_extra": horas_nocturnas_extra,
            "Horas_diurnas_extra_festivo": horas_diurnas_extra_festivo,
            "Horas_nocturnas_extra_festivo": horas_nocturnas_extra_festivo,
            "Días_Libres": dias_libres,
            "Porcentaje_seguro_salud": porcentaje_seguro_salud,
            "Porcentaje_retiro": porcentaje_retiro,
            "percentage_retirement_fund": porcentaje_fondo_retiro
        }

        # Envia la solicitud POST para crear el nuevo usuario
        self.client.post("/crear_usuario", data=data)



    @task
    def buscar_usuario(self):
        # Genera datos aleatorios para buscar el usuario
        nombre = fake.first_name()
        cedula = fake.random_number(digits=10)

        # Envía la solicitud GET para buscar el usuario
        response = self.client.get("/buscar-usuario", params={"nombre": nombre, "cedula": cedula})
        
        if response.status_code == 200:
            # Simula que el usuario presiona el botón de búsqueda
            self.client.get(f"/buscar_usuario_result?nombre={nombre}&cedula={cedula}")
        else:
            print(f"Error al buscar usuario: {response.status_code}, {response.text}")

    @task
    def actualizar_usuario(self):
        self.client.get("/actualizar-usuario")

    @task
    def calcular_liquidacion(self):
        self.client.get("/calcular-liquidacion")

    @task
    def eliminar_usuario(self):
        self.client.get("/eliminar-usuario")


    @task
    def eliminar_usuario(self):
        self.client.get("/eliminar-usuario")
