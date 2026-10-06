# ==============================================================
# HEALTHCARE DATA ANALYTICS & PATIENT INTELLIGENCE SYSTEM
# ==============================================================
# Technologies:
# Python | Pandas | NumPy | Matplotlib | Seaborn | MySQL
# ==============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector


# ==============================================================
# GLOBAL VARIABLES
# ==============================================================

patients = None
doctors = None
appointments = None
treatments = None
billing = None

connection = None
cursor = None


# ==============================================================
# DATABASE CONNECTION
# ==============================================================

def connect_database():

    global connection
    global cursor

    print("\n" + "=" * 70)
    print("                    DATABASE CONNECTION")
    print("=" * 70)

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="venky123",
            database="healthcare_db"
        )

        cursor = connection.cursor()

        print("\n✓ MySQL Database Connected Successfully")
        print("✓ Database: healthcare_db")

        return True

    except Exception as e:

        print("\n✗ Database Connection Failed")
        print("Error:", e)

        return False


# ==============================================================
#LOAD CSV DATA
# ==============================================================

def load_data():

    global patients
    global doctors
    global appointments
    global treatments
    global billing

    print("\n" + "=" * 70)
    print("                     LOADING DATA")
    print("=" * 70)

    try:

        patients = pd.read_csv("patients.csv")
        doctors = pd.read_csv("doctors.csv")
        appointments = pd.read_csv("appointments.csv")
        treatments = pd.read_csv("treatments.csv")
        billing = pd.read_csv("billing.csv")

        print("\n✓ Patients data loaded")
        print("✓ Doctors data loaded")
        print("✓ Appointments data loaded")
        print("✓ Treatments data loaded")
        print("✓ Billing data loaded")

        return True

    except Exception as e:

        print("\n✗ Error while loading CSV files")
        print("Error:", e)

        return False


# ==============================================================
# DATA CLEANING
# ==============================================================

def clean_data():

    global patients
    global doctors
    global appointments
    global treatments
    global billing

    print("\n" + "=" * 70)
    print("                     DATA CLEANING")
    print("=" * 70)

    # Convert dates

    patients["Admission_Date"] = pd.to_datetime(
        patients["Admission_Date"],
        errors="coerce"
    )

    patients["Discharge_Date"] = pd.to_datetime(
        patients["Discharge_Date"],
        errors="coerce"
    )

    appointments["Appointment_Date"] = pd.to_datetime(
        appointments["Appointment_Date"],
        errors="coerce"
    )

    # Remove duplicates

    patients.drop_duplicates(inplace=True)
    doctors.drop_duplicates(inplace=True)
    appointments.drop_duplicates(inplace=True)
    treatments.drop_duplicates(inplace=True)
    billing.drop_duplicates(inplace=True)

    print("\n✓ Duplicate records checked")
    print("✓ Date columns converted")
    print("✓ Data cleaning completed successfully")


# ==============================================================
#DATASET SUMMARY
# ==============================================================

def dataset_summary():

    print("\n" + "=" * 70)
    print("                     DATASET SUMMARY")
    print("=" * 70)

    print(f"\nPatients        : {len(patients):,}")
    print(f"Doctors         : {len(doctors):,}")
    print(f"Appointments    : {len(appointments):,}")
    print(f"Treatments      : {len(treatments):,}")
    print(f"Billing Records : {len(billing):,}")

    total_records = (
        len(patients)
        + len(doctors)
        + len(appointments)
        + len(treatments)
        + len(billing)
    )

    print(f"\nTotal Records   : {total_records:,}")


# ==============================================================
#DATA QUALITY CHECK
# ==============================================================

def data_quality_check():

    print("\n" + "=" * 70)
    print("                     DATA QUALITY CHECK")
    print("=" * 70)

    patient_missing = patients.isnull().sum().sum()
    doctor_missing = doctors.isnull().sum().sum()
    appointment_missing = appointments.isnull().sum().sum()
    treatment_missing = treatments.isnull().sum().sum()
    billing_missing = billing.isnull().sum().sum()

    print("\nMissing Values:")

    print(f"Patients       : {patient_missing}")
    print(f"Doctors        : {doctor_missing}")
    print(f"Appointments   : {appointment_missing}")
    print(f"Treatments     : {treatment_missing}")
    print(f"Billing        : {billing_missing}")

    print("\n✓ Data quality check completed")


