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

# Definir constantes para mensajes de entrada y columnas
MSG_NOMBRE_TRABAJADOR = "Ingresa el nombre del trabajador: "
MSG_CEDULA_TRABAJADOR = "Ingresa la cédula del trabajador: "

SALARIO_BASICO = "Salario básico"
DIAS_TRABAJADOS = "Días trabajados"
DIAS_DE_LICENCIA = "Días de licencia"
SUBSIDIO_DE_TRANSPORTE = "Subsidio de transporte"
HORAS_EXTRAS_DIURNAS = "Horas extras diurnas"
HORAS_EXTRAS_NOCTURNAS = "Horas extras nocturnas"
HORAS_EXTRAS_DIURNAS_FESTIVOS = "Horas extras diurnas en días festivos"
HORAS_EXTRAS_NOCTURNAS_FESTIVOS = "Horas extras nocturnas en días festivos"
DIAS_DE_INCAPACIDAD = "Días de incapacidad"
PORCENTAJE_DE_CONTRIBUCION_A_SALUD = "Porcentaje de contribución a salud"
PORCENTAJE_DE_CONTRIBUCION_A_PENSION = "Porcentaje de contribución a pensión"
PORCENTAJE_DE_CONTRIBUCION_A_FONDO_SOLIDARIDAD = "Porcentaje de contribución al fondo de solidaridad pensional"

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

def createtables():
    WorkersIncomeData.Droptable()
    WorkersIncomeData.CreateTable()
    WorkersoutputsData.Droptable()
    WorkersoutputsData.CreateTable()

def getemployer():
    "Ingresa la siguiente información del trabajador"
    name = input(MSG_NOMBRE_TRABAJADOR)
    id = input(MSG_CEDULA_TRABAJADOR)
    basic_salary = float(input(f"Ingresa el {SALARIO_BASICO} del empleado: "))
    monthly_worked_days = int(input(f"Ingresa el valor de {DIAS_TRABAJADOS} por el empleado: ")) 
    days_leave = int(input(f"Ingresa el número de {DIAS_DE_LICENCIA} del empleado: "))
    transportation_allowance = float(input(f"Ingresa el {SUBSIDIO_DE_TRANSPORTE} del empleado: "))
    daytime_overtime_hours = float(input(f"Ingresa las {HORAS_EXTRAS_DIURNAS} trabajadas por el empleado: "))
    nighttime_overtime_hours = float(input(f"Ingresa las {HORAS_EXTRAS_NOCTURNAS} trabajadas por el empleado: "))
    daytime_holiday_overtime_hours = float(input(f"Ingresa las {HORAS_EXTRAS_DIURNAS_FESTIVOS} trabajadas por el empleado: "))
    nighttime_holiday_overtime_hours = float(input(f"Ingresa las {HORAS_EXTRAS_NOCTURNAS_FESTIVOS} trabajadas por el empleado: "))
    sick_leave_days = int(input(f"Ingresa el número de {DIAS_DE_INCAPACIDAD} del empleado: "))
    health_contribution_percentage = float(input(f"Ingresa el {PORCENTAJE_DE_CONTRIBUCION_A_SALUD} del empleado: "))
    pension_contribution_percentage = float(input(f"Ingresa el {PORCENTAJE_DE_CONTRIBUCION_A_PENSION} del empleado: "))
    solidarity_pension_fund_contribution_percentage = float(input(f"Ingresa el {PORCENTAJE_DE_CONTRIBUCION_A_FONDO_SOLIDARIDAD} del empleado: "))

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
            SALARIO_BASICO: findemployer.basic_salary,
            DIAS_TRABAJADOS: findemployer.monthly_worked_days,
            DIAS_DE_LICENCIA: findemployer.days_leave,
            SUBSIDIO_DE_TRANSPORTE: findemployer.transportation_allowance,
            HORAS_EXTRAS_DIURNAS: findemployer.daytime_overtime_hours,
            HORAS_EXTRAS_NOCTURNAS: findemployer.nighttime_overtime_hours,
            HORAS_EXTRAS_DIURNAS_FESTIVOS: findemployer.daytime_holiday_overtime_hours,
            HORAS_EXTRAS_NOCTURNAS_FESTIVOS: findemployer.nighttime_holiday_overtime_hours,
            DIAS_DE_INCAPACIDAD: findemployer.sick_leave_days,
            PORCENTAJE_DE_CONTRIBUCION_A_SALUD: findemployer.health_contribution_percentage,
            PORCENTAJE_DE_CONTRIBUCION_A_PENSION: findemployer.pension_contribution_percentage,
            PORCENTAJE_DE_CONTRIBUCION_A_FONDO_SOLIDARIDAD: findemployer.solidarity_pension_fund_contribution_percentage
        })
        print(data_series)
    else:
        print("No se encontró ningún trabajador con el nombre y la cédula proporcionados.")

