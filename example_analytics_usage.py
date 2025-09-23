#!/usr/bin/env python3
"""
Example script showing how to use the GBM Tracker advanced analytics features
"""

import requests
import json
from datetime import date

# Base URL for your GBM Tracker application
BASE_URL = "http://localhost:8000"

def get_survival_analysis(patient_ids=None):
    """Get survival analysis for all patients or specific patients"""
    url = f"{BASE_URL}/api/analytics/survival"
    if patient_ids:
        # Convert list to comma-separated string
        patient_ids_str = ",".join(map(str, patient_ids))
        url += f"?patient_ids={patient_ids_str}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_molecular_correlations(patient_ids=None):
    """Get molecular marker correlation analysis"""
    url = f"{BASE_URL}/api/analytics/molecular-correlations"
    if patient_ids:
        patient_ids_str = ",".join(map(str, patient_ids))
        url += f"?patient_ids={patient_ids_str}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_treatment_response_analysis(patient_ids=None):
    """Get treatment response analysis"""
    url = f"{BASE_URL}/api/analytics/treatment-response"
    if patient_ids:
        patient_ids_str = ",".join(map(str, patient_ids))
        url += f"?patient_ids={patient_ids_str}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_comprehensive_analytics(patient_ids=None):
    """Get all analytics in one call"""
    url = f"{BASE_URL}/api/analytics/comprehensive"
    if patient_ids:
        patient_ids_str = ",".join(map(str, patient_ids))
        url += f"?patient_ids={patient_ids_str}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def download_pdf_report(filename="gbm_report.pdf", patient_ids=None, title="GBM Analytics Report"):
    """Download PDF report"""
    url = f"{BASE_URL}/api/reports/clinical-research-pdf"
    params = {
        "include_charts": True,
        "title": title
    }
    if patient_ids:
        params["patient_ids"] = ",".join(map(str, patient_ids))

    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF report saved as {filename}")
        return True
    else:
        print(f"Error generating PDF: {response.status_code} - {response.text}")
        return False

def analyze_idh_mgmt_subgroups():
    """Example: Analyze different IDH/MGMT subgroups"""
    print("=== IDH/MGMT Subgroup Analysis ===")

    # Get molecular correlations
    molecular_data = get_molecular_correlations()
    if not molecular_data:
        return

    print(f"Total patients with molecular data: {molecular_data['total_patients_with_molecular_data']}")
    print(f"IDH distribution: {molecular_data['idh_distribution']}")
    print(f"MGMT distribution: {molecular_data['mgmt_distribution']}")

    print("\nMolecular Combination Analysis:")
    for correlation in molecular_data['correlations']:
        print(f"  {correlation['combination']}:")
        print(f"    - Patients: {correlation['patient_count']}")
        print(f"    - Mean survival: {correlation['mean_survival_days']:.1f} days")
        print(f"    - Progression rate: {correlation['progression_rate']:.1%}")

def compare_patient_cohorts():
    """Example: Compare different patient cohorts"""
    print("=== Patient Cohort Comparison ===")

    # Compare first 10 vs last 10 patients
    all_survival = get_survival_analysis()
    first_cohort = get_survival_analysis([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    if all_survival and first_cohort:
        print("All patients:")
        print(f"  - Total: {all_survival['total_patients']}")
        print(f"  - Mean OS: {all_survival['overall_survival']['mean_days']:.1f} days")
        print(f"  - Progression rate: {all_survival['progression_rate']:.1%}")

        print("\nFirst 10 patients:")
        print(f"  - Total: {first_cohort['total_patients']}")
        print(f"  - Mean OS: {first_cohort['overall_survival']['mean_days']:.1f} days")
        print(f"  - Progression rate: {first_cohort['progression_rate']:.1%}")

def generate_study_reports():
    """Example: Generate different study reports"""
    print("=== Generating Study Reports ===")

    # Generate comprehensive report for all patients
    success = download_pdf_report(
        filename=f"comprehensive_gbm_report_{date.today().isoformat()}.pdf",
        title="Comprehensive GBM Study Analysis"
    )
    if success:
        print("Comprehensive report generated")

    # Generate report for specific cohort
    success = download_pdf_report(
        filename=f"pilot_cohort_report_{date.today().isoformat()}.pdf",
        patient_ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        title="Pilot Cohort Analysis (First 10 Patients)"
    )
    if success:
        print("Pilot cohort report generated")

def main():
    """Main function demonstrating analytics usage"""
    print("GBM Tracker Advanced Analytics Demo")
    print("=" * 50)

    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/hello")
        if response.status_code != 200:
            print("Cannot connect to GBM Tracker. Make sure it's running on http://localhost:8000")
            return

        print("Connected to GBM Tracker")
        print()

        # Run different analytics examples
        analyze_idh_mgmt_subgroups()
        print()

        compare_patient_cohorts()
        print()

        generate_study_reports()
        print()

        # Get comprehensive analytics
        print("=== Comprehensive Analytics Summary ===")
        comprehensive = get_comprehensive_analytics()
        if comprehensive:
            print(f"Patient cohort size: {comprehensive['patient_cohort_size']}")
            print(f"Patients alive: {comprehensive['survival_analysis']['alive_patients']}")
            print(f"Molecular data available: {comprehensive['molecular_correlations']['total_patients_with_molecular_data']}")
            print(f"Treatment analyses: {comprehensive['treatment_response']['total_treatments']}")

        print("\nAnalytics demo completed successfully!")

    except requests.exceptions.ConnectionError:
        print("Cannot connect to GBM Tracker. Make sure it's running:")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()