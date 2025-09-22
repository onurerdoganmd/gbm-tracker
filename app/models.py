from datetime import datetime, date
from enum import Enum as PyEnum
from typing import Optional, List
from decimal import Decimal

from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class WHOGrade(PyEnum):
    GRADE_I = "I"
    GRADE_II = "II"
    GRADE_III = "III"
    GRADE_IV = "IV"

class IDHStatus(PyEnum):
    WILDTYPE = "wildtype"
    MUTANT = "mutant"
    UNKNOWN = "unknown"

class MGMTStatus(PyEnum):
    METHYLATED = "methylated"
    UNMETHYLATED = "unmethylated"
    UNKNOWN = "unknown"

class ATRXStatus(PyEnum):
    RETAINED = "retained"
    LOST = "lost"
    UNKNOWN = "unknown"

class CodeletionStatus(PyEnum):
    PRESENT = "present"
    ABSENT = "absent"
    UNKNOWN = "unknown"

class SurgeryType(PyEnum):
    BIOPSY = "biopsy"
    PARTIAL_RESECTION = "partial_resection"
    SUBTOTAL_RESECTION = "subtotal_resection"
    GROSS_TOTAL_RESECTION = "gross_total_resection"

class TreatmentType(PyEnum):
    RADIATION = "radiation"
    CHEMOTHERAPY = "chemotherapy"
    IMMUNOTHERAPY = "immunotherapy"
    TARGETED_THERAPY = "targeted_therapy"
    COMBINATION = "combination"

class TreatmentStatus(PyEnum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    DISCONTINUED = "discontinued"
    ON_HOLD = "on_hold"

class PerformanceStatus(PyEnum):
    KARNOFSKY_90_100 = "karnofsky_90_100"
    KARNOFSKY_70_80 = "karnofsky_70_80"
    KARNOFSKY_50_60 = "karnofsky_50_60"
    KARNOFSKY_30_40 = "karnofsky_30_40"
    KARNOFSKY_10_20 = "karnofsky_10_20"

class ImagingResponse(PyEnum):
    COMPLETE_RESPONSE = "complete_response"
    PARTIAL_RESPONSE = "partial_response"
    STABLE_DISEASE = "stable_disease"
    PROGRESSIVE_DISEASE = "progressive_disease"

class NeurologicalStatus(PyEnum):
    STABLE = "stable"
    IMPROVED = "improved"
    DECLINED = "declined"

class ECOGScore(PyEnum):
    SCORE_0 = "0"  # Fully active
    SCORE_1 = "1"  # Restricted in physically strenuous activity
    SCORE_2 = "2"  # Ambulatory and capable of self-care
    SCORE_3 = "3"  # Capable of only limited self-care
    SCORE_4 = "4"  # Completely disabled


class Patient(BaseModel):
    __tablename__ = "patients"

    medical_record_number = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)

    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))

    initial_diagnosis_date = Column(Date)
    primary_location = Column(String(200))
    referring_physician = Column(String(200))
    insurance_info = Column(Text)

    medical_history = Column(Text)
    family_history = Column(Text)
    current_medications = Column(Text)
    allergies = Column(Text)
    notes = Column(Text)

    surgeries = relationship("Surgery", back_populates="patient", cascade="all, delete-orphan")
    pathologies = relationship("Pathology", back_populates="patient", cascade="all, delete-orphan")
    treatments = relationship("Treatment", back_populates="patient", cascade="all, delete-orphan")
    follow_up_visits = relationship("FollowUpVisit", back_populates="patient", cascade="all, delete-orphan")

class Surgery(BaseModel):
    __tablename__ = "surgeries"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    surgery_date = Column(Date, nullable=False)
    surgery_type = Column(Enum(SurgeryType), nullable=False)
    surgeon_name = Column(String(200), nullable=False)
    hospital = Column(String(200))

    preop_imaging_date = Column(Date)
    preop_tumor_size = Column(String(100))
    tumor_location = Column(String(200))
    laterality = Column(String(50))

    procedure_details = Column(Text)
    operative_time_minutes = Column(Integer)
    estimated_blood_loss_ml = Column(Integer)
    extent_of_resection = Column(String(100))

    complications = Column(Text)
    postop_imaging_date = Column(Date)
    postop_findings = Column(Text)
    discharge_date = Column(Date)
    notes = Column(Text)

    patient = relationship("Patient", back_populates="surgeries")
    pathology = relationship("Pathology", back_populates="surgery", uselist=False)

