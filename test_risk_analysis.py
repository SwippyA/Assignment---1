import unittest
from insurance_system import InsuranceSystem
from datetime import datetime, timedelta
import sys
sys.path.append('D:/projects/Data Science Intern Project')

class TestRiskAnalysis(unittest.TestCase):
    def setUp(self):
        self.system = InsuranceSystem()
        self.ph_id = self.system.register_policyholder(
            name="Test User", age=30, policy_type="Health", sum_insured=100000
        ).id

    def test_high_risk_frequency(self):
        """Test >3 claims triggers high-risk"""
        for _ in range(4):
            self.system.add_claim(
                policyholder_id=self.ph_id,
                amount=1000,
                reason="Test",
                status="Approved"
            )
        high_risk = self.system.identify_high_risk_policyholders()
        self.assertTrue(any(ph['policyholder']['id'] == self.ph_id for ph in high_risk))

    def test_high_risk_ratio(self):
        """Test >80% claim ratio triggers high-risk"""
        self.system.add_claim(
            policyholder_id=self.ph_id,
            amount=90000,  # 90% of 100,000 sum insured
            reason="Major Surgery",
            status="Approved"
        )
        high_risk = self.system.identify_high_risk_policyholders()
        self.assertTrue(any(ph['policyholder']['id'] == self.ph_id for ph in high_risk))

    def test_not_high_risk(self):
        """Test normal policyholders aren't flagged"""
        self.system.add_claim(
            policyholder_id=self.ph_id,
            amount=5000,  # Only 5% of sum insured
            reason="Checkup",
            status="Approved"
        )
        high_risk = self.system.identify_high_risk_policyholders()
        self.assertFalse(any(ph['policyholder']['id'] == self.ph_id for ph in high_risk))

if __name__ == '__main__':
    unittest.main()