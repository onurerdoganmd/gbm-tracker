from datetime import datetime, date
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
import statistics
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, case

from .models import Patient, Surgery, Pathology, Treatment, FollowUpVisit
from .models import ImagingResponse, TreatmentStatus, IDHStatus, MGMTStatus, WHOGrade


@dataclass
class SurvivalMetrics:
    patient_id: int
    medical_record_number: str
    diagnosis_date: Optional[date]
    last_follow_up_date: Optional[date]
    progression_date: Optional[date]
    death_date: Optional[date]
    time_to_progression_days: Optional[int]
    overall_survival_days: Optional[int]
    progression_free_survival_days: Optional[int]
    is_alive: bool
    has_progressed: bool


@dataclass
class TreatmentResponse:
    patient_id: int
    treatment_id: int
    treatment_type: str
    start_date: date
    end_date: Optional[date]
    response_category: str  # complete_response, partial_response, stable_disease, progressive_disease
    time_to_response_days: Optional[int]
    duration_of_response_days: Optional[int]
    best_response: str


@dataclass
class MolecularCorrelation:
    idh_status: str
    mgmt_status: str
    who_grade: str
    patient_count: int
    mean_survival_days: Optional[float]
    median_survival_days: Optional[float]
    progression_rate: float
    treatment_response_rate: float


