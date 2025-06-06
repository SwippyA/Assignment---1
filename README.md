# Insurance Claims Management System

![Docker](https://img.shields.io/badge/Docker-✓-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.3-green)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)

A REST API for managing insurance policies, claims, and risk analysis built with Flask and Docker.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop ([Download](https://www.docker.com/products/docker-desktop))
- Python 3.9+ (for local development)
- Postman ([Download](https://www.postman.com/downloads/))

### Run with Docker (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/insurance-app.git
cd insurance-app

# 2. Build the Docker image
docker build -t insurance-app .

# 3. Run the container
docker run -p 5000:5000 insurance-app

##Local Development

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
flask run --host=0.0.0.0

Project Structure

insurance-app/
├── api_endpoints.py       # Flask routes and controllers
├── insurance_system.py    # Business logic and data models
├── test_risk_analysis.py  # Unit tests
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
└── README.md              # This file


📚 API Documentation 
Endpoints
Endpoint	Method	Description	Example Request
/api/policyholders	POST	Register new policyholder	Example
/api/claims	POST	File new claim	Example
/api/risk/high_risk	GET	List high-risk policyholders	-
/api/reports	GET	Generate system reports	-
/api/claims/by_policy_type	GET	Claims by policy type	-

##Postman collection link : https://lunar-space-396691.postman.co/workspace/back-end-postions-Workspace~bbef1616-c104-4e8c-93ef-90558db4ba6d/collection/32531181-b0ce2f9e-f11d-488a-b6be-6be49efe475f?action=share&creator=32531181&active-environment=32531181-8bdf599b-fb7e-4cec-9674-ed82edc2a960
