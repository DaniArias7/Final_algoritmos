# Importacion de bibliotecas
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
import sys
import os

# Obtener la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Obtener la ruta del directorio principal del proyecto
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
# Obtener la ruta del directorio del modelo
model_dir = os.path.join(project_dir, "Model")

# Agregar la ruta del directorio principal del proyecto y del modelo al sys.path
# Esto permite importar módulos desde esos directorios
sys.path.append(project_dir)
sys.path.append(model_dir)
sys.path.append("./src")

# Importar módulos específicos del proyecto
from Controller.Controladortablas import WorkersIncomeData, WorkersoutputsData
from Model.TablesEmployer import Employerinput, Employeroutput as Temployer, Employeroutput
import Model.TablesEmployer as Temployer
import Model.MonthlyPaymentLogic as mp
from Model.MonthlyPaymentLogic import calculate_settlement, InvalidRetirementFundPercentageError, SettlementParameters
import pandas as pd

# Inicializar las tablas de datos eliminando las existentes y creando nuevas
WorkersIncomeData.drop_table()
WorkersIncomeData.create_table()
WorkersoutputsData.drop_table()
WorkersoutputsData.create_table()

# Crear la aplicación Flask
app = Flask(__name__)
# Crear un blueprint para las vistas de usuarios
blueprint = Blueprint("vista_usuarios", __name__, template_folder="templates")

# Definir una constante para la plantilla "resultado.html"
RESULT_TEMPLATE = "resultado.html"

# Definir una constante para el mensaje de trabajador no encontrado
TRABAJADOR_NO_ENCONTRADO = "No se encontró ningún trabajador con el nombre y la cédula proporcionados."

# Definir la ruta para la página de inicio
@blueprint.route("/")
def home():
    """
    Renderiza la página de inicio.
    """
    return render_template("inicio.html")

# Definir la ruta para la página de creación de un nuevo usuario
@blueprint.route("/new-user")
def nuevo():
    """
    Renderiza la página para crear un nuevo usuario.
    """
    return render_template("crear_usuario.html")

# Definir la ruta para la creación de un nuevo usuario
@blueprint.route("/crear_usuario")
def crear_usuario():
    """
    Crea un nuevo usuario en la base de datos con los datos proporcionados en el formulario.
    """
    nuevo_empleado = Employerinput(
        name=request.args["nombre"],  # Nombre del empleado
        id=request.args["cedula"],  # Cédula del empleado
        basic_salary=float(request.args["salario"]),  # Salario básico del empleado
        monthly_worked_days=int(request.args["Días_Trabajados"]),  # Días trabajados en el mes
        days_leave=int(request.args["Días_Libres"]),  # Días libres del empleado
        transportation_allowance=float(request.args["Auxilio_Trasporte"]),  # Auxilio de transporte
        daytime_overtime_hours=float(request.args["Horas_diurnas_extra"]),  # Horas extra diurnas
        nighttime_overtime_hours=float(request.args["Horas_nocturnas_extra"]),  # Horas extra nocturnas
        daytime_holiday_overtime_hours=float(request.args["Horas_diurnas_extra_festivo"]),  # Horas extra diurnas en festivos
        nighttime_holiday_overtime_hours=float(request.args["Horas_nocturnas_extra_festivo"]),  # Horas extra nocturnas en festivos
        sick_leave_days=int(request.args["Días_enfermedad"]),  # Días de licencia por enfermedad
        health_contribution_percentage=float(request.args["Porcentaje_seguro_salud"]),  # Porcentaje de contribución a salud
        pension_contribution_percentage=float(request.args["Porcentaje_retiro"]),  # Porcentaje de contribución a pensiones
        solidarity_pension_fund_contribution_percentage=float(request.args["percentage_retirement_fund"])  # Porcentaje de contribución al fondo de solidaridad
    )

    # Insertar el nuevo empleado en la base de datos
    WorkersIncomeData.insert(nuevo_empleado)
    return render_template(RESULT_TEMPLATE, user=nuevo_empleado, mensaje="Usuario insertado exitosamente!")