# ==============================================================
#PATIENT ANALYSIS
# ==============================================================

def patient_analysis():

    print("\n" + "=" * 70)
    print("                     PATIENT ANALYSIS")
    print("=" * 70)

    total_patients = len(patients)

    average_age = patients["Age"].mean()

    print(f"\nTotal Patients      : {total_patients:,}")
    print(f"Average Patient Age : {average_age:.1f} years")

    # Gender

    print("\n--- Gender Distribution ---")

    gender_count = patients["Gender"].value_counts()

    for gender, count in gender_count.items():

        percentage = (count / total_patients) * 100

        print(
            f"{gender:<15} : "
            f"{count:,} patients ({percentage:.1f}%)"
        )

    # City

    print("\n--- Top 5 Cities ---")

    city_count = patients["City"].value_counts()

    for city, count in city_count.head(5).items():

        print(
            f"{city:<20} : {count:,} patients"
        )

    # Blood Group

    print("\n--- Blood Group Distribution ---")

    blood_count = patients["Blood_Group"].value_counts()

    for blood_group, count in blood_count.items():

        print(
            f"{blood_group:<10} : {count:,}"
        )

    # Insurance

    print("\n--- Insurance Distribution ---")

    insurance_count = patients["Insurance_Type"].value_counts()

    for insurance, count in insurance_count.items():

        print(
            f"{insurance:<20} : {count:,}"
        )


# ==============================================================
#DOCTOR ANALYSIS
# ==============================================================

def doctor_analysis():

    print("\n" + "=" * 70)
    print("                     DOCTOR ANALYSIS")
    print("=" * 70)

    total_doctors = len(doctors)

    average_experience = doctors["Experience_Years"].mean()

    print(f"\nTotal Doctors       : {total_doctors:,}")
    print(f"Average Experience : {average_experience:.1f} years")

    # Department

    print("\n--- Doctors by Department ---")

    department_count = doctors["Department"].value_counts()

    for department, count in department_count.items():

        print(
            f"{department:<20} : {count:,} doctors"
        )

    # Highest Experience

    highest_experience = doctors.loc[
        doctors["Experience_Years"].idxmax()
    ]

    print("\n--- Most Experienced Doctor ---")

    print(
        f"Doctor     : {highest_experience['Doctor_Name']}"
    )

    print(
        f"Department : {highest_experience['Department']}"
    )

    print(
        f"Experience : {highest_experience['Experience_Years']} years"
    )

    # Highest Consultation Fee

    highest_fee = doctors.loc[
        doctors["Consultation_Fee"].idxmax()
    ]

    print("\n--- Highest Consultation Fee ---")

    print(
        f"Doctor     : {highest_fee['Doctor_Name']}"
    )

    print(
        f"Department : {highest_fee['Department']}"
    )

    print(
        f"Consultation Fee : ₹{highest_fee['Consultation_Fee']:,.2f}"
    )


# ==============================================================
#APPOINTMENT ANALYSIS
# ==============================================================

def appointment_analysis():

    print("\n" + "=" * 70)
    print("                  APPOINTMENT ANALYSIS")
    print("=" * 70)

    total_appointments = len(appointments)

    average_wait = appointments[
        "Wait_Time_Minutes"
    ].mean()

    maximum_wait = appointments[
        "Wait_Time_Minutes"
    ].max()

    minimum_wait = appointments[
        "Wait_Time_Minutes"
    ].min()

    print(
        f"\nTotal Appointments   : {total_appointments:,}"
    )

    print(
        f"Average Waiting Time : {average_wait:.1f} minutes"
    )

    print(
        f"Maximum Waiting Time : {maximum_wait:.0f} minutes"
    )

    print(
        f"Minimum Waiting Time : {minimum_wait:.0f} minutes"
    )

    # Status

    print("\n--- Appointment Status ---")

    status_count = appointments[
        "Appointment_Status"
    ].value_counts()

    for status, count in status_count.items():

        percentage = (
            count / total_appointments
        ) * 100

        print(
            f"{status:<15} : "
            f"{count:,} ({percentage:.1f}%)"
        )

    # Type

    print("\n--- Appointment Type ---")

    type_count = appointments[
        "Appointment_Type"
    ].value_counts()

    for appointment_type, count in type_count.items():

        print(
            f"{appointment_type:<20} : {count:,}"
        )


