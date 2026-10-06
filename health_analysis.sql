CREATE DATABASE healthcare_db;

USE healthcare_db;
CREATE TABLE patients (
    Patient_ID VARCHAR(20) PRIMARY KEY,
    Patient_Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(20),
    City VARCHAR(50),
    Blood_Group VARCHAR(10),
    Admission_Date DATE,
    Discharge_Date DATE,
    Insurance_Type VARCHAR(50)
);
DESC doctors;

CREATE TABLE doctors (
    Doctor_ID VARCHAR(20) PRIMARY KEY,
    Doctor_Name VARCHAR(100),
    Department VARCHAR(100),
    Experience_Years INT,
    Consultation_Fee DECIMAL(10,2)
);

DROP TABLE doctors;

CREATE TABLE appointments (
    Appointment_ID VARCHAR(20) PRIMARY KEY,
    Patient_ID VARCHAR(20),
    Doctor_ID VARCHAR(20),
    Appointment_Date DATE,
    Appointment_Type VARCHAR(50),
    Wait_Time_Minutes INT,
    Appointment_Status VARCHAR(30),

    FOREIGN KEY (Patient_ID)
        REFERENCES patients(Patient_ID),

    FOREIGN KEY (Doctor_ID)
        REFERENCES doctors(Doctor_ID)
);


CREATE TABLE treatments (
    Treatment_ID VARCHAR(20) PRIMARY KEY,
    Appointment_ID VARCHAR(20),
    Diagnosis VARCHAR(100),
    Treatment_Type VARCHAR(100),
    Treatment_Duration_Days INT,
    Outcome VARCHAR(50),
    Readmission_Within_30_Days VARCHAR(10),

    FOREIGN KEY (Appointment_ID)
        REFERENCES appointments(Appointment_ID)
);


CREATE TABLE billing (
    Bill_ID VARCHAR(20) PRIMARY KEY,
    Appointment_ID VARCHAR(20),
    Total_Amount DECIMAL(12,2),
    Discount_Percent DECIMAL(5,2),
    Insurance_Coverage DECIMAL(12,2),
    Patient_Payment DECIMAL(12,2),
    Payment_Method VARCHAR(50),
    Payment_Status VARCHAR(30),	

    FOREIGN KEY (Appointment_ID)
        REFERENCES appointments(Appointment_ID)
);



SELECT COUNT(*) FROM patients;

SELECT COUNT(*) FROM doctors;

SELECT COUNT(*) FROM appointments;

SELECT COUNT(*) FROM treatments;

SELECT COUNT(*) FROM billing;

SELECT * FROM patients LIMIT 10;

SELECT * FROM doctors LIMIT 10;

SELECT * FROM patients LIMIT 5;

SELECT COUNT(*) AS Total_Patients FROM patients;

SELECT ROUND(AVG(Age),2) AS Average_Age FROM patients;

SELECT Gender, COUNT(*) AS Patient_Count FROM patients GROUP BY Gender;

SELECT City, COUNT(*) AS Patient_Count FROM patients GROUP BY City ORDER BY Patient_Count DESC;

SELECT Blood_Group, COUNT(*) AS Patient_Count FROM patients
GROUP BY Blood_Group
ORDER BY Patient_Count DESC;

SELECT COUNT(*) AS Total_Doctors
FROM doctors;

SELECT Department, COUNT(*) AS Doctor_Count
FROM doctors
GROUP BY Department
ORDER BY Doctor_Count DESC;

SELECT ROUND(AVG(Experience_Years),2) AS Average_Experience
FROM doctors;

SELECT * FROM doctors
ORDER BY Experience_Years DESC
LIMIT 1;

SELECT * FROM doctors
ORDER BY Consultation_Fee DESC
LIMIT 1;

SELECT COUNT(*) AS Total_Appointments
FROM appointments;

SELECT Appointment_Status, COUNT(*) AS Appointment_Count
FROM appointments
GROUP BY Appointment_Status
ORDER BY Appointment_Count DESC;

