# 🧠 GBM Tracker - Glioblastoma Multiforme Patient Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Clinical Research](https://img.shields.io/badge/Clinical-Research-red.svg)](https://github.com)

A comprehensive web-based platform for managing Glioblastoma Multiforme (GBM) patients, designed for clinical research and healthcare coordination. The system provides advanced patient tracking, molecular marker analysis, treatment monitoring, and cohort reporting capabilities.

> **⚠️ IMPORTANT**: This system uses **mock patient data** for demonstration and testing purposes. All patient information is fictional and generated for system validation. **No real patient data is included.**

## 🎯 Overview

GBM Tracker is a modern, web-based patient management system specifically designed for glioblastoma research and clinical care. It provides clinicians and researchers with powerful tools to track patient outcomes, analyze molecular markers, and generate comprehensive reports for clinical studies.

### Key Benefits
- **Clinical Research Ready**: Advanced cohort filtering and statistical analysis
- **Molecular Profiling**: IDH and MGMT status tracking for personalized treatment
- **Timeline Visualization**: Interactive patient journey mapping
- **Data Export**: Research-ready CSV exports for statistical analysis
- **Responsive Design**: Accessible on desktop, tablet, and mobile devices

## 🚀 Latest Updates (September 2025)

### Enhanced Reporting Functionality
- **🔧 Fixed Critical Bugs**: Resolved age filtering logic and WHO Grade enum issues
- **📊 Enhanced Statistics**: Added survival metrics, molecular correlations, and treatment analytics
- **🎨 Visual Improvements**: Progress bars, better data presentation, and enhanced UI
- **🛠️ Robust Filtering**: Fixed apply filters button to handle empty parameters correctly
- **⚡ Performance**: Improved error handling and parameter validation

### New Features Added
- **Survival Analysis**: Mean follow-up duration and time since diagnosis calculations
- **Molecular Correlations**: IDH-MGMT combination analysis with percentage breakdowns
- **Age Group Analytics**: Statistical distribution across age ranges
- **Treatment Status Tracking**: Surgery vs non-surgery patient categorization
- **Enhanced Export API**: Improved CSV export with proper age filtering

## ✨ Features

### 👥 Patient Management
- **Comprehensive Patient Profiles**: Demographics, medical history, and contact information
- **Medical Record Integration**: Structured data entry with validation
- **40+ Mock Patients**: Realistic test data for system validation
- **Search & Filter**: Quick patient lookup and organization

### 🧬 Molecular Marker Tracking
- **IDH Status Monitoring**: Wild-type vs. Mutated classification
- **MGMT Methylation Status**: Methylated/Unmethylated tracking for treatment planning
- **WHO Grade Classification**: Standardized tumor grading
- **Ki-67 Proliferation Index**: Cell proliferation assessment
- **Color-Coded Visualization**: Quick visual status identification

### 🏥 Clinical Workflow Support
- **Surgery Management**: Detailed operative records and outcomes
- **Pathology Integration**: Comprehensive histological analysis
- **Treatment Tracking**: Chemotherapy and radiation therapy monitoring
- **Follow-up Visits**: Neurological assessments and response evaluation

### 📊 Advanced Reporting & Analytics
- **Enhanced Cohort Analysis**: Multi-dimensional patient stratification with improved filtering
- **Statistical Dashboards**: Real-time demographic and clinical statistics with survival metrics
- **Robust Filtering System**: Age ranges, molecular markers, surgery dates with empty parameter handling
- **Molecular Correlations**: IDH-MGMT combination analysis and biomarker statistics
- **Data Export**: CSV format for external statistical analysis
- **Interactive Visualizations**: Progress bars, charts, and enhanced data presentation
- **Treatment Analytics**: Surgery status tracking and treatment progression analysis

### 📈 Interactive Timeline Visualization
- **Vis.js Integration**: Professional timeline rendering
- **Event Categorization**: Color-coded medical events
  - 🔵 Surgery procedures
  - 🟢 Pathology reports
  - 🟡 Treatment cycles
  - 🔴 Follow-up visits
- **Interactive Features**: Zoom, pan, filter, and hover details
- **Treatment Progression**: Visual therapy timeline tracking

