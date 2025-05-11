
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/search', methods=['POST'])
def search_trials():
    data = request.json
    condition = data.get('condition', '')

    # Construct ClinicalTrials.gov API query
    base_url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": f"stem cell AND {condition}",
        "fields": "NCTId,BriefTitle,LocationCity,LocationState,LeadSponsorName,EligibilityCriteria,OverallStatus",
        "min_rnk": 1,
        "max_rnk": 10,
        "fmt": "JSON"
    }

    response = requests.get(base_url, params=params)
    api_data = response.json()

    results = []
    for study in api_data["StudyFieldsResponse"]["StudyFields"]:
        results.append({
            "title": study.get("BriefTitle", [""])[0],
            "location": f"{study.get('LocationCity', [''])[0]}, {study.get('LocationState', [''])[0]}",
            "contact": study.get("LeadSponsorName", ["N/A"])[0],
            "eligibility": study.get("EligibilityCriteria", ["N/A"])[0],
            "status": study.get("OverallStatus", ["N/A"])[0],
        })

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