# ==============================================================
#DEPARTMENT PERFORMANCE
# ==============================================================

def department_analysis():

    print("\n" + "=" * 70)
    print("                  DEPARTMENT PERFORMANCE")
    print("=" * 70)

    appointment_doctor = appointments.merge(
        doctors,
        on="Doctor_ID",
        how="left"
    )

    department_performance = appointment_doctor.groupby(
        "Department"
    ).agg(
        Total_Appointments=(
            "Appointment_ID",
            "count"
        ),

        Average_Wait_Time=(
            "Wait_Time_Minutes",
            "mean"
        )
    ).sort_values(
        "Total_Appointments",
        ascending=False
    )

    print()

    for department, row in department_performance.iterrows():

        print(
            f"{department:<20} | "
            f"Appointments: "
            f"{int(row['Total_Appointments']):>5} | "
            f"Avg Wait: "
            f"{row['Average_Wait_Time']:.1f} mins"
        )


# ==============================================================
#TREATMENT ANALYSIS
# ==============================================================

def treatment_analysis():

    print("\n" + "=" * 70)
    print("                     TREATMENT ANALYSIS")
    print("=" * 70)

    total_treatments = len(treatments)

    print(
        f"\nTotal Treatments : {total_treatments:,}"
    )

    # Diseases

    print("\n--- Top 10 Diagnoses ---")

    disease_count = treatments[
        "Diagnosis"
    ].value_counts()

    for disease, count in disease_count.head(10).items():

        print(
            f"{disease:<25} : {count:,} cases"
        )

    # Treatment Type

    print("\n--- Treatment Types ---")

    treatment_count = treatments[
        "Treatment_Type"
    ].value_counts()

    for treatment, count in treatment_count.items():

        print(
            f"{treatment:<25} : {count:,}"
        )

    # Outcome

    print("\n--- Treatment Outcomes ---")

    outcome_count = treatments[
        "Outcome"
    ].value_counts()

    for outcome, count in outcome_count.items():

        percentage = (
            count / total_treatments
        ) * 100

        print(
            f"{outcome:<20} : "
            f"{count:,} ({percentage:.1f}%)"
        )


# ==============================================================
# READMISSION ANALYSIS
# ==============================================================

def readmission_analysis():

    print("\n" + "=" * 70)
    print("                   READMISSION ANALYSIS")
    print("=" * 70)

    total_treatments = len(treatments)

    readmission_count = (
        treatments[
            "Readmission_Within_30_Days"
        ]
        .astype(str)
        .str.lower()
        .eq("yes")
        .sum()
    )

    readmission_rate = (
        readmission_count
        / total_treatments
    ) * 100

    print(
        f"\nReadmissions within 30 Days : "
        f"{readmission_count:,}"
    )

    print(
        f"Readmission Rate            : "
        f"{readmission_rate:.2f}%"
    )


# ==============================================================
# BILLING ANALYSIS
# ==============================================================

def billing_analysis():

    print("\n" + "=" * 70)
    print("                     BILLING ANALYSIS")
    print("=" * 70)

    total_billing = billing[
        "Total_Amount"
    ].sum()

    total_insurance = billing[
        "Insurance_Coverage"
    ].sum()

    total_patient_payment = billing[
        "Patient_Payment"
    ].sum()

    average_bill = billing[
        "Total_Amount"
    ].mean()

    print(
        f"\nTotal Billing Amount : "
        f"₹{total_billing:,.2f}"
    )

    print(
        f"Insurance Coverage  : "
        f"₹{total_insurance:,.2f}"
    )

    print(
        f"Patient Payment     : "
        f"₹{total_patient_payment:,.2f}"
    )

    print(
        f"Average Bill Amount : "
        f"₹{average_bill:,.2f}"
    )

    # Payment Method

    print("\n--- Payment Methods ---")

    payment_method = billing[
        "Payment_Method"
    ].value_counts()

    for method, count in payment_method.items():

        print(
            f"{method:<20} : {count:,}"
        )

    # Payment Status

    print("\n--- Payment Status ---")

    payment_status = billing[
        "Payment_Status"
    ].value_counts()

    for status, count in payment_status.items():

        print(
            f"{status:<20} : {count:,}"
        )


