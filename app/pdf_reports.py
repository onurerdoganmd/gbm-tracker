from datetime import datetime, date
from typing import List, Dict, Optional, Any
import io
import base64
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.platypus import PageBreak, Image
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from sqlalchemy.orm import Session
from .analytics import AdvancedAnalyticsEngine, SurvivalAnalysisEngine, TreatmentResponseAnalyzer, MolecularCorrelationAnalyzer
from .models import Patient


class ClinicalReportGenerator:
    def __init__(self, db: Session):
        self.db = db
        self.analytics_engine = AdvancedAnalyticsEngine(db)
        self.survival_engine = SurvivalAnalysisEngine(db)
        self.treatment_analyzer = TreatmentResponseAnalyzer(db)
        self.molecular_analyzer = MolecularCorrelationAnalyzer(db)

    def generate_comprehensive_report(self,
                                    patient_ids: Optional[List[int]] = None,
                                    include_charts: bool = True,
                                    title: str = "GBM Clinical Research Analytics Report") -> bytes:

        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab is required for PDF generation. Install with: pip install reportlab")

        # Create PDF buffer
        buffer = io.BytesIO()

        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        # Build the content
        story = []
        styles = getSampleStyleSheet()

        # Add custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#1f2937')
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=20,
            textColor=HexColor('#374151')
        )

        # Title page
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        story.append(Spacer(1, 24))

        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        analytics_data = self.analytics_engine.generate_comprehensive_analytics(patient_ids)

        summary_data = [
            ["Metric", "Value"],
            ["Total Patients", str(analytics_data['patient_cohort_size'])],
            ["Patients with Survival Data", str(analytics_data['survival_analysis']['overall_survival']['count'])],
            ["Mean Overall Survival (days)", f"{analytics_data['survival_analysis']['overall_survival']['mean_days']:.1f}" if analytics_data['survival_analysis']['overall_survival']['mean_days'] else "N/A"],
            ["Progression Rate", f"{analytics_data['survival_analysis']['progression_rate']:.1%}"],
            ["Overall Response Rate", f"{analytics_data['treatment_response'].get('overall_response_rate', 0):.1%}"],
        ]

        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb'))
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 24))

        # Survival Analysis Section
        story.extend(self._add_survival_analysis_section(analytics_data['survival_analysis'], styles, heading_style))

        # Treatment Response Section
        story.extend(self._add_treatment_response_section(analytics_data['treatment_response'], styles, heading_style))

        # Molecular Correlations Section
        story.extend(self._add_molecular_correlations_section(analytics_data['molecular_correlations'], styles, heading_style))

        # Add charts if requested and available
        if include_charts and MATPLOTLIB_AVAILABLE:
            story.extend(self._add_visualization_section(analytics_data, styles, heading_style))

        # Patient Details Section
        if patient_ids and len(patient_ids) <= 20:  # Only include for small cohorts
            story.extend(self._add_patient_details_section(patient_ids, styles, heading_style))

        # Methodology and Notes
        story.extend(self._add_methodology_section(styles, heading_style))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def _add_survival_analysis_section(self, survival_data: Dict, styles, heading_style) -> List:
        content = []
        content.append(Paragraph("Survival Analysis", heading_style))

        # Create survival analysis table
        survival_table_data = [
            ["Survival Metric", "Mean (days)", "Median (days)", "Sample Size"],
            [
                "Overall Survival",
                f"{survival_data['overall_survival']['mean_days']:.1f}" if survival_data['overall_survival']['mean_days'] else "N/A",
                f"{survival_data['overall_survival']['median_days']:.1f}" if survival_data['overall_survival']['median_days'] else "N/A",
                str(survival_data['overall_survival']['count'])
            ],
            [
                "Time to Progression",
                f"{survival_data['time_to_progression']['mean_days']:.1f}" if survival_data['time_to_progression']['mean_days'] else "N/A",
                f"{survival_data['time_to_progression']['median_days']:.1f}" if survival_data['time_to_progression']['median_days'] else "N/A",
                str(survival_data['time_to_progression']['count'])
            ],
            [
                "Progression-Free Survival",
                f"{survival_data['progression_free_survival']['mean_days']:.1f}" if survival_data['progression_free_survival']['mean_days'] else "N/A",
                f"{survival_data['progression_free_survival']['median_days']:.1f}" if survival_data['progression_free_survival']['median_days'] else "N/A",
                str(survival_data['progression_free_survival']['count'])
            ]
        ]

        survival_table = Table(survival_table_data)
        survival_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb'))
        ]))

        content.append(survival_table)
        content.append(Spacer(1, 12))

        # Add interpretation
        interpretation = f"""
        <b>Key Findings:</b><br/>
        • {survival_data['alive_patients']} of {survival_data['total_patients']} patients are alive<br/>
        • {survival_data['progressed_patients']} patients have experienced progression<br/>
        • Progression rate: {survival_data['progression_rate']:.1%}<br/>
        """
        content.append(Paragraph(interpretation, styles['Normal']))
        content.append(Spacer(1, 24))

        return content

    def _add_treatment_response_section(self, treatment_data: Dict, styles, heading_style) -> List:
        content = []
        content.append(Paragraph("Treatment Response Analysis", heading_style))

        if treatment_data.get('total_treatments', 0) == 0:
            content.append(Paragraph("No treatment response data available.", styles['Normal']))
            content.append(Spacer(1, 24))
            return content

        # Response distribution table
        response_dist = treatment_data.get('response_distribution', {})
        response_table_data = [
            ["Response Category", "Count", "Percentage"],
            ["Complete Response", str(response_dist.get('complete_response', 0)), f"{response_dist.get('complete_response', 0) / treatment_data['total_treatments']:.1%}"],
            ["Partial Response", str(response_dist.get('partial_response', 0)), f"{response_dist.get('partial_response', 0) / treatment_data['total_treatments']:.1%}"],
            ["Stable Disease", str(response_dist.get('stable_disease', 0)), f"{response_dist.get('stable_disease', 0) / treatment_data['total_treatments']:.1%}"],
            ["Progressive Disease", str(response_dist.get('progressive_disease', 0)), f"{response_dist.get('progressive_disease', 0) / treatment_data['total_treatments']:.1%}"]
        ]

        response_table = Table(response_table_data)
        response_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb'))
        ]))

        content.append(response_table)
        content.append(Spacer(1, 12))

        # Key metrics
        metrics_text = f"""
        <b>Treatment Response Summary:</b><br/>
        • Total treatments analyzed: {treatment_data['total_treatments']}<br/>
        • Overall response rate: {treatment_data.get('overall_response_rate', 0):.1%}<br/>
        • Disease control rate: {treatment_data.get('disease_control_rate', 0):.1%}<br/>
        """
        content.append(Paragraph(metrics_text, styles['Normal']))
        content.append(Spacer(1, 24))

        return content

    def _add_molecular_correlations_section(self, molecular_data: Dict, styles, heading_style) -> List:
        content = []
        content.append(Paragraph("Molecular Marker Correlations", heading_style))

        # IDH distribution
        idh_dist = molecular_data.get('idh_distribution', {})
        mgmt_dist = molecular_data.get('mgmt_distribution', {})

        # Create molecular markers summary table
        molecular_table_data = [
            ["Biomarker", "Category", "Count", "Percentage"]
        ]

        total_patients = molecular_data.get('total_patients_with_molecular_data', 1)

        for status, count in idh_dist.items():
            molecular_table_data.append(["IDH Status", status.title(), str(count), f"{count/total_patients:.1%}"])

        for status, count in mgmt_dist.items():
            molecular_table_data.append(["MGMT Status", status.title(), str(count), f"{count/total_patients:.1%}"])

        molecular_table = Table(molecular_table_data)
        molecular_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb'))
        ]))

        content.append(molecular_table)
        content.append(Spacer(1, 24))

        return content

    def _add_visualization_section(self, analytics_data: Dict, styles, heading_style) -> List:
        content = []
        content.append(PageBreak())
        content.append(Paragraph("Statistical Visualizations", heading_style))

        try:
            # Create survival analysis chart
            survival_chart = self._create_survival_chart(analytics_data['survival_analysis'])
            if survival_chart:
                content.append(Image(survival_chart, width=6*inch, height=4*inch))
                content.append(Spacer(1, 12))

            # Create treatment response chart
            response_chart = self._create_response_chart(analytics_data['treatment_response'])
            if response_chart:
                content.append(Image(response_chart, width=6*inch, height=4*inch))
                content.append(Spacer(1, 12))

        except Exception as e:
            content.append(Paragraph(f"Charts could not be generated: {str(e)}", styles['Normal']))

        return content

    def _create_survival_chart(self, survival_data: Dict) -> Optional[io.BytesIO]:
        if not MATPLOTLIB_AVAILABLE:
            return None

        try:
            plt.figure(figsize=(10, 6))

            # Prepare data
            metrics = ['Overall Survival', 'Time to Progression', 'PFS']
            means = [
                survival_data['overall_survival']['mean_days'] or 0,
                survival_data['time_to_progression']['mean_days'] or 0,
                survival_data['progression_free_survival']['mean_days'] or 0
            ]

            # Convert days to months for better readability
            means_months = [m/30.44 for m in means]  # 30.44 average days per month

            plt.bar(metrics, means_months, color=['#3b82f6', '#ef4444', '#10b981'])
            plt.title('Survival Metrics (Mean Values)', fontsize=14, fontweight='bold')
            plt.ylabel('Months')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            plt.close()

            return buffer
        except Exception:
            return None

    def _create_response_chart(self, treatment_data: Dict) -> Optional[io.BytesIO]:
        if not MATPLOTLIB_AVAILABLE or treatment_data.get('total_treatments', 0) == 0:
            return None

        try:
            plt.figure(figsize=(8, 6))

            response_dist = treatment_data.get('response_distribution', {})
            labels = [k.replace('_', ' ').title() for k in response_dist.keys()]
            values = list(response_dist.values())
            colors_list = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']

            plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors_list)
            plt.title('Treatment Response Distribution', fontsize=14, fontweight='bold')

            # Save to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            plt.close()

            return buffer
        except Exception:
            return None

    def _add_patient_details_section(self, patient_ids: List[int], styles, heading_style) -> List:
        content = []
        content.append(PageBreak())
        content.append(Paragraph("Patient Cohort Details", heading_style))

        # Get patient details
        patients = self.db.query(Patient).filter(Patient.id.in_(patient_ids)).all()

        for patient in patients[:10]:  # Limit to first 10 patients
            patient_text = f"""
            <b>{patient.first_name} {patient.last_name}</b> (MRN: {patient.medical_record_number})<br/>
            DOB: {patient.date_of_birth}<br/>
            Diagnosis Date: {patient.initial_diagnosis_date or 'Not recorded'}<br/>
            Primary Location: {patient.primary_location or 'Not recorded'}<br/>
            """
            content.append(Paragraph(patient_text, styles['Normal']))
            content.append(Spacer(1, 12))

        if len(patients) > 10:
            content.append(Paragraph(f"... and {len(patients) - 10} additional patients", styles['Normal']))

        content.append(Spacer(1, 24))
        return content

    def _add_methodology_section(self, styles, heading_style) -> List:
        content = []
        content.append(PageBreak())
        content.append(Paragraph("Methodology and Notes", heading_style))

        methodology_text = """
        <b>Data Analysis Methodology:</b><br/>
        • Survival metrics calculated from diagnosis date to last follow-up or event<br/>
        • Time-to-progression defined as time from diagnosis to first progressive disease<br/>
        • Treatment response assessed using RECIST criteria when available<br/>
        • Molecular markers analyzed for correlation with clinical outcomes<br/>
        • Statistical calculations performed using standard clinical research methods<br/>
        <br/>
        <b>Limitations:</b><br/>
        • Analysis based on available data; missing data may affect results<br/>
        • Follow-up times may vary between patients<br/>
        • Treatment response assessment dependent on imaging availability<br/>
        <br/>
        <b>Generated by:</b> GBM Tracker Advanced Analytics Engine<br/>
        <b>Report Date:</b> {}<br/>
        """.format(datetime.now().strftime('%B %d, %Y'))

        content.append(Paragraph(methodology_text, styles['Normal']))
        return content


def generate_clinical_research_report(db: Session,
                                     patient_ids: Optional[List[int]] = None,
                                     include_charts: bool = True,
                                     title: str = "GBM Clinical Research Analytics Report") -> bytes:
    generator = ClinicalReportGenerator(db)
    return generator.generate_comprehensive_report(
        patient_ids=patient_ids,
        include_charts=include_charts,
        title=title
    )