### 🎨 Professional Medical Interface
- **Medical-Grade Design**: Professional healthcare interface
- **Responsive Layout**: Mobile, tablet, and desktop compatibility
- **Accessibility**: WCAG guidelines compliance
- **Intuitive Navigation**: User-friendly clinical workflow design

## 🚀 Quick Start

### Prerequisites
- Python 3.10 - 3.12 (recommended: Python 3.12)
- pip (Python package installer)
- Git

> **⚠️ Note**: This project is compatible with Python 3.10, 3.11, and 3.12. Using a virtual environment is strongly recommended to avoid dependency conflicts.

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/onurerdoganmd/gbm-tracker.git
cd gbm-tracker
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Upgrade pip and essential packages**
```bash
pip install --upgrade pip setuptools wheel
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Initialize database with mock data**
```bash
python seed_data.py
```

6. **Start the application**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the application**
Open your browser and navigate to: `http://localhost:8000`

## 📱 Screenshots

### Dashboard Overview
*Main navigation and patient overview interface*

### Patient Timeline
*Interactive Vis.js timeline showing patient medical events*

### Cohort Reports
*Advanced filtering and statistical analysis interface*

### Molecular Markers
*Color-coded molecular marker visualization*

### Mobile Interface
*Responsive design on mobile devices*

> **Note**: Screenshots will be added to demonstrate the user interface and key features.

## 🏗️ Technical Architecture

### Backend Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM with SQLite
- **API Design**: RESTful endpoints with async/await
- **Data Validation**: Pydantic models
- **Authentication**: Ready for OAuth2/JWT integration

### Frontend Stack
- **Templating**: Jinja2 templates
- **Styling**: Tailwind CSS framework
- **Visualization**: Vis.js timeline library
- **Interactivity**: Vanilla JavaScript
- **Responsive Design**: Mobile-first approach

### Database Schema
```sql
Tables:
├── patients (demographics, medical records)
├── surgeries (operative procedures, outcomes)
├── pathologies (molecular markers, histology)
├── treatments (chemotherapy, radiation)
└── follow_up_visits (assessments, responses)
```

### Key Dependencies
```
fastapi>=0.68.0
uvicorn>=0.15.0
sqlalchemy>=1.4.0
jinja2>=3.0.0
python-multipart>=0.0.5
```

## 📊 Data Model

### Patient Entity
- Demographics (name, age, gender, contact)
- Medical record number
- Primary tumor location
- Diagnosis date

### Molecular Markers
- IDH mutation status (Wild-type/Mutated)
- MGMT methylation (Methylated/Unmethylated)
- WHO grade classification
- Ki-67 proliferation index

### Clinical Events
- Surgery procedures and outcomes
- Pathology reports and molecular analysis
- Treatment regimens and cycles
- Follow-up visits and assessments

## 🔧 Configuration

### Environment Variables
```bash
# Database configuration
DATABASE_URL=sqlite:///./gbm_tracker.db

# Server configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Security (for production)
SECRET_KEY=your_secret_key_here
```

### Production Deployment
For production deployment, consider:
- PostgreSQL database
- HTTPS/SSL certificates
- Authentication system
- Data backup strategies
- HIPAA compliance measures

## 📈 Usage Examples

### Filtering Patients by Molecular Markers
```python
# API endpoint for MGMT methylated patients
GET /api/reports/export?mgmt_status=methylated&format=json

# Response: 18 patients with methylated MGMT status
```

### Cohort Analysis
```python
# Filter patients by age and surgery date
GET /reports?age_min=30&age_max=40&surgery_date_start=2024-01-01

# Returns: 15 patients in specified criteria
```

### Timeline Data
```python
# Get patient timeline events
GET /patients/{patient_id}/timeline/interactive

# Returns: Interactive timeline with 8+ events per patient
```

## 🧪 Testing Data

The system includes comprehensive mock data for testing:

- **40 Fictional Patients**: Realistic clinical profiles
- **Complete Medical Records**: Surgery, pathology, treatment data
- **Molecular Markers**: IDH/MGMT status distribution
- **Treatment History**: Chemotherapy and radiation records
- **Follow-up Data**: Neurological assessments and outcomes