# Definir la ruta para la página de búsqueda de un usuario
@blueprint.route("/buscar-usuario")
def buscar_usuario():
    """
    Renderiza la página para buscar un usuario.
    """
    return render_template("buscar_usuario.html")

# Definir la ruta para mostrar el resultado de la búsqueda de un usuario
@blueprint.route("/buscar_usuario_result", methods=["GET"])
def buscar_usuario_result():
    """
    Busca un usuario en la base de datos y muestra los resultados.
    """
    nombre = request.args["nombre"]  # Nombre del usuario a buscar
    cedula = request.args["cedula"]  # Cédula del usuario a buscar
    trabajador = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
    if trabajador:
        return render_template(
            "buscar_usuario_result.html",
            user=trabajador,
            mensaje="Trabajador encontrado:"
        )
    else:
        return render_template(
            "buscar_usuario_result.html",
            mensaje=TRABAJADOR_NO_ENCONTRADO
        )

# Definir la ruta para la página de actualización de un usuario
@blueprint.route("/actualizar-usuario")
def modificar_usuario():
    """
    Renderiza la página para actualizar la información de un usuario.
    """
    return render_template("actualizar_usuario.html")

# Definir la ruta para mostrar el resultado de la actualización de un usuario
@blueprint.route("/actualizar_usuario_result", methods=["POST"])
def actualizar_usuario_result():
    """
    Actualiza la información de un usuario en la base de datos.
    """
    nombre = request.form["nombre"]  # Nombre del usuario a actualizar
    cedula = request.form["cedula"]  # Cédula del usuario a actualizar
    columna = request.form["columna"]  # Columna a actualizar
    valor = request.form["valor"]  # Nuevo valor para la columna

    try:
        # Convertir el valor al tipo adecuado según la columna que se está actualizando
        if columna in ["basic_salary", "transportation_allowance", "daytime_overtime_hours", "nighttime_overtime_hours",
                       "daytime_holiday_overtime_hours", "nighttime_holiday_overtime_hours", "health_contribution_percentage",
                       "pension_contribution_percentage", "solidarity_pension_fund_contribution_percentage"]:
            valor = float(valor)  # Convertir a float para columnas de tipo numérico con decimales
        else:
            valor = int(valor)  # Convertir a int para columnas de tipo numérico sin decimales
        
        worker = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
        if worker:
            WorkersIncomeData.update(nombre, cedula, KEYUPDATE=columna, VALUEUPDATE=valor)  # Actualizar la información del trabajador en la base de datos
            mensaje = "Información del trabajador actualizada exitosamente!"
        else:
            mensaje = TRABAJADOR_NO_ENCONTRADO
        return render_template(RESULT_TEMPLATE, mensaje=mensaje)
    except Temployer.not_exist as e:
        mensaje = f"Error al actualizar: {str(e)}"
        return render_template(RESULT_TEMPLATE, mensaje=mensaje)
    except Exception as e:
        mensaje = f"Error inesperado: {str(e)}"
        return render_template(RESULT_TEMPLATE, mensaje=mensaje)

# Definir la ruta para la página de eliminación de un usuario
@blueprint.route("/eliminar-usuario")
def eliminar_usuario():
    """
    Renderiza la página para eliminar un usuario.
    """
    return render_template("eliminar_usuario.html")

# Definir la ruta para mostrar el resultado de la eliminación de un usuario
@blueprint.route("/eliminar_usuario_result", methods=["POST"])
def eliminar_usuario_result():
    """
    Elimina un usuario de la base de datos.
    """
    nombre = request.form["nombre"]  # Nombre del usuario a eliminar
    cedula = request.form["cedula"]  # Cédula del usuario a eliminar

    trabajador = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
    if trabajador:
        WorkersIncomeData.delete_worker(nombre, cedula)  # Eliminar el trabajador de la base de datos
        return render_template(RESULT_TEMPLATE, mensaje="Trabajador eliminado exitosamente!")
    else:
        return render_template(RESULT_TEMPLATE, mensaje=TRABAJADOR_NO_ENCONTRADO)
    
