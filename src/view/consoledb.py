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
from Model.MonthlyPaymentLogic import calculate_salary, calculate_transportation_aid, calculate_extra_hours, calculate_health_insurance, calculate_retirement_insurance, calculate_retirement_fund, MINIMUM_WAGE, UVT, EXTRA_HOUR_DAYSHIFT, EXTRA_HOUR_NIGHTSHIFT, EXTRA_HOUR_DAYSHIFT_HOLIDAYS, EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS, MONTH_DAYS, MONTH_HOURS, PERCENTAGE_HEALTH_INSURANCE, PERCENTAGE_RETIREMENT_FUND
import Model.MonthlyPaymentLogic as mp
from Controller.Controladortablas import WorkersIncomeData
from Controller.Controladortablas import WorkersoutputsData
import Model.TablesEmployer as Temployer
import pandas as pd


print("""Bienvenido a este calculador de nómina, el cual va a tener la posibilidad de conectarse a una base de datos.
           Dentro de las siguientes características que va a tener el programa están las siguientes: primero, puedes construir 
           una tabla inicial en la cual puedes insertar tus trabajadores y asignarles las características de sus sueldos
           correspondientes como "salario básico", "días mensuales laborados", "días de licencia", "ayuda de transporte", "horas extra diurnas",
           "horas extra nocturnas", "horas extra diurnas festivos", "horas extra nocturnas festivos", "días de licencia por enfermedad",
           "porcentaje de aporte a salud", "porcentaje de aporte a pensión", "porcentaje de aporte a fondo de solidaridad pensional".""")

print("""Además de esto, a esta tabla podrás actualizar los datos, eliminarlos, insertar y hacer consultas sobre los trabajadores.""")

print()

print("""Ahora bien, también puedes acceder a la segunda tabla, la cual va a contener información de los pagos a los trabajadores. 
            A esta tabla podrás hacer consultas y ver todo lo referente a los trabajadores.""")

#CONSTANTES
nombre = "Ingresa el nombre del trabajador: "
cedula = "ingresa la cedula del trabajador:"
salario_basico = "salario basico"
dias_trabajados = "dias trabajador"
dias_licencia = "Días de licencia"
sub_transporte = "Subsidio de transporte"
horas_ext_diu = "Horas extras diurnas"
horas_ext_noc = "Horas extras nocturnas"
horas_ext_di_f= "Horas extras diurnas en días festivos"
horas_ext_noc_f ="Horas extras nocturnas en días festivos"
dias_incapacidad =  "Días de incapacidad"
por_contri_salud = "Porcentaje de contribución a salud"
por_contri_pension= "Porcentaje de contribución a pensión"
por_contri_fondo ="Porcentaje de contribución al fondo de solidaridad pensional"


def createtables():
    WorkersIncomeData.drop_table()
    WorkersIncomeData.create_table()
    WorkersoutputsData.drop_table()
    WorkersoutputsData.create_table()

def getemployer():
    "Ingresa la siguiente información del trabajador"
    name = input(nombre)
    employee_id  = input(cedula)
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
        "id": employee_id ,
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
    quantityemployees=int(input("ingrese la cantidad de trabajadores a calcular la nomina: "))
    for workers in range(quantityemployees):
        print(f"Datos trabajador {workers+1}")
        dic_info_enter=getemployer()
        employer=Temployer.Employerinput(name=dic_info_enter["name"],id=dic_info_enter["id"], basic_salary=dic_info_enter["basic_salary"], 
                                       monthly_worked_days=dic_info_enter["monthly_worked_days"], days_leave=dic_info_enter["days_leave"], 
                                       transportation_allowance=dic_info_enter["transportation_allowance"], 
                                       daytime_overtime_hours=dic_info_enter["daytime_overtime_hours"], 
                                       nighttime_overtime_hours=dic_info_enter["nighttime_overtime_hours"], 
                                       daytime_holiday_overtime_hours=dic_info_enter["daytime_holiday_overtime_hours"],
                                        nighttime_holiday_overtime_hours=dic_info_enter["nighttime_holiday_overtime_hours"], 
                                        sick_leave_days=dic_info_enter["sick_leave_days"], 
                                        health_contribution_percentage=dic_info_enter["health_contribution_percentage"],
                                        pension_contribution_percentage=dic_info_enter["pension_contribution_percentage"], 
                                        solidarity_pension_fund_contribution_percentage=dic_info_enter["solidarity_pension_fund_contribution_percentage"])
        WorkersIncomeData.insert(employer)
        print("")
    print("se realizo con exito la insercion de trabajadores") 

