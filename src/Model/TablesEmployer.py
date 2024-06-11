import sys
import os
from MonthlyPaymentLogic import *

# Obtenemos la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Obtenemos la ruta del directorio principal del proyecto
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
# Agregamos el directorio principal del proyecto al sys.path
sys.path.append(project_dir)
# Ahora podemos importar los módulos del proyecto
from MonthlyPaymentLogic import *
import MonthlyPaymentLogic as mp
#from Controller.Controladortablas import WorkersIncomeData

class FailePrimaryKey(Exception):
    pass

class NotExist(Exception):
    pass

class NotFound(Exception):
    pass

class UpdateNotFound(Exception):
    pass

class EmployerInput:
    """
    Clase para representar los datos de entrada de un empleador.
    Parameters:
    -----------
    name : str
        Nombre del empleador.
    id : int
        Identificador único del empleador.
    basic_salary : float
        Salario básico del empleador.
    monthly_worked_days : int
        Número de días trabajados por el empleador en un mes.
    days_leave : int
        Número de días de permiso tomados por el empleador.
    transportation_allowance : float
        Subsidio para gastos de transporte.
    daytime_overtime_hours : float
        Número de horas extras trabajadas durante el día.
    nighttime_overtime_hours : float
        Número de horas extras trabajadas durante la noche.
    daytime_holiday_overtime_hours : float
        Número de horas extras trabajadas durante días festivos diurnos.
    nighttime_holiday_overtime_hours : float
        Número de horas extras trabajadas durante días festivos nocturnos.
    sick_leave_days : int
        Número de días de licencia por enfermedad tomados por el empleador.
    health_contribution_percentage : float
        Porcentaje de contribución al seguro de salud.
    pension_contribution_percentage : float
        Porcentaje de contribución a la pensión.
    solidarity_pension_fund_contribution_percentage : float
        Porcentaje de contribución al fondo de pensiones solidarias.
    """
    def __init__(self,name, id, basic_salary, monthly_worked_days, days_leave, transportation_allowance,
                 daytime_overtime_hours, nighttime_overtime_hours, daytime_holiday_overtime_hours,
                 nighttime_holiday_overtime_hours, sick_leave_days, health_contribution_percentage,
                 pension_contribution_percentage, solidarity_pension_fund_contribution_percentage):
        
        self.name = name
        self.id = id
        self.basic_salary = basic_salary
        self.monthly_worked_days = monthly_worked_days
        self.days_leave = days_leave
        self.transportation_allowance = transportation_allowance
        self.daytime_overtime_hours = daytime_overtime_hours
        self.nighttime_overtime_hours = nighttime_overtime_hours
        self.daytime_holiday_overtime_hours = daytime_holiday_overtime_hours
        self.nighttime_holiday_overtime_hours = nighttime_holiday_overtime_hours
        self.sick_leave_days = sick_leave_days
        self.health_contribution_percentage = health_contribution_percentage
        self.pension_contribution_percentage = pension_contribution_percentage
        self.solidarity_pension_fund_contribution_percentage = solidarity_pension_fund_contribution_percentage
    
    def is_equal(self, dbneon):
        """
        Verifica si dos instancias de EmployerInput son iguales en todos sus atributos.
        Parameters:
        -----------
        dbneon : EmployerInput
            Otra instancia de EmployerInput para comparar.
        Raises:
        -------
        AssertionError:
            Si algún atributo de las dos instancias no es igual.
        """
        assert (self.name == dbneon.name)
        assert (self.id == dbneon.id)
        assert (self.basic_salary == dbneon.basic_salary)
        assert (self.monthly_worked_days == dbneon.monthly_worked_days)
        assert (self.days_leave == dbneon.days_leave)
        assert (self.transportation_allowance == dbneon.transportation_allowance)
        assert (self.daytime_overtime_hours == dbneon.daytime_overtime_hours)
        assert (self.nighttime_overtime_hours == dbneon.nighttime_overtime_hours)
        assert (self.daytime_holiday_overtime_hours == dbneon.daytime_holiday_overtime_hours)
        assert (self.nighttime_holiday_overtime_hours == dbneon.nighttime_holiday_overtime_hours)
        assert (self.sick_leave_days == dbneon.sick_leave_days)
        assert (self.health_contribution_percentage == dbneon.health_contribution_percentage)
        assert (self.pension_contribution_percentage == dbneon.pension_contribution_percentage)
        assert (self.solidarity_pension_fund_contribution_percentage == dbneon.solidarity_pension_fund_contribution_percentage)
    
    @staticmethod
    def primary_key(name, id, module):
        """
        Verifica si la combinación de nombre e ID ya existe en la base de datos.
        Parameters:
        -----------
        name : str
            Nombre del empleador.
        id : int
            Identificador único del empleador.
        module : Module
            Módulo que contiene la función QueryWorker para consultar la base de datos.
        Raises:
        -------
        FailePrimaryKey:
            Si la combinación de nombre e ID ya existe en la base de datos.
        """      
        value = module.QueryWorker(name, id)
        if value is not None:
            raise FailePrimaryKey(f"Ya ingresaste este usuario: {name} - {id}")
        
    @staticmethod
    def not_exist(employer):
        """
        Verifica si algún atributo del objeto employer es None.
        Parameters:
        -----------
        employer : EmployerInput
            Una instancia de la clase EmployerInput.
        Raises:
        -------
        NotExist:
            Si algún atributo del objeto employer es None.
        """
        if any(value is None for value in employer.__dict__.values()):
            raise NotExist("Falta un valor al crear la clase EmployerInput")
    
    @staticmethod
    def valor_presente(atributo):
        """
        Verifica si el atributo dado está presente en la lista de atributos esperados.
        Parameters:
        -----------
        atributo : str
            El nombre del atributo a verificar.
        Raises:
        -------
        UpdateNotFound:
            Si el atributo dado no se encuentra en la lista de atributos esperados.
        """
        lista_atributos = [
            "name", "id", "basic_salary", "monthly_worked_days", "days_leave", "transportation_allowance",
            "daytime_overtime_hours", "nighttime_overtime_hours", "daytime_holiday_overtime_hours",
            "nighttime_holiday_overtime_hours", "sick_leave_days", "health_contribution_percentage",
            "pension_contribution_percentage", "solidarity_pension_fund_contribution_percentage"
        ]
        if atributo not in lista_atributos:
            raise UpdateNotFound("No se encuentra el valor para realizar el update")