# Definir la ruta para la página de cálculo de liquidación
@blueprint.route("/calcular-liquidacion", methods=["GET"])
def calcular_liquidacion():
    """
    Renderiza la página para calcular la liquidación de un trabajador.
    """
    return render_template("calcular_liquidacion.html")

# Definir la ruta para mostrar el resultado del cálculo de liquidación
@blueprint.route("/mostrar_resultado_liquidacion", methods=["POST"])
def mostrar_resultado_liquidacion():
    """
    Calcula y muestra el resultado de la liquidación de un trabajador.
    """
    nombre = request.form["nombre"]  # Nombre del usuario para el cálculo de liquidación
    cedula = request.form["cedula"]  # Cédula del usuario para el cálculo de liquidación
    
    try:
        trabajador = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
        if trabajador:
            # Preparar los parámetros para el cálculo de la liquidación
            settlement_params = SettlementParameters(
                basic_salary=trabajador.basic_salary,  # Salario básico del trabajador
                workdays=trabajador.monthly_worked_days,  # Días trabajados en el mes
                sick_leave=trabajador.sick_leave_days,  # Días de licencia por enfermedad
                transportation_aid=trabajador.transportation_allowance,  # Auxilio de transporte
                dayshift_extra_hours=trabajador.daytime_overtime_hours,  # Horas extra diurnas
                nightshift_extra_hours=trabajador.nighttime_overtime_hours,  # Horas extra nocturnas
                dayshift_extra_hours_holidays=trabajador.daytime_holiday_overtime_hours,  # Horas extra diurnas en festivos
                nightshift_extra_hours_holidays=trabajador.nighttime_holiday_overtime_hours,  # Horas extra nocturnas en festivos
                leave_days=trabajador.days_leave,  # Días de licencia
                percentage_health_insurance=trabajador.health_contribution_percentage / 100,  # Porcentaje de contribución a salud
                percentage_retirement_insurance=trabajador.pension_contribution_percentage / 100,  # Porcentaje de contribución a pensiones
                percentage_retirement_fund=trabajador.solidarity_pension_fund_contribution_percentage / 100  # Porcentaje de contribución al fondo de solidaridad
            )
            liquidacion = calculate_settlement(settlement_params)  # Calcular la liquidación
            
            return render_template(
                "resultado_liquidacion.html",
                nombre=trabajador.name,  # Nombre del trabajador
                cedula=trabajador.id,  # Cédula del trabajador
                salario_basico=trabajador.basic_salary,  # Salario básico del trabajador
                dias_trabajados=trabajador.monthly_worked_days,  # Días trabajados en el mes
                dias_licencia_enfermedad=trabajador.sick_leave_days,  # Días de licencia por enfermedad
                subsidio_transporte=trabajador.transportation_allowance,  # Auxilio de transporte
                horas_extra_diurnas=trabajador.daytime_overtime_hours,  # Horas extra diurnas
                horas_extra_nocturnas=trabajador.nighttime_overtime_hours,  # Horas extra nocturnas
                horas_extra_diurnas_festivos=trabajador.daytime_holiday_overtime_hours,  # Horas extra diurnas en festivos
                horas_extra_nocturnas_festivos=trabajador.nighttime_holiday_overtime_hours,  # Horas extra nocturnas en festivos
                dias_licencia=trabajador.days_leave,  # Días de licencia
                porcentaje_seguro_salud=trabajador.health_contribution_percentage,  # Porcentaje de contribución a salud
                porcentaje_aporte_pensiones=trabajador.pension_contribution_percentage,  # Porcentaje de contribución a pensiones
                porcentaje_aporte_fondo_retiro=trabajador.solidarity_pension_fund_contribution_percentage,  # Porcentaje de contribución al fondo de solidaridad
                total_a_pagar=liquidacion  # Total a pagar en la liquidación
            )
        else:
            return render_template(RESULT_TEMPLATE, mensaje=TRABAJADOR_NO_ENCONTRADO)
    except Temployer.not_found as e:
        return render_template(RESULT_TEMPLATE, mensaje=str(e))
    except Exception as e:
        return render_template(RESULT_TEMPLATE, mensaje=str(e))
    
