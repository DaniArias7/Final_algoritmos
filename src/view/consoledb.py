import sys
import os
import pandas as pd

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

# Importar solo los módulos necesarios
import Model.MonthlyPaymentLogic as mp
from Controller.Controladortablas import WorkersIncomeData, WorkersoutputsData
import Model.TablesEmployer as Temployer

# Mensaje de bienvenida
print("""
Bienvenido a este calculador de nómina, el cual va a tener la posibilidad de conectarse a una base de datos.
Dentro de las siguientes características que va a tener el programa están las siguientes: primero, puedes construir 
una tabla inicial en la cual puedes insertar tus trabajadores y asignarles las características de sus sueldos
correspondientes como "salario básico", "días mensuales laborados", "días de licencia", "ayuda de transporte", "horas extra diurnas",
"horas extra nocturnas", "horas extra diurnas festivos", "horas extra nocturnas festivos", "días de licencia por enfermedad",
"porcentaje de aporte a salud", "porcentaje de aporte a pensión", "porcentaje de aporte a fondo de solidaridad pensional".
""")
print("""
Además de esto, a esta tabla podrás actualizar los datos, eliminarlos, insertar y hacer consultas sobre los trabajadores.
""")
print("""
Ahora bien, también puedes acceder a la segunda tabla, la cual va a contener información de los pagos a los trabajadores. 
A esta tabla podrás hacer consultas y ver todo lo referente a los trabajadores.
""")

# Definir constantes para mensajes de entrada
MSG_NOMBRE_TRABAJADOR = "Ingresa el nombre del trabajador: "
MSG_CEDULA_TRABAJADOR = "Ingresa la cédula del trabajador: "

def createtables():
    WorkersIncomeData.Droptable()
    WorkersIncomeData.CreateTable()
    WorkersoutputsData.Droptable()
    WorkersoutputsData.CreateTable()

def getemployer():
    "Ingresa la siguiente información del trabajador"
    name = input(MSG_NOMBRE_TRABAJADOR)
    id = input(MSG_CEDULA_TRABAJADOR)
    basic_salary = float(input("Ingresa el salario básico del empleado: "))
    monthly_worked_days = int(input("Ingresa el valor de días trabajados por el empleado: ")) 
    days_leave = int(input("Ingresa el número de días de licencia del empleado: "))
    transportation_allowance = float(input("Ingresa el subsidio de transporte del empleado: "))
    daytime_overtime_hours = float(input("Ingresa las horas extras diurnas trabajadas por el empleado: "))
    nighttime_overtime_hours = float(input("Ingresa las horas extras nocturnas trabajadas por el empleado: "))
    daytime_holiday_overtime_hours = float(input("Ingresa las horas extras diurnas en días festivos trabajadas por el empleado: "))
    nighttime_holiday_overtime_hours = float(input("Ingresa las horas extras nocturnas en días festivos trabajadas por el empleado: "))
    sick_leave_days = int(input("Ingresa el número de días de incapacidad del empleado: "))
    health_contribution_percentage = float(input("Ingresa el porcentaje de contribución a salud del empleado: "))
    pension_contribution_percentage = float(input("Ingresa el porcentaje de contribución a pensión del empleado: "))
    solidarity_pension_fund_contribution_percentage = float(input("Ingresa el porcentaje de contribución al fondo de solidaridad pensional del empleado: "))

    employer_info = {
        "name": name,
        "id": id,
        "basic_salary": basic_salary,
        "monthly_worked_days": monthly_worked_days,
        "days_leave": days_leave,
        "transportation_allowance": transportation_allowance,
        "daytime_overtime_hours": daytime_overtime_hours,
        "nighttime_overtime_hours": nighttime_overtime_hours,
        "daytime_holiday_overtime_hours": daytime_holiday_overtime_hours,
        "nighttime_holiday_overtime_hours": nighttime_holiday_overtime_hours,
        "sick_leave_days": sick_leave_days,
        "health_contribution_percentage": health_contribution_percentage,
        "pension_contribution_percentage": pension_contribution_percentage,
        "solidarity_pension_fund_contribution_percentage": solidarity_pension_fund_contribution_percentage
    }
    return employer_info

