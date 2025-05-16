from flask import Flask, request, jsonify
from insurance_system import InsuranceSystem  # Your existing class

app = Flask(__name__)
insurance_system = InsuranceSystem()  # Your existing in-memory system

# Policyholder Registration
@app.route('/api/policyholders', methods=['POST'])
def register_policyholder():
    data = request.json
    try:
        policyholder = insurance_system.register_policyholder(
            name=data['name'],
            age=data['age'],
            policy_type=data['policy_type'],
            sum_insured=data['sum_insured']
        )
        return jsonify(policyholder.__dict__), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Add a Claim
@app.route('/api/claims', methods=['POST'])
def add_claim():
    data = request.json
    try:
        claim = insurance_system.add_claim(
            policyholder_id=data['policyholder_id'],
            amount=data['amount'],
            reason=data['reason'],
            status=data.get('status', 'Pending')
        )
        return jsonify(claim.__dict__), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get Claim Frequency for Policyholder (NEW ENDPOINT)
@app.route('/api/policyholders/<policyholder_id>/claim_frequency', methods=['GET'])
def get_claim_frequency(policyholder_id):
    try:
        frequency = insurance_system.get_claim_frequency(policyholder_id)
        return jsonify({
            "policyholder_id": policyholder_id,
            "claim_frequency": frequency
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Get High-Risk Policyholders
@app.route('/api/risk/high_risk', methods=['GET'])
def get_high_risk():
    high_risk = insurance_system.identify_high_risk_policyholders()
    return jsonify(high_risk)

# Generate Reports
@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = insurance_system.generate_reports()
    return jsonify(reports)

# Get Claims by Policy Type (NEW ENDPOINT)
@app.route('/api/claims/by_policy_type', methods=['GET'])
def get_claims_by_policy_type():
    try:
        claims_by_type = insurance_system.get_claims_by_policy_type()
        return jsonify(claims_by_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)