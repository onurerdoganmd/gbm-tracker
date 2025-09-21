import random
import sys
import os
from datetime import datetime, date, timedelta
from faker import Faker

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import (
    Patient, Surgery, Pathology, Treatment, FollowUpVisit,
    Gender, WHOGrade, IDHStatus, MGMTStatus, SurgeryType,
    TreatmentType, PerformanceStatus, ImagingResponse,
    TreatmentStatus, NeurologicalStatus, ECOGScore
)

fake = Faker()

def create_realistic_patient(patient_number):
    """Create a realistic GBM patient with demographics"""
    # Generate realistic age (GBM typically affects older adults, peak 60-70 years)
    age = random.choices(
        range(20, 85),
        weights=[1, 2, 3, 5, 8, 12, 15, 20, 25, 30, 25, 20, 15, 10, 8, 5, 3, 2, 1] + [1]*46
    )[0]

    birth_date = fake.date_of_birth(minimum_age=age, maximum_age=age)

    # Gender distribution (slight male predominance in GBM)
    gender = random.choices([Gender.MALE, Gender.FEMALE], weights=[55, 45])[0]

    # Generate realistic names based on gender
    if gender == Gender.MALE:
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()

    last_name = fake.last_name()

    # Diagnosis date (recent cases within last 3 years)
    diagnosis_date = fake.date_between(start_date='-3y', end_date='today')

    # Brain tumor locations (realistic GBM locations)
    locations = [
        "Right frontal lobe", "Left frontal lobe", "Right temporal lobe", "Left temporal lobe",
        "Right parietal lobe", "Left parietal lobe", "Right occipital lobe", "Left occipital lobe",
        "Bilateral frontal", "Thalamus", "Basal ganglia", "Corpus callosum",
        "Right fronto-parietal", "Left fronto-parietal", "Right temporo-parietal",
        "Left temporo-parietal", "Brainstem", "Cerebellum"
    ]

    patient = Patient(
        medical_record_number=f"MRN{str(patient_number).zfill(6)}",
        first_name=first_name,
        last_name=last_name,
        date_of_birth=birth_date,
        gender=gender,
        contact_phone=fake.phone_number()[:20],
        contact_email=fake.email(),
        emergency_contact_name=fake.name(),
        emergency_contact_phone=fake.phone_number()[:20],
        initial_diagnosis_date=diagnosis_date,
        primary_location=random.choice(locations),
        referring_physician=f"Dr. {fake.last_name()}",
        insurance_info=random.choice([
            "Medicare", "Medicaid", "Blue Cross Blue Shield", "Aetna",
            "UnitedHealthcare", "Cigna", "Humana", "Kaiser Permanente"
        ]),
        medical_history=generate_medical_history(),
        family_history=generate_family_history(),
        current_medications=generate_medications(),
        allergies=generate_allergies(),
        notes=f"Patient enrolled on {diagnosis_date.strftime('%Y-%m-%d')}. Primary treating team: Neuro-oncology."
    )

    return patient

def generate_medical_history():
    """Generate realistic medical history"""
    conditions = []

    # Common comorbidities in older adults
    if random.random() < 0.3:
        conditions.append("Hypertension")
    if random.random() < 0.2:
        conditions.append("Type 2 Diabetes Mellitus")
    if random.random() < 0.15:
        conditions.append("Hyperlipidemia")
    if random.random() < 0.1:
        conditions.append("Coronary artery disease")
    if random.random() < 0.08:
        conditions.append("COPD")
    if random.random() < 0.05:
        conditions.append("Previous stroke")
    if random.random() < 0.03:
        conditions.append("Previous cancer (different primary)")

    if conditions:
        return "Past medical history significant for: " + ", ".join(conditions) + "."
    else:
        return "No significant past medical history."

def generate_family_history():
    """Generate realistic family history"""
    if random.random() < 0.7:  # 70% have some family history
        histories = []
        if random.random() < 0.3:
            histories.append("Cancer (various types) in family members")
        if random.random() < 0.1:
            histories.append("Brain tumor in family history")
        if random.random() < 0.2:
            histories.append("Cardiovascular disease")
        if random.random() < 0.15:
            histories.append("Diabetes")

        if histories:
            return "Family history positive for: " + ", ".join(histories) + "."

    return "No significant family history."

