# Savanna Auto Suspend_Resume API Automation Framework

## Overview

This project is a Python Pytest-based API automation framework created to validate Savanna / TigerGraph workspace auto suspend and auto resume behavior.

The framework validates workspace status, auto suspend behavior, auto resume behavior, RESTPP query execution, negative scenarios, and state transition scenarios.

---

## Tech Stack

| Tool | Usage |
|---|---|
| Python | Automation scripting |
| Pytest | Test framework |
| Requests | API automation |
| python-dotenv | Environment variable handling |
| pytest-html | HTML report generation |

---

## Project Structure

```text
savanna_auto_suspend_tests/
│
├── tests/
│   ├── test_debug_connection.py
│   ├── test_auto_suspend.py
│   ├── test_auto_resume.py
│   ├── test_negative_cases.py
│   └── test_state_transition.py
│
├── utils/
│   ├── savanna_client.py
│   └── wait_utils.py
│
├── reports/
│   ├── test_report.html
│   ├── auto_suspend_report.html
│   └── negative_report.html
│
├── .env
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md


Install dependencies:

pip install -r requirements.txt

How to Run Tests:

Run debug connection test
pytest tests/test_debug_connection.py -v -s

Run auto suspend tests
pytest tests/test_auto_suspend.py -v -s

Run auto resume tests
pytest tests/test_auto_resume.py -v -s

Run negative tests
pytest tests/test_negative_cases.py -v -s

Run state transition tests
pytest tests/test_state_transition.py -v -s

Run all tests
pytest -v -s


Generate HTML Reports
Full report
pytest -v -s --html=reports/test_final_report.html --self-contained-html


Auto Suspend Scenarios:

TC ID	Scenario
TC01	Verify workspace API is reachable
TC02	Verify minimum auto suspend configuration
TC03	Verify workspace should not suspend before configured time
TC04	Verify keep-alive activity resets suspend timer
TC05	Verify long-running query prevents suspend
TC06	Verify manual suspend workspace

Auto Resume Scenarios:
TC ID	Scenario
TC07	Verify workspace auto resumes from API request
TC08	Verify query execution after resume
TC09	Verify workspace remains active after resume
TC10	Verify resume timeout handling

Negative Scenarios:

TC ID	Scenario
TC11	Invalid API key should return unauthorized
TC12	Invalid workspace ID should return not found
TC13	Invalid auto suspend time below minimum
TC14	Invalid auto suspend time above maximum
TC15	Invalid RESTPP endpoint or query payload

State Transition Scenarios:

TC ID	Scenario
TC16	Verify active to suspended transition
TC17	Verify suspended to active transition
TC18	Verify multiple resume requests
TC19	Verify workspace status consistency