# ==============================================================
# REVENUE ANALYSIS
# ==============================================================

def revenue_analysis():

    print("\n" + "=" * 70)
    print("                     REVENUE ANALYSIS")
    print("=" * 70)

    billing_appointment = billing.merge(
        appointments,
        on="Appointment_ID",
        how="left"
    )

    billing_department = billing_appointment.merge(
        doctors[
            ["Doctor_ID", "Department"]
        ],
        on="Doctor_ID",
        how="left"
    )

    department_revenue = billing_department.groupby(
        "Department"
    )["Total_Amount"].sum().sort_values(
        ascending=False
    )

    print("\n--- Revenue by Department ---")

    for department, revenue in department_revenue.items():

        print(
            f"{department:<20} : "
            f"₹{revenue:,.2f}"
        )

    # Disease Revenue

    treatment_appointment = treatments.merge(
        appointments,
        on="Appointment_ID",
        how="left"
    )

    disease_revenue = treatment_appointment.merge(
        billing[
            [
                "Appointment_ID",
                "Total_Amount"
            ]
        ],
        on="Appointment_ID",
        how="left"
    )

    disease_revenue = disease_revenue.groupby(
        "Diagnosis"
    )["Total_Amount"].sum().sort_values(
        ascending=False
    )

    print("\n--- Top 10 Diagnoses by Revenue ---")

    for disease, revenue in disease_revenue.head(10).items():

        print(
            f"{disease:<25} : "
            f"₹{revenue:,.2f}"
        )


# ==============================================================
# MONTHLY TREND ANALYSIS
# ==============================================================