def generate_medications():
    """Generate realistic current medications"""
    meds = []

    # Anti-seizure medications (very common in GBM patients)
    if random.random() < 0.8:
        aeds = ["Levetiracetam 500mg BID", "Phenytoin 100mg TID", "Lacosamide 100mg BID"]
        meds.append(random.choice(aeds))

    # Steroids (common for cerebral edema)
    if random.random() < 0.6:
        meds.append("Dexamethasone 4mg BID")

    # Common comorbidity medications
    if random.random() < 0.3:
        meds.append("Lisinopril 10mg daily")
    if random.random() < 0.2:
        meds.append("Metformin 500mg BID")
    if random.random() < 0.15:
        meds.append("Atorvastatin 20mg daily")

    if meds:
        return "; ".join(meds)
    else:
        return "None"

def generate_allergies():
    """Generate realistic allergies"""
    if random.random() < 0.3:  # 30% have allergies
        allergies = ["NKDA (No Known Drug Allergies)", "Penicillin", "Sulfa", "Contrast dye", "NSAIDs"]
        return random.choice(allergies)
    return "NKDA"

def create_surgery_record(patient, db_session):
    """Create surgery record for a patient"""
    # Surgery typically occurs within days of diagnosis
    surgery_date = patient.initial_diagnosis_date + timedelta(days=random.randint(0, 14))

    # Surgery types with realistic distribution for GBM
    surgery_types = [
        (SurgeryType.GROSS_TOTAL_RESECTION, 0.4),
        (SurgeryType.SUBTOTAL_RESECTION, 0.35),
        (SurgeryType.PARTIAL_RESECTION, 0.2),
        (SurgeryType.BIOPSY, 0.05)
    ]

    surgery_type = random.choices(
        [s[0] for s in surgery_types],
        weights=[s[1] for s in surgery_types]
    )[0]

    # Realistic extent of resection percentages
    extent_map = {
        SurgeryType.GROSS_TOTAL_RESECTION: ["95-100%", "98%", ">95%"],
        SurgeryType.SUBTOTAL_RESECTION: ["80-95%", "85%", "90%"],
        SurgeryType.PARTIAL_RESECTION: ["50-80%", "60%", "70%"],
        SurgeryType.BIOPSY: ["Biopsy only", "Tissue sampling"]
    }

    surgeons = [
        "Dr. Anderson", "Dr. Chen", "Dr. Rodriguez", "Dr. Johnson",
        "Dr. Williams", "Dr. Smith", "Dr. Brown", "Dr. Davis"
    ]

    surgery = Surgery(
        patient_id=patient.id,
        surgery_date=surgery_date,
        surgery_type=surgery_type,
        surgeon_name=random.choice(surgeons),
        hospital="University Medical Center",
        preop_imaging_date=surgery_date - timedelta(days=random.randint(1, 5)),
        preop_tumor_size=f"{random.randint(25, 65)}x{random.randint(20, 55)}x{random.randint(15, 45)}mm",
        tumor_location=patient.primary_location,
        laterality="Right" if "Right" in patient.primary_location else "Left" if "Left" in patient.primary_location else "Midline",
        procedure_details=f"Craniotomy and {surgery_type.value.replace('_', ' ')} using stereotactic navigation and intraoperative monitoring.",
        operative_time_minutes=random.randint(180, 420),
        estimated_blood_loss_ml=random.randint(50, 300),
        extent_of_resection=random.choice(extent_map[surgery_type]),
        complications=generate_surgical_complications(),
        postop_imaging_date=surgery_date + timedelta(days=1),
        postop_findings=f"Post-operative changes consistent with {surgery_type.value.replace('_', ' ')}. No acute complications.",
        discharge_date=surgery_date + timedelta(days=random.randint(2, 7)),
        notes="Patient tolerated procedure well. Post-operative course uncomplicated."
    )

    return surgery

def generate_surgical_complications():
    """Generate realistic surgical complications"""
    if random.random() < 0.15:  # 15% complication rate
        complications = [
            "None", "Mild cerebral edema", "Temporary speech difficulty",
            "Temporary motor weakness", "Small amount of pneumocephalus",
            "Mild wound infection"
        ]
        return random.choice(complications[1:])  # Exclude "None"
    return "None"