# Definir la ruta para la página de descripción
@blueprint.route('/description')
def description():
    """
    Renderiza la página de descripción con información detallada sobre los parámetros utilizados en los cálculos.
    """
    return render_template('description.html', 
                           MINIMUM_WAGE=mp.MINIMUM_WAGE,  # Salario mínimo
                           UVT=mp.UVT,  # Unidad de Valor Tributario
                           EXTRA_HOUR_DAYSHIFT=mp.EXTRA_HOUR_DAYSHIFT,  # Valor de la hora extra diurna
                           EXTRA_HOUR_NIGHTSHIFT=mp.EXTRA_HOUR_NIGHTSHIFT,  # Valor de la hora extra nocturna
                           EXTRA_HOUR_DAYSHIFT_HOLIDAYS=mp.EXTRA_HOUR_DAYSHIFT_HOLIDAYS,  # Valor de la hora extra diurna en festivos
                           EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS=mp.EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS,  # Valor de la hora extra nocturna en festivos
                           MONTH_DAYS=mp.MONTH_DAYS,  # Días del mes
                           MONTH_HOURS=mp.MONTH_HOURS,  # Horas del mes
                           PERCENTAGE_HEALTH_INSURANCE=mp.PERCENTAGE_HEALTH_INSURANCE * 100,  # Porcentaje de seguro de salud
                           PERCENTAGE_RETIREMENT_FUND=mp.PERCENTAGE_RETIREMENT_FUND * 100)  # Porcentaje de fondo de retiro

# Registrar el blueprint en la aplicación Flask
app.register_blueprint(blueprint, url_prefix="/")
# Importacion de bibliotecas
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
import sys
import os

# Obtener la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Obtener la ruta del directorio principal del proyecto
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
# Obtener la ruta del directorio del modelo
model_dir = os.path.join(project_dir, "Model")

# Agregar la ruta del directorio principal del proyecto y del modelo al sys.path
# Esto permite importar módulos desde esos directorios
sys.path.append(project_dir)
sys.path.append(model_dir)
sys.path.append("./src")

# Importar módulos específicos del proyecto
from Controller.Controladortablas import WorkersIncomeData, WorkersoutputsData
from Model.TablesEmployer import Employerinput, Employeroutput as Temployer, Employeroutput
import Model.TablesEmployer as Temployer
import Model.MonthlyPaymentLogic as mp
from Model.MonthlyPaymentLogic import calculate_settlement, InvalidRetirementFundPercentageError, SettlementParameters
import pandas as pd

# Inicializar las tablas de datos eliminando las existentes y creando nuevas
WorkersIncomeData.drop_table()
WorkersIncomeData.create_table()
WorkersoutputsData.drop_table()
WorkersoutputsData.create_table()

# Crear la aplicación Flask
app = Flask(__name__)
# Crear un blueprint para las vistas de usuarios
blueprint = Blueprint("vista_usuarios", __name__, template_folder="templates")

# Definir una constante para la plantilla "resultado.html"
RESULT_TEMPLATE = "resultado.html"

# Definir una constante para el mensaje de trabajador no encontrado
TRABAJADOR_NO_ENCONTRADO = "No se encontró ningún trabajador con el nombre y la cédula proporcionados."

# Definir la ruta para la página de inicio
@blueprint.route("/")
def home():
    """
    Renderiza la página de inicio.
    """
    return render_template("inicio.html")

# Definir la ruta para la página de creación de un nuevo usuario
@blueprint.route("/new-user")
def nuevo():
    """
    Renderiza la página para crear un nuevo usuario.
    """
    return render_template("crear_usuario.html")