class SurvivalAnalysisEngine:
    def __init__(self, db: Session):
        self.db = db

    def calculate_survival_metrics(self, patient_ids: Optional[List[int]] = None) -> List[SurvivalMetrics]:
        query = self.db.query(Patient)
        if patient_ids:
            query = query.filter(Patient.id.in_(patient_ids))

        patients = query.all()
        survival_metrics = []

        for patient in patients:
            metrics = self._calculate_patient_survival(patient)
            survival_metrics.append(metrics)

        return survival_metrics

    def _calculate_patient_survival(self, patient: Patient) -> SurvivalMetrics:
        diagnosis_date = patient.initial_diagnosis_date

        # Get last follow-up date
        last_follow_up = self.db.query(FollowUpVisit)\
            .filter(FollowUpVisit.patient_id == patient.id)\
            .order_by(FollowUpVisit.visit_date.desc())\
            .first()

        last_follow_up_date = last_follow_up.visit_date if last_follow_up else None

        # Determine progression date (first instance of progressive disease)
        progression_visit = self.db.query(FollowUpVisit)\
            .filter(
                FollowUpVisit.patient_id == patient.id,
                FollowUpVisit.imaging_response == ImagingResponse.PROGRESSIVE_DISEASE
            )\
            .order_by(FollowUpVisit.visit_date.asc())\
            .first()

        progression_date = progression_visit.visit_date if progression_visit else None

        # Calculate survival metrics
        death_date = None  # Would need to be tracked in a separate field
        is_alive = True    # Assume alive unless death date exists
        has_progressed = progression_date is not None

        time_to_progression_days = None
        overall_survival_days = None
        progression_free_survival_days = None

        if diagnosis_date:
            if progression_date:
                time_to_progression_days = (progression_date - diagnosis_date).days
                progression_free_survival_days = time_to_progression_days

            if last_follow_up_date:
                overall_survival_days = (last_follow_up_date - diagnosis_date).days
                if not has_progressed:
                    progression_free_survival_days = overall_survival_days

        return SurvivalMetrics(
            patient_id=patient.id,
            medical_record_number=patient.medical_record_number,
            diagnosis_date=diagnosis_date,
            last_follow_up_date=last_follow_up_date,
            progression_date=progression_date,
            death_date=death_date,
            time_to_progression_days=time_to_progression_days,
            overall_survival_days=overall_survival_days,
            progression_free_survival_days=progression_free_survival_days,
            is_alive=is_alive,
            has_progressed=has_progressed
        )

    def get_survival_statistics(self, patient_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        metrics = self.calculate_survival_metrics(patient_ids)

        # Filter out None values for calculations
        ttp_values = [m.time_to_progression_days for m in metrics if m.time_to_progression_days is not None]
        os_values = [m.overall_survival_days for m in metrics if m.overall_survival_days is not None]
        pfs_values = [m.progression_free_survival_days for m in metrics if m.progression_free_survival_days is not None]

        alive_count = sum(1 for m in metrics if m.is_alive)
        progressed_count = sum(1 for m in metrics if m.has_progressed)

        return {
            "total_patients": len(metrics),
            "alive_patients": alive_count,
            "progressed_patients": progressed_count,
            "progression_rate": progressed_count / len(metrics) if metrics else 0,
            "time_to_progression": {
                "mean_days": statistics.mean(ttp_values) if ttp_values else None,
                "median_days": statistics.median(ttp_values) if ttp_values else None,
                "count": len(ttp_values)
            },
            "overall_survival": {
                "mean_days": statistics.mean(os_values) if os_values else None,
                "median_days": statistics.median(os_values) if os_values else None,
                "count": len(os_values)
            },
            "progression_free_survival": {
                "mean_days": statistics.mean(pfs_values) if pfs_values else None,
                "median_days": statistics.median(pfs_values) if pfs_values else None,
                "count": len(pfs_values)
            }
        }


class TreatmentResponseAnalyzer:
    def __init__(self, db: Session):
        self.db = db

    def analyze_treatment_responses(self, patient_ids: Optional[List[int]] = None) -> List[TreatmentResponse]:
        query = self.db.query(Treatment)
        if patient_ids:
            query = query.filter(Treatment.patient_id.in_(patient_ids))

        treatments = query.all()
        responses = []

        for treatment in treatments:
            response = self._analyze_treatment_response(treatment)
            if response:
                responses.append(response)

        return responses

    def _analyze_treatment_response(self, treatment: Treatment) -> Optional[TreatmentResponse]:
        # Get follow-up visits during treatment period
        follow_ups = self.db.query(FollowUpVisit)\
            .filter(
                FollowUpVisit.patient_id == treatment.patient_id,
                FollowUpVisit.visit_date >= treatment.start_date
            )\
            .order_by(FollowUpVisit.visit_date.asc())\
            .all()

        if treatment.end_date:
            follow_ups = [f for f in follow_ups if f.visit_date <= treatment.end_date]

        if not follow_ups:
            return None

        # Find best response
        responses = [f.imaging_response for f in follow_ups if f.imaging_response]
        if not responses:
            return None

        # Determine best response (priority: CR > PR > SD > PD)
        response_priority = {
            ImagingResponse.COMPLETE_RESPONSE: 4,
            ImagingResponse.PARTIAL_RESPONSE: 3,
            ImagingResponse.STABLE_DISEASE: 2,
            ImagingResponse.PROGRESSIVE_DISEASE: 1
        }

        best_response_enum = max(responses, key=lambda x: response_priority.get(x, 0))
        best_response = best_response_enum.value

        # Calculate time to response (first non-PD response)
        first_response_visit = next(
            (f for f in follow_ups if f.imaging_response and f.imaging_response != ImagingResponse.PROGRESSIVE_DISEASE),
            None
        )

        time_to_response_days = None
        if first_response_visit:
            time_to_response_days = (first_response_visit.visit_date - treatment.start_date).days

        # Calculate duration of response
        duration_of_response_days = None
        if first_response_visit and treatment.end_date:
            progression_visit = next(
                (f for f in follow_ups if f.visit_date > first_response_visit.visit_date and
                 f.imaging_response == ImagingResponse.PROGRESSIVE_DISEASE),
                None
            )

            end_date = progression_visit.visit_date if progression_visit else treatment.end_date
            duration_of_response_days = (end_date - first_response_visit.visit_date).days

        return TreatmentResponse(
            patient_id=treatment.patient_id,
            treatment_id=treatment.id,
            treatment_type=treatment.treatment_type.value,
            start_date=treatment.start_date,
            end_date=treatment.end_date,
            response_category=best_response,
            time_to_response_days=time_to_response_days,
            duration_of_response_days=duration_of_response_days,
            best_response=best_response
        )

    def get_response_statistics(self, patient_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        responses = self.analyze_treatment_responses(patient_ids)

        if not responses:
            return {"total_treatments": 0}

        # Group by treatment type
        by_treatment_type = defaultdict(list)
        for response in responses:
            by_treatment_type[response.treatment_type].append(response)

        # Calculate overall response rates
        total_treatments = len(responses)
        cr_count = sum(1 for r in responses if r.best_response == "complete_response")
        pr_count = sum(1 for r in responses if r.best_response == "partial_response")
        sd_count = sum(1 for r in responses if r.best_response == "stable_disease")
        pd_count = sum(1 for r in responses if r.best_response == "progressive_disease")

        overall_response_rate = (cr_count + pr_count) / total_treatments if total_treatments > 0 else 0
        disease_control_rate = (cr_count + pr_count + sd_count) / total_treatments if total_treatments > 0 else 0

        return {
            "total_treatments": total_treatments,
            "overall_response_rate": overall_response_rate,
            "disease_control_rate": disease_control_rate,
            "response_distribution": {
                "complete_response": cr_count,
                "partial_response": pr_count,
                "stable_disease": sd_count,
                "progressive_disease": pd_count
            },
            "by_treatment_type": {
                treatment_type: {
                    "count": len(type_responses),
                    "response_rate": sum(1 for r in type_responses if r.best_response in ["complete_response", "partial_response"]) / len(type_responses) if type_responses else 0
                }
                for treatment_type, type_responses in by_treatment_type.items()
            }
        }


class MolecularCorrelationAnalyzer:
    def __init__(self, db: Session):
        self.db = db

    def analyze_molecular_correlations(self, patient_ids: Optional[List[int]] = None) -> List[MolecularCorrelation]:
        # Get patients with pathology data
        query = self.db.query(Patient, Pathology)\
            .join(Pathology, Patient.id == Pathology.patient_id)

        if patient_ids:
            query = query.filter(Patient.id.in_(patient_ids))

        results = query.all()

        # Group by molecular marker combinations
        combinations = defaultdict(list)
        for patient, pathology in results:
            key = (
                pathology.idh_status.value if pathology.idh_status else "unknown",
                pathology.mgmt_status.value if pathology.mgmt_status else "unknown",
                pathology.who_grade.value if pathology.who_grade else "unknown"
            )
            combinations[key].append(patient)

        correlations = []
        survival_engine = SurvivalAnalysisEngine(self.db)
        treatment_analyzer = TreatmentResponseAnalyzer(self.db)

        for (idh_status, mgmt_status, who_grade), patients in combinations.items():
            patient_ids_subset = [p.id for p in patients]

            # Calculate survival metrics for this group
            survival_stats = survival_engine.get_survival_statistics(patient_ids_subset)

            # Calculate treatment response for this group
            response_stats = treatment_analyzer.get_response_statistics(patient_ids_subset)

            correlation = MolecularCorrelation(
                idh_status=idh_status,
                mgmt_status=mgmt_status,
                who_grade=who_grade,
                patient_count=len(patients),
                mean_survival_days=survival_stats["overall_survival"]["mean_days"],
                median_survival_days=survival_stats["overall_survival"]["median_days"],
                progression_rate=survival_stats["progression_rate"],
                treatment_response_rate=response_stats.get("overall_response_rate", 0)
            )
            correlations.append(correlation)

        return correlations

    def get_molecular_summary(self, patient_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        correlations = self.analyze_molecular_correlations(patient_ids)

        total_patients = sum(c.patient_count for c in correlations)

        # Group by individual markers
        idh_groups = defaultdict(int)
        mgmt_groups = defaultdict(int)
        grade_groups = defaultdict(int)

        for correlation in correlations:
            idh_groups[correlation.idh_status] += correlation.patient_count
            mgmt_groups[correlation.mgmt_status] += correlation.patient_count
            grade_groups[correlation.who_grade] += correlation.patient_count

        return {
            "total_patients_with_molecular_data": total_patients,
            "idh_distribution": dict(idh_groups),
            "mgmt_distribution": dict(mgmt_groups),
            "grade_distribution": dict(grade_groups),
            "correlations": [
                {
                    "combination": f"IDH-{c.idh_status}/MGMT-{c.mgmt_status}/Grade-{c.who_grade}",
                    "patient_count": c.patient_count,
                    "mean_survival_days": c.mean_survival_days,
                    "progression_rate": c.progression_rate,
                    "response_rate": c.treatment_response_rate
                }
                for c in correlations
            ]
        }


class AdvancedAnalyticsEngine:
    def __init__(self, db: Session):
        self.db = db
        self.survival_engine = SurvivalAnalysisEngine(db)
        self.treatment_analyzer = TreatmentResponseAnalyzer(db)
        self.molecular_analyzer = MolecularCorrelationAnalyzer(db)

    def generate_comprehensive_analytics(self, patient_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        return {
            "survival_analysis": self.survival_engine.get_survival_statistics(patient_ids),
            "treatment_response": self.treatment_analyzer.get_response_statistics(patient_ids),
            "molecular_correlations": self.molecular_analyzer.get_molecular_summary(patient_ids),
            "patient_cohort_size": len(patient_ids) if patient_ids else self.db.query(Patient).count()
        }