import sys
import os
import psycopg2
from psycopg2 import sql

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
from Model import MonthlyPaymentLogic as mp
from Model import TablesEmployer as Temployer
import securitydb as st


class WorkersIncomeData:

    @staticmethod
    def GetCursor():
        """Establishes connection to the database and returns a cursor for querying"""
        connection = psycopg2.connect(database=st.PGDATABASE, user=st.PGUSER, password=st.PGPASSWORD, host=st.PGHOST, port=st.PGPORT)
        cursor = connection.cursor()
        return cursor
    
    @classmethod
    def CreateTable(cls):
        """Creates the user table in the database"""
        try:
            cursor = cls.GetCursor()
            cursor.execute("""
                CREATE TABLE Employerinput(
                    name VARCHAR(300) NOT NULL,
                    id VARCHAR(300) PRIMARY KEY NOT NULL,
                    basic_salary FLOAT NOT NULL,
                    monthly_worked_days INT NOT NULL,
                    days_leave INT NOT NULL,
                    transportation_allowance FLOAT NOT NULL,
                    daytime_overtime_hours INT NOT NULL,
                    nighttime_overtime_hours INT NOT NULL,
                    daytime_holiday_overtime_hours INT NOT NULL,
                    nighttime_holiday_overtime_hours INT NOT NULL,
                    sick_leave_days INT NOT NULL,
                    health_contribution_percentage FLOAT NOT NULL,
                    pension_contribution_percentage FLOAT NOT NULL,
                    solidarity_pension_fund_contribution_percentage FLOAT NOT NULL
                );
            """)
            cursor.connection.commit()
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e
    
    @classmethod
    def Droptable(cls):
        """Drop the 'Employerinput' table if it exists in the database."""
        try:
            cursor = cls.GetCursor()
            cursor.execute("DROP TABLE IF EXISTS Employerinput")
            cursor.connection.commit()
        except psycopg2.Error as e:
            print(f"Error dropping table: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e
    
    @classmethod
    def Insert(cls, EMPLOYER: Temployer.Employerinput):
        """Insert an employer's data into the 'Employerinput' table."""
        try:
            cursor = cls.GetCursor()
            Temployer.Employerinput.primary_key(EMPLOYER.name, EMPLOYER.id, WorkersIncomeData)
            Temployer.Employerinput.notexist(EMPLOYER)
            cursor.execute(sql.SQL("""
                INSERT INTO Employerinput (name, id, basic_salary, monthly_worked_days, days_leave, transportation_allowance, 
                                           daytime_overtime_hours, nighttime_overtime_hours, daytime_holiday_overtime_hours, 
                                           nighttime_holiday_overtime_hours, sick_leave_days, health_contribution_percentage, 
                                           pension_contribution_percentage, solidarity_pension_fund_contribution_percentage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """), (EMPLOYER.name, EMPLOYER.id, EMPLOYER.basic_salary, EMPLOYER.monthly_worked_days, EMPLOYER.days_leave, 
                  EMPLOYER.transportation_allowance, EMPLOYER.daytime_overtime_hours, EMPLOYER.nighttime_overtime_hours, 
                  EMPLOYER.daytime_holiday_overtime_hours, EMPLOYER.nighttime_holiday_overtime_hours, EMPLOYER.sick_leave_days, 
                  EMPLOYER.health_contribution_percentage, EMPLOYER.pension_contribution_percentage, 
                  EMPLOYER.solidarity_pension_fund_contribution_percentage))
            cursor.connection.commit()
        except Temployer.faileprimarykey as error_primary_key:
            print(f"Primary key error: {error_primary_key}")
            cursor.connection.rollback()
        
        except Temployer.not_exist as error_not_exist:
            print(f"Not exist error: {error_not_exist}")
            cursor.connection.rollback()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e
    
    @classmethod
    def DeleteWorker(cls, NAME, ID):
        """Delete a worker from the 'Employerinput' table based on the provided name and ID."""
        try:
            cursor = cls.GetCursor()
            cursor.execute(sql.SQL("DELETE FROM Employerinput WHERE name=%s AND id=%s"), (NAME, ID))
            cursor.connection.commit()
        except psycopg2.Error as e:
            print(f"Error deleting worker: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e
    
    @classmethod
    def Update(cls, NAME, ID, KEYUPDATE, VALUEUPDATE):
        """Update a worker's data in the 'Employerinput' table."""
        try:
            Temployer.Employerinput.valor_presente(KEYUPDATE)
            cursor = cls.GetCursor()
            cursor.execute(sql.SQL("UPDATE Employerinput SET {}=%s WHERE name=%s AND id=%s").format(sql.Identifier(KEYUPDATE)), 
                           (VALUEUPDATE, NAME, ID))
            cursor.connection.commit()
        except Temployer.updatenotfount:
            pass
        except psycopg2.Error as e:
            print(f"Error updating worker: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e

    @classmethod
    def QueryWorker(cls, NAME, ID):
        """Query the data of a worker from the 'Employerinput' table based on the provided name and ID."""
        try:
            cursor = cls.GetCursor()
            cursor.execute(sql.SQL("SELECT * FROM Employerinput WHERE name=%s AND id=%s"), (NAME, ID))
            fila = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error querying worker: {e}")
            return None
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e

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

class WorkersoutputsData:
    
    @staticmethod
    def GetCursor():
        """Establishes connection to the database and returns a cursor for querying"""
        connection = psycopg2.connect(database=st.PGDATABASE, user=st.PGUSER, password=st.PGPASSWORD, host=st.PGHOST, port=st.PGPORT)
        cursor = connection.cursor()
        return cursor
    
    @classmethod
    def CreateTable(cls):
        """Creates the user table in the database"""
        try:
            cursor = cls.GetCursor()
            cursor.execute("""
                CREATE TABLE Employeroutput(
                    name VARCHAR(300) NOT NULL,
                    id VARCHAR(300) PRIMARY KEY NOT NULL,
                    basic_salary FLOAT NOT NULL,
                    workdays INT NOT NULL,
                    sick_leave INT NOT NULL,
                    transportation_aid FLOAT NOT NULL,
                    dayshift_extra_hours INT NOT NULL,
                    nightshift_extra_hours INT NOT NULL,
                    dayshift_extra_hours_holidays INT NOT NULL,
                    nightshift_extra_hours_holidays INT NOT NULL,
                    leave_days INT NOT NULL,
                    percentage_health_insurance FLOAT NOT NULL,
                    percentage_retirement_insurance FLOAT NOT NULL,
                    percentage_retirement_fund FLOAT NOT NULL,
                    devengado FLOAT NOT NULL,
                    deducido FLOAT NOT NULL,
                    amounttopay FLOAT NOT NULL
                );
            """)
            cursor.connection.commit()
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e

    @classmethod
    def Droptable(cls):
        """Drop the 'Employeroutput' table if it exists in the database."""
        try:
            cursor = cls.GetCursor()
            cursor.execute("DROP TABLE IF EXISTS Employeroutput")
            cursor.connection.commit()
        except psycopg2.Error as e:
            print(f"Error dropping table: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e
    
    @classmethod
    def PopulateTable(cls):
        """Populate the 'Employeroutput' table based on the data from the 'Employerinput' table.

           This function retrieves data from the 'Employerinput' table and calculates additional attributes 
           based on the provided data. It then inserts the calculated data into the 'Employeroutput' table."""
        try:
            cursor = cls.GetCursor()
            cursorWorkersIncomeData = WorkersIncomeData.GetCursor()
            cursorWorkersIncomeData.execute("SELECT * FROM Employerinput")
            employers = cursorWorkersIncomeData.fetchall()  # Obtener todas las filas

            for employer in employers:
                verificar_result_total = mp.SettlementParameters(employer[2], employer[3], employer[4], employer[5],
                                                                employer[6], employer[7], employer[8], employer[9], employer[10],
                                                                employer[11], employer[12], employer[13])
                cursor.execute(sql.SQL("""
                    INSERT INTO Employeroutput (name, id, basic_salary, workdays, sick_leave, transportation_aid, 
                                                dayshift_extra_hours, nightshift_extra_hours, dayshift_extra_hours_holidays, 
                                                nightshift_extra_hours_holidays, leave_days, percentage_health_insurance,
                                                percentage_retirement_insurance, percentage_retirement_fund, devengado, deducido, amounttopay)
                    
                    SELECT name, id, 
                           %s, -- basic_salary
                           monthly_worked_days, 
                           %s, -- leave_days
                           %s, -- transportation_allowance 
                           %s, -- daytime_overtime_hours
                           %s, -- nighttime_overtime_hours
                           %s, -- daytime_holiday_overtime_hours 
                           %s, -- nighttime_holiday_overtime_hours
                           %s, -- sick_leave_days
                           %s, -- health_contribution_percentage
                           %s, -- pension_contribution_percentage
                           %s, -- solidarity_pension_fund_contribution_percentage
                           %s, -- devengado 
                           %s, -- deducido
                           %s -- amounttopay 
                    FROM Employerinput WHERE name=%s AND id=%s
                """), (round(mp.calculate_salary(employer[2], employer[3], employer[4], employer[10]), 2), 
                       round(mp.calculate_leave(employer[2], employer[10]), 2), 
                       mp.calculate_transportation_aid(employer[5], employer[2]), 
                       round(mp.calculate_extra_hours(employer[2], employer[6], mp.EXTRA_HOUR_DAYSHIFT), 2), 
                       round(mp.calculate_extra_hours(employer[2], employer[7], mp.EXTRA_HOUR_NIGHTSHIFT), 2), 
                       round(mp.calculate_extra_hours(employer[2], employer[8], mp.EXTRA_HOUR_DAYSHIFT_HOLIDAYS), 2), 
                       round(mp.calculate_extra_hours(employer[2], employer[9], mp.EXTRA_HOUR_NIGHTSHIFT_HOLIDAYS), 2), 
                       round(mp.calculate_sick_leave(employer[2], employer[4]), 2), 
                       round(mp.calculate_health_insurance(employer[2], employer[11]), 2), 
                       round(mp.calculate_retirement_insurance(employer[2], employer[12]), 2), 
                       round(mp.calculate_retirement_fund(employer[2], employer[13]), 2), 
                       round(mp.calculate_accrued_values(verificar_result_total), 2), 
                       round(mp.calculate_deducted_values(verificar_result_total), 2), 
                       round(mp.calculate_settlement(verificar_result_total), 2), 
                       employer[0], employer[1]))
                cursor.connection.commit()
        except psycopg2.Error as e:
            print(f"Error populating table: {e}")
            cursor.connection.rollback()
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e

    @classmethod
    def QueryWorker(cls, NAME, ID):
        """Query the data of a worker from the 'Employeroutput' table based on the provided name and ID."""
        try:
            cursor = cls.GetCursor()
            cursor.execute(sql.SQL("SELECT * FROM Employeroutput WHERE name=%s AND id=%s"), (NAME, ID))
            fila = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error querying worker: {e}")
            return None
        except SystemExit as e:
            raise e
        except BaseException as e:
            print(f"Unexpected error: {e}")
            raise e

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

# Esta es la lista de campos y sus índices correspondiente
# 0. name
# 1. id
# 2. basic_salary
# 3. workdays
# 4. sick_leave
# 5. transportation_aid
# 6. dayshift_extra_hours
# 7. nightshift_extra_hours
# 8. dayshift_extra_hours_holidays
# 9. nightshift_extra_hours_holidays
# 10. leave_days
# 11. percentage_health_insurance
# 12. percentage_retirement_insurance
# 13. percentage_retirement_fund
# 14. devengado
# 15. deducido
# 16. amounttopay