def insert_employer():
    quantityemployees = int(input("Ingresa la cantidad de trabajadores a calcular la nomina: "))
    for worker in range(quantityemployees):
        print(f"Datos trabajador {worker + 1}")
        dic_info_enter = getemployer()
        employer = Temployer.Employerinput(
            name=dic_info_enter["name"], id=dic_info_enter["id"], basic_salary=dic_info_enter["basic_salary"], 
            monthly_worked_days=dic_info_enter["monthly_worked_days"], days_leave=dic_info_enter["days_leave"], 
            transportation_allowance=dic_info_enter["transportation_allowance"], 
            daytime_overtime_hours=dic_info_enter["daytime_overtime_hours"], 
            nighttime_overtime_hours=dic_info_enter["nighttime_overtime_hours"], 
            daytime_holiday_overtime_hours=dic_info_enter["daytime_holiday_overtime_hours"],
            nighttime_holiday_overtime_hours=dic_info_enter["nighttime_holiday_overtime_hours"], 
            sick_leave_days=dic_info_enter["sick_leave_days"], 
            health_contribution_percentage=dic_info_enter["health_contribution_percentage"],
            pension_contribution_percentage=dic_info_enter["pension_contribution_percentage"], 
            solidarity_pension_fund_contribution_percentage=dic_info_enter["solidarity_pension_fund_contribution_percentage"]
        )
        WorkersIncomeData.Insert(employer)
        print("")
    print("Se realizó con éxito la inserción de trabajadores.") 

def query_employees():
    name = input(MSG_NOMBRE_TRABAJADOR)
    id = input(MSG_CEDULA_TRABAJADOR)
    
    findemployer = WorkersIncomeData.QueryWorker(name, id)
    
    if findemployer:
        data_series = pd.Series({
            "Nombre": findemployer.name,
            "Cédula": findemployer.id,
            "Salario básico": findemployer.basic_salary,
            "Días trabajados": findemployer.monthly_worked_days,
            "Días de licencia": findemployer.days_leave,
            "Subsidio de transporte": findemployer.transportation_allowance,
            "Horas extras diurnas": findemployer.daytime_overtime_hours,
            "Horas extras nocturnas": findemployer.nighttime_overtime_hours,
            "Horas extras diurnas en días festivos": findemployer.daytime_holiday_overtime_hours,
            "Horas extras nocturnas en días festivos": findemployer.nighttime_holiday_overtime_hours,
            "Días de incapacidad": findemployer.sick_leave_days,
            "Porcentaje de contribución a salud": findemployer.health_contribution_percentage,
            "Porcentaje de contribución a pensión": findemployer.pension_contribution_percentage,
            "Porcentaje de contribución al fondo de solidaridad pensional": findemployer.solidarity_pension_fund_contribution_percentage
        })
        print(data_series)
    else:
        print("No se encontró ningún trabajador con el nombre y la cédula proporcionados.")

def obtener_significado(valor):
    significados = {
        "Salario básico": "basic_salary",
        "Días trabajados": "monthly_worked_days",
        "Días de licencia": "days_leave",
        "Subsidio de transporte": "transportation_allowance",
        "Horas extras diurnas": "daytime_overtime_hours",
        "Horas extras nocturnas": "nighttime_overtime_hours",
        "Horas extras diurnas en días festivos": "daytime_holiday_overtime_hours",
        "Horas extras nocturnas en días festivos": "nighttime_holiday_overtime_hours",
        "Días de incapacidad": "sick_leave_days",
        "Porcentaje de contribución a salud": "health_contribution_percentage",
        "Porcentaje de contribución a pensión": "pension_contribution_percentage",
        "Porcentaje de contribución al fondo de solidaridad pensional": "solidarity_pension_fund_contribution_percentage"
    }

    return significados.get(valor, "Valor desconocido")