def query_employees():
    name = input(nombre)
    employee_id = input(cedula)
    
    findemployer = WorkersIncomeData.query_worker(name, employee_id)
    
    if findemployer:
        data_series = pd.Series({
            "Nombre": findemployer.name,
            "Cédula": findemployer.id,
            salario_basico: findemployer.basic_salary,
            dias_trabajados: findemployer.monthly_worked_days,
            dias_licencia: findemployer.days_leave,
            sub_transporte: findemployer.transportation_allowance,
            horas_ext_diu: findemployer.daytime_overtime_hours,
            horas_ext_noc: findemployer.nighttime_overtime_hours,
            horas_ext_di_f: findemployer.daytime_holiday_overtime_hours,
            horas_ext_noc_f: findemployer.nighttime_holiday_overtime_hours,
            dias_incapacidad: findemployer.sick_leave_days,
            por_contri_salud : findemployer.health_contribution_percentage,
            por_contri_pension: findemployer.pension_contribution_percentage,
            por_contri_fondo: findemployer.solidarity_pension_fund_contribution_percentage
        })
        print(data_series)
    else:
        print("No se encontró ningún trabajador con el nombre y la cédula proporcionados.")

def obtener_significado(valor):
    significados = {
        salario_basico: "basic_salary",
        dias_trabajados: "monthly_worked_days",
        dias_licencia: "days_leave",
        sub_transporte: "transportation_allowance",
        horas_ext_diu:  "daytime_overtime_hours",
        horas_ext_noc: "nighttime_overtime_hours",
        horas_ext_di_f: "daytime_holiday_overtime_hours",
        horas_ext_noc_f: "nighttime_holiday_overtime_hours",
        dias_incapacidad: "sick_leave_days",
        por_contri_salud : "health_contribution_percentage",
        por_contri_pension: "pension_contribution_percentage",
        por_contri_fondo:  "solidarity_pension_fund_contribution_percentage"
    }

    return significados.get(valor, "Valor desconocido")

def update_employer():
        name=input(nombre)
        employee_id = input(cedula)
        print("""columnas que puedes cambiar 
                Salario básico
                Días trabajados
                Días de licencia
                Subsidio de transporte
                Horas extras diurnas
                Horas extras nocturnas
                Horas extras diurnas en días festivos
                Horas extras nocturnas en días festivos
                Días de incapacidad
                Porcentaje de contribución a salud
                Porcentaje de contribución a pensión
                Porcentaje de contribución al fondo de solidaridad pensional""")
        
        KEY=input("ingrese la columna que quiere cambiar:  ")
        KEYUPDATE=obtener_significado(KEY)
        VALUEUPDATE=float(input("ingrese el valor:   "))
        WorkersIncomeData.update(name,employee_id,KEYUPDATE=KEYUPDATE, VALUEUPDATE=VALUEUPDATE)

def delete_employer():
    name = input(nombre)
    worker_id = input(worker_id)
    WorkersIncomeData.delete_worker(name,id)


def query_employees_page():
    name = input(nombre)
    worker_id = input(worker_id)
    findemployer =WorkersoutputsData.QueryWorker(name,id)
    
    data_series = pd.Series({
    "Nombre": findemployer.name,
    "Cédula": findemployer.id,
    salario_basico: findemployer.basic_salary,
    dias_trabajados: findemployer.workdays,
    dias_licencia: findemployer.leave_days,
    sub_transporte: findemployer.transportation_aid,
    horas_ext_diu: findemployer.dayshift_extra_hours,
    horas_ext_noc: findemployer.nightshift_extra_hours,
    horas_ext_di_f: findemployer.dayshift_extra_hours_holidays,
    horas_ext_noc_f: findemployer.nightshift_extra_hours_holidays,
    dias_incapacidad: findemployer.sick_leave,
    por_contri_salud : findemployer.percentage_health_insurance,
    por_contri_pension: findemployer.percentage_retirement_insurance,
    por_contri_fondo: findemployer.percentage_retirement_fund,
    "Devengado":findemployer.devengado,
    "deducido": findemployer.deducido,
    "total a pagar":findemployer.amounttopay
    })
      
    print(data_series)
createtables()

while True:
    print("""¿Que vas a hacer?: 
            insertar_trabajador
            buscar_trabajador
            actualizar_informacion
            eliminar_trabajador
            llenar_tabla_de_pagos
            hacer_busquedas_en_tabla_de_pagos
            finalizar
            """)

    list_opciones=["insertar_trabajador","buscar_trabajador","actualizar_informacion","eliminar_trabajador","llenar_tabla_de_pagos",
                   "hacer_busquedas_en_tabla_de_pagos","finalizar"]
    valor=input("selecciona una de las anteriores:   ")
    
    try:
        if valor.lower() in list_opciones:
            if valor.lower() == "insertar_trabajador":
                insert_employer()

            if valor.lower() =="buscar_trabajador":
                query_employees()

            if valor.lower()=="actualizar_informacion":
                update_employer()

            if valor.lower()=="eliminar_trabajador":
                delete_employer()

            if valor.lower()=="llenar_tabla_de_pagos":
                WorkersoutputsData.PopulateTable() 

            if valor.lower()=="hacer_busquedas_en_tabla_de_pagos":
                query_employees_page()   

            if valor.lower() == "finalizar":
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

    
    