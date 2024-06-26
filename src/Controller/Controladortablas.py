import sys
import os
import psycopg2

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
sys.path.append(".")


# Importaciones
from Model.MonthlyPaymentLogic import  calculate_salary, calculate_leave, calculate_transportation_aid, calculate_extra_hours, calculate_sick_leave, calculate_health_insurance, calculate_retirement_insurance, calculate_retirement_fund, calculate_accrued_values, calculate_deducted_values, calculate_settlement, SettlementParameters
import Model.MonthlyPaymentLogic as mp
import Model.TablesEmployer as Temployer
import securitydb as st


class WorkersIncomeData:

    @classmethod
    def get_cursor(cls):
        """ Establishes connection to the database and returns a cursor for querying """
        connection = psycopg2.connect(database=st.PGDATABASE, user=st.PGUSER, password=st.PGPASSWORD, host=st.PGHOST, port=st.PGPORT)
        # All statements are executed through a cursor
        cursor = connection.cursor()
        return cursor
    
    @classmethod
    def create_table(cls):
        """ Creates the user table in the database """
        try:
            cursor =  cls.get_cursor()
            cursor.execute("""CREATE TABLE Employerinput(
                        name varchar(300)  NOT NULL,
                        id varchar(300) PRIMARY KEY NOT NULL,
                        basic_salary float  NOT NULL , 
                        monthly_worked_days int  NOT NULL, 
                        days_leave int  NOT NULL, 
                        transportation_allowance float  NOT NULL,
                        daytime_overtime_hours int  NOT NULL, 
                        nighttime_overtime_hours int  NOT NULL, 
                        daytime_holiday_overtime_hours int  NOT NULL,
                        nighttime_holiday_overtime_hours int  NOT NULL, 
                        sick_leave_days int  NOT NULL, 
                        health_contribution_percentage float  NOT NULL,
                        pension_contribution_percentage float  NOT NULL, 
                        solidarity_pension_fund_contribution_percentage float NOT NULL ); """)
            cursor.connection.commit()
        except psycopg2.Error as e:
            pass
    
    
    @classmethod
    def drop_table(cls):
        """
        Drop the 'Employerinput' table if it exists in the database.

        This function attempts to drop the table 'Employerinput' from the database. 
        If the table does not exist or any error occurs during the execution, it is ignored.
        """
        try:
            cursor=cls.get_cursor()
            cursor.execute(""" DROP TABLE Employerinput""")
            cursor.connection.commit()
        except psycopg2.Error as e:
            pass
    
    @classmethod
    def insert(cls, employer: Temployer.Employerinput):
        """  insert an employer's data into the 'Employerinput' table."""
        try:
            cursor =  cls.get_cursor()
            Temployer.Employerinput.primary_key(employer.name,employer.id, cls)
            Temployer.Employerinput.notexist(employer)
            cursor.execute(f""" INSERT INTO Employerinput  (name, id, basic_salary, monthly_worked_days, 
                                days_leave, transportation_allowance, daytime_overtime_hours, nighttime_overtime_hours, 
                                daytime_holiday_overtime_hours, nighttime_holiday_overtime_hours,
                                sick_leave_days, health_contribution_percentage, pension_contribution_percentage, 
                                solidarity_pension_fund_contribution_percentage)
                                VALUES 
                                ('{employer.name}', '{employer.id}' ,{employer.basic_salary},{employer.monthly_worked_days}, 
                                {employer.days_leave},{employer.transportation_allowance}, {employer.daytime_overtime_hours}, {employer.nighttime_overtime_hours}, 
                                {employer.daytime_holiday_overtime_hours},{employer.nighttime_holiday_overtime_hours},
                                {employer.sick_leave_days}, {employer.health_contribution_percentage},{employer.pension_contribution_percentage},
                                {employer.solidarity_pension_fund_contribution_percentage});""")
            cursor.connection.commit()
        except Temployer.faileprimarykey as error_primaey_key:
            cursor.connection.rollback()
        
        except Temployer.not_exist as error_not_exist:
            cursor.connection.rollback()
    
    
    
    @classmethod
    def delete_worker(cls, name,id):
        """  Delete a worker from the 'Employerinput' table based on the provided name and id. """
        cursor =  cls.get_cursor() 
        cursor.execute(f""" DELETE 
                        FROM Employerinput
                        WHERE name= '{name}' AND id='{id}'; 
                        """)
        cursor.connection.commit() 
    
    @classmethod
    def update(cls, name,id,keyupdate,valueupdate):
        """ update a worker's data in the 'Employerinput' table."""
        try:
            Temployer.Employerinput.valor_presente(keyupdate)
            cursor =  cls.get_cursor()
            cursor.execute(f""" update Employerinput
                            SET {keyupdate} = {valueupdate}
                            WHERE name= '{name}' AND id='{id}'; 
                            """)
            cursor.connection.commit()
        except Temployer.updatenotfount:
            #cursor.connection.rollback()
            pass

    @classmethod
    def query_worker(cls, name, id):
        """ Query the data of a worker from the 'Employerinput' table based on the provided name and id. """
        cursor = cls.get_cursor()
        cursor.execute(f"""SELECT * FROM Employerinput WHERE name = '{name}' AND id = '{id}';""")
        fila = cursor.fetchone()

