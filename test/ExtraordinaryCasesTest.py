import unittest
import sys
import os

# Agregar el directorio padre al path para permitir importaciones relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.Model.MonthlyPaymentLogic as mp


class MonthlyPaymentExtraordinary(unittest.TestCase):

    def test_over_time_hours_at_night(self):
        # Input data
        basic_salary = 2700000
        workdays = 30
        sick_leave = 0
        transportation_aid = 0
        dayshift_extra_hours = 0
        nightshift_extra_hours = 4
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 3
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        # Expected output data
        total_to_pay = 2650595.74  # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)

    def test_evaluate_case_license(self):
        # Input data
        basic_salary = 2800000
        workdays = 12
        sick_leave = 0
        transportation_aid = 0
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 18
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        # Expected output data
        total_to_pay = 2576000  # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)

    def test_evaluate_disability_case(self):
        # Input data
        basic_salary = 2000000
        workdays = 28
        sick_leave = 2
        transportation_aid = 0
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 0
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        # Expected output data
        total_to_pay = 1840000  # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)

    def test_evaluate_dayshift_overtime(self):
        # Input data
        basic_salary = 1300000
        workdays = 30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 6
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 8
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        # Expected output data
        total_to_pay = 1486000  # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)

    def test_evaluate_salaries_above_five_min_wages(self):
        # Input data
        basic_salary = 10000000
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
        percentage_retirement_fund = 0.01

        # Expected output data
        total_to_pay = 8629290.51 # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)

    def test_evaluate_extra_hours_and_subsidies(self):
        # Input data
        basic_salary = 2200000
        workdays = 14
        sick_leave = 1
        transportation_aid = 160000
        dayshift_extra_hours = 4
        nightshift_extra_hours = 5
        dayshift_extra_hours_holidays = 7
        nightshift_extra_hours_holidays = 4
        leave_days = 15
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.04
        percentage_retirement_fund = 0

        # Expected output data
        total_to_pay = 2537404.26  # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)

    def test_evaluate_no_pension_contribution(self):
        # Input data
        basic_salary = 1941365
        workdays = 30
        sick_leave = 0
        transportation_aid = 160000
        dayshift_extra_hours = 0
        nightshift_extra_hours = 0
        dayshift_extra_hours_holidays = 6
        nightshift_extra_hours_holidays = 0
        leave_days = 0
        percentage_health_insurance = 0.04
        percentage_retirement_insurance = 0.0
        percentage_retirement_fund = 0

        # Expected output data
        total_to_pay = 2122843.93  # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)

    def test_evaluate_salary_between_zero_and_one_million(self):
        # Input data
        basic_salary = 800000
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

        # Expected output data
        total_to_pay = 896000  # Total to pay

        # Process
        # We create a SettlementParameters object with the input data.
        settlement_params = mp.SettlementParameters(basic_salary, workdays, sick_leave, transportation_aid,
                                                    dayshift_extra_hours,
                                                    nightshift_extra_hours, dayshift_extra_hours_holidays,
                                                    nightshift_extra_hours_holidays,
                                                    leave_days, percentage_health_insurance,
                                                    percentage_retirement_insurance, percentage_retirement_fund)

        # We call the calculate_settlement function with the SettlementParameters object.
        result_total_to_pay = mp.calculate_settlement(settlement_params)

        # We compare the result with the expected value using self.assertEqual.
        self.assertAlmostEqual(total_to_pay, result_total_to_pay, places=2)


if __name__ == '__main__':
    unittest.main()