SELECT Appointment_Type,
    COUNT(*) AS Appointment_Count
FROM appointments
GROUP BY Appointment_Type
ORDER BY Appointment_Count DESC;

SELECT ROUND(AVG(Wait_Time_Minutes),2) AS Average_Wait_Time
FROM appointments;

SELECT
    ROUND(AVG(Wait_Time_Minutes),2) AS Average_Wait_Time
FROM appointments;

SELECT
    MAX(Wait_Time_Minutes) AS Maximum_Wait_Time
FROM appointments;

SELECT
    MIN(Wait_Time_Minutes) AS Minimum_Wait_Time
FROM appointments;

SELECT d.Department, COUNT(a.Appointment_ID) AS Total_Appointments
FROM appointments a
JOIN doctors d
    ON a.Doctor_ID = d.Doctor_ID
GROUP BY d.Department
ORDER BY Total_Appointments DESC;

SELECT
    d.Department,
    ROUND(AVG(a.Wait_Time_Minutes),2) AS Average_Wait_Time
FROM appointments a
JOIN doctors d
    ON a.Doctor_ID = d.Doctor_ID
GROUP BY d.Department
ORDER BY Average_Wait_Time DESC;

SELECT COUNT(*) AS Total_Treatments
FROM treatments;

SELECT
    Diagnosis,
    COUNT(*) AS Cases
FROM treatments
GROUP BY Diagnosis
ORDER BY Cases DESC;

SELECT
    Treatment_Type,
    COUNT(*) AS Treatment_Count
FROM treatments
GROUP BY Treatment_Type
ORDER BY Treatment_Count DESC;

SELECT
    Outcome,
    COUNT(*) AS Outcome_Count
FROM treatments
GROUP BY Outcome
ORDER BY Outcome_Count DESC;

SELECT
    COUNT(*) AS Readmission_Count
FROM treatments
WHERE Readmission_Within_30_Days = 'Yes';