# Definir la ruta para la creación de un nuevo usuario
@blueprint.route("/crear_usuario")
def crear_usuario():
    """
    Crea un nuevo usuario en la base de datos con los datos proporcionados en el formulario.
    """
    nuevo_empleado = Employerinput(
        name=request.args["nombre"],  # Nombre del empleado
        id=request.args["cedula"],  # Cédula del empleado
        basic_salary=float(request.args["salario"]),  # Salario básico del empleado
        monthly_worked_days=int(request.args["Días_Trabajados"]),  # Días trabajados en el mes
        days_leave=int(request.args["Días_Libres"]),  # Días libres del empleado
        transportation_allowance=float(request.args["Auxilio_Trasporte"]),  # Auxilio de transporte
        daytime_overtime_hours=float(request.args["Horas_diurnas_extra"]),  # Horas extra diurnas
        nighttime_overtime_hours=float(request.args["Horas_nocturnas_extra"]),  # Horas extra nocturnas
        daytime_holiday_overtime_hours=float(request.args["Horas_diurnas_extra_festivo"]),  # Horas extra diurnas en festivos
        nighttime_holiday_overtime_hours=float(request.args["Horas_nocturnas_extra_festivo"]),  # Horas extra nocturnas en festivos
        sick_leave_days=int(request.args["Días_enfermedad"]),  # Días de licencia por enfermedad
        health_contribution_percentage=float(request.args["Porcentaje_seguro_salud"]),  # Porcentaje de contribución a salud
        pension_contribution_percentage=float(request.args["Porcentaje_retiro"]),  # Porcentaje de contribución a pensiones
        solidarity_pension_fund_contribution_percentage=float(request.args["percentage_retirement_fund"])  # Porcentaje de contribución al fondo de solidaridad
    )

    # Insertar el nuevo empleado en la base de datos
    WorkersIncomeData.insert(nuevo_empleado)
    return render_template(RESULT_TEMPLATE, user=nuevo_empleado, mensaje="Usuario insertado exitosamente!")

# Definir la ruta para la página de búsqueda de un usuario
@blueprint.route("/buscar-usuario")
def buscar_usuario():
    """
    Renderiza la página para buscar un usuario.
    """
    return render_template("buscar_usuario.html")

# Definir la ruta para mostrar el resultado de la búsqueda de un usuario
@blueprint.route("/buscar_usuario_result", methods=["GET"])
def buscar_usuario_result():
    """
    Busca un usuario en la base de datos y muestra los resultados.
    """
    nombre = request.args["nombre"]  # Nombre del usuario a buscar
    cedula = request.args["cedula"]  # Cédula del usuario a buscar
    trabajador = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
    if trabajador:
        return render_template(
            "buscar_usuario_result.html",
            user=trabajador,
            mensaje="Trabajador encontrado:"
        )
    else:
        return render_template(
            "buscar_usuario_result.html",
            mensaje=TRABAJADOR_NO_ENCONTRADO
        )

# Definir la ruta para la página de actualización de un usuario
@blueprint.route("/actualizar-usuario")
def modificar_usuario():
    """
    Renderiza la página para actualizar la información de un usuario.
    """
    return render_template("actualizar_usuario.html")

