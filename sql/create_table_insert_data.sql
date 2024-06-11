CREATE TABLE Employerinput(
    name VARCHAR2(300) NOT NULL,
    id VARCHAR2(300) PRIMARY KEY NOT NULL,
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