def create_pathology_record(patient, surgery, db_session):
    """Create pathology record linked to surgery"""
    pathology_date = surgery.surgery_date + timedelta(days=random.randint(1, 3))

    pathologists = [
        "Dr. Martinez", "Dr. Thompson", "Dr. Wilson", "Dr. Garcia",
        "Dr. Lee", "Dr. Taylor", "Dr. Clark", "Dr. Moore"
    ]

    # GBM is WHO Grade IV by definition
    who_grade = WHOGrade.GRADE_IV

    # IDH status (typically wildtype in primary GBM, especially in older patients)
    idh_status = random.choices(
        [IDHStatus.WILDTYPE, IDHStatus.MUTANT, IDHStatus.UNKNOWN],
        weights=[85, 10, 5]
    )[0]

    # MGMT methylation status (important for treatment decisions)
    mgmt_status = random.choices(
        [MGMTStatus.METHYLATED, MGMTStatus.UNMETHYLATED, MGMTStatus.UNKNOWN],
        weights=[40, 55, 5]
    )[0]

    pathology = Pathology(
        patient_id=patient.id,
        surgery_id=surgery.id,
        specimen_date=pathology_date,
        pathologist_name=random.choice(pathologists),
        histologic_diagnosis="Glioblastoma (WHO Grade IV)",
        who_grade=who_grade,
        tumor_cellularity_percent=random.randint(70, 95),
        necrosis_present=random.choice([True, False]),
        microvascular_proliferation=random.choice([True, False]),
        idh_status=idh_status,
        mgmt_status=mgmt_status,
        p53_mutation=random.choice(["Positive", "Negative", "Unknown"]),
        egfr_amplification=random.choice([True, False]),
        ki67_index=random.randint(15, 35),
        molecular_markers=generate_molecular_markers(),
        immunohistochemistry_results=generate_ihc_results(),
        genetic_testing_results=generate_genetic_results(),
        pathology_report=f"High-grade astrocytic neoplasm consistent with glioblastoma, WHO grade IV. IDH {idh_status.value}, MGMT {mgmt_status.value}.",
        notes="Specimen processed according to standard protocols. Molecular testing completed."
    )

    return pathology

def generate_molecular_markers():
    """Generate additional molecular markers"""
    markers = []
    if random.random() < 0.7:
        markers.append(f"TERT promoter mutation: {'Present' if random.random() < 0.8 else 'Absent'}")
    if random.random() < 0.3:
        markers.append(f"ATRX loss: {'Present' if random.random() < 0.15 else 'Absent'}")
    if random.random() < 0.5:
        markers.append(f"1p/19q codeletion: {'Absent' if random.random() < 0.95 else 'Present'}")

    return "; ".join(markers) if markers else "Standard molecular panel completed"

def generate_ihc_results():
    """Generate immunohistochemistry results"""
    results = [
        "GFAP: Positive",
        "Ki-67: " + str(random.randint(15, 35)) + "%",
        "p53: " + random.choice(["Positive", "Negative", "Overexpressed"]),
        "IDH1 R132H: " + random.choice(["Negative", "Positive"])
    ]
    return "; ".join(results)

def generate_genetic_results():
    """Generate genetic testing results"""
    if random.random() < 0.8:  # 80% get genetic testing
        return f"Next-generation sequencing completed. IDH wildtype confirmed. MGMT promoter methylation analysis performed."
    return "Genetic testing pending"

