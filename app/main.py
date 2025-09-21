from typing import List, Optional
from datetime import date
import json
import csv
import io
from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .models import Patient, Surgery, Pathology, Treatment, FollowUpVisit, Gender, SurgeryType, WHOGrade, IDHStatus, MGMTStatus, TreatmentType, TreatmentStatus, NeurologicalStatus, ECOGScore

app = FastAPI(title="GBM Tracker", description="Glioblastoma Multiforme Patient Tracking System")

# Pydantic models for Surgery CRUD operations
class SurgeryCreate(BaseModel):
    patient_id: int
    surgery_date: date
    surgery_type: SurgeryType
    surgeon_name: str
    hospital: Optional[str] = None
    preop_tumor_size: Optional[str] = None
    tumor_location: Optional[str] = None
    laterality: Optional[str] = None
    procedure_details: Optional[str] = None
    operative_time_minutes: Optional[int] = None
    estimated_blood_loss_ml: Optional[int] = None
    extent_of_resection: Optional[str] = None
    complications: Optional[str] = None
    postop_findings: Optional[str] = None
    discharge_date: Optional[date] = None
    notes: Optional[str] = None

class SurgeryUpdate(BaseModel):
    surgery_date: Optional[date] = None
    surgery_type: Optional[SurgeryType] = None
    surgeon_name: Optional[str] = None
    hospital: Optional[str] = None
    preop_tumor_size: Optional[str] = None
    tumor_location: Optional[str] = None
    laterality: Optional[str] = None
    procedure_details: Optional[str] = None
    operative_time_minutes: Optional[int] = None
    estimated_blood_loss_ml: Optional[int] = None
    extent_of_resection: Optional[str] = None
    complications: Optional[str] = None
    postop_findings: Optional[str] = None
    discharge_date: Optional[date] = None
    notes: Optional[str] = None

# Pydantic models for Pathology CRUD operations
class PathologyCreate(BaseModel):
    patient_id: int
    surgery_id: Optional[int] = None
    specimen_date: date
    pathologist_name: Optional[str] = None
    histologic_diagnosis: str
    who_grade: Optional[WHOGrade] = None
    tumor_cellularity_percent: Optional[int] = None
    necrosis_present: Optional[bool] = None
    microvascular_proliferation: Optional[bool] = None
    idh_status: Optional[IDHStatus] = None
    mgmt_status: Optional[MGMTStatus] = None
    p53_mutation: Optional[str] = None
    egfr_amplification: Optional[bool] = None
    ki67_index: Optional[int] = None
    molecular_markers: Optional[str] = None
    immunohistochemistry_results: Optional[str] = None
    genetic_testing_results: Optional[str] = None
    pathology_report: Optional[str] = None
    notes: Optional[str] = None

class PathologyUpdate(BaseModel):
    specimen_date: Optional[date] = None
    pathologist_name: Optional[str] = None
    histologic_diagnosis: Optional[str] = None
    who_grade: Optional[WHOGrade] = None
    tumor_cellularity_percent: Optional[int] = None
    necrosis_present: Optional[bool] = None
    microvascular_proliferation: Optional[bool] = None
    idh_status: Optional[IDHStatus] = None
    mgmt_status: Optional[MGMTStatus] = None
    p53_mutation: Optional[str] = None
    egfr_amplification: Optional[bool] = None
    ki67_index: Optional[int] = None
    molecular_markers: Optional[str] = None
    immunohistochemistry_results: Optional[str] = None
    genetic_testing_results: Optional[str] = None
    pathology_report: Optional[str] = None
    notes: Optional[str] = None

# Pydantic models for Treatment CRUD operations
class TreatmentCreate(BaseModel):
    patient_id: int
    treatment_type: TreatmentType
    start_date: date
    end_date: Optional[date] = None
    regimen: Optional[str] = None
    cycles_planned: Optional[int] = None
    cycles_delivered: Optional[int] = None
    dose: Optional[str] = None
    treatment_status: TreatmentStatus

    protocol_name: Optional[str] = None
    treating_physician: Optional[str] = None
    treatment_center: Optional[str] = None

    radiation_dose_gy: Optional[float] = None
    radiation_fractions: Optional[int] = None
    radiation_technique: Optional[str] = None

    chemotherapy_regimen: Optional[str] = None
    drug_names: Optional[str] = None
    dosing_schedule: Optional[str] = None
    route_of_administration: Optional[str] = None

    response_assessment: Optional[str] = None
    toxicities: Optional[str] = None
    dose_modifications: Optional[str] = None
    reason_for_discontinuation: Optional[str] = None
    notes: Optional[str] = None