def obtener_significado(valor):
    significados = {
        SALARIO_BASICO: "basic_salary",
        DIAS_TRABAJADOS: "monthly_worked_days",
        DIAS_DE_LICENCIA: "days_leave",
        SUBSIDIO_DE_TRANSPORTE: "transportation_allowance",
        HORAS_EXTRAS_DIURNAS: "daytime_overtime_hours",
        HORAS_EXTRAS_NOCTURNAS: "nighttime_overtime_hours",
        HORAS_EXTRAS_DIURNAS_FESTIVOS: "daytime_holiday_overtime_hours",
        HORAS_EXTRAS_NOCTURNAS_FESTIVOS: "nighttime_holiday_overtime_hours",
        DIAS_DE_INCAPACIDAD: "sick_leave_days",
        PORCENTAJE_DE_CONTRIBUCION_A_SALUD: "health_contribution_percentage",
        PORCENTAJE_DE_CONTRIBUCION_A_PENSION: "pension_contribution_percentage",
        PORCENTAJE_DE_CONTRIBUCION_A_FONDO_SOLIDARIDAD: "solidarity_pension_fund_contribution_percentage"
    }

    return significados.get(valor, "Valor desconocido")

def update_employer():
    name = input(MSG_NOMBRE_TRABAJADOR)
    id = input(MSG_CEDULA_TRABAJADOR)
    print(f"""
    Columnas que puedes cambiar:
    - {SALARIO_BASICO}
    - {DIAS_TRABAJADOS}
    - {DIAS_DE_LICENCIA}
    - {SUBSIDIO_DE_TRANSPORTE}
    - {HORAS_EXTRAS_DIURNAS}
    - {HORAS_EXTRAS_NOCTURNAS}
    - {HORAS_EXTRAS_DIURNAS_FESTIVOS}
    - {HORAS_EXTRAS_NOCTURNAS_FESTIVOS}
    - {DIAS_DE_INCAPACIDAD}
    - {PORCENTAJE_DE_CONTRIBUCION_A_SALUD}
    - {PORCENTAJE_DE_CONTRIBUCION_A_PENSION}
    - {PORCENTAJE_DE_CONTRIBUCION_A_FONDO_SOLIDARIDAD}
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
        SALARIO_BASICO: findemployer.basic_salary,
        DIAS_TRABAJADOS: findemployer.workdays,
        DIAS_DE_LICENCIA: findemployer.leave_days,
        SUBSIDIO_DE_TRANSPORTE: findemployer.transportation_aid,
        HORAS_EXTRAS_DIURNAS: findemployer.dayshift_extra_hours,
        HORAS_EXTRAS_NOCTURNAS: findemployer.nightshift_extra_hours,
        HORAS_EXTRAS_DIURNAS_FESTIVOS: findemployer.dayshift_extra_hours_holidays,
        HORAS_EXTRAS_NOCTURNAS_FESTIVOS: findemployer.nightshift_extra_hours_holidays,
        DIAS_DE_INCAPACIDAD: findemployer.sick_leave,
        PORCENTAJE_DE_CONTRIBUCION_A_SALUD: findemployer.percentage_health_insurance,
        PORCENTAJE_DE_CONTRIBUCION_A_PENSION: findemployer.percentage_retirement_insurance,
        PORCENTAJE_DE_CONTRIBUCION_A_FONDO_SOLIDARIDAD: findemployer.percentage_retirement_fund,
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