# Definir la ruta para mostrar el resultado de la actualización de un usuario
@blueprint.route("/actualizar_usuario_result", methods=["POST"])
def actualizar_usuario_result():
    """
    Actualiza la información de un usuario en la base de datos.
    """
    nombre = request.form["nombre"]  # Nombre del usuario a actualizar
    cedula = request.form["cedula"]  # Cédula del usuario a actualizar
    columna = request.form["columna"]  # Columna a actualizar
    valor = request.form["valor"]  # Nuevo valor para la columna

    try:
        # Convertir el valor al tipo adecuado según la columna que se está actualizando
        if columna in ["basic_salary", "transportation_allowance", "daytime_overtime_hours", "nighttime_overtime_hours",
                       "daytime_holiday_overtime_hours", "nighttime_holiday_overtime_hours", "health_contribution_percentage",
                       "pension_contribution_percentage", "solidarity_pension_fund_contribution_percentage"]:
            valor = float(valor)  # Convertir a float para columnas de tipo numérico con decimales
        else:
            valor = int(valor)  # Convertir a int para columnas de tipo numérico sin decimales
        
        worker = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
        if worker:
            WorkersIncomeData.update(nombre, cedula, KEYUPDATE=columna, VALUEUPDATE=valor)  # Actualizar la información del trabajador en la base de datos
            mensaje = "Información del trabajador actualizada exitosamente!"
        else:
            mensaje = TRABAJADOR_NO_ENCONTRADO
        return render_template(RESULT_TEMPLATE, mensaje=mensaje)
    except Temployer.not_exist as e:
        mensaje = f"Error al actualizar: {str(e)}"
        return render_template(RESULT_TEMPLATE, mensaje=mensaje)
    except Exception as e:
        mensaje = f"Error inesperado: {str(e)}"
        return render_template(RESULT_TEMPLATE, mensaje=mensaje)

# Definir la ruta para la página de eliminación de un usuario
@blueprint.route("/eliminar-usuario")
def eliminar_usuario():
    """
    Renderiza la página para eliminar un usuario.
    """
    return render_template("eliminar_usuario.html")

# Definir la ruta para mostrar el resultado de la eliminación de un usuario
@blueprint.route("/eliminar_usuario_result", methods=["POST"])
def eliminar_usuario_result():
    """
    Elimina un usuario de la base de datos.
    """
    nombre = request.form["nombre"]  # Nombre del usuario a eliminar
    cedula = request.form["cedula"]  # Cédula del usuario a eliminar

    trabajador = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
    if trabajador:
        WorkersIncomeData.delete_worker(nombre, cedula)  # Eliminar el trabajador de la base de datos
        return render_template(RESULT_TEMPLATE, mensaje="Trabajador eliminado exitosamente!")
    else:
        return render_template(RESULT_TEMPLATE, mensaje=TRABAJADOR_NO_ENCONTRADO)
    
# Definir la ruta para la página de cálculo de liquidación
@blueprint.route("/calcular-liquidacion", methods=["GET"])
def calcular_liquidacion():
    """
    Renderiza la página para calcular la liquidación de un trabajador.
    """
    return render_template("calcular_liquidacion.html")

