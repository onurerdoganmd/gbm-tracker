# 📊 Advanced Analytics Features for GBM Tracker

## Overview

The GBM Tracker now includes comprehensive advanced analytics capabilities for clinical research, including survival analysis, treatment response tracking, molecular marker correlations, and PDF report generation.

## 🔬 New Analytics Features

### 1. **Survival Analysis**
- **Time-to-Progression (TTP)**: Tracks time from diagnosis to first progressive disease
- **Overall Survival (OS)**: Tracks time from diagnosis to last follow-up
- **Progression-Free Survival (PFS)**: Tracks time from diagnosis to progression or last follow-up
- **Statistical Metrics**: Mean, median, and sample sizes for all survival endpoints

### 2. **Treatment Response Tracking**
- **RECIST-based Response Assessment**: Complete response, partial response, stable disease, progressive disease
- **Response Rates**: Overall response rate and disease control rate
- **Time to Response**: Days from treatment start to first response
- **Duration of Response**: Duration of treatment benefit
- **Treatment Type Analysis**: Response rates by treatment modality

### 3. **Molecular Marker Correlation Analysis**
- **IDH Status Correlation**: Wild-type vs. mutated outcomes
- **MGMT Methylation Analysis**: Methylated vs. unmethylated survival differences
- **WHO Grade Integration**: Grade-specific molecular correlations
- **Combination Analysis**: IDH-MGMT interaction effects on survival and treatment response

### 4. **Comprehensive PDF Report Generation**
- **Clinical Research Reports**: Publication-ready analytics reports
- **Statistical Visualizations**: Survival curves and response distribution charts
- **Executive Summary**: Key findings and metrics
- **Methodology Section**: Analysis approach and limitations
- **Patient Cohort Details**: Individual patient summaries (for small cohorts)

## 🚀 API Endpoints

### Survival Analysis
```
GET /api/analytics/survival
GET /api/analytics/survival/details
```
**Parameters:**
- `patient_ids` (optional): Comma-separated list of patient IDs to analyze

### Treatment Response Analysis
```
GET /api/analytics/treatment-response
GET /api/analytics/treatment-response/details
```
**Parameters:**
- `patient_ids` (optional): Comma-separated list of patient IDs to analyze

### Molecular Correlations
```
GET /api/analytics/molecular-correlations
```
**Parameters:**
- `patient_ids` (optional): Comma-separated list of patient IDs to analyze

### Comprehensive Analytics
```
GET /api/analytics/comprehensive
```
**Parameters:**
- `patient_ids` (optional): Comma-separated list of patient IDs to analyze

### PDF Report Generation
```
GET /api/reports/clinical-research-pdf
```
**Parameters:**
- `patient_ids` (optional): Comma-separated list of patient IDs to include
- `include_charts` (optional): Whether to include statistical charts (default: true)
- `title` (optional): Custom report title

## 📈 Example Usage

### 1. Get Survival Analysis for All Patients
```bash
curl "http://localhost:8000/api/analytics/survival"
```

### 2. Get Molecular Correlations for Specific Patients
```bash
curl "http://localhost:8000/api/analytics/molecular-correlations?patient_ids=1,2,3,4,5"
```

### 3. Generate PDF Report for a Cohort
```bash
curl "http://localhost:8000/api/reports/clinical-research-pdf?patient_ids=1,2,3,4,5&title=Pilot%20Study%20Analysis" --output cohort_report.pdf
```

### 4. Get Comprehensive Analytics
```bash
curl "http://localhost:8000/api/analytics/comprehensive"
```

## 📊 Sample Analytics Results

### Survival Analysis Output
```json
{
    "total_patients": 43,
    "alive_patients": 43,
    "progressed_patients": 24,
    "progression_rate": 0.558,
    "time_to_progression": {
        "mean_days": 566.25,
        "median_days": 543.5,
        "count": 24
    },
    "overall_survival": {
        "mean_days": 723.16,
        "median_days": 702.5,
        "count": 38
    },
    "progression_free_survival": {
        "mean_days": 625.26,
        "median_days": 602.0,
        "count": 38
    }
}
```

### Molecular Correlations Output
```json
{
    "total_patients_with_molecular_data": 42,
    "idh_distribution": {
        "wildtype": 33,
        "unknown": 3,
        "mutant": 6
    },
    "mgmt_distribution": {
        "unmethylated": 20,
        "methylated": 19,
        "unknown": 3
    },
    "correlations": [
        {
            "combination": "IDH-wildtype/MGMT-unmethylated/Grade-IV",
            "patient_count": 15,
            "mean_survival_days": 713.46,
            "progression_rate": 0.4,
            "response_rate": 0
        }
    ]
}
```

## 🛠️ Technical Implementation

### Core Analytics Engine
- **`app/analytics.py`**: Main analytics engine with survival, treatment response, and molecular correlation analyzers
- **`app/pdf_reports.py`**: PDF report generation with ReportLab and matplotlib integration

### Key Classes
1. **`SurvivalAnalysisEngine`**: Calculates survival metrics and statistics
2. **`TreatmentResponseAnalyzer`**: Analyzes treatment outcomes and response rates
3. **`MolecularCorrelationAnalyzer`**: Correlates molecular markers with clinical outcomes
4. **`ClinicalReportGenerator`**: Generates comprehensive PDF reports

### Dependencies Added
- `matplotlib>=3.8.0`: Statistical visualizations
- `seaborn>=0.13.0`: Enhanced plotting capabilities
- `scipy>=1.11.0`: Statistical calculations
- `reportlab>=4.0.0`: PDF generation
- `scikit-learn>=1.3.0`: Machine learning utilities
- `lifelines>=0.27.0`: Survival analysis tools

## 🔍 Clinical Research Applications

### 1. **Biomarker Studies**
- IDH-MGMT interaction analysis
- Molecular marker survival correlations
- Treatment response by biomarker status

### 2. **Treatment Efficacy Research**
- Response rate comparisons
- Time-to-progression analysis
- Duration of treatment benefit

### 3. **Survival Analysis**
- Kaplan-Meier curve preparation
- Median survival calculations
- Progression-free survival endpoints

### 4. **Cohort Characterization**
- Patient stratification by molecular markers
- Treatment history analysis
- Demographic correlations

## 📋 Data Quality Considerations

### Survival Analysis
- Requires `initial_diagnosis_date` for meaningful calculations
- Progression determined by `imaging_response = 'progressive_disease'`
- Last follow-up based on most recent `FollowUpVisit`

### Treatment Response
- Based on `imaging_response` during treatment periods
- Requires follow-up visits during treatment timeframe
- Best response prioritizes CR > PR > SD > PD

### Molecular Correlations
- Requires pathology data with `idh_status` and `mgmt_status`
- Unknown values are handled separately in analysis
- Combined molecular profiles show interaction effects

## 🚨 Important Notes

1. **Mock Data**: All analysis uses fictional patient data for demonstration
2. **Clinical Validation**: Results should be validated with clinical team before publication
3. **Statistical Significance**: Large cohorts recommended for meaningful statistical analysis
4. **Missing Data**: Analytics handle missing values appropriately
5. **Performance**: Large cohort analysis may take additional processing time

## 🔮 Future Enhancements

- **Kaplan-Meier Curves**: Full survival curve generation
- **Statistical Testing**: Log-rank tests for group comparisons
- **Machine Learning**: Predictive outcome models
- **Advanced Visualizations**: Interactive survival plots
- **Export Formats**: Additional formats for statistical software integration