class Pathology(BaseModel):
    __tablename__ = "pathologies"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    surgery_id = Column(Integer, ForeignKey("surgeries.id"), nullable=True)
    specimen_date = Column(Date, nullable=False)
    pathologist_name = Column(String(200))

    histologic_diagnosis = Column(String(200), nullable=False)
    who_grade = Column(Enum(WHOGrade))
    tumor_cellularity_percent = Column(Integer)
    necrosis_present = Column(Boolean)
    microvascular_proliferation = Column(Boolean)

    idh_status = Column(Enum(IDHStatus))
    mgmt_status = Column(Enum(MGMTStatus))
    atrx_status = Column(Enum(ATRXStatus))
    codeletion_1p19q_status = Column(Enum(CodeletionStatus))
    p53_mutation = Column(String(100))
    egfr_amplification = Column(Boolean)
    ki67_index = Column(Integer)

    molecular_markers = Column(Text)
    immunohistochemistry_results = Column(Text)
    genetic_testing_results = Column(Text)

    pathology_report = Column(Text)
    notes = Column(Text)

    patient = relationship("Patient", back_populates="pathologies")
    surgery = relationship("Surgery", back_populates="pathology")

class Treatment(BaseModel):
    __tablename__ = "treatments"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    treatment_type = Column(Enum(TreatmentType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)

    # Core treatment fields as requested
    regimen = Column(String(200))  # e.g., 'Temozolomide', 'Bevacizumab'
    cycles_planned = Column(Integer)
    cycles_delivered = Column(Integer)  # cycles_completed renamed to cycles_delivered
    dose = Column(String(200))  # Flexible dose field for various units
    treatment_status = Column(Enum(TreatmentStatus), nullable=False)

    protocol_name = Column(String(200))
    treating_physician = Column(String(200))
    treatment_center = Column(String(200))

    radiation_dose_gy = Column(Numeric(5, 2))
    radiation_fractions = Column(Integer)
    radiation_technique = Column(String(100))

    chemotherapy_regimen = Column(String(200))  # Keeping this for backward compatibility
    drug_names = Column(Text)
    dosing_schedule = Column(Text)
    route_of_administration = Column(String(50))

    response_assessment = Column(Text)
    toxicities = Column(Text)
    dose_modifications = Column(Text)
    reason_for_discontinuation = Column(String(200))
    notes = Column(Text)

    patient = relationship("Patient", back_populates="treatments")

class FollowUpVisit(BaseModel):
    __tablename__ = "follow_up_visits"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    visit_type = Column(String(100))  # routine/urgent/post-op
    attending_physician = Column(String(200))

    # Core GBM clinical assessment fields as requested
    kps_score = Column(Integer)  # Karnofsky Performance Status 0-100
    ecog_score = Column(Enum(ECOGScore))  # ECOG performance status 0-4
    neurological_status = Column(Enum(NeurologicalStatus))  # stable, improved, declined
    cognitive_assessment = Column(Text)  # cognitive function assessment
    motor_function = Column(Text)  # motor function assessment
    speech_assessment = Column(Text)  # speech function assessment
    seizure_activity = Column(Text)  # seizure activity notes
    steroid_dose_mg = Column(Numeric(8, 2))  # steroid dose in mg
    current_medications = Column(Text)  # current medications
    symptoms_reported = Column(Text)  # symptoms reported by patient
    physical_exam_findings = Column(Text)  # physical examination findings
    clinical_impression = Column(Text)  # clinician's impression
    next_appointment_date = Column(Date)  # next appointment date
    visit_notes = Column(Text)  # comprehensive visit notes

    # Legacy/additional fields
    performance_status = Column(Enum(PerformanceStatus))
    symptoms = Column(Text)  # keeping for backward compatibility

    imaging_date = Column(Date)
    imaging_type = Column(String(100))
    imaging_response = Column(Enum(ImagingResponse))
    tumor_measurements = Column(Text)
    imaging_notes = Column(Text)

    lab_date = Column(Date)
    lab_results = Column(Text)

    medication_changes = Column(Text)

    next_visit_date = Column(Date)
    next_imaging_date = Column(Date)
    treatment_plan = Column(Text)
    notes = Column(Text)  # keeping for backward compatibility

    patient = relationship("Patient", back_populates="follow_up_visits")