# Ahora la variable 'fila' contiene el resultado de la consulta

        if fila is None:
            return None
        else:
            result = Temployer.Employerinput(name=fila[0], 
                                            id=fila[1],
                                            basic_salary=fila[2],
                                            monthly_worked_days=fila[3],
                                            days_leave=fila[4],
                                            transportation_allowance=fila[5],
                                            daytime_overtime_hours=fila[6],
                                            nighttime_overtime_hours=fila[7],
                                            daytime_holiday_overtime_hours=fila[8],
                                            nighttime_holiday_overtime_hours=fila[9],
                                            sick_leave_days=fila[10],
                                            health_contribution_percentage=fila[11],
                                            pension_contribution_percentage=fila[12],
                                            solidarity_pension_fund_contribution_percentage=fila[13])
            return result
        

 
        
class  WorkersoutputsData():
    
    @classmethod
    def get_cursor(cls):
        """ Establishes connection to the database and returns a cursor for querying """
        connection = psycopg2.connect(database=st.PGDATABASE, user=st.PGUSER, password=st.PGPASSWORD, host=st.PGHOST, port=st.PGPORT)
        # All statements are executed through a cursor
        cursor = connection.cursor()
        return cursor
    
    @classmethod
    def create_table(cls):
        """ Creates the user table in the database """
        try:
            cursor = cls.get_cursor()
            cursor.execute("""CREATE TABLE Employeroutput(
                        name varchar(300) NOT NULL,
                        id varchar(300) PRIMARY KEY NOT NULL,
                        basic_salary float NOT NULL, 
                        workdays int NOT NULL, 
                        sick_leave int NOT NULL, 
                        transportation_aid float NOT NULL,
                        dayshift_extra_hours int NOT NULL, 
                        nightshift_extra_hours int NOT NULL, 
                        dayshift_extra_hours_holidays int NOT NULL,
                        nightshift_extra_hours_holidays int NOT NULL, 
                        leave_days int NOT NULL, 
                        percentage_health_insurance float NOT NULL,
                        percentage_retirement_insurance float NOT NULL, 
                        percentage_retirement_fund float NOT NULL, 
                        devengado float NOT NULL,
                        deducido float NOT NULL,  
                        amounttopay float NOT NULL) ; """)
            cursor.connection.commit()
        except psycopg2.Error as e:
            pass

    @classmethod
    def drop_table(cls):
        """ Drop the 'Employeroutput' table if it exists in the database. """
        try:
            cursor=cls.get_cursor()
            cursor.execute(""" DROP TABLE Employeroutput""")
            cursor.connection.commit()
        except psycopg2.Error as e:
            pass
    
    @classmethod
    def PopulateTable(cls):
        """ Populate the 'Employeroutput' table based on the data from the 'Employerinput' table.

            This function retrieves data from the 'Employerinput' table and calculates additional attributes 
            based on the provided data. It then inserts the calculated data into the 'Employeroutput' table."""
        cursor = cls.get_cursor()
        cursorWorkersIncomeData = WorkersIncomeData.get_cursor()
        cursorWorkersIncomeData.execute("SELECT * FROM Employerinput")
        employers = cursorWorkersIncomeData.fetchall()  # Obtener todas las filas

        for employer in employers:
            verificar_result_total = mp.SettlementParameters(employer[2], employer[3], employer[4], employer[5],
                                                            employer[6], employer[7], employer[8], employer[9], employer[10],
                                                            employer[11], employer[12], employer[13])
            cursor.execute(
                f"""INSERT INTO Employeroutput (name, id ,basic_salary,workdays,sick_leave,transportation_aid, 
                                                dayshift_extra_hours,nightshift_extra_hours,dayshift_extra_hours_holidays, 
                                                nightshift_extra_hours_holidays,leave_days,percentage_health_insurance,
                                                percentage_retirement_insurance,percentage_retirement_fund,devengado,deducido,amounttopay)
                    
                        SELECT Employerinput.name,
                        Employerinput.id,
                        {round(calculate_salary(employer[2], employer[3], employer[4], employer[10]), 2)}, --basic_salary
                        Employerinput.monthly_worked_days,
                        {round(calculate_leave(employer[2], employer[10]), 2)}, --Employerinput.days_leave
                        {calculate_transportation_aid(employer[5], employer[2])}, --Employerinput.transportation_allowance 
                        {round(calculate_extra_hours(employer[2], employer[6], mp.EXTRA_HOUR_DAYSHIFT), 2)}, --Employerinput.daytime_overtime_hours
                        {round(calculate_extra_hours(employer[2], employer[7], mp.EXTRA_HOUR_NIGHTSHIFT), 2)}, --Employerinput.nighttime_overtime_hours
                        {round(calculate_extra_hours(employer[2], employer[8], mp.EXTRA_HOUR_DAYSHIFT_HOLidAYS), 2)}, --Employerinput.daytime_holiday_overtime_hours 
                        {round(calculate_extra_hours(employer[2], employer[9], mp.EXTRA_HOUR_NIGHTSHIFT_HOLidAYS), 2)}, --Employerinput.nighttime_holiday_overtime_hours
                        {round(calculate_sick_leave(employer[2], employer[4]), 2)}, --Employerinput.sick_leave_days
                        {round(calculate_health_insurance(employer[2], employer[11]), 2)}, --Employerinput.health_contribution_percentage
                        {round(calculate_retirement_insurance(employer[2], employer[12]), 2)}, --Employerinput.pension_contribution_percentage
                        {round(calculate_retirement_fund(employer[2], employer[13]), 2)}, --Employerinput.solidarity_pension_fund_contribution_percentage
                        {round(calculate_accrued_values(verificar_result_total), 2)}, ---devengado 
                        {round(calculate_deducted_values(verificar_result_total), 2)}, --deducido
                        {round(mp.calculate_settlement(verificar_result_total), 2)} --amounttopay  
                    
                    FROM Employerinput where name='{employer[0]}' and id='{employer[1]}' ;""")  # Agregar una cláusula WHERE para filtrar por el id del empleador
            cursor.connection.commit()

    @classmethod
    def query_worker(cls, name, id):
        """ Query the data of a worker from the 'Employeroutput' table based on the provided name and id. """
        cursor = WorkersIncomeData.get_cursor()
        cursor.execute(f"""SELECT * FROM Employeroutput WHERE name = '{name}' AND id = '{id}';""")
        fila = cursor.fetchone()

            # Ahora la variable 'fila' contiene el resultado de la consulta

        if fila is None:
            return None
        else:
            Temployer.Employeroutput.employernotfound(fila)
            result = Temployer.Employeroutput(name=fila[0], 
                                                id=fila[1],
                                                basic_salary=fila[2],
                                                workdays=fila[3],
                                                sick_leave=fila[4],
                                                transportation_aid=fila[5], 
                                                dayshift_extra_hours=fila[6],
                                                nightshift_extra_hours=fila[7],
                                                dayshift_extra_hours_holidays=fila[8], 
                                                nightshift_extra_hours_holidays=fila[9],
                                                leave_days=fila[10],
                                                percentage_health_insurance=fila[11],
                                                percentage_retirement_insurance=fila[12],
                                                percentage_retirement_fund=fila[13],
                                                devengado=fila[14],
                                                deducido=fila[15],
                                                amounttopay=fila[16])
            return result

