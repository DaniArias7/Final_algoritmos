import unittest
import sys
import os

# Agregar el directorio padre al path para permitir importaciones relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.Model.MonthlyPaymentLogic as mp

class MonthlyPaymentExtraordinary(unittest.TestCase):

    def test_zero_salary_error(self):
        # Test case to check if LowerMinimumWageError is raised when the basic salary is zero
        # Input data
        basic_salary = 0
        workdays = 30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if LowerMinimumWageError is raised
        self.assertRaises(mp.LowerMinimumWageError, mp.calculate_settlement, settlement_params)

    def test_zero_time_work_error(self):
        # Test case to check if NoWorkDaysError is raised when workdays is zero
        # Input data
        basic_salary = 1779801
        workdays = 0
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if NoWorkDaysError is raised
        self.assertRaises(mp.NoWorkDaysError, mp.calculate_settlement, settlement_params)

    def test_zero_health_contribution_error(self):
        # Test case to check if InvalidHealthInsurancePercentageError is raised when health insurance percentage is zero
        # Input data
        basic_salary = 2746252
        workdays = 30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.00
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if InvalidHealthInsurancePercentageError is raised
        self.assertRaises(mp.InvalidHealthInsurancePercentageError, mp.calculate_settlement, settlement_params)

    def test_invalid_retirement_fund_percentage_error(self):
        # Test case to check if InvalidRetirementFundPercentageError is raised when retirement fund percentage is zero for salaries above 5,000,000
        # Input data
        basic_salary = 6372589
        workdays = 30
        sick_leave = 0
        transportation_aid = 0
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if InvalidRetirementFundPercentageError is raised
        self.assertRaises(mp.InvalidRetirementFundPercentageError, mp.calculate_settlement, settlement_params)

    def test_invalid_retirement_fund_percentage_error_salary_menor(self):
        # Test case to check if InvalidRetirementFundPercentageErrorSalaryMenor is raised when retirement fund percentage is not zero for salaries below 5,000,000
        # Input data
        basic_salary = 2360465
        workdays = 30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0.01

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if InvalidRetirementFundPercentageErrorSalaryMenor is raised
        self.assertRaises(mp.InvalidRetirementFundPercentageErrorSalaryMenor, mp.calculate_settlement, settlement_params)

    def test_invalid_transportation_aid_error(self):
        # Test case to check if InvalidTransportationAidError is raised when transportation aid is not zero for salaries above 2,600,000
        # Input data
        basic_salary = 5243695
        workdays = 30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0.01

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if InvalidTransportationAidError is raised
        self.assertRaises(mp.InvalidTransportationAidError, mp.calculate_settlement, settlement_params)

    def test_sintaxis_error(self):
        # Test case to check if SintaxiError is raised when basic salary is not an integer or float
        # Input data
        basic_salary = "Dos millones"
        workdays = 30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if SintaxiError is raised
        self.assertRaises(mp.SintaxiError, mp.calculate_settlement, settlement_params)

    def test_negatived_day_work(self):
        # Test case to check if NegativedayWork is raised when workdays is negative
        # Input data
        basic_salary = 1300000
        workdays = -30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # Use assertRaises to verify if NegativedayWork is raised
        self.assertRaises(mp.NegativedayWork, mp.calculate_settlement, settlement_params)

if __name__ == '__main__':
    unittest.main()