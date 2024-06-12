import unittest
import sys
import os

# Agregar el directorio padre al path para permitir importaciones relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.Model.MonthlyPaymentLogic as mp
import src.Model.MonthlyPaymentLogic as mp

# We create the class that will contain the unit tests.
class TestMonthlyPayment(unittest.TestCase):

    def test_regular_case_one(self):
        # Input data
        basic_salary = 1600000
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
        total_to_pay = 1632000  # Total to pay

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

        # We compare the result with the expected value using self.assertAlmostEqual.
        self.assertAlmostEqual(total_to_pay, round(result_total_to_pay, 2))

    def test_regular_case_two(self):
        # Input data
        basic_salary = 2800000
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

        # We compare the result with the expected value using self.assertAlmostEqual.
        self.assertAlmostEqual(total_to_pay, round(result_total_to_pay, 2))

    def test_regular_case_three(self):
        # Input data
        basic_salary = 1400000
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
        total_to_pay = 1448000  # Total to pay

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

        # We compare the result with the expected value using self.assertAlmostEqual.
        self.assertAlmostEqual(total_to_pay, round(result_total_to_pay, 2))

    def test_regular_case_four(self):
        # Input data
        basic_salary = 1300000
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
        total_to_pay = 1356000  # Total to pay

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

        # We compare the result with the expected value using self.assertAlmostEqual.
        self.assertAlmostEqual(total_to_pay, round(result_total_to_pay, 2))

    def test_regular_case_five(self):
        # Input data
        basic_salary = 2300000
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

        # Expected output data
        total_to_pay = 2116000  # Total to pay

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

        # We compare the result with the expected value using self.assertAlmostEqual.
        self.assertAlmostEqual(total_to_pay, round(result_total_to_pay, 2))

    def test_regular_case_six(self):
        # Input data
        basic_salary = 2800000
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

        # We compare the result with the expected value using self.assertAlmostEqual.
        self.assertAlmostEqual(total_to_pay, round(result_total_to_pay, 2))


if __name__ == '__main__':
    unittest.main()