SELECT ROUND(
        100 * SUM(
            CASE
                WHEN Readmission_Within_30_Days = 'Yes'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS Readmission_Rate_Percent
FROM treatments;

SELECT
    ROUND(SUM(Total_Amount),2) AS Total_Billing
FROM billing;

SELECT
    ROUND(SUM(Insurance_Coverage),2) AS Total_Insurance_Coverage
FROM billing;

SELECT
    ROUND(SUM(Patient_Payment),2) AS Total_Patient_Payment
FROM billing;

SELECT
    ROUND(AVG(Total_Amount),2) AS Average_Bill
FROM billing;

SELECT
    Payment_Method,
    COUNT(*) AS Transaction_Count,
    ROUND(SUM(Patient_Payment),2) AS Total_Payment
FROM billing
GROUP BY Payment_Method
ORDER BY Total_Payment DESC;

SELECT
    Payment_Status,
    COUNT(*) AS Payment_Count
FROM billing
GROUP BY Payment_Status;

SELECT
    t.Diagnosis,
    COUNT(*) AS Cases,
    ROUND(SUM(b.Total_Amount),2) AS Total_Revenue
FROM treatments t
JOIN appointments a
    ON t.Appointment_ID = a.Appointment_ID
JOIN billing b
    ON a.Appointment_ID = b.Appointment_ID
GROUP BY t.Diagnosis
ORDER BY Total_Revenue DESC;

SELECT
    d.Department,
    COUNT(b.Bill_ID) AS Total_Bills,
    ROUND(SUM(b.Total_Amount),2) AS Total_Revenue
FROM billing b
JOIN appointments a
    ON b.Appointment_ID = a.Appointment_ID
JOIN doctors d
    ON a.Doctor_ID = d.Doctor_ID
GROUP BY d.Department
ORDER BY Total_Revenue DESC;

SELECT
    d.Doctor_ID,
    d.Doctor_Name,
    d.Department,
    COUNT(a.Appointment_ID) AS Total_Appointments,
    ROUND(AVG(a.Wait_Time_Minutes),2) AS Avg_Wait_Time
FROM doctors d
LEFT JOIN appointments a
    ON d.Doctor_ID = a.Doctor_ID
GROUP BY
    d.Doctor_ID,
    d.Doctor_Name,
    d.Department
ORDER BY Total_Appointments DESC;

SELECT
    p.Patient_ID,
    p.Patient_Name,
    COUNT(a.Appointment_ID) AS Total_Appointments
FROM patients p
LEFT JOIN appointments a
    ON p.Patient_ID = a.Patient_ID
GROUP BY
    p.Patient_ID,
    p.Patient_Name
ORDER BY Total_Appointments DESC;

SELECT
    p.Patient_Name,
    d.Doctor_Name,
    d.Department,
    a.Appointment_Date,
    a.Appointment_Status
FROM patients p
JOIN appointments a
    ON p.Patient_ID = a.Patient_ID
JOIN doctors d
    ON a.Doctor_ID = d.Doctor_ID
LIMIT 20;

SELECT
    p.Patient_ID,
    p.Patient_Name,
    p.Age,
    p.Gender,
    p.City,
    p.Insurance_Type,

    a.Appointment_ID,
    a.Appointment_Date,
    a.Appointment_Type,
    a.Wait_Time_Minutes,
    a.Appointment_Status,

    d.Doctor_Name,
    d.Department,
    d.Experience_Years,

    t.Diagnosis,
    t.Treatment_Type,
    t.Treatment_Duration_Days,
    t.Outcome,
    t.Readmission_Within_30_Days,

    b.Total_Amount,
    b.Discount_Percent,
    b.Insurance_Coverage,
    b.Patient_Payment,
    b.Payment_Method,
    b.Payment_Status

FROM patients p

JOIN appointments a
    ON p.Patient_ID = a.Patient_ID

JOIN doctors d
    ON a.Doctor_ID = d.Doctor_ID

JOIN treatments t
    ON a.Appointment_ID = t.Appointment_ID

JOIN billing b
    ON a.Appointment_ID = b.Appointment_ID;
    
    
    
    SELECT
    YEAR(Appointment_Date) AS Year,
    MONTH(Appointment_Date) AS Month,
    COUNT(*) AS Total_Appointments
FROM appointments
GROUP BY
    YEAR(Appointment_Date),
    MONTH(Appointment_Date)
ORDER BY
    Year,
    Month;
    
    
    SELECT
    YEAR(a.Appointment_Date) AS Year,
    MONTH(a.Appointment_Date) AS Month,
    ROUND(SUM(b.Total_Amount),2) AS Total_Revenue
FROM appointments a
JOIN billing b
    ON a.Appointment_ID = b.Appointment_ID
GROUP BY
    YEAR(a.Appointment_Date),
    MONTH(a.Appointment_Date)
ORDER BY
    Year,
    Month;
    
    SELECT
    CASE
        WHEN Age < 18 THEN 'Below 18'
        WHEN Age BETWEEN 18 AND 30 THEN '18-30'
        WHEN Age BETWEEN 31 AND 45 THEN '31-45'
        WHEN Age BETWEEN 46 AND 60 THEN '46-60'
        ELSE '60+'
    END AS Age_Group,
    COUNT(*) AS Patient_Count
FROM patients
GROUP BY Age_Group
ORDER BY Patient_Count DESC;

SELECT
    d.Department,
    t.Diagnosis,
    COUNT(*) AS Cases
FROM doctors d
JOIN appointments a
    ON d.Doctor_ID = a.Doctor_ID
JOIN treatments t
    ON a.Appointment_ID = t.Appointment_ID
GROUP BY
    d.Department,
    t.Diagnosis
ORDER BY
    d.Department,
    Cases DESC;
    
    SELECT
    d.Department,
    t.Outcome,
    COUNT(*) AS Outcome_Count
FROM doctors d
JOIN appointments a
    ON d.Doctor_ID = a.Doctor_ID
JOIN treatments t
    ON a.Appointment_ID = t.Appointment_ID
GROUP BY
    d.Department,
    t.Outcome
ORDER BY
    d.Department;
    
    SELECT
    a.Appointment_ID,
    p.Patient_Name,
    d.Doctor_Name,
    d.Department,
    a.Wait_Time_Minutes
FROM appointments a
JOIN patients p
    ON a.Patient_ID = p.Patient_ID
JOIN doctors d
    ON a.Doctor_ID = d.Doctor_ID
WHERE a.Wait_Time_Minutes > 60
ORDER BY a.Wait_Time_Minutes DESC;

SELECT
    b.Bill_ID,
    p.Patient_Name,
    b.Total_Amount,
    b.Insurance_Coverage,
    b.Patient_Payment
FROM billing b
JOIN appointments a
    ON b.Appointment_ID = a.Appointment_ID
JOIN patients p
    ON a.Patient_ID = p.Patient_ID
ORDER BY b.Total_Amount DESC
LIMIT 10;

SELECT
    d.Doctor_Name,
    d.Department,
    COUNT(a.Appointment_ID) AS Total_Appointments
FROM doctors d
JOIN appointments a
    ON d.Doctor_ID = a.Doctor_ID
GROUP BY
    d.Doctor_ID,
    d.Doctor_Name,
    d.Department
ORDER BY Total_Appointments DESC
LIMIT 10;

SELECT
    Doctor_Name,
    Department,
    Experience_Years
FROM doctors
WHERE Experience_Years >= 15
ORDER BY Experience_Years DESC;

SELECT
    ROUND(
        100 * SUM(
            CASE
                WHEN Appointment_Status = 'Cancelled'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS Cancellation_Rate_Percent
FROM appointments;

SELECT
    ROUND(
        100 * SUM(
            CASE
                WHEN Outcome = 'Recovered'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS Recovery_Rate_Percent
FROM treatments;


SELECT
    p.Insurance_Type,
    COUNT(b.Bill_ID) AS Total_Bills,
    ROUND(SUM(b.Total_Amount),2) AS Total_Billing,
    ROUND(SUM(b.Insurance_Coverage),2) AS Insurance_Coverage,
    ROUND(SUM(b.Patient_Payment),2) AS Patient_Payment
FROM patients p
JOIN appointments a
    ON p.Patient_ID = a.Patient_ID
JOIN billing b
    ON a.Appointment_ID = b.Appointment_ID
GROUP BY p.Insurance_Type
ORDER BY Total_Billing DESC;

SELECT
    p.Patient_ID,
    p.Patient_Name,
    p.Age,
    p.Gender,
    p.City,
    p.Blood_Group,
    p.Insurance_Type,

    a.Appointment_ID,
    a.Appointment_Date,
    a.Appointment_Type,
    a.Wait_Time_Minutes,
    a.Appointment_Status,

    d.Doctor_ID,
    d.Doctor_Name,
    d.Department,
    d.Experience_Years,
    d.Consultation_Fee,

    t.Treatment_ID,
    t.Diagnosis,
    t.Treatment_Type,
    t.Treatment_Duration_Days,
    t.Outcome,
    t.Readmission_Within_30_Days,

    b.Bill_ID,
    b.Total_Amount,
    b.Discount_Percent,
    b.Insurance_Coverage,
    b.Patient_Payment,
    b.Payment_Method,
    b.Payment_Status

FROM patients p
LEFT JOIN appointments a
    ON p.Patient_ID = a.Patient_ID

LEFT JOIN doctors d
    ON a.Doctor_ID = d.Doctor_ID

LEFT JOIN treatments t
    ON a.Appointment_ID = t.Appointment_ID

LEFT JOIN billing b
    ON a.Appointment_ID = b.Appointment_ID;