def monthly_analysis():

    print("\n" + "=" * 70)
    print("                  MONTHLY APPOINTMENT TREND")
    print("=" * 70)

    temp_data = appointments.copy()

    temp_data["Month"] = (
        temp_data[
            "Appointment_Date"
        ]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = temp_data.groupby(
        "Month"
    ).size()

    print()

    for month, count in monthly.items():

        print(
            f"{month:<10} : "
            f"{count:,} appointments"
        )


# ==============================================================
# KEY BUSINESS INSIGHTS
# ==============================================================

def key_insights():

    print("\n" + "=" * 70)
    print("                    KEY BUSINESS INSIGHTS")
    print("=" * 70)

    total_patients = len(patients)

    average_age = patients[
        "Age"
    ].mean()

    average_wait = appointments[
        "Wait_Time_Minutes"
    ].mean()

    total_revenue = billing[
        "Total_Amount"
    ].sum()

    top_city = patients[
        "City"
    ].value_counts().idxmax()

    top_disease = treatments[
        "Diagnosis"
    ].value_counts().idxmax()

    busiest_department = (
        appointments
        .merge(
            doctors,
            on="Doctor_ID",
            how="left"
        )
        ["Department"]
        .value_counts()
        .idxmax()
    )

    top_payment_method = billing[
        "Payment_Method"
    ].value_counts().idxmax()

    readmission_count = (
        treatments[
            "Readmission_Within_30_Days"
        ]
        .astype(str)
        .str.lower()
        .eq("yes")
        .sum()
    )

    readmission_rate = (
        readmission_count
        / len(treatments)
    ) * 100

    print(
        f"\n1. Total Patients              : "
        f"{total_patients:,}"
    )

    print(
        f"2. Average Patient Age         : "
        f"{average_age:.1f} years"
    )

    print(
        f"3. Highest Patient City        : "
        f"{top_city}"
    )

    print(
        f"4. Most Common Diagnosis       : "
        f"{top_disease}"
    )

    print(
        f"5. Busiest Department          : "
        f"{busiest_department}"
    )

    print(
        f"6. Average Waiting Time        : "
        f"{average_wait:.1f} minutes"
    )

    print(
        f"7. Total Healthcare Revenue    : "
        f"₹{total_revenue:,.2f}"
    )

    print(
        f"8. Most Used Payment Method   : "
        f"{top_payment_method}"
    )

    print(
        f"9. Readmission Rate            : "
        f"{readmission_rate:.2f}%"
    )


# ==============================================================
# CREATE CHARTS
# ==============================================================

def generate_charts():

    print("\n" + "=" * 70)
    print("                    GENERATING CHARTS")
    print("=" * 70)

    # ----------------------------------------------------------
    # Chart 1 - Gender
    # ----------------------------------------------------------

    plt.figure(figsize=(7, 5))

    patients[
        "Gender"
    ].value_counts().plot(
        kind="bar"
    )

    plt.title(
        "Patient Distribution by Gender"
    )

    plt.xlabel("Gender")
    plt.ylabel("Number of Patients")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.show()


    # ----------------------------------------------------------
    # Chart 2 - Top Diseases
    # ----------------------------------------------------------

    plt.figure(figsize=(9, 5))

    treatments[
        "Diagnosis"
    ].value_counts().head(10).plot(
        kind="bar"
    )

    plt.title(
        "Top 10 Diseases / Diagnoses"
    )

    plt.xlabel("Diagnosis")
    plt.ylabel("Number of Cases")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


    # ----------------------------------------------------------
    # Chart 3 - Appointment Status
    # ----------------------------------------------------------

    plt.figure(figsize=(7, 5))

    appointments[
        "Appointment_Status"
    ].value_counts().plot(
        kind="bar"
    )

    plt.title(
        "Appointment Status Analysis"
    )

    plt.xlabel("Appointment Status")
    plt.ylabel("Number of Appointments")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.show()


    # ----------------------------------------------------------
    # Chart 4 - Department
    # ----------------------------------------------------------

    department_data = appointments.merge(
        doctors,
        on="Doctor_ID",
        how="left"
    )

    department_count = (
        department_data[
            "Department"
        ]
        .value_counts()
    )

    plt.figure(figsize=(10, 5))

    department_count.plot(
        kind="bar"
    )

    plt.title(
        "Appointments by Department"
    )

    plt.xlabel("Department")
    plt.ylabel("Number of Appointments")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


    # ----------------------------------------------------------
    # Chart 5 - Treatment Outcome
    # ----------------------------------------------------------

    plt.figure(figsize=(7, 5))

    treatments[
        "Outcome"
    ].value_counts().plot(
        kind="bar"
    )

    plt.title(
        "Treatment Outcome Analysis"
    )

    plt.xlabel("Outcome")
    plt.ylabel("Number of Treatments")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.show()


    # ----------------------------------------------------------
    # Chart 6 - Payment Method
    # ----------------------------------------------------------

    plt.figure(figsize=(7, 5))

    billing[
        "Payment_Method"
    ].value_counts().plot(
        kind="bar"
    )

    plt.title(
        "Payment Method Analysis"
    )

    plt.xlabel("Payment Method")
    plt.ylabel("Number of Transactions")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


    # ----------------------------------------------------------
    # Chart 7 - Age Distribution
    # ----------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.hist(
        patients["Age"],
        bins=15
    )

    plt.title(
        "Patient Age Distribution"
    )

    plt.xlabel("Age")
    plt.ylabel("Number of Patients")

    plt.tight_layout()

    plt.show()


    # ----------------------------------------------------------
    # Chart 8 - Waiting Time
    # ----------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.hist(
        appointments[
            "Wait_Time_Minutes"
        ],
        bins=20
    )

    plt.title(
        "Patient Waiting Time Distribution"
    )

    plt.xlabel("Waiting Time (Minutes)")
    plt.ylabel("Number of Appointments")

    plt.tight_layout()

    plt.show()


    print("\n✓ All charts generated successfully")


# ==============================================================
# VIEW ALL ANALYSIS
# ==============================================================