class EmployerOutput:
    """
    Clase para representar los datos de salida de un empleador.

    Parameters:
    -----------
    name : str
        Nombre del empleador.
    id : int
        Identificador único del empleador.
    basic_salary : float
        Salario básico del empleador.
    workdays : int
        Número de días trabajados por el empleador.
    sick_leave : int
        Número de días de licencia por enfermedad tomados por el empleador.
    transportation_aid : float
        Ayuda financiera para gastos de transporte.
    dayshift_extra_hours : float
        Número de horas extra trabajadas durante el turno diurno.
    nightshift_extra_hours : float
        Número de horas extra trabajadas durante el turno nocturno.
    dayshift_extra_hours_holidays : float
        Número de horas extra trabajadas durante días festivos en el turno diurno.
    nightshift_extra_hours_holidays : float
        Número de horas extra trabajadas durante días festivos en el turno nocturno.
    leave_days : int
        Número de días de permiso tomados por el empleador.
    percentage_health_insurance : float
        Porcentaje de contribución al seguro de salud.
    percentage_retirement_insurance : float
        Porcentaje de contribución al seguro de jubilación.
    percentage_retirement_fund : float
        Porcentaje de contribución al fondo de jubilación.
    devengado : float
        Monto ganado por el empleador.
    deducido : float
        Monto deducido de las ganancias del empleador.
    amounttopay : float
        Monto total a pagar al empleador.
    """
    def __init__(self, name, id, basic_salary, workdays, sick_leave, transportation_aid, dayshift_extra_hours, nightshift_extra_hours,
                 dayshift_extra_hours_holidays, nightshift_extra_hours_holidays, leave_days, percentage_health_insurance,
                 percentage_retirement_insurance, percentage_retirement_fund, devengado, deducido, amounttopay):
        self.name = name
        self.id = id
        self.basic_salary = basic_salary
        self.workdays = workdays
        self.sick_leave = sick_leave
        self.transportation_aid = transportation_aid
        self.dayshift_extra_hours = dayshift_extra_hours
        self.nightshift_extra_hours = nightshift_extra_hours
        self.dayshift_extra_hours_holidays = dayshift_extra_hours_holidays
        self.nightshift_extra_hours_holidays = nightshift_extra_hours_holidays
        self.leave_days = leave_days
        self.percentage_health_insurance = percentage_health_insurance
        self.percentage_retirement_insurance = percentage_retirement_insurance
        self.percentage_retirement_fund = percentage_retirement_fund
        self.devengado = devengado
        self.deducido = deducido
        self.amounttopay = amounttopay
    
    def is_equivalent(self, dbneon):
        """
        Verifica si dos instancias de EmployerOutput son equivalentes en todos sus atributos.
        Parameters:
        -----------
        dbneon : EmployerOutput
            Otra instancia de EmployerOutput para comparar.
        Returns:
        --------
        bool:
            True si todos los atributos son equivalentes, False de lo contrario.
        """
        assert (self.name == dbneon.name)
        assert (self.id == dbneon.id)
        assert (self.basic_salary == dbneon.basic_salary)
        assert (self.workdays == dbneon.workdays)
        assert (self.sick_leave == dbneon.sick_leave)
        assert (self.transportation_aid == dbneon.transportation_aid)
        assert (self.dayshift_extra_hours == dbneon.dayshift_extra_hours) 
        assert (self.nightshift_extra_hours == dbneon.nightshift_extra_hours) 
        assert (self.dayshift_extra_hours_holidays == dbneon.dayshift_extra_hours_holidays)
        assert (self.nightshift_extra_hours_holidays == dbneon.nightshift_extra_hours_holidays)
        assert (self.leave_days == dbneon.leave_days) 
        assert (self.percentage_health_insurance == dbneon.percentage_health_insurance)
        assert (self.percentage_retirement_insurance == dbneon.percentage_retirement_insurance) 
        assert (self.percentage_retirement_fund == dbneon.percentage_retirement_fund) 
        assert (self.devengado == dbneon.devengado) 
        assert (self.deducido == dbneon.deducido)
        assert (self.amounttopay == dbneon.amounttopay)
        return True
    
    @staticmethod
    def employer_not_found(query):
        """
        Lanza una excepción si el empleador consultado no se encuentra.
        Parameters:
        -----------
        query : object
            El resultado de una operación de consulta. Si es None, indica que no se encontró el empleador.
        Raises:
        -------
        NotFound:
            Si no se encuentra el empleador consultado.
        """
        if query is None:
            raise NotFound("No se ha encontrado su búsqueda")
