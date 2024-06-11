import sys
import os

# Obtener la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Obtener la ruta del directorio principal del proyecto
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
# Obtener la ruta del directorio del modelo
model_dir = os.path.join(project_dir, "Model")
# Agregar la ruta del directorio principal del proyecto y del modelo al sys.path
sys.path.append(project_dir)
sys.path.append(model_dir)
sys.path.append("./src")

import Model.MonthlyPaymentLogic as mp

from kivy.app import App  # Es necesario para iniciar y ejecutar una aplicación Kivy.
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class Mein_menu(Screen):
    def __init__(self, **kwargs):
        super(Mein_menu, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')
        header = BoxLayout(orientation='horizontal')
        text_header = Label(text="Bienvenido a la aplicación Calculadora de nómina", font_size=27, color=(1, 0, 0, 1),
                            bold=True, italic=True, font_name='Arial')
        header.add_widget(text_header)
        img = Image(source=r'\bienvenidos44.png')
        header.add_widget(img)
        main_layout.add_widget(header)
        buttons_ = BoxLayout(orientation='vertical')
        button_one = Button(text="Ir a la Descripción", font_size=25, color=(0, 0, 1, 1),
                            bold=True, italic=True, font_name='Arial', on_press=self.go_to_tutorial)
        button_two = Button(text="Ir a la aplicación", font_size=25, color=(0, 0, 1, 1),
                            bold=True, italic=True, font_name='Arial', on_press=self.go_to_aplicacion)
        buttons_.add_widget(button_one)
        buttons_.add_widget(button_two)
        main_layout.add_widget(buttons_)
        self.add_widget(main_layout)

    def go_to_tutorial(self, instance):
        self.manager.current = "Descripción"

    def go_to_aplicacion(self, instance):
        self.manager.current = "Aplicación"


class Description(Screen):
    def __init__(self, **kwargs):
        super(Description, self).__init__(**kwargs)
        header_description = BoxLayout(orientation='vertical')
        scroll_view = ScrollView()
        text_layout = BoxLayout(orientation='vertical')
        text_description = f"""
El propósito del programa es calcular el salario mensual de un empleado 
considerando diferentes variables como el salario básico, días laborados, 
días de licencia, y días de incapacidad, entre otros.

Para llevar a cabo este cálculo, se utilizan varias constantes:

1) El salario mínimo legal en Colombia es de ${mp.MINIMUM_WAGE}.
2) La Unidad de Valor Tributario (UVT) tiene un valor de ${mp.UVT}.
3) Coeficientes para calcular el pago de horas extras en diferentes situaciones:
    * Horas extras diurnas: {mp.EXTRA_HOUR_DAYSHIFT}
    * Horas extras nocturnas: {mp.EXTRA_HOUR_NIGHTSHIFT}
    * Horas extras diurnas en días festivos: {mp.EXTRA_HOUR_DAYSHIFT_HOLIDAYS}
    * Horas extras nocturnas en días festivos: {mp.EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS}
4) El número de días y horas en un mes se establece en {mp.MONTH_DAYS} días y {mp.MONTH_HOURS} horas.
5) Porcentajes utilizados para calcular contribuciones de seguro de salud, aportes a pensiones, fondos de retiro y licencias por enfermedad:
    * Porcentaje de seguro de salud y aportes a pensiones: {mp.PERCENTAGE_HEALTH_INSURANCE * 100}%
    * Porcentaje de fondo de retiro: {mp.PERCENTAGE_RETIREMENT_FUND * 100}%
6) Una lista que define los porcentajes de retención salarial en función del salario en UVT.
"""
        description_label = Label(text=text_description, font_size=20, size_hint_y=None, halign="justify", valign="top",
                                  font_name='Arial')
        text_proposito = Label(text="Propósito", font_size=30, bold=True, italic=True, font_name='Arial')
        description_label.bind(texture_size=description_label.setter('size'))
        text_layout.add_widget(text_proposito)
        text_layout.add_widget(description_label)
        scroll_view.add_widget(text_layout)
        header_description.add_widget(scroll_view)
        contenedor_botones = BoxLayout(orientation="vertical", size_hint=(0.5, 0.8))
        contenedor_botones.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        button_next = Button(text="Ir a la Aplicación", on_press=self.go_to_aplicacion)
        button_back = Button(text="Regresar al menú principal", on_press=self.go_to_Mein_menu)
        contenedor_botones.add_widget(button_next)
        contenedor_botones.add_widget(button_back)
        header_description.add_widget(contenedor_botones)
        self.add_widget(header_description)

    def go_to_Mein_menu(self, instance):
        self.manager.current = 'Menu Principal'

    def go_to_aplicacion(self, instance):
        self.manager.current = "Aplicación"


class Aplicacion(Screen):
    def __init__(self, **kwargs):
        super(Aplicacion, self).__init__(**kwargs)
        contenedor = GridLayout(cols=4, padding=20, spacing=20)
        lista_contenedor = ["salario básico",
                            "días mensuales laborados",
                            "días licencia",
                            "ayuda transporte",
                            "horas extra diurnas",
                            "horas extra nocturnas",
                            "horas extra diurnas festivos",
                            "horas extra nocturnas festivos",
                            "días licencia enfermedad",
                            "porcentaje aporte a salud",
                            "porcentaje aporte a pensión",
                            "porcentaje aporte a fondo de solidaridad pensional"]
        self.text_inputs = {}
        for index in lista_contenedor:
            contenedor.add_widget(Label(text=index))
            self.text_inputs[index] = TextInput(font_size=30)
            contenedor.add_widget(self.text_inputs[index])
        self.button_menu = Button(text="Menú principal", on_press=self.go_to_Mein_menu)
        contenedor.add_widget(self.button_menu)
        self.button_calculator = Button(text="Calcular", on_press=self.result_payment)
        contenedor.add_widget(self.button_calculator)
        self.button_description = Button(text="Descripción", on_press=self.go_to_description)
        contenedor.add_widget(self.button_description)
        imgudm = Image(source=r'\3192b796-96f1-4894-a3f0-98e88584ce1e.png')
        contenedor.add_widget(imgudm)
        self.add_widget(contenedor)

    def result_payment(self, sender):
        try:
            self.validar()
            self.basic_salary = float(self.text_inputs["salario básico"].text)
            self.workdays = int(self.text_inputs["días mensuales laborados"].text)
            self.sick_leave = int(self.text_inputs["días licencia"].text)
            self.transportation_aid = float(self.text_inputs["ayuda transporte"].text)
            self.dayshift_extra_hours = float(self.text_inputs["horas extra diurnas"].text)
            self.nightshift_extra_hours = float(self.text_inputs["horas extra nocturnas"].text)
            self.dayshift_extra_hours_holidays = float(self.text_inputs["horas extra diurnas festivos"].text)
            self.nightshift_extra_hours_holidays = float(self.text_inputs["horas extra nocturnas festivos"].text)
            self.leave_days = int(self.text_inputs["días licencia enfermedad"].text)
            self.percentage_health_insurance = float(self.text_inputs["porcentaje aporte a salud"].text) / 100
            self.percentage_retirement_insurance = float(self.text_inputs["porcentaje aporte a pensión"].text) / 100
            self.percentage_retirement_fund = float(self.text_inputs["porcentaje aporte a fondo de solidaridad pensional"].text) / 100

            self.verificar_result_total = mp.SettlementParameters(
                self.basic_salary, self.workdays, self.sick_leave, self.transportation_aid,
                self.dayshift_extra_hours, self.nightshift_extra_hours,
                self.dayshift_extra_hours_holidays, self.nightshift_extra_hours_holidays,
                self.leave_days, self.percentage_health_insurance,
                self.percentage_retirement_insurance, self.percentage_retirement_fund
            )

            self.result_total_to_pay = round(mp.calculate_settlement(self.verificar_result_total), 2)
            self.mostrar_repuestas()

        except ValueError as err:
            self.mostrar_error(err)
        except Exception as err:
            self.mostrar_error(err)

    def validar(self):
        for key, value in self.text_inputs.items():
            if not value.text:
                raise Exception(f"El valor de {key} no puede estar vacío")
            try:
                float(value.text)
            except ValueError:
                raise Exception(f"El valor de {key} debe ser un número válido")

        for key, value in self.text_inputs.items():
            if 0 > float(value.text):
                raise Exception(f"El valor de {key} no puede ser negativo")

    def mostrar_error(self, err):
        contenido = GridLayout(cols=1)
        contenido.add_widget(Label(text=str(err)))
        cerrar = Button(text="Cerrar")
        contenido.add_widget(cerrar)
        popup = Popup(title="Error", content=contenido)
        cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def mostrar_repuestas(self):
        contenedor_respuestas = GridLayout(cols=4, padding=20, spacing=20)
        lista_respuestas = ["Salario", "Subsidio de transporte", "Valor horas extras diurnas",
                            "Valor horas extra nocturnas", "Valor horas extras festivas",
                            "Valor aporte salud", "Valor aporte pensión", "Valor aporte solidario",
                            "Valor incapacidades", "Valor licencias", "Retención en la fuente", "Total a pagar"]

        self.labels_respuestas = {}

        for index in lista_respuestas:
            contenedor_respuestas.add_widget(Label(text=index))
            self.labels_respuestas[index] = TextInput(font_size=30)
            contenedor_respuestas.add_widget(self.labels_respuestas[index])

        self.labels_respuestas["Salario"].text = str(round(mp.calculate_salary(self.basic_salary, self.workdays, self.leave_days, self.sick_leave), 2))
        self.labels_respuestas["Subsidio de transporte"].text = str(mp.calculate_transportation_aid(self.transportation_aid, self.basic_salary))
        self.labels_respuestas["Valor horas extras diurnas"].text = str(round(mp.calculate_extra_hours(self.basic_salary, self.dayshift_extra_hours, mp.EXTRA_HOUR_DAYSHIFT), 2))
        self.labels_respuestas["Valor horas extra nocturnas"].text = str(round(mp.calculate_extra_hours(self.basic_salary, self.nightshift_extra_hours, mp.EXTRA_HOUR_NIGHTSHIFT), 2))
        values_hours_HOLIDAYS = mp.calculate_extra_hours(self.basic_salary, self.dayshift_extra_hours_holidays, mp.EXTRA_HOUR_DAYSHIFT_HOLIDAYS) + mp.calculate_extra_hours(self.basic_salary, self.nightshift_extra_hours_holidays, mp.EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS)
        self.labels_respuestas["Valor horas extras festivas"].text = str(round(values_hours_HOLIDAYS, 2))
        self.labels_respuestas["Valor aporte salud"].text = str(round(mp.calculate_health_insurance(self.basic_salary, self.percentage_health_insurance), 2))
        self.labels_respuestas["Valor aporte pensión"].text = str(round(mp.calculate_retirement_insurance(self.basic_salary, self.percentage_retirement_insurance), 2))
        self.labels_respuestas["Valor aporte solidario"].text = str(round(mp.calculate_retirement_fund(self.basic_salary, self.percentage_retirement_fund), 2))
        self.labels_respuestas["Valor incapacidades"].text = str(round(mp.calculate_sick_leave(self.basic_salary, self.sick_leave), 2))
        self.labels_respuestas["Valor licencias"].text = str(round(mp.calculate_leave(self.basic_salary, self.leave_days), 2))
        self.labels_respuestas["Retención en la fuente"].text = str(round(mp.calculate_salary_holdback(self.basic_salary), 2))
        self.labels_respuestas["Total a pagar"].text = str(self.result_total_to_pay)

        cerrar = Button(text="Cerrar")
        contenedor_respuestas.add_widget(cerrar)
        popup = Popup(title="Respuestas", content=contenedor_respuestas)
        cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def go_to_Mein_menu(self, instance):
        self.manager.current = 'Menu Principal'

    def go_to_description(self, instance):
        self.manager.current = "Descripción"


class NominaCalculator(App):
    def build(self):
        boss_screen = ScreenManager()
        boss_screen.add_widget(Mein_menu(name="Menu Principal"))
        boss_screen.add_widget(Description(name="Descripción"))
        boss_screen.add_widget(Aplicacion(name="Aplicación"))
        return boss_screen


if __name__ == "__main__":
    NominaCalculator().run()