def create_treatment_record(patient, pathology, db_session):
    """Create treatment records for a patient"""
    treatments = []

    # Standard Stupp protocol (radiation + temozolomide)
    if random.random() < 0.9:  # 90% get standard treatment
        # Radiation therapy
        radiation_start = pathology.specimen_date + timedelta(days=random.randint(14, 28))
        radiation = Treatment(
            patient_id=patient.id,
            treatment_type=TreatmentType.RADIATION,
            start_date=radiation_start,
            end_date=radiation_start + timedelta(days=42),  # 6 weeks
            treatment_status=TreatmentStatus.COMPLETED,
            protocol_name="Standard fractionated radiotherapy",
            treating_physician=random.choice(["Dr. Kumar", "Dr. Patel", "Dr. Zhang", "Dr. Adams"]),
            treatment_center="Radiation Oncology Department",
            radiation_dose_gy=60.0,
            radiation_fractions=30,
            radiation_technique="IMRT",
            response_assessment="Stable disease on post-radiation imaging",
            toxicities=generate_radiation_toxicities(),
            notes="Patient completed radiation therapy as planned with concurrent temozolomide."
        )
        treatments.append(radiation)

        # Concurrent and adjuvant temozolomide
        chemo_start = radiation_start
        chemo = Treatment(
            patient_id=patient.id,
            treatment_type=TreatmentType.CHEMOTHERAPY,
            start_date=chemo_start,
            end_date=chemo_start + timedelta(days=365),  # Up to 1 year
            treatment_status=random.choice([TreatmentStatus.COMPLETED, TreatmentStatus.DISCONTINUED]),
            protocol_name="Temozolomide (Stupp protocol)",
            treating_physician=random.choice(["Dr. Williams", "Dr. Johnson", "Dr. Brown", "Dr. Davis"]),
            treatment_center="Medical Oncology",
            chemotherapy_regimen="Temozolomide",
            cycles_planned=6,
            cycles_delivered=random.randint(3, 6),
            drug_names="Temozolomide",
            dosing_schedule="75 mg/m2 daily during RT, then 150-200 mg/m2 days 1-5 q28 days",
            route_of_administration="Oral",
            response_assessment=random.choice([
                "Stable disease", "Partial response", "Progressive disease"
            ]),
            toxicities=generate_chemo_toxicities(),
            notes="Standard Stupp protocol completed with manageable toxicity profile."
        )
        treatments.append(chemo)

    # Some patients may have additional treatments
    if random.random() < 0.2 and treatments and len(treatments) >= 2:  # 20% get additional treatment if they have chemo
        chemo_treatment = treatments[1]  # Get the chemotherapy treatment
        second_line_start = chemo_treatment.end_date + timedelta(days=random.randint(30, 90))
        second_line = Treatment(
            patient_id=patient.id,
            treatment_type=TreatmentType.TARGETED_THERAPY,
            start_date=second_line_start,
            end_date=second_line_start + timedelta(days=180),
            treatment_status=TreatmentStatus.DISCONTINUED,
            protocol_name="Bevacizumab",
            treating_physician=chemo_treatment.treating_physician,
            treatment_center="Medical Oncology",
            drug_names="Bevacizumab",
            dosing_schedule="10 mg/kg IV every 2 weeks",
            route_of_administration="Intravenous",
            response_assessment="Progressive disease",
            reason_for_discontinuation="Disease progression",
            notes="Second-line therapy for recurrent disease."
        )
        treatments.append(second_line)

    return treatments

def generate_radiation_toxicities():
    """Generate realistic radiation toxicities"""
    toxicities = []
    if random.random() < 0.6:
        toxicities.append("Grade 1-2 fatigue")
    if random.random() < 0.4:
        toxicities.append("Grade 1 alopecia")
    if random.random() < 0.3:
        toxicities.append("Grade 1 skin erythema")
    if random.random() < 0.1:
        toxicities.append("Grade 2 cerebral edema")

    return "; ".join(toxicities) if toxicities else "Well tolerated, no significant toxicities"

def generate_chemo_toxicities():
    """Generate realistic chemotherapy toxicities"""
    toxicities = []
    if random.random() < 0.5:
        toxicities.append("Grade 1-2 nausea")
    if random.random() < 0.4:
        toxicities.append("Grade 1-2 fatigue")
    if random.random() < 0.3:
        toxicities.append("Grade 1 thrombocytopenia")
    if random.random() < 0.2:
        toxicities.append("Grade 1 lymphopenia")
    if random.random() < 0.1:
        toxicities.append("Grade 2 constipation")

    return "; ".join(toxicities) if toxicities else "Well tolerated, no significant toxicities"

def create_follow_up_visits(patient, treatments, db_session):
    """Create follow-up visit records"""
    visits = []

    # Regular follow-up schedule
    if treatments:
        last_treatment_end = max(t.end_date for t in treatments if t.end_date)

        # Create 3-6 follow-up visits
        for i in range(random.randint(3, 6)):
            visit_date = last_treatment_end + timedelta(days=60 * (i + 1))  # Every 2 months

            visit = FollowUpVisit(
                patient_id=patient.id,
                visit_date=visit_date,
                visit_type="Routine follow-up",
                attending_physician=random.choice([
                    "Dr. Williams", "Dr. Johnson", "Dr. Brown", "Dr. Davis",
                    "Dr. Kumar", "Dr. Patel", "Dr. Zhang", "Dr. Adams"
                ]),
                kps_score=random.randint(60, 100),
                neurological_status=random.choice(list(NeurologicalStatus)),
                steroid_dose_mg=random.choice([0, 2, 4, 6, 8]),
                ecog_score=random.choice(list(ECOGScore)),
                symptoms=generate_symptoms(),
                physical_exam_findings=generate_physical_exam(),
                next_appointment_date=visit_date + timedelta(days=60),
                performance_status=random.choice(list(PerformanceStatus)),
                imaging_date=visit_date - timedelta(days=random.randint(1, 7)),
                imaging_type="MRI brain with and without contrast",
                imaging_response=random.choice(list(ImagingResponse)),
                tumor_measurements=generate_tumor_measurements(),
                imaging_notes="MRI compared to prior studies",
                lab_date=visit_date,
                lab_results=generate_lab_results(),
                current_medications=patient.current_medications,
                next_visit_date=visit_date + timedelta(days=60),
                next_imaging_date=visit_date + timedelta(days=60),
                treatment_plan=generate_treatment_plan(),
                notes=f"Patient continues routine surveillance. Overall clinical status stable."
            )
            visits.append(visit)

    return visits