class TreatmentUpdate(BaseModel):
    treatment_type: Optional[TreatmentType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    regimen: Optional[str] = None
    cycles_planned: Optional[int] = None
    cycles_delivered: Optional[int] = None
    dose: Optional[str] = None
    treatment_status: Optional[TreatmentStatus] = None

    protocol_name: Optional[str] = None
    treating_physician: Optional[str] = None
    treatment_center: Optional[str] = None

    radiation_dose_gy: Optional[float] = None
    radiation_fractions: Optional[int] = None
    radiation_technique: Optional[str] = None

    chemotherapy_regimen: Optional[str] = None
    drug_names: Optional[str] = None
    dosing_schedule: Optional[str] = None
    route_of_administration: Optional[str] = None

    response_assessment: Optional[str] = None
    toxicities: Optional[str] = None
    dose_modifications: Optional[str] = None
    reason_for_discontinuation: Optional[str] = None
    notes: Optional[str] = None

# Pydantic models for FollowUpVisit CRUD operations
class FollowUpVisitCreate(BaseModel):
    patient_id: int
    visit_date: date
    visit_type: Optional[str] = None
    attending_physician: Optional[str] = None

    # Core clinical assessment fields
    kps_score: Optional[int] = None
    neurological_status: Optional[NeurologicalStatus] = None
    steroid_dose_mg: Optional[float] = None
    ecog_score: Optional[ECOGScore] = None
    symptoms: Optional[str] = None
    physical_exam_findings: Optional[str] = None
    next_appointment_date: Optional[date] = None

    # Additional clinical fields
    imaging_date: Optional[date] = None
    imaging_type: Optional[str] = None
    tumor_measurements: Optional[str] = None
    imaging_notes: Optional[str] = None

    lab_date: Optional[date] = None
    lab_results: Optional[str] = None

    current_medications: Optional[str] = None
    medication_changes: Optional[str] = None

    next_visit_date: Optional[date] = None
    next_imaging_date: Optional[date] = None
    treatment_plan: Optional[str] = None
    notes: Optional[str] = None

class FollowUpVisitUpdate(BaseModel):
    visit_date: Optional[date] = None
    visit_type: Optional[str] = None
    attending_physician: Optional[str] = None

    # Core clinical assessment fields
    kps_score: Optional[int] = None
    neurological_status: Optional[NeurologicalStatus] = None
    steroid_dose_mg: Optional[float] = None
    ecog_score: Optional[ECOGScore] = None
    symptoms: Optional[str] = None
    physical_exam_findings: Optional[str] = None
    next_appointment_date: Optional[date] = None

    # Additional clinical fields
    imaging_date: Optional[date] = None
    imaging_type: Optional[str] = None
    tumor_measurements: Optional[str] = None
    imaging_notes: Optional[str] = None

    lab_date: Optional[date] = None
    lab_results: Optional[str] = None

    current_medications: Optional[str] = None
    medication_changes: Optional[str] = None

    next_visit_date: Optional[date] = None
    next_imaging_date: Optional[date] = None
    treatment_plan: Optional[str] = None
    notes: Optional[str] = None

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/patients", response_class=HTMLResponse)
async def get_patients(request: Request, db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return templates.TemplateResponse("patients.html", {
        "request": request,
        "patients": patients,
        "title": "All Patients"
    })

@app.get("/patients/{patient_id}", response_class=HTMLResponse)
async def get_patient_detail(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return templates.TemplateResponse("patient_detail.html", {
        "request": request,
        "patient": patient,
        "title": f"Patient: {patient.first_name} {patient.last_name}"
    })

@app.get("/api/patients")
async def api_get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return {"patients": [{"id": p.id, "name": f"{p.first_name} {p.last_name}", "mrn": p.medical_record_number} for p in patients]}

@app.get("/api/patients/{patient_id}")
async def api_get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "id": patient.id,
        "medical_record_number": patient.medical_record_number,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        "gender": patient.gender.value if patient.gender else None,
        "contact_phone": patient.contact_phone,
        "contact_email": patient.contact_email,
        "initial_diagnosis_date": patient.initial_diagnosis_date.isoformat() if patient.initial_diagnosis_date else None,
        "primary_location": patient.primary_location,
        "referring_physician": patient.referring_physician,
        "created_at": patient.created_at.isoformat() if patient.created_at else None
    }

# Patient Timeline View

@app.get("/patients/{patient_id}/timeline", response_class=HTMLResponse)
async def get_patient_timeline(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get all surgeries for this patient
    surgeries = db.query(Surgery).filter(Surgery.patient_id == patient_id).all()

    # Get all pathologies for this patient
    pathologies = db.query(Pathology).filter(Pathology.patient_id == patient_id).all()

    # Get all treatments for this patient
    treatments = db.query(Treatment).filter(Treatment.patient_id == patient_id).all()

    # Get all follow-up visits for this patient
    follow_up_visits = db.query(FollowUpVisit).filter(FollowUpVisit.patient_id == patient_id).all()

    # Create timeline events
    timeline_events = []

    # Add surgery events
    for surgery in surgeries:
        if surgery.surgery_date:
            timeline_events.append({
                "date": surgery.surgery_date.isoformat() if surgery.surgery_date else None,
                "type": "surgery",
                "title": f"{surgery.surgery_type.value.replace('_', ' ').title()}" if surgery.surgery_type else "Surgery",
                "description": f"Performed by {surgery.surgeon_name}" if surgery.surgeon_name else "Surgery performed",
                "details": {
                    "surgeon": surgery.surgeon_name,
                    "hospital": surgery.hospital,
                    "extent_of_resection": surgery.extent_of_resection,
                    "complications": surgery.complications,
                    "operative_time": surgery.operative_time_minutes,
                    "estimated_blood_loss": surgery.estimated_blood_loss_ml
                },
                "id": surgery.id,
                "url": f"/surgeries/{surgery.id}"
            })

    # Add pathology events
    for pathology in pathologies:
        if pathology.specimen_date:
            timeline_events.append({
                "date": pathology.specimen_date.isoformat() if pathology.specimen_date else None,
                "type": "pathology",
                "title": pathology.histologic_diagnosis or "Pathology Report",
                "description": f"Analyzed by {pathology.pathologist_name}" if pathology.pathologist_name else "Pathology analysis",
                "details": {
                    "pathologist": pathology.pathologist_name,
                    "who_grade": pathology.who_grade.value if pathology.who_grade else None,
                    "idh_status": pathology.idh_status.value if pathology.idh_status else None,
                    "mgmt_status": pathology.mgmt_status.value if pathology.mgmt_status else None,
                    "ki67_index": pathology.ki67_index,
                    "tumor_cellularity": pathology.tumor_cellularity_percent,
                    "necrosis_present": pathology.necrosis_present,
                    "microvascular_proliferation": pathology.microvascular_proliferation
                },
                "id": pathology.id,
                "url": f"/pathologies/{pathology.id}"
            })

    # Add treatment events
    for treatment in treatments:
        if treatment.start_date:
            timeline_events.append({
                "date": treatment.start_date.isoformat() if treatment.start_date else None,
                "type": "treatment",
                "title": f"{treatment.treatment_type.value.replace('_', ' ').title()}" if treatment.treatment_type else "Treatment",
                "description": f"{treatment.regimen}" if treatment.regimen else f"Treating physician: {treatment.treating_physician}" if treatment.treating_physician else "Treatment administered",
                "details": {
                    "regimen": treatment.regimen,
                    "treatment_type": treatment.treatment_type.value.title() if treatment.treatment_type else None,
                    "treatment_status": treatment.treatment_status.value.title() if treatment.treatment_status else None,
                    "treating_physician": treatment.treating_physician,
                    "treatment_center": treatment.treatment_center,
                    "cycles_planned": treatment.cycles_planned,
                    "cycles_delivered": treatment.cycles_delivered,
                    "dose": treatment.dose,
                    "start_date": treatment.start_date.isoformat() if treatment.start_date else None,
                    "end_date": treatment.end_date.isoformat() if treatment.end_date else None,
                    "protocol_name": treatment.protocol_name,
                    "route_of_administration": treatment.route_of_administration
                },
                "id": treatment.id,
                "url": f"/treatments/{treatment.id}"
            })

    # Add follow-up visit events
    for visit in follow_up_visits:
        if visit.visit_date:
            timeline_events.append({
                "date": visit.visit_date.isoformat() if visit.visit_date else None,
                "type": "follow_up",
                "title": f"Follow-Up Visit" + (f" - {visit.visit_type}" if visit.visit_type else ""),
                "description": f"Attending: {visit.attending_physician}" if visit.attending_physician else "Follow-up appointment",
                "details": {
                    "attending_physician": visit.attending_physician,
                    "visit_type": visit.visit_type,
                    "kps_score": visit.kps_score,
                    "neurological_status": visit.neurological_status.value.title() if visit.neurological_status else None,
                    "ecog_score": f"ECOG {visit.ecog_score.value}" if visit.ecog_score else None,
                    "steroid_dose_mg": f"{visit.steroid_dose_mg} mg" if visit.steroid_dose_mg else None,
                    "symptoms": visit.symptoms,
                    "physical_exam_findings": visit.physical_exam_findings,
                    "next_appointment_date": visit.next_appointment_date.isoformat() if visit.next_appointment_date else None,
                    "treatment_plan": visit.treatment_plan
                },
                "id": visit.id,
                "url": f"/follow-up-visits/{visit.id}"
            })

    # Add initial diagnosis event if available
    if patient.initial_diagnosis_date:
        timeline_events.append({
            "date": patient.initial_diagnosis_date.isoformat() if patient.initial_diagnosis_date else None,
            "type": "diagnosis",
            "title": "Initial Diagnosis",
            "description": f"Primary location: {patient.primary_location}" if patient.primary_location else "Initial GBM diagnosis",
            "details": {
                "primary_location": patient.primary_location,
                "referring_physician": patient.referring_physician
            },
            "id": None,
            "url": None
        })

    # Sort events by date (most recent first) - handle mixed date types safely
    def safe_date_key(event):
        date_val = event["date"]
        if date_val is None:
            return ""
        elif hasattr(date_val, 'isoformat'):
            return date_val.isoformat()
        else:
            return str(date_val)

    timeline_events.sort(key=safe_date_key, reverse=True)

    # Convert string dates back to date objects for template compatibility
    from datetime import datetime
    for event in timeline_events:
        if isinstance(event["date"], str) and event["date"]:
            try:
                event["date"] = datetime.fromisoformat(event["date"]).date()
            except:
                # If conversion fails, leave as string
                pass

    return templates.TemplateResponse("patient_timeline.html", {
        "request": request,
        "patient": patient,
        "timeline_events": timeline_events,
        "title": f"Timeline for {patient.first_name} {patient.last_name}"
    })

@app.get("/patients/{patient_id}/timeline/interactive", response_class=HTMLResponse)
async def get_patient_timeline_interactive(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get all surgeries for this patient
    surgeries = db.query(Surgery).filter(Surgery.patient_id == patient_id).all()

    # Get all pathologies for this patient
    pathologies = db.query(Pathology).filter(Pathology.patient_id == patient_id).all()

    # Get all treatments for this patient
    treatments = db.query(Treatment).filter(Treatment.patient_id == patient_id).all()

    # Get all follow-up visits for this patient
    follow_up_visits = db.query(FollowUpVisit).filter(FollowUpVisit.patient_id == patient_id).all()

    # Create timeline events
    timeline_events = []

    # Add surgery events
    for surgery in surgeries:
        if surgery.surgery_date:
            timeline_events.append({
                "date": surgery.surgery_date.isoformat() if surgery.surgery_date else None,
                "type": "surgery",
                "title": f"{surgery.surgery_type.value.replace('_', ' ').title()}" if surgery.surgery_type else "Surgery",
                "description": f"Performed by {surgery.surgeon_name}" if surgery.surgeon_name else "Surgery performed",
                "details": {
                    "surgeon": surgery.surgeon_name,
                    "hospital": surgery.hospital,
                    "extent_of_resection": surgery.extent_of_resection,
                    "complications": surgery.complications,
                    "operative_time": f"{surgery.operative_time_minutes} min" if surgery.operative_time_minutes else None,
                    "estimated_blood_loss": f"{surgery.estimated_blood_loss_ml} ml" if surgery.estimated_blood_loss_ml else None
                },
                "id": surgery.id,
                "url": f"/surgeries/{surgery.id}"
            })

    # Add pathology events
    for pathology in pathologies:
        if pathology.specimen_date:
            timeline_events.append({
                "date": pathology.specimen_date.isoformat() if pathology.specimen_date else None,
                "type": "pathology",
                "title": pathology.histologic_diagnosis or "Pathology Report",
                "description": f"Analyzed by {pathology.pathologist_name}" if pathology.pathologist_name else "Pathology analysis",
                "details": {
                    "pathologist": pathology.pathologist_name,
                    "who_grade": f"Grade {pathology.who_grade.value}" if pathology.who_grade else None,
                    "idh_status": pathology.idh_status.value.title() if pathology.idh_status else None,
                    "mgmt_status": pathology.mgmt_status.value.title() if pathology.mgmt_status else None,
                    "ki67_index": f"{pathology.ki67_index}%" if pathology.ki67_index else None,
                    "tumor_cellularity": f"{pathology.tumor_cellularity_percent}%" if pathology.tumor_cellularity_percent else None,
                    "necrosis_present": "Yes" if pathology.necrosis_present else "No" if pathology.necrosis_present is not None else None,
                    "microvascular_proliferation": "Yes" if pathology.microvascular_proliferation else "No" if pathology.microvascular_proliferation is not None else None
                },
                "id": pathology.id,
                "url": f"/pathologies/{pathology.id}"
            })

    # Add treatment events
    for treatment in treatments:
        if treatment.start_date:
            timeline_events.append({
                "date": treatment.start_date.isoformat() if treatment.start_date else None,
                "type": "treatment",
                "title": f"{treatment.treatment_type.value.replace('_', ' ').title()}" if treatment.treatment_type else "Treatment",
                "description": f"{treatment.regimen}" if treatment.regimen else f"Treating physician: {treatment.treating_physician}" if treatment.treating_physician else "Treatment administered",
                "details": {
                    "regimen": treatment.regimen,
                    "treatment_type": treatment.treatment_type.value.title() if treatment.treatment_type else None,
                    "treatment_status": treatment.treatment_status.value.title() if treatment.treatment_status else None,
                    "treating_physician": treatment.treating_physician,
                    "treatment_center": treatment.treatment_center,
                    "cycles_planned": treatment.cycles_planned,
                    "cycles_delivered": treatment.cycles_delivered,
                    "dose": treatment.dose,
                    "start_date": treatment.start_date.isoformat() if treatment.start_date else None,
                    "end_date": treatment.end_date.isoformat() if treatment.end_date else None,
                    "protocol_name": treatment.protocol_name,
                    "route_of_administration": treatment.route_of_administration
                },
                "id": treatment.id,
                "url": f"/treatments/{treatment.id}"
            })

    # Add follow-up visit events
    for visit in follow_up_visits:
        if visit.visit_date:
            timeline_events.append({
                "date": visit.visit_date.isoformat() if visit.visit_date else None,
                "type": "follow_up",
                "title": f"Follow-Up Visit" + (f" - {visit.visit_type}" if visit.visit_type else ""),
                "description": f"Attending: {visit.attending_physician}" if visit.attending_physician else "Follow-up appointment",
                "details": {
                    "attending_physician": visit.attending_physician,
                    "visit_type": visit.visit_type,
                    "kps_score": visit.kps_score,
                    "neurological_status": visit.neurological_status.value.title() if visit.neurological_status else None,
                    "ecog_score": f"ECOG {visit.ecog_score.value}" if visit.ecog_score else None,
                    "steroid_dose_mg": f"{visit.steroid_dose_mg} mg" if visit.steroid_dose_mg else None,
                    "symptoms": visit.symptoms,
                    "physical_exam_findings": visit.physical_exam_findings,
                    "next_appointment_date": visit.next_appointment_date.isoformat() if visit.next_appointment_date else None,
                    "treatment_plan": visit.treatment_plan
                },
                "id": visit.id,
                "url": f"/follow-up-visits/{visit.id}"
            })

    # Add initial diagnosis event if available
    if patient.initial_diagnosis_date:
        timeline_events.append({
            "date": patient.initial_diagnosis_date.isoformat() if patient.initial_diagnosis_date else None,
            "type": "diagnosis",
            "title": "Initial Diagnosis",
            "description": f"Primary location: {patient.primary_location}" if patient.primary_location else "Initial GBM diagnosis",
            "details": {
                "primary_location": patient.primary_location,
                "referring_physician": patient.referring_physician
            },
            "id": None,
            "url": None
        })

    # Sort events by date safely for Vis.js timeline
    try:
        def safe_date_key(event):
            date_val = event["date"]
            if date_val is None:
                return ""
            elif hasattr(date_val, 'isoformat'):
                return date_val.isoformat()
            else:
                return str(date_val)

        timeline_events.sort(key=safe_date_key, reverse=False)
    except Exception as e:
        # If sorting fails, just proceed without sorting to preserve events
        print(f"Timeline sorting error: {e}")
        pass

    # Convert timeline events to JSON string for JavaScript
    timeline_events_json = json.dumps(timeline_events)

    return templates.TemplateResponse("patient_timeline_interactive.html", {
        "request": request,
        "patient": patient,
        "timeline_events": timeline_events,
        "timeline_events_json": timeline_events_json,
        "title": f"Interactive Timeline for {patient.first_name} {patient.last_name}"
    })

@app.get("/api/patients/{patient_id}/timeline")
async def api_get_patient_timeline(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get all surgeries for this patient
    surgeries = db.query(Surgery).filter(Surgery.patient_id == patient_id).all()

    # Get all pathologies for this patient
    pathologies = db.query(Pathology).filter(Pathology.patient_id == patient_id).all()

    # Get all treatments for this patient
    treatments = db.query(Treatment).filter(Treatment.patient_id == patient_id).all()

    # Get all follow-up visits for this patient
    follow_up_visits = db.query(FollowUpVisit).filter(FollowUpVisit.patient_id == patient_id).all()

    # Create timeline events for API response
    timeline_events = []

    # Add surgery events
    for surgery in surgeries:
        if surgery.surgery_date:
            timeline_events.append({
                "date": surgery.surgery_date.isoformat() if surgery.surgery_date else None,
                "type": "surgery",
                "title": f"{surgery.surgery_type.value.replace('_', ' ').title()}" if surgery.surgery_type else "Surgery",
                "description": f"Performed by {surgery.surgeon_name}" if surgery.surgeon_name else "Surgery performed",
                "details": {
                    "surgeon": surgery.surgeon_name,
                    "hospital": surgery.hospital,
                    "extent_of_resection": surgery.extent_of_resection,
                    "complications": surgery.complications,
                    "operative_time_minutes": surgery.operative_time_minutes,
                    "estimated_blood_loss_ml": surgery.estimated_blood_loss_ml
                },
                "reference_id": surgery.id,
                "reference_url": f"/surgeries/{surgery.id}"
            })

    # Add pathology events
    for pathology in pathologies:
        if pathology.specimen_date:
            timeline_events.append({
                "date": pathology.specimen_date.isoformat() if pathology.specimen_date else None,
                "type": "pathology",
                "title": pathology.histologic_diagnosis or "Pathology Report",
                "description": f"Analyzed by {pathology.pathologist_name}" if pathology.pathologist_name else "Pathology analysis",
                "details": {
                    "pathologist": pathology.pathologist_name,
                    "who_grade": pathology.who_grade.value if pathology.who_grade else None,
                    "idh_status": pathology.idh_status.value if pathology.idh_status else None,
                    "mgmt_status": pathology.mgmt_status.value if pathology.mgmt_status else None,
                    "ki67_index": pathology.ki67_index,
                    "tumor_cellularity_percent": pathology.tumor_cellularity_percent,
                    "necrosis_present": pathology.necrosis_present,
                    "microvascular_proliferation": pathology.microvascular_proliferation
                },
                "reference_id": pathology.id,
                "reference_url": f"/pathologies/{pathology.id}"
            })

    # Add treatment events
    for treatment in treatments:
        if treatment.start_date:
            timeline_events.append({
                "date": treatment.start_date.isoformat() if treatment.start_date else None,
                "type": "treatment",
                "title": f"{treatment.treatment_type.value.replace('_', ' ').title()}" if treatment.treatment_type else "Treatment",
                "description": f"{treatment.regimen}" if treatment.regimen else f"Treating physician: {treatment.treating_physician}" if treatment.treating_physician else "Treatment administered",
                "details": {
                    "regimen": treatment.regimen,
                    "treatment_type": treatment.treatment_type.value if treatment.treatment_type else None,
                    "treatment_status": treatment.treatment_status.value if treatment.treatment_status else None,
                    "treating_physician": treatment.treating_physician,
                    "treatment_center": treatment.treatment_center,
                    "cycles_planned": treatment.cycles_planned,
                    "cycles_delivered": treatment.cycles_delivered,
                    "dose": treatment.dose,
                    "start_date": treatment.start_date.isoformat() if treatment.start_date else None,
                    "end_date": treatment.end_date.isoformat() if treatment.end_date else None
                },
                "reference_id": treatment.id,
                "reference_url": f"/treatments/{treatment.id}"
            })

    # Add follow-up visit events
    for visit in follow_up_visits:
        if visit.visit_date:
            timeline_events.append({
                "date": visit.visit_date.isoformat() if visit.visit_date else None,
                "type": "follow_up",
                "title": f"Follow-Up Visit" + (f" - {visit.visit_type}" if visit.visit_type else ""),
                "description": f"Attending: {visit.attending_physician}" if visit.attending_physician else "Follow-up appointment",
                "details": {
                    "attending_physician": visit.attending_physician,
                    "visit_type": visit.visit_type,
                    "kps_score": visit.kps_score,
                    "neurological_status": visit.neurological_status.value.title() if visit.neurological_status else None,
                    "ecog_score": f"ECOG {visit.ecog_score.value}" if visit.ecog_score else None,
                    "steroid_dose_mg": f"{visit.steroid_dose_mg} mg" if visit.steroid_dose_mg else None,
                    "symptoms": visit.symptoms,
                    "physical_exam_findings": visit.physical_exam_findings,
                    "next_appointment_date": visit.next_appointment_date.isoformat() if visit.next_appointment_date else None,
                    "treatment_plan": visit.treatment_plan
                },
                "id": visit.id,
                "url": f"/follow-up-visits/{visit.id}"
            })

    # Add initial diagnosis event if available
    if patient.initial_diagnosis_date:
        timeline_events.append({
            "date": patient.initial_diagnosis_date.isoformat() if patient.initial_diagnosis_date else None,
            "type": "diagnosis",
            "title": "Initial Diagnosis",
            "description": f"Primary location: {patient.primary_location}" if patient.primary_location else "Initial GBM diagnosis",
            "details": {
                "primary_location": patient.primary_location,
                "referring_physician": patient.referring_physician
            },
            "reference_id": None,
            "reference_url": None
        })

    # Sort events by date (most recent first) - handle mixed date types safely
    def safe_date_key(event):
        date_val = event["date"]
        if date_val is None:
            return ""
        elif hasattr(date_val, 'isoformat'):
            return date_val.isoformat()
        else:
            return str(date_val)

    timeline_events.sort(key=safe_date_key, reverse=True)

    return {
        "patient_id": patient_id,
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "patient_mrn": patient.medical_record_number,
        "timeline_events": timeline_events,
        "total_events": len(timeline_events)
    }

@app.get("/api/patients/navigation/{patient_id}")
async def api_get_patient_navigation(patient_id: int, direction: str, db: Session = Depends(get_db)):
    """Get next or previous patient for navigation between timelines"""
    current_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not current_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if direction == "next":
        next_patient = db.query(Patient).filter(Patient.id > patient_id).order_by(Patient.id.asc()).first()
        return {"patient_id": next_patient.id if next_patient else None}
    elif direction == "previous":
        prev_patient = db.query(Patient).filter(Patient.id < patient_id).order_by(Patient.id.desc()).first()
        return {"patient_id": prev_patient.id if prev_patient else None}
    else:
        raise HTTPException(status_code=400, detail="Direction must be 'next' or 'previous'")

# Surgery CRUD Operations

@app.get("/surgeries", response_class=HTMLResponse)
async def get_surgeries(request: Request, db: Session = Depends(get_db)):
    surgeries = db.query(Surgery).join(Patient).all()
    return templates.TemplateResponse("surgeries.html", {
        "request": request,
        "surgeries": surgeries,
        "title": "All Surgeries"
    })

@app.get("/surgeries/{surgery_id}", response_class=HTMLResponse)
async def get_surgery_detail(request: Request, surgery_id: int, db: Session = Depends(get_db)):
    surgery = db.query(Surgery).filter(Surgery.id == surgery_id).first()
    if not surgery:
        raise HTTPException(status_code=404, detail="Surgery not found")

    return templates.TemplateResponse("surgery_detail.html", {
        "request": request,
        "surgery": surgery,
        "title": f"Surgery: {surgery.surgery_type.value.replace('_', ' ').title()}"
    })

@app.get("/patients/{patient_id}/surgeries", response_class=HTMLResponse)
async def get_patient_surgeries(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    surgeries = db.query(Surgery).filter(Surgery.patient_id == patient_id).all()
    return templates.TemplateResponse("patient_surgeries.html", {
        "request": request,
        "patient": patient,
        "surgeries": surgeries,
        "title": f"Surgeries for {patient.first_name} {patient.last_name}"
    })

# Surgery API Endpoints

@app.get("/api/surgeries")
async def api_get_surgeries(db: Session = Depends(get_db)):
    surgeries = db.query(Surgery).join(Patient).all()
    return {
        "surgeries": [
            {
                "id": s.id,
                "patient_name": f"{s.patient.first_name} {s.patient.last_name}",
                "patient_mrn": s.patient.medical_record_number,
                "surgery_date": s.surgery_date.isoformat() if s.surgery_date else None,
                "surgery_type": s.surgery_type.value if s.surgery_type else None,
                "surgeon_name": s.surgeon_name,
                "extent_of_resection": s.extent_of_resection
            }
            for s in surgeries
        ]
    }

@app.get("/api/surgeries/{surgery_id}")
async def api_get_surgery(surgery_id: int, db: Session = Depends(get_db)):
    surgery = db.query(Surgery).filter(Surgery.id == surgery_id).first()
    if not surgery:
        raise HTTPException(status_code=404, detail="Surgery not found")

    return {
        "id": surgery.id,
        "patient_id": surgery.patient_id,
        "patient_name": f"{surgery.patient.first_name} {surgery.patient.last_name}",
        "patient_mrn": surgery.patient.medical_record_number,
        "surgery_date": surgery.surgery_date.isoformat() if surgery.surgery_date else None,
        "surgery_type": surgery.surgery_type.value if surgery.surgery_type else None,
        "surgeon_name": surgery.surgeon_name,
        "hospital": surgery.hospital,
        "preop_tumor_size": surgery.preop_tumor_size,
        "tumor_location": surgery.tumor_location,
        "laterality": surgery.laterality,
        "procedure_details": surgery.procedure_details,
        "operative_time_minutes": surgery.operative_time_minutes,
        "estimated_blood_loss_ml": surgery.estimated_blood_loss_ml,
        "extent_of_resection": surgery.extent_of_resection,
        "complications": surgery.complications,
        "postop_findings": surgery.postop_findings,
        "discharge_date": surgery.discharge_date.isoformat() if surgery.discharge_date else None,
        "notes": surgery.notes,
        "created_at": surgery.created_at.isoformat() if surgery.created_at else None
    }

@app.get("/api/patients/{patient_id}/surgeries")
async def api_get_patient_surgeries(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    surgeries = db.query(Surgery).filter(Surgery.patient_id == patient_id).all()
    return {
        "patient_id": patient_id,
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "surgeries": [
            {
                "id": s.id,
                "surgery_date": s.surgery_date.isoformat() if s.surgery_date else None,
                "surgery_type": s.surgery_type.value if s.surgery_type else None,
                "surgeon_name": s.surgeon_name,
                "extent_of_resection": s.extent_of_resection,
                "complications": s.complications
            }
            for s in surgeries
        ]
    }

# Surgery CREATE, UPDATE, DELETE operations

@app.post("/api/surgeries")
async def api_create_surgery(surgery_data: SurgeryCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == surgery_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Create new surgery
    surgery = Surgery(**surgery_data.dict())
    db.add(surgery)
    db.commit()
    db.refresh(surgery)

    return {
        "id": surgery.id,
        "patient_id": surgery.patient_id,
        "surgery_date": surgery.surgery_date.isoformat(),
        "surgery_type": surgery.surgery_type.value,
        "surgeon_name": surgery.surgeon_name,
        "extent_of_resection": surgery.extent_of_resection,
        "message": "Surgery created successfully"
    }

@app.put("/api/surgeries/{surgery_id}")
async def api_update_surgery(surgery_id: int, surgery_data: SurgeryUpdate, db: Session = Depends(get_db)):
    surgery = db.query(Surgery).filter(Surgery.id == surgery_id).first()
    if not surgery:
        raise HTTPException(status_code=404, detail="Surgery not found")

    # Update only provided fields
    update_data = surgery_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(surgery, field, value)

    db.commit()
    db.refresh(surgery)

    return {
        "id": surgery.id,
        "patient_id": surgery.patient_id,
        "surgery_date": surgery.surgery_date.isoformat() if surgery.surgery_date else None,
        "surgery_type": surgery.surgery_type.value if surgery.surgery_type else None,
        "surgeon_name": surgery.surgeon_name,
        "extent_of_resection": surgery.extent_of_resection,
        "message": "Surgery updated successfully"
    }

@app.delete("/api/surgeries/{surgery_id}")
async def api_delete_surgery(surgery_id: int, db: Session = Depends(get_db)):
    surgery = db.query(Surgery).filter(Surgery.id == surgery_id).first()
    if not surgery:
        raise HTTPException(status_code=404, detail="Surgery not found")

    db.delete(surgery)
    db.commit()

    return {"message": f"Surgery {surgery_id} deleted successfully"}

# Pathology CRUD Operations

@app.get("/pathologies", response_class=HTMLResponse)
async def get_pathologies(request: Request, db: Session = Depends(get_db)):
    pathologies = db.query(Pathology).join(Patient).all()
    return templates.TemplateResponse("pathologies.html", {
        "request": request,
        "pathologies": pathologies,
        "title": "All Pathology Results"
    })

@app.get("/pathologies/{pathology_id}", response_class=HTMLResponse)
async def get_pathology_detail(request: Request, pathology_id: int, db: Session = Depends(get_db)):
    pathology = db.query(Pathology).filter(Pathology.id == pathology_id).first()
    if not pathology:
        raise HTTPException(status_code=404, detail="Pathology not found")

    return templates.TemplateResponse("pathology_detail.html", {
        "request": request,
        "pathology": pathology,
        "title": f"Pathology: {pathology.histologic_diagnosis}"
    })

@app.get("/patients/{patient_id}/pathologies", response_class=HTMLResponse)
async def get_patient_pathologies(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    pathologies = db.query(Pathology).filter(Pathology.patient_id == patient_id).all()
    return templates.TemplateResponse("patient_pathologies.html", {
        "request": request,
        "patient": patient,
        "pathologies": pathologies,
        "title": f"Pathology Results for {patient.first_name} {patient.last_name}"
    })

# Pathology API Endpoints

@app.get("/api/pathologies")
async def api_get_pathologies(db: Session = Depends(get_db)):
    pathologies = db.query(Pathology).join(Patient).all()
    return {
        "pathologies": [
            {
                "id": p.id,
                "patient_name": f"{p.patient.first_name} {p.patient.last_name}",
                "patient_mrn": p.patient.medical_record_number,
                "specimen_date": p.specimen_date.isoformat() if p.specimen_date else None,
                "histologic_diagnosis": p.histologic_diagnosis,
                "who_grade": p.who_grade.value if p.who_grade else None,
                "idh_status": p.idh_status.value if p.idh_status else None,
                "mgmt_status": p.mgmt_status.value if p.mgmt_status else None,
                "pathologist_name": p.pathologist_name
            }
            for p in pathologies
        ]
    }

@app.get("/api/pathologies/{pathology_id}")
async def api_get_pathology(pathology_id: int, db: Session = Depends(get_db)):
    pathology = db.query(Pathology).filter(Pathology.id == pathology_id).first()
    if not pathology:
        raise HTTPException(status_code=404, detail="Pathology not found")

    return {
        "id": pathology.id,
        "patient_id": pathology.patient_id,
        "patient_name": f"{pathology.patient.first_name} {pathology.patient.last_name}",
        "patient_mrn": pathology.patient.medical_record_number,
        "surgery_id": pathology.surgery_id,
        "specimen_date": pathology.specimen_date.isoformat() if pathology.specimen_date else None,
        "pathologist_name": pathology.pathologist_name,
        "histologic_diagnosis": pathology.histologic_diagnosis,
        "who_grade": pathology.who_grade.value if pathology.who_grade else None,
        "tumor_cellularity_percent": pathology.tumor_cellularity_percent,
        "necrosis_present": pathology.necrosis_present,
        "microvascular_proliferation": pathology.microvascular_proliferation,
        "idh_status": pathology.idh_status.value if pathology.idh_status else None,
        "mgmt_status": pathology.mgmt_status.value if pathology.mgmt_status else None,
        "p53_mutation": pathology.p53_mutation,
        "egfr_amplification": pathology.egfr_amplification,
        "ki67_index": pathology.ki67_index,
        "molecular_markers": pathology.molecular_markers,
        "immunohistochemistry_results": pathology.immunohistochemistry_results,
        "genetic_testing_results": pathology.genetic_testing_results,
        "pathology_report": pathology.pathology_report,
        "notes": pathology.notes,
        "created_at": pathology.created_at.isoformat() if pathology.created_at else None
    }

@app.get("/api/patients/{patient_id}/pathologies")
async def api_get_patient_pathologies(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    pathologies = db.query(Pathology).filter(Pathology.patient_id == patient_id).all()
    return {
        "patient_id": patient_id,
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "pathologies": [
            {
                "id": p.id,
                "specimen_date": p.specimen_date.isoformat() if p.specimen_date else None,
                "histologic_diagnosis": p.histologic_diagnosis,
                "who_grade": p.who_grade.value if p.who_grade else None,
                "idh_status": p.idh_status.value if p.idh_status else None,
                "mgmt_status": p.mgmt_status.value if p.mgmt_status else None,
                "pathologist_name": p.pathologist_name
            }
            for p in pathologies
        ]
    }

# Pathology CREATE, UPDATE, DELETE operations

@app.post("/api/pathologies")
async def api_create_pathology(pathology_data: PathologyCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == pathology_data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Verify surgery exists if surgery_id is provided
    if pathology_data.surgery_id:
        surgery = db.query(Surgery).filter(Surgery.id == pathology_data.surgery_id).first()
        if not surgery:
            raise HTTPException(status_code=404, detail="Surgery not found")

    # Create new pathology
    pathology = Pathology(**pathology_data.dict())
    db.add(pathology)
    db.commit()
    db.refresh(pathology)

    return {
        "id": pathology.id,
        "patient_id": pathology.patient_id,
        "specimen_date": pathology.specimen_date.isoformat(),
        "histologic_diagnosis": pathology.histologic_diagnosis,
        "who_grade": pathology.who_grade.value if pathology.who_grade else None,
        "idh_status": pathology.idh_status.value if pathology.idh_status else None,
        "mgmt_status": pathology.mgmt_status.value if pathology.mgmt_status else None,
        "message": "Pathology created successfully"
    }

@app.put("/api/pathologies/{pathology_id}")
async def api_update_pathology(pathology_id: int, pathology_data: PathologyUpdate, db: Session = Depends(get_db)):
    pathology = db.query(Pathology).filter(Pathology.id == pathology_id).first()
    if not pathology:
        raise HTTPException(status_code=404, detail="Pathology not found")

    # Update only provided fields
    update_data = pathology_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pathology, field, value)

    db.commit()
    db.refresh(pathology)

    return {
        "id": pathology.id,
        "patient_id": pathology.patient_id,
        "specimen_date": pathology.specimen_date.isoformat() if pathology.specimen_date else None,
        "histologic_diagnosis": pathology.histologic_diagnosis,
        "who_grade": pathology.who_grade.value if pathology.who_grade else None,
        "idh_status": pathology.idh_status.value if pathology.idh_status else None,
        "mgmt_status": pathology.mgmt_status.value if pathology.mgmt_status else None,
        "message": "Pathology updated successfully"
    }

@app.delete("/api/pathologies/{pathology_id}")
async def api_delete_pathology(pathology_id: int, db: Session = Depends(get_db)):
    pathology = db.query(Pathology).filter(Pathology.id == pathology_id).first()
    if not pathology:
        raise HTTPException(status_code=404, detail="Pathology not found")

    db.delete(pathology)
    db.commit()

    return {"message": f"Pathology {pathology_id} deleted successfully"}

# Treatment CRUD Operations

@app.get("/treatments", response_class=HTMLResponse)
async def get_treatments(request: Request, db: Session = Depends(get_db)):
    treatments = db.query(Treatment).join(Patient).all()
    return templates.TemplateResponse("treatments.html", {
        "request": request,
        "treatments": treatments,
        "title": "All Treatments"
    })

@app.get("/treatments/{treatment_id}", response_class=HTMLResponse)
async def get_treatment_detail(request: Request, treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    return templates.TemplateResponse("treatment_detail.html", {
        "request": request,
        "treatment": treatment,
        "title": f"Treatment: {treatment.treatment_type.value.replace('_', ' ').title()}"
    })

@app.get("/patients/{patient_id}/treatments", response_class=HTMLResponse)
async def get_patient_treatments(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    treatments = db.query(Treatment).filter(Treatment.patient_id == patient_id).all()
    return templates.TemplateResponse("patient_treatments.html", {
        "request": request,
        "patient": patient,
        "treatments": treatments,
        "title": f"Treatments for {patient.first_name} {patient.last_name}"
    })

@app.get("/api/treatments")
async def api_get_treatments(db: Session = Depends(get_db)):
    treatments = db.query(Treatment).join(Patient).all()
    return {
        "treatments": [
            {
                "id": t.id,
                "patient_name": f"{t.patient.first_name} {t.patient.last_name}",
                "patient_mrn": t.patient.medical_record_number,
                "treatment_type": t.treatment_type.value if t.treatment_type else None,
                "regimen": t.regimen,
                "start_date": t.start_date.isoformat() if t.start_date else None,
                "end_date": t.end_date.isoformat() if t.end_date else None,
                "treatment_status": t.treatment_status.value if t.treatment_status else None,
                "cycles_planned": t.cycles_planned,
                "cycles_delivered": t.cycles_delivered
            }
            for t in treatments
        ]
    }

@app.get("/api/treatments/{treatment_id}")
async def api_get_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    return {
        "id": treatment.id,
        "patient_id": treatment.patient_id,
        "patient_name": f"{treatment.patient.first_name} {treatment.patient.last_name}",
        "patient_mrn": treatment.patient.medical_record_number,
        "treatment_type": treatment.treatment_type.value if treatment.treatment_type else None,
        "start_date": treatment.start_date.isoformat() if treatment.start_date else None,
        "end_date": treatment.end_date.isoformat() if treatment.end_date else None,
        "regimen": treatment.regimen,
        "cycles_planned": treatment.cycles_planned,
        "cycles_delivered": treatment.cycles_delivered,
        "dose": treatment.dose,
        "treatment_status": treatment.treatment_status.value if treatment.treatment_status else None,
        "protocol_name": treatment.protocol_name,
        "treating_physician": treatment.treating_physician,
        "treatment_center": treatment.treatment_center,
        "radiation_dose_gy": float(treatment.radiation_dose_gy) if treatment.radiation_dose_gy else None,
        "radiation_fractions": treatment.radiation_fractions,
        "radiation_technique": treatment.radiation_technique,
        "chemotherapy_regimen": treatment.chemotherapy_regimen,
        "drug_names": treatment.drug_names,
        "dosing_schedule": treatment.dosing_schedule,
        "route_of_administration": treatment.route_of_administration,
        "response_assessment": treatment.response_assessment,
        "toxicities": treatment.toxicities,
        "dose_modifications": treatment.dose_modifications,
        "reason_for_discontinuation": treatment.reason_for_discontinuation,
        "notes": treatment.notes,
        "created_at": treatment.created_at.isoformat() if treatment.created_at else None
    }

@app.get("/api/patients/{patient_id}/treatments")
async def api_get_patient_treatments(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    treatments = db.query(Treatment).filter(Treatment.patient_id == patient_id).all()
    return {
        "patient_id": patient_id,
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "patient_mrn": patient.medical_record_number,
        "treatments": [
            {
                "id": t.id,
                "treatment_type": t.treatment_type.value if t.treatment_type else None,
                "regimen": t.regimen,
                "start_date": t.start_date.isoformat() if t.start_date else None,
                "end_date": t.end_date.isoformat() if t.end_date else None,
                "treatment_status": t.treatment_status.value if t.treatment_status else None,
                "cycles_planned": t.cycles_planned,
                "cycles_delivered": t.cycles_delivered,
                "dose": t.dose
            }
            for t in treatments
        ]
    }

@app.post("/api/treatments")
async def api_create_treatment(treatment: TreatmentCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == treatment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db_treatment = Treatment(**treatment.dict())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)

    return {"message": "Treatment created successfully", "treatment_id": db_treatment.id}

@app.put("/api/treatments/{treatment_id}")
async def api_update_treatment(treatment_id: int, treatment: TreatmentUpdate, db: Session = Depends(get_db)):
    db_treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if not db_treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    for field, value in treatment.dict(exclude_unset=True).items():
        setattr(db_treatment, field, value)

    db.commit()
    db.refresh(db_treatment)

    return {"message": "Treatment updated successfully", "treatment_id": treatment_id}

@app.delete("/api/treatments/{treatment_id}")
async def api_delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    db.delete(treatment)
    db.commit()

    return {"message": f"Treatment {treatment_id} deleted successfully"}

# Follow-Up Visit CRUD Operations

@app.get("/follow-up-visits", response_class=HTMLResponse)
async def get_follow_up_visits(request: Request, db: Session = Depends(get_db)):
    visits = db.query(FollowUpVisit).join(Patient).all()
    return templates.TemplateResponse("follow_up_visits.html", {
        "request": request,
        "visits": visits,
        "title": "All Follow-Up Visits"
    })

@app.get("/follow-up-visits/{visit_id}", response_class=HTMLResponse)
async def get_follow_up_visit_detail(request: Request, visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(FollowUpVisit).filter(FollowUpVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Follow-up visit not found")

    return templates.TemplateResponse("follow_up_visit_detail.html", {
        "request": request,
        "visit": visit,
        "title": f"Follow-Up Visit: {visit.visit_date}"
    })

@app.get("/patients/{patient_id}/follow-up-visits", response_class=HTMLResponse)
async def get_patient_follow_up_visits(request: Request, patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    visits = db.query(FollowUpVisit).filter(FollowUpVisit.patient_id == patient_id).order_by(FollowUpVisit.visit_date.desc()).all()
    return templates.TemplateResponse("patient_follow_up_visits.html", {
        "request": request,
        "patient": patient,
        "visits": visits,
        "title": f"Follow-Up Visits for {patient.first_name} {patient.last_name}"
    })

@app.get("/api/follow-up-visits")
async def api_get_follow_up_visits(db: Session = Depends(get_db)):
    visits = db.query(FollowUpVisit).join(Patient).all()
    return {
        "visits": [
            {
                "id": v.id,
                "patient_name": f"{v.patient.first_name} {v.patient.last_name}",
                "patient_mrn": v.patient.medical_record_number,
                "visit_date": v.visit_date.isoformat() if v.visit_date else None,
                "visit_type": v.visit_type,
                "attending_physician": v.attending_physician,
                "kps_score": v.kps_score,
                "neurological_status": v.neurological_status.value if v.neurological_status else None,
                "ecog_score": v.ecog_score.value if v.ecog_score else None,
                "next_appointment_date": v.next_appointment_date.isoformat() if v.next_appointment_date else None
            }
            for v in visits
        ]
    }

@app.get("/api/follow-up-visits/{visit_id}")
async def api_get_follow_up_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(FollowUpVisit).filter(FollowUpVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Follow-up visit not found")

    return {
        "id": visit.id,
        "patient_id": visit.patient_id,
        "patient_name": f"{visit.patient.first_name} {visit.patient.last_name}",
        "patient_mrn": visit.patient.medical_record_number,
        "visit_date": visit.visit_date.isoformat() if visit.visit_date else None,
        "visit_type": visit.visit_type,
        "attending_physician": visit.attending_physician,
        "kps_score": visit.kps_score,
        "neurological_status": visit.neurological_status.value if visit.neurological_status else None,
        "steroid_dose_mg": float(visit.steroid_dose_mg) if visit.steroid_dose_mg else None,
        "ecog_score": visit.ecog_score.value if visit.ecog_score else None,
        "symptoms": visit.symptoms,
        "physical_exam_findings": visit.physical_exam_findings,
        "next_appointment_date": visit.next_appointment_date.isoformat() if visit.next_appointment_date else None,
        "imaging_date": visit.imaging_date.isoformat() if visit.imaging_date else None,
        "imaging_type": visit.imaging_type,
        "tumor_measurements": visit.tumor_measurements,
        "imaging_notes": visit.imaging_notes,
        "lab_date": visit.lab_date.isoformat() if visit.lab_date else None,
        "lab_results": visit.lab_results,
        "current_medications": visit.current_medications,
        "medication_changes": visit.medication_changes,
        "next_visit_date": visit.next_visit_date.isoformat() if visit.next_visit_date else None,
        "next_imaging_date": visit.next_imaging_date.isoformat() if visit.next_imaging_date else None,
        "treatment_plan": visit.treatment_plan,
        "notes": visit.notes,
        "created_at": visit.created_at.isoformat() if visit.created_at else None
    }

@app.get("/api/patients/{patient_id}/follow-up-visits")
async def api_get_patient_follow_up_visits(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    visits = db.query(FollowUpVisit).filter(FollowUpVisit.patient_id == patient_id).order_by(FollowUpVisit.visit_date.desc()).all()
    return {
        "patient_id": patient_id,
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "patient_mrn": patient.medical_record_number,
        "visits": [
            {
                "id": v.id,
                "visit_date": v.visit_date.isoformat() if v.visit_date else None,
                "visit_type": v.visit_type,
                "attending_physician": v.attending_physician,
                "kps_score": v.kps_score,
                "neurological_status": v.neurological_status.value if v.neurological_status else None,
                "ecog_score": v.ecog_score.value if v.ecog_score else None,
                "steroid_dose_mg": float(v.steroid_dose_mg) if v.steroid_dose_mg else None,
                "next_appointment_date": v.next_appointment_date.isoformat() if v.next_appointment_date else None
            }
            for v in visits
        ]
    }

@app.post("/api/follow-up-visits")
async def api_create_follow_up_visit(visit: FollowUpVisitCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == visit.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db_visit = FollowUpVisit(**visit.dict())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)

    return {"message": "Follow-up visit created successfully", "visit_id": db_visit.id}

@app.put("/api/follow-up-visits/{visit_id}")
async def api_update_follow_up_visit(visit_id: int, visit: FollowUpVisitUpdate, db: Session = Depends(get_db)):
    db_visit = db.query(FollowUpVisit).filter(FollowUpVisit.id == visit_id).first()
    if not db_visit:
        raise HTTPException(status_code=404, detail="Follow-up visit not found")

    for field, value in visit.dict(exclude_unset=True).items():
        setattr(db_visit, field, value)

    db.commit()
    db.refresh(db_visit)

    return {"message": "Follow-up visit updated successfully", "visit_id": visit_id}

@app.delete("/api/follow-up-visits/{visit_id}")
async def api_delete_follow_up_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(FollowUpVisit).filter(FollowUpVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Follow-up visit not found")

    db.delete(visit)
    db.commit()

    return {"message": f"Follow-up visit {visit_id} deleted successfully"}

@app.get("/reports", response_class=HTMLResponse)
async def get_reports(
    request: Request,
    db: Session = Depends(get_db),
    idh_status: str = None,
    mgmt_status: str = None,
    age_min: int = None,
    age_max: int = None,
    surgery_date_start: str = None,
    surgery_date_end: str = None,
    who_grade: str = None
):
    # Start with all patients who have pathology data
    query = db.query(Patient).join(Pathology, Patient.id == Pathology.patient_id)

    # Apply filters
    filters_applied = []

    if idh_status and idh_status != "all":
        if idh_status == "wild_type":
            query = query.filter(Pathology.idh_status == IDHStatus.WILD_TYPE)
            filters_applied.append(f"IDH: Wild-type")
        elif idh_status == "mutated":
            query = query.filter(Pathology.idh_status == IDHStatus.MUTATED)
            filters_applied.append(f"IDH: Mutated")

    if mgmt_status and mgmt_status != "all":
        if mgmt_status == "methylated":
            query = query.filter(Pathology.mgmt_status == MGMTStatus.METHYLATED)
            filters_applied.append(f"MGMT: Methylated")
        elif mgmt_status == "unmethylated":
            query = query.filter(Pathology.mgmt_status == MGMTStatus.UNMETHYLATED)
            filters_applied.append(f"MGMT: Unmethylated")

    if who_grade and who_grade != "all":
        if who_grade == "grade_4":
            query = query.filter(Pathology.who_grade == WHOGrade.GRADE_4)
            filters_applied.append(f"WHO Grade: IV")

    # Calculate age from date of birth if age filters are provided
    if age_min is not None or age_max is not None:
        from datetime import date
        current_date = date.today()

        if age_min is not None:
            min_birth_date = date(current_date.year - age_max if age_max else 120, current_date.month, current_date.day)
            query = query.filter(Patient.date_of_birth >= min_birth_date)
            filters_applied.append(f"Age ≥ {age_min}")

        if age_max is not None:
            max_birth_date = date(current_date.year - age_min if age_min else 0, current_date.month, current_date.day)
            query = query.filter(Patient.date_of_birth <= max_birth_date)
            filters_applied.append(f"Age ≤ {age_max}")

    # Apply surgery date filters
    if surgery_date_start or surgery_date_end:
        query = query.join(Surgery, Patient.id == Surgery.patient_id)

        if surgery_date_start:
            from datetime import datetime
            start_date = datetime.strptime(surgery_date_start, "%Y-%m-%d").date()
            query = query.filter(Surgery.surgery_date >= start_date)
            filters_applied.append(f"Surgery ≥ {start_date}")

        if surgery_date_end:
            from datetime import datetime
            end_date = datetime.strptime(surgery_date_end, "%Y-%m-%d").date()
            query = query.filter(Surgery.surgery_date <= end_date)
            filters_applied.append(f"Surgery ≤ {end_date}")

    # Get distinct patients (avoid duplicates from joins)
    patients = query.distinct().all()

    # Build patient cohort data with molecular markers
    cohort_data = []
    for patient in patients:
        # Get the most recent pathology for each patient
        pathology = db.query(Pathology).filter(Pathology.patient_id == patient.id).order_by(Pathology.specimen_date.desc()).first()

        # Get the most recent surgery
        surgery = db.query(Surgery).filter(Surgery.patient_id == patient.id).order_by(Surgery.surgery_date.desc()).first()

        # Calculate age
        age = None
        if patient.date_of_birth:
            from datetime import date
            today = date.today()
            age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))

        patient_data = {
            "id": patient.id,
            "name": f"{patient.first_name} {patient.last_name}",
            "mrn": patient.medical_record_number,
            "age": age,
            "gender": patient.gender.value if patient.gender else None,
            "diagnosis_date": patient.initial_diagnosis_date,
            "primary_location": patient.primary_location,
            "idh_status": pathology.idh_status.value if pathology and pathology.idh_status else "Unknown",
            "mgmt_status": pathology.mgmt_status.value if pathology and pathology.mgmt_status else "Unknown",
            "who_grade": f"Grade {pathology.who_grade.value}" if pathology and pathology.who_grade else "Unknown",
            "ki67_index": pathology.ki67_index if pathology else None,
            "surgery_date": surgery.surgery_date if surgery else None,
            "extent_of_resection": surgery.extent_of_resection if surgery else None,
        }
        cohort_data.append(patient_data)

    # Generate summary statistics
    total_patients = len(cohort_data)

    # IDH status distribution
    idh_wild_type = sum(1 for p in cohort_data if p["idh_status"] == "wild_type")
    idh_mutated = sum(1 for p in cohort_data if p["idh_status"] == "mutated")
    idh_unknown = sum(1 for p in cohort_data if p["idh_status"] == "Unknown")

    # MGMT status distribution
    mgmt_methylated = sum(1 for p in cohort_data if p["mgmt_status"] == "methylated")
    mgmt_unmethylated = sum(1 for p in cohort_data if p["mgmt_status"] == "unmethylated")
    mgmt_unknown = sum(1 for p in cohort_data if p["mgmt_status"] == "Unknown")

    # Age statistics
    ages = [p["age"] for p in cohort_data if p["age"] is not None]
    age_stats = {
        "mean": round(sum(ages) / len(ages), 1) if ages else None,
        "median": sorted(ages)[len(ages)//2] if ages else None,
        "min": min(ages) if ages else None,
        "max": max(ages) if ages else None
    }

    # Gender distribution
    male_count = sum(1 for p in cohort_data if p["gender"] == "male")
    female_count = sum(1 for p in cohort_data if p["gender"] == "female")

    summary_stats = {
        "total_patients": total_patients,
        "idh_distribution": {
            "wild_type": idh_wild_type,
            "mutated": idh_mutated,
            "unknown": idh_unknown
        },
        "mgmt_distribution": {
            "methylated": mgmt_methylated,
            "unmethylated": mgmt_unmethylated,
            "unknown": mgmt_unknown
        },
        "age_stats": age_stats,
        "gender_distribution": {
            "male": male_count,
            "female": female_count
        }
    }

    return templates.TemplateResponse("reports.html", {
        "request": request,
        "cohort_data": cohort_data,
        "summary_stats": summary_stats,
        "filters_applied": filters_applied,
        "current_filters": {
            "idh_status": idh_status,
            "mgmt_status": mgmt_status,
            "age_min": age_min,
            "age_max": age_max,
            "surgery_date_start": surgery_date_start,
            "surgery_date_end": surgery_date_end,
            "who_grade": who_grade
        }
    })

@app.get("/api/reports/export")
async def export_reports(
    db: Session = Depends(get_db),
    idh_status: str = None,
    mgmt_status: str = None,
    age_min: int = None,
    age_max: int = None,
    surgery_date_start: str = None,
    surgery_date_end: str = None,
    who_grade: str = None,
    format: str = "json"
):
    # Use the same filtering logic as the main reports endpoint
    query = db.query(Patient).join(Pathology, Patient.id == Pathology.patient_id)

    # Apply filters (same logic as get_reports)
    if idh_status and idh_status != "all":
        if idh_status == "wild_type":
            query = query.filter(Pathology.idh_status == IDHStatus.WILD_TYPE)
        elif idh_status == "mutated":
            query = query.filter(Pathology.idh_status == IDHStatus.MUTATED)

    if mgmt_status and mgmt_status != "all":
        if mgmt_status == "methylated":
            query = query.filter(Pathology.mgmt_status == MGMTStatus.METHYLATED)
        elif mgmt_status == "unmethylated":
            query = query.filter(Pathology.mgmt_status == MGMTStatus.UNMETHYLATED)

    if who_grade and who_grade != "all":
        if who_grade == "grade_4":
            query = query.filter(Pathology.who_grade == WHOGrade.GRADE_4)

    # Apply age filters
    if age_min is not None:
        query = query.filter(Patient.age >= age_min)
    if age_max is not None:
        query = query.filter(Patient.age <= age_max)

    # Apply surgery date filters
    if surgery_date_start or surgery_date_end:
        query = query.join(Surgery, Patient.id == Surgery.patient_id)
        if surgery_date_start:
            query = query.filter(Surgery.surgery_date >= surgery_date_start)
        if surgery_date_end:
            query = query.filter(Surgery.surgery_date <= surgery_date_end)

    patients = query.distinct().all()

    if format == "csv":
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'Patient Name', 'MRN', 'Age', 'Gender', 'Date of Birth',
            'Primary Location', 'IDH Status', 'MGMT Status', 'WHO Grade',
            'Ki-67 Index', 'Surgery Date', 'Extent of Resection',
            'Surgeon Name', 'Hospital', 'Pathologist Name'
        ])

        # Write patient data
        for patient in patients:
            # Get pathology and surgery data
            pathology = db.query(Pathology).filter(Pathology.patient_id == patient.id).first()
            surgery = db.query(Surgery).filter(Surgery.patient_id == patient.id).first()

            # Calculate age
            today = date.today()
            age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day)) if patient.date_of_birth else None

            writer.writerow([
                f"{patient.first_name} {patient.last_name}",
                patient.medical_record_number,
                age,
                patient.gender,
                patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else '',
                patient.primary_location or '',
                pathology.idh_status.value if pathology and pathology.idh_status else '',
                pathology.mgmt_status.value if pathology and pathology.mgmt_status else '',
                pathology.who_grade.value if pathology and pathology.who_grade else '',
                pathology.ki67_index if pathology and pathology.ki67_index else '',
                surgery.surgery_date.strftime('%Y-%m-%d') if surgery and surgery.surgery_date else '',
                surgery.extent_of_resection if surgery else '',
                surgery.surgeon_name if surgery else '',
                surgery.hospital if surgery else '',
                pathology.pathologist_name if pathology else ''
            ])

        content = output.getvalue()
        output.close()

        # Return CSV as downloadable file
        return StreamingResponse(
            io.StringIO(content),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=gbm_cohort_{date.today().isoformat()}.csv"}
        )

    else:
        # Return JSON format
        patient_data = []
        for patient in patients:
            pathology = db.query(Pathology).filter(Pathology.patient_id == patient.id).first()
            surgery = db.query(Surgery).filter(Surgery.patient_id == patient.id).first()

            # Calculate age
            today = date.today()
            age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day)) if patient.date_of_birth else None

            patient_data.append({
                "id": patient.id,
                "name": f"{patient.first_name} {patient.last_name}",
                "mrn": patient.medical_record_number,
                "age": age,
                "gender": patient.gender,
                "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
                "primary_location": patient.primary_location,
                "idh_status": pathology.idh_status.value if pathology and pathology.idh_status else None,
                "mgmt_status": pathology.mgmt_status.value if pathology and pathology.mgmt_status else None,
                "who_grade": pathology.who_grade.value if pathology and pathology.who_grade else None,
                "ki67_index": pathology.ki67_index if pathology else None,
                "surgery_date": surgery.surgery_date.isoformat() if surgery and surgery.surgery_date else None,
                "extent_of_resection": surgery.extent_of_resection if surgery else None,
                "surgeon_name": surgery.surgeon_name if surgery else None,
                "hospital": surgery.hospital if surgery else None,
                "pathologist_name": pathology.pathologist_name if pathology else None
            })

        return {"patients": patient_data, "count": len(patient_data)}

@app.get("/hello")
async def hello_world():
    return {"message": "Hello World!"}