# Definir la ruta para mostrar el resultado del cálculo de liquidación
@blueprint.route("/mostrar_resultado_liquidacion", methods=["POST"])
def mostrar_resultado_liquidacion():
    """
    Calcula y muestra el resultado de la liquidación de un trabajador.
    """
    nombre = request.form["nombre"]  # Nombre del usuario para el cálculo de liquidación
    cedula = request.form["cedula"]  # Cédula del usuario para el cálculo de liquidación
    
    try:
        trabajador = WorkersIncomeData.query_worker(nombre, cedula)  # Consultar el trabajador en la base de datos
        if trabajador:
            # Preparar los parámetros para el cálculo de la liquidación
            settlement_params = SettlementParameters(
                basic_salary=trabajador.basic_salary,  # Salario básico del trabajador
                workdays=trabajador.monthly_worked_days,  # Días trabajados en el mes
                sick_leave=trabajador.sick_leave_days,  # Días de licencia por enfermedad
                transportation_aid=trabajador.transportation_allowance,  # Auxilio de transporte
                dayshift_extra_hours=trabajador.daytime_overtime_hours,  # Horas extra diurnas
                nightshift_extra_hours=trabajador.nighttime_overtime_hours,  # Horas extra nocturnas
                dayshift_extra_hours_holidays=trabajador.daytime_holiday_overtime_hours,  # Horas extra diurnas en festivos
                nightshift_extra_hours_holidays=trabajador.nighttime_holiday_overtime_hours,  # Horas extra nocturnas en festivos
                leave_days=trabajador.days_leave,  # Días de licencia
                percentage_health_insurance=trabajador.health_contribution_percentage / 100,  # Porcentaje de contribución a salud
                percentage_retirement_insurance=trabajador.pension_contribution_percentage / 100,  # Porcentaje de contribución a pensiones
                percentage_retirement_fund=trabajador.solidarity_pension_fund_contribution_percentage / 100  # Porcentaje de contribución al fondo de solidaridad
            )
            liquidacion = calculate_settlement(settlement_params)  # Calcular la liquidación
            
            return render_template(
                "resultado_liquidacion.html",
                nombre=trabajador.name,  # Nombre del trabajador
                cedula=trabajador.id,  # Cédula del trabajador
                salario_basico=trabajador.basic_salary,  # Salario básico del trabajador
                dias_trabajados=trabajador.monthly_worked_days,  # Días trabajados en el mes
                dias_licencia_enfermedad=trabajador.sick_leave_days,  # Días de licencia por enfermedad
                subsidio_transporte=trabajador.transportation_allowance,  # Auxilio de transporte
                horas_extra_diurnas=trabajador.daytime_overtime_hours,  # Horas extra diurnas
                horas_extra_nocturnas=trabajador.nighttime_overtime_hours,  # Horas extra nocturnas
                horas_extra_diurnas_festivos=trabajador.daytime_holiday_overtime_hours,  # Horas extra diurnas en festivos
                horas_extra_nocturnas_festivos=trabajador.nighttime_holiday_overtime_hours,  # Horas extra nocturnas en festivos
                dias_licencia=trabajador.days_leave,  # Días de licencia
                porcentaje_seguro_salud=trabajador.health_contribution_percentage,  # Porcentaje de contribución a salud
                porcentaje_aporte_pensiones=trabajador.pension_contribution_percentage,  # Porcentaje de contribución a pensiones
                porcentaje_aporte_fondo_retiro=trabajador.solidarity_pension_fund_contribution_percentage,  # Porcentaje de contribución al fondo de solidaridad
                total_a_pagar=liquidacion  # Total a pagar en la liquidación
            )
        else:
            return render_template(RESULT_TEMPLATE, mensaje=TRABAJADOR_NO_ENCONTRADO)
    except Temployer.not_found as e:
        return render_template(RESULT_TEMPLATE, mensaje=str(e))
    except Exception as e:
        return render_template(RESULT_TEMPLATE, mensaje=str(e))
    
# Definir la ruta para la página de descripción
@blueprint.route('/description')
def description():
    """
    Renderiza la página de descripción con información detallada sobre los parámetros utilizados en los cálculos.
    """
    return render_template('description.html', 
                           MINIMUM_WAGE=mp.MINIMUM_WAGE,  # Salario mínimo
                           UVT=mp.UVT,  # Unidad de Valor Tributario
                           EXTRA_HOUR_DAYSHIFT=mp.EXTRA_HOUR_DAYSHIFT,  # Valor de la hora extra diurna
                           EXTRA_HOUR_NIGHTSHIFT=mp.EXTRA_HOUR_NIGHTSHIFT,  # Valor de la hora extra nocturna
                           EXTRA_HOUR_DAYSHIFT_HOLIDAYS=mp.EXTRA_HOUR_DAYSHIFT_HOLIDAYS,  # Valor de la hora extra diurna en festivos
                           EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS=mp.EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS,  # Valor de la hora extra nocturna en festivos
                           MONTH_DAYS=mp.MONTH_DAYS,  # Días del mes
                           MONTH_HOURS=mp.MONTH_HOURS,  # Horas del mes
                           PERCENTAGE_HEALTH_INSURANCE=mp.PERCENTAGE_HEALTH_INSURANCE * 100,  # Porcentaje de seguro de salud
                           PERCENTAGE_RETIREMENT_FUND=mp.PERCENTAGE_RETIREMENT_FUND * 100)  # Porcentaje de fondo de retiro

# Registrar el blueprint en la aplicación Flask
app.register_blueprint(blueprint, url_prefix="/")