def generate_neuro_status():
    """Generate neurological status"""
    statuses = [
        "Neurologically stable", "Mild cognitive changes", "Speech intact",
        "Motor function preserved", "Mild word-finding difficulty",
        "Stable neurological deficits", "No new neurological symptoms"
    ]
    return random.choice(statuses)

def generate_physical_exam():
    """Generate physical exam findings"""
    exams = [
        "ECOG 0-1, alert and oriented x3",
        "Vital signs stable, no acute distress",
        "Craniotomy site well-healed",
        "Neurological exam non-focal",
        "ECOG 1-2, mild fatigue noted"
    ]
    return random.choice(exams)

def generate_symptoms():
    """Generate patient-reported symptoms"""
    if random.random() < 0.3:  # 30% have symptoms
        symptoms = [
            "Mild headaches", "Occasional fatigue", "Memory concerns",
            "Sleep disturbance", "Mild nausea", "Word-finding difficulty"
        ]
        return random.choice(symptoms)
    return "No new symptoms reported"

def generate_tumor_measurements():
    """Generate tumor measurements"""
    responses = {
        ImagingResponse.COMPLETE_RESPONSE: "No residual enhancing disease",
        ImagingResponse.PARTIAL_RESPONSE: "Decreased size of enhancing lesion",
        ImagingResponse.STABLE_DISEASE: "Stable post-surgical changes",
        ImagingResponse.PROGRESSIVE_DISEASE: "New or increased enhancement"
    }
    return "Stable post-operative changes with expected evolution"

def generate_lab_results():
    """Generate laboratory results"""
    return f"CBC: WBC {random.randint(4, 10)}k, Hgb {random.randint(10, 14)}, Plt {random.randint(150, 400)}k; CMP normal"

def generate_treatment_plan():
    """Generate treatment plan"""
    plans = [
        "Continue routine surveillance",
        "Maintain current supportive care",
        "Follow-up in 2 months with imaging",
        "Continue anti-seizure medications",
        "Monitor for disease progression"
    ]
    return random.choice(plans)

def seed_database():
    """Main function to seed the database with 40 realistic GBM patients"""
    db = SessionLocal()

    try:
        print("Starting to generate 40 realistic GBM patients...")

        for i in range(1, 41):
            print(f"Creating patient {i}/40...")

            # Create patient
            patient = create_realistic_patient(i)
            db.add(patient)
            db.flush()  # Get the patient ID

            # Create surgery record
            surgery = create_surgery_record(patient, db)
            db.add(surgery)
            db.flush()

            # Create pathology record
            pathology = create_pathology_record(patient, surgery, db)
            db.add(pathology)
            db.flush()

            # Create treatment records
            treatments = create_treatment_record(patient, pathology, db)
            for treatment in treatments:
                db.add(treatment)
            db.flush()

            # Create follow-up visits
            visits = create_follow_up_visits(patient, treatments, db)
            for visit in visits:
                db.add(visit)

            db.flush()

        # Commit all changes
        db.commit()
        print("Successfully created 40 realistic GBM patients with complete medical records!")
        print("Database seeded with:")
        print("- 40 patients with demographics and medical history")
        print("- 40 surgery records with realistic details")
        print("- 40 pathology reports with molecular profiles")
        print("- ~60-80 treatment records (radiation, chemotherapy)")
        print("- ~150-240 follow-up visit records")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("GBM Tracker Database Seeding Tool")
    print("=====================================")

    response = input("This will add 40 realistic GBM patients to the database. Continue? (y/N): ")
    if response.lower() in ['y', 'yes']:
        seed_database()
    else:
        print("Seeding cancelled.")