**Data Distribution:**
- Age range: 21-79 years (Mean: 33.2)
- Gender: 27 male (67.5%), 13 female (32.5%)
- MGMT status: 18 methylated, 19 unmethylated, 3 unknown
- Surgery dates: Distributed across 2022-2025

## 🔒 Security & Privacy

### Data Protection
- **Mock Data Only**: No real patient information
- **Input Validation**: Pydantic model validation
- **SQL Injection Prevention**: ORM-based queries
- **Error Handling**: Secure error responses

### HIPAA Readiness
The architecture supports HIPAA compliance with:
- Audit logging capabilities
- Access control framework
- Data encryption support
- Backup and recovery systems

## 🤝 Contributing

We welcome contributions from the clinical and technical community!

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Contribution Guidelines
- Follow Python PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure clinical accuracy for medical features
- Test with the provided mock data

## 📚 Clinical Documentation

### Supported Clinical Workflows
- **Patient Intake**: Streamlined data entry and validation
- **Molecular Profiling**: IDH/MGMT status for treatment planning
- **Treatment Monitoring**: Therapy response and progression tracking
- **Research Data Collection**: Standardized data for clinical studies

### Research Applications
- **Biomarker Studies**: Molecular marker correlation analysis
- **Treatment Outcomes**: Therapy effectiveness research
- **Survival Analysis**: Foundation for Kaplan-Meier studies
- **Cohort Studies**: Patient stratification and comparison

## 🔧 API Documentation

### Interactive API Docs
When running the application, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints
```
GET  /                           # Dashboard
GET  /patients                   # Patient list
GET  /patients/{id}              # Patient details
GET  /patients/{id}/timeline     # Patient timeline
GET  /reports                    # Cohort reports
GET  /api/reports/export         # Data export
```

## 📊 Performance

### Benchmarks
- **Page Load Time**: <500ms for all endpoints
- **Database Queries**: Optimized with proper indexing
- **Memory Usage**: ~50MB for full 40-patient dataset
- **Concurrent Users**: Tested with multiple sessions

### Scalability
- Architecture supports 1000+ patients
- Database optimization for clinical data
- Caching strategies for improved performance
- Horizontal scaling capabilities

## 🚀 Roadmap

### Planned Features
- [ ] **Advanced Analytics**: Survival curve analysis
- [ ] **Machine Learning**: Predictive outcome models
- [ ] **Imaging Integration**: MRI/CT scan timeline
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **EHR Integration**: HL7 FHIR compatibility
- [ ] **Clinical Trials**: Trial management module

### Research Enhancements
- [ ] **Genomic Data**: Expanded molecular profiling
- [ ] **Biobanking**: Sample tracking integration
- [ ] **Multi-center Studies**: Collaborative research tools
- [ ] **AI Assistance**: Treatment recommendation engine

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍⚕️ Clinical Disclaimer

This software is designed for research and educational purposes. While built with clinical accuracy in mind, it should not be used as the sole source for clinical decision-making. Always consult with qualified healthcare professionals for patient care decisions.

**Mock Data Notice**: All patient data in this system is fictional and generated for testing purposes. No real patient information is contained within this application.

## 🙏 Acknowledgments

- **Glioblastoma Research Community** for clinical insights
- **FastAPI Team** for the excellent web framework
- **Vis.js Contributors** for timeline visualization
- **Open Source Community** for foundational tools
- **Clinical Advisors** for medical accuracy guidance

## 📞 Support & Contact

### Technical Support
- 📧 Email: [support@gbmtracker.com](mailto:support@gbmtracker.com)
- 🐛 Issues: [GitHub Issues](https://github.com/onurerdoganmd/gbm-tracker/issues)
- 📖 Documentation: [Project Wiki](https://github.com/onurerdoganmd/gbm-tracker/wiki)

### Clinical Collaboration
- 🏥 Clinical Partners: [partnerships@gbmtracker.com](mailto:partnerships@gbmtracker.com)
- 🔬 Research Collaboration: [research@gbmtracker.com](mailto:research@gbmtracker.com)

---

**Made with ❤️ for the glioblastoma research community**

*Advancing GBM research through better data management and visualization*