def view_all_analysis():

    dataset_summary()

    data_quality_check()

    patient_analysis()

    doctor_analysis()

    appointment_analysis()

    department_analysis()

    treatment_analysis()

    readmission_analysis()

    billing_analysis()

    revenue_analysis()

    monthly_analysis()

    key_insights()


# ==============================================================
#MAIN MENU
# ==============================================================

def main_menu():

    while True:

        print("\n\n")

        print("=" * 70)

        print(
            "       HEALTHCARE DATA ANALYTICS & PATIENT INTELLIGENCE SYSTEM"
        )

        print("=" * 70)

        print("\n")

        print("1.  Patient Analysis")

        print("2.  Doctor Analysis")

        print("3.  Appointment Analysis")

        print("4.  Department Performance")

        print("5.  Treatment Analysis")

        print("6.  Readmission Analysis")

        print("7.  Billing Analysis")

        print("8.  Revenue Analysis")

        print("9.  Monthly Appointment Trend")

        print("10. Key Business Insights")

        print("11. Generate Charts")

        print("12. View All Analysis")

        print("0.  Exit")

        print("\n" + "-" * 70)

        choice = input(
            "\nEnter your choice: "
        )

        # ------------------------------------------------------
        # OPTION 1
        # ------------------------------------------------------

        if choice == "1":

            patient_analysis()

        # ------------------------------------------------------
        # OPTION 2
        # ------------------------------------------------------

        elif choice == "2":

            doctor_analysis()

        # ------------------------------------------------------
        # OPTION 3
        # ------------------------------------------------------

        elif choice == "3":

            appointment_analysis()

        # ------------------------------------------------------
        # OPTION 4
        # ------------------------------------------------------

        elif choice == "4":

            department_analysis()

        # ------------------------------------------------------
        # OPTION 5
        # ------------------------------------------------------

        elif choice == "5":

            treatment_analysis()

        # ------------------------------------------------------
        # OPTION 6
        # ------------------------------------------------------

        elif choice == "6":

            readmission_analysis()

        # ------------------------------------------------------
        # OPTION 7
        # ------------------------------------------------------

        elif choice == "7":

            billing_analysis()

        # ------------------------------------------------------
        # OPTION 8
        # ------------------------------------------------------

        elif choice == "8":

            revenue_analysis()

        # ------------------------------------------------------
        # OPTION 9
        # ------------------------------------------------------

        elif choice == "9":

            monthly_analysis()

        # ------------------------------------------------------
        # OPTION 10
        # ------------------------------------------------------

        elif choice == "10":

            key_insights()

        # ------------------------------------------------------
        # OPTION 11
        # ------------------------------------------------------

        elif choice == "11":

            generate_charts()

        # ------------------------------------------------------
        # OPTION 12
        # ------------------------------------------------------

        elif choice == "12":

            view_all_analysis()

        # ------------------------------------------------------
        # EXIT
        # ------------------------------------------------------

        elif choice == "0":

            print("\n" + "=" * 70)

            print(
                "       Thank You for Using Healthcare Analytics System"
            )

            print("=" * 70)

            break

        # ------------------------------------------------------
        # INVALID OPTION
        # ------------------------------------------------------

        else:

            print(
                "\n✗ Invalid Choice."
            )

            print(
                "Please select a valid option."
            )


# ==============================================================
# PROJECT START
# ==============================================================

def start_project():

    print("\n")

    print("=" * 70)

    print(
        "       HEALTHCARE DATA ANALYTICS & PATIENT INTELLIGENCE SYSTEM"
    )

    print("=" * 70)

    print(
        "\nProject: Healthcare Data Analytics"
    )

    print(
        "Purpose: Analyze patients, doctors, appointments,"
    )

    print(
        "         treatments and billing data."
    )

    print("=" * 70)


    # Connect Database

    database_connected = connect_database()

    if not database_connected:

        return


    # Load Data

    data_loaded = load_data()

    if not data_loaded:

        return


    # Clean Data

    clean_data()


    # Start Menu

    main_menu()


    # Close Database

    try:

        cursor.close()

        connection.close()

        print(
            "\n✓ MySQL connection closed successfully"
        )

    except:

        pass


# ==============================================================
# RUN PROJECT
# ==============================================================

start_project()
