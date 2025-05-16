import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
from dataclasses import dataclass, field
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Data storage
policyholders = {}
claims = []

@dataclass
class Policyholder:
    id: str
    name: str
    age: int
    policy_type: str  # Health, Vehicle, Life
    sum_insured: float
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "policy_type": self.policy_type,
            "sum_insured": self.sum_insured
        }

@dataclass
class Claim:
    id: str
    policyholder_id: str
    amount: float
    reason: str
    status: str  # Pending, Approved, Rejected
    date: str
    
    def to_dict(self):
        return {
            "id": self.id,
            "policyholder_id": self.policyholder_id,
            "amount": self.amount,
            "reason": self.reason,
            "status": self.status,
            "date": self.date
        }

class InsuranceSystem:
    def __init__(self):
        self.policyholders: Dict[str, Policyholder] = {}
        self.claims: List[Claim] = []
    
    def register_policyholder(self, name: str, age: int, policy_type: str, sum_insured: float) -> Policyholder:
        """Register a new policyholder"""
        if age < 18:
            raise ValueError("Policyholder must be at least 18 years old")
        if policy_type not in ["Health", "Vehicle", "Life"]:
            raise ValueError("Invalid policy type")
        if sum_insured <= 0:
            raise ValueError("Sum insured must be positive")
        
        policyholder_id = str(uuid.uuid4())
        policyholder = Policyholder(
            id=policyholder_id,
            name=name,
            age=age,
            policy_type=policy_type,
            sum_insured=sum_insured
        )
        self.policyholders[policyholder_id] = policyholder
        return policyholder
    
    def add_claim(self, policyholder_id: str, amount: float, reason: str, status: str = "Pending") -> Claim:
        """Add a new claim for a policyholder"""
        if policyholder_id not in self.policyholders:
            raise ValueError("Policyholder not found")
        if amount <= 0:
            raise ValueError("Claim amount must be positive")
        if status not in ["Pending", "Approved", "Rejected"]:
            raise ValueError("Invalid claim status")
        
        claim_id = str(uuid.uuid4())
        claim = Claim(
            id=claim_id,
            policyholder_id=policyholder_id,
            amount=amount,
            reason=reason,
            status=status,
            date=datetime.now().strftime("%Y-%m-%d")
        )
        self.claims.append(claim)
        return claim
    
    def get_claim_frequency(self, policyholder_id: str) -> int:
        """Calculate claim frequency for a policyholder"""
        if policyholder_id not in self.policyholders:
            raise ValueError("Policyholder not found")
        return len([c for c in self.claims if c.policyholder_id == policyholder_id])
    
    def identify_high_risk_policyholders(self) -> List[Dict]:
        """Identify high-risk policyholders"""
        high_risk = []
        one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        for ph_id, ph in self.policyholders.items():
            # Get claims in last year
            recent_claims = [
                c for c in self.claims 
                if c.policyholder_id == ph_id and c.date >= one_year_ago
            ]
            
            # Calculate total claim amount
            total_claims = sum(c.amount for c in self.claims if c.policyholder_id == ph_id)
            claim_ratio = total_claims / ph.sum_insured if ph.sum_insured > 0 else 0
            
            if len(recent_claims) > 3 or claim_ratio > 0.8:
                high_risk.append({
                    "policyholder": ph.to_dict(),
                    "claim_count": len(recent_claims),
                    "claim_ratio": claim_ratio
                })
        
        return high_risk
    
    def get_claims_by_policy_type(self) -> Dict:
        """Aggregate claims by policy type"""
        result = defaultdict(list)
        for claim in self.claims:
            ph = self.policyholders.get(claim.policyholder_id)
            if ph:
                result[ph.policy_type].append(claim.to_dict())
        return dict(result)
    
    def generate_reports(self) -> Dict:
        """Generate various reports"""
        # Total claims per month
        monthly_claims = defaultdict(int)
        for claim in self.claims:
            month = claim.date[:7]  # YYYY-MM
            monthly_claims[month] += 1
        
        # Average claim amount by policy type
        policy_type_stats = defaultdict(lambda: {"total": 0, "count": 0})
        for claim in self.claims:
            ph = self.policyholders.get(claim.policyholder_id)
            if ph:
                policy_type_stats[ph.policy_type]["total"] += claim.amount
                policy_type_stats[ph.policy_type]["count"] += 1
        
        avg_claim_by_type = {
            pt: stats["total"] / stats["count"] if stats["count"] > 0 else 0
            for pt, stats in policy_type_stats.items()
        }
        
        # Highest claim
        highest_claim = max(self.claims, key=lambda x: x.amount, default=None)
        
        # Policyholders with pending claims
        pending_ph_ids = {c.policyholder_id for c in self.claims if c.status == "Pending"}
        pending_policyholders = [
            self.policyholders[ph_id].to_dict() 
            for ph_id in pending_ph_ids 
            if ph_id in self.policyholders
        ]
        
        return {
            "monthly_claims": dict(monthly_claims),
            "avg_claim_by_type": avg_claim_by_type,
            "highest_claim": highest_claim.to_dict() if highest_claim else None,
            "pending_policyholders": pending_policyholders
        }

# Initialize the system
insurance_system = InsuranceSystem()

# Flask API Endpoints
@app.route('/policyholders', methods=['POST'])
def register_policyholder():
    data = request.json
    try:
        ph = insurance_system.register_policyholder(
            name=data['name'],
            age=data['age'],
            policy_type=data['policy_type'],
            sum_insured=data['sum_insured']
        )
        return jsonify(ph.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/claims', methods=['POST'])
def add_claim():
    data = request.json
    try:
        claim = insurance_system.add_claim(
            policyholder_id=data['policyholder_id'],
            amount=data['amount'],
            reason=data['reason'],
            status=data.get('status', 'Pending')
        )
        return jsonify(claim.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/policyholders/<ph_id>/claim_frequency', methods=['GET'])
def get_claim_frequency(ph_id):
    try:
        frequency = insurance_system.get_claim_frequency(ph_id)
        return jsonify({
            "policyholder_id": ph_id,
            "claim_frequency": frequency
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/risk/high_risk', methods=['GET'])
def get_high_risk():
    high_risk = insurance_system.identify_high_risk_policyholders()
    return jsonify(high_risk)

@app.route('/reports', methods=['GET'])
def get_reports():
    reports = insurance_system.generate_reports()
    return jsonify(reports)

@app.route('/claims/by_policy_type', methods=['GET'])
def get_claims_by_type():
    claims_by_type = insurance_system.get_claims_by_policy_type()
    return jsonify(claims_by_type)

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)