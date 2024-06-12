import unittest
import sys
import os

# Agregar el directorio padre al path para permitir importaciones relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.Model.MonthlyPaymentLogic as mp
from src.Controller.Controladortablas import WorkersIncomeData, WorkersoutputsData
import src.Model.TablesEmployer as Temployer


class ControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Llamar a la clase Controlador para que cree la tabla
        WorkersIncomeData.drop_table()
        WorkersIncomeData.create_table()
        WorkersoutputsData.drop_table()
        WorkersoutputsData.create_table()

    def testinsertemployer(self):
        employer = Temployer.Employerinput(
            name='juana', id='10013', basic_salary=6000000, monthly_worked_days=30, days_leave=0,
            transportation_allowance=0, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.04,
            pension_contribution_percentage=0.04, solidarity_pension_fund_contribution_percentage=0.01
        )
        WorkersIncomeData.insert(employer)
        findemployer = WorkersIncomeData.query_worker(employer.name, employer.id)
        self.assertTrue(findemployer.Isequal(employer))

    def testupdateworkers(self):
        employer = Temployer.Employerinput(
            name='ROSA', id='100000', basic_salary=2000000, monthly_worked_days=20, days_leave=0,
            transportation_allowance=160000, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.04,
            pension_contribution_percentage=0.04, solidarity_pension_fund_contribution_percentage=0
        )
        WorkersIncomeData.insert(employer)
        KEYUPDATE = "monthly_worked_days"
        VALUEUPDATE = 30
        # Actualizar el valor del atributo correspondiente utilizando setattr
        setattr(employer, KEYUPDATE, VALUEUPDATE)
        WorkersIncomeData.Update(employer.name, employer.id, KEYUPDATE=KEYUPDATE, VALUEUPDATE=VALUEUPDATE)
        findemployer = WorkersIncomeData.query_worker(employer.name, employer.id)
        self.assertTrue(findemployer.Isequal(employer))

    def testdeleteworkers(self):
        employer = Temployer.Employerinput(
            name='PePe', id='100000', basic_salary=5000000, monthly_worked_days=20, days_leave=0,
            transportation_allowance=0, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.4,
            pension_contribution_percentage=0.4, solidarity_pension_fund_contribution_percentage=4
        )
        WorkersIncomeData.insert(employer)
        WorkersIncomeData.delete_worker(employer.name, employer.id)
        findemployer = WorkersIncomeData.query_worker(employer.name, employer.id)
        self.assertIsNone(findemployer)

    def testprovesalary(self):
        employer = Temployer.Employerinput(
            name='bruno', id='1000000', basic_salary=1600000, monthly_worked_days=30, days_leave=0,
            transportation_allowance=160000, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.04,
            pension_contribution_percentage=0.04, solidarity_pension_fund_contribution_percentage=0
        )
        WorkersIncomeData.insert(employer)
        WorkersoutputsData.PopulateTable()
        findoutput = WorkersoutputsData.query_worker(employer.name, employer.id)
        employeroutputsData = Temployer.Employeroutput(
            name='bruno', id='1000000', basic_salary=1600000, workdays=30, sick_leave=0, transportation_aid=160000,
            dayshift_extra_hours=0, nightshift_extra_hours=0, dayshift_extra_hours_holidays=0,
            nightshift_extra_hours_holidays=0, leave_days=0, percentage_health_insurance=64000,
            percentage_retirement_insurance=64000, percentage_retirement_fund=0,
            devengado=1760000, deducido=128000, amounttopay=1632000
        )
        self.assertTrue(employeroutputsData.Isequivalent(findoutput))

    def testerrorprimarykey(self):
        name_employer = 'robert'
        id = '430380'
        employer = Temployer.Employerinput(
            name=name_employer, id=id, basic_salary=1600000, monthly_worked_days=30, days_leave=0,
            transportation_allowance=160000, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.04,
            pension_contribution_percentage=0.04, solidarity_pension_fund_contribution_percentage=0
        )
        WorkersIncomeData.insert(employer)

        employer_repeat = Temployer.Employerinput(
            name=name_employer, id=id, basic_salary=1600000, monthly_worked_days=30, days_leave=0,
            transportation_allowance=160000, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.04,
            pension_contribution_percentage=0.04, solidarity_pension_fund_contribution_percentage=0
        )
        with self.assertRaises(Temployer.faileprimarykey):
            Temployer.Employerinput.primary_key(employer_repeat.name, employer_repeat.id, WorkersIncomeData)

    def testfaultdata(self):
        employer = Temployer.Employerinput(
            name='joselu', id='1234', basic_salary=None, monthly_worked_days=30, days_leave=0,
            transportation_allowance=160000, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.04,
            pension_contribution_percentage=0.04, solidarity_pension_fund_contribution_percentage=0
        )
        with self.assertRaises(Temployer.not_exist):
            Temployer.Employerinput.notexist(employer)

    def testinfonotfound(self):
        busqueda = WorkersoutputsData.query_worker("neuer", "15151515")
        with self.assertRaises(Temployer.not_found):
            Temployer.Employeroutput.employernotfound(busqueda)

    def testerrorupdateEmployerinput(self):
        employer = Temployer.Employerinput(
            name='jhosepe', id='09879878', basic_salary=2000000, monthly_worked_days=20, days_leave=0,
            transportation_allowance=160000, daytime_overtime_hours=0,
            nighttime_overtime_hours=0, daytime_holiday_overtime_hours=0,
            nighttime_holiday_overtime_hours=0, sick_leave_days=0, health_contribution_percentage=0.04,
            pension_contribution_percentage=0.04, solidarity_pension_fund_contribution_percentage=0
        )
        WorkersIncomeData.insert(employer)
        KEYUPDATE = "monthly_worked_ds"  # copia mal el days
        VALUEUPDATE = 30
        # Actualizar el valor del atributo correspondiente utilizando setattr
        setattr(employer, KEYUPDATE, VALUEUPDATE)
        WorkersIncomeData.Update(employer.name, employer.id, KEYUPDATE=KEYUPDATE, VALUEUPDATE=VALUEUPDATE)
        with self.assertRaises(Temployer.updatenotfount):
            Temployer.Employerinput.valor_presente(KEYUPDATE)


if __name__ == '__main__':
    unittest.main()