def update_employer():
    name = input(MSG_NOMBRE_TRABAJADOR)
    id = input(MSG_CEDULA_TRABAJADOR)
    print("""
    Columnas que puedes cambiar:
    - Salario básico
    - Días trabajados
    - Días de licencia
    - Subsidio de transporte
    - Horas extras diurnas
    - Horas extras nocturnas
    - Horas extras diurnas en días festivos
    - Horas extras nocturnas en días festivos
    - Días de incapacidad
    - Porcentaje de contribución a salud
    - Porcentaje de contribución a pensión
    - Porcentaje de contribución al fondo de solidaridad pensional
    """)
    
    key = input("Ingresa la columna que quieres cambiar: ")
    key_update = obtener_significado(key)
    value_update = float(input("Ingresa el valor: "))
    WorkersIncomeData.Update(name, id, key_update=key_update, value_update=value_update)

def delete_employer():
    name = input(MSG_NOMBRE_TRABAJADOR)
    id = input(MSG_CEDULA_TRABAJADOR)
    WorkersIncomeData.DeleteWorker(name, id)

def query_employees_page():
    name = input(MSG_NOMBRE_TRABAJADOR)
    id = input(MSG_CEDULA_TRABAJADOR)
    findemployer = WorkersoutputsData.QueryWorker(name, id)
    
    data_series = pd.Series({
        "Nombre": findemployer.name,
        "Cédula": findemployer.id,
        "Salario básico": findemployer.basic_salary,
        "Días trabajados": findemployer.workdays,
        "Días de licencia": findemployer.leave_days,
        "Subsidio de transporte": findemployer.transportation_aid,
        "Horas extras diurnas": findemployer.dayshift_extra_hours,
        "Horas extras nocturnas": findemployer.nightshift_extra_hours,
        "Horas extras diurnas en días festivos": findemployer.dayshift_extra_hours_holidays,
        "Horas extras nocturnas en días festivos": findemployer.nightshift_extra_hours_holidays,
        "Días de incapacidad": findemployer.sick_leave,
        "Porcentaje de contribución a salud": findemployer.percentage_health_insurance,
        "Porcentaje de contribución a pensión": findemployer.percentage_retirement_insurance,
        "Porcentaje de contribución al fondo de solidaridad pensional": findemployer.percentage_retirement_fund,
        "Devengado": findemployer.devengado,
        "Deducido": findemployer.deducido,
        "Total a pagar": findemployer.amounttopay
    })
    
    print(data_series)

# Crear las tablas al inicio
createtables()

# Bucle principal del programa
while True:
    print("""
    ¿Qué vas a hacer?:
    - insertar_trabajador
    - buscar_trabajador
    - actualizar_informacion
    - eliminar_trabajador
    - llenar_tabla_de_pagos
    - hacer_busquedas_en_tabla_de_pagos
    - finalizar
    """)

    list_opciones = [
        "insertar_trabajador", "buscar_trabajador", "actualizar_informacion", 
        "eliminar_trabajador", "llenar_tabla_de_pagos", "hacer_busquedas_en_tabla_de_pagos", "finalizar"
    ]
    
    valor = input("Selecciona una de las anteriores: ").lower()
    
    try:
        if valor in list_opciones:
            if valor == "insertar_trabajador":
                insert_employer()
            elif valor == "buscar_trabajador":
                query_employees()
            elif valor == "actualizar_informacion":
                update_employer()
            elif valor == "eliminar_trabajador":
                delete_employer()
            elif valor == "llenar_tabla_de_pagos":
                WorkersoutputsData.PopulateTable() 
            elif valor == "hacer_busquedas_en_tabla_de_pagos":
                query_employees_page()
            elif valor == "finalizar":
                break
        else:
            print(f"La palabra '{valor}' no está dentro de las opciones")
    except Temployer.faileprimarykey as primarykey_:
        print(f"Se produjo un error: {primarykey_}")
    except Temployer.not_exist as not_exist_:
        print(f"Se produjo un error: {not_exist_}")
    except Temployer.not_found as not_found_:
        print(f"Se produjo un error: {not_found_}")
    except Temployer.updatenotfount as updatenotfount_:
        print(f"Se produjo un error: {updatenotfount_}")
    except Exception as e:
        print(f"Se produjo un error: {e}")
