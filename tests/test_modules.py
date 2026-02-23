"""
test_modules.py
---------------
Basic tests for the NHS vs Private tool.
Run with: pytest tests/test_modules.py

Tests show recruiters you write professional, reliable code.
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.wait_parser import parse_wait_time, calculate_urgency
from modules.procedure_finder import find_procedure, list_all_procedures
from modules.private_costs import calculate_finance, assess_budget


# ── Wait Parser Tests ─────────────────────────────────────────────────────────

def test_parse_days():
    result = parse_wait_time("3 days")
    assert result["days_waited"] == 3

def test_parse_weeks():
    result = parse_wait_time("2 weeks")
    assert result["days_waited"] == 14

def test_parse_months():
    result = parse_wait_time("1 month")
    assert result["days_waited"] == 30

def test_parse_invalid():
    result = parse_wait_time("tomorrow")
    assert result is None

def test_parse_case_insensitive():
    result = parse_wait_time("3 Weeks")
    assert result["days_waited"] == 21


# ── Urgency Tests ─────────────────────────────────────────────────────────────

def test_urgency_critical():
    # Waited more than average → CRITICAL
    result = calculate_urgency(days_waited=300, nhs_avg_wait_weeks=38)
    assert result["urgency"] == "CRITICAL"

def test_urgency_high():
    # Only waited 1 week out of 38 → HIGH
    result = calculate_urgency(days_waited=7, nhs_avg_wait_weeks=38)
    assert result["urgency"] == "HIGH"

def test_urgency_low():
    # Waited 35 out of 38 weeks → LOW
    result = calculate_urgency(days_waited=245, nhs_avg_wait_weeks=38)
    assert result["urgency"] == "LOW"


# ── Procedure Finder Tests ────────────────────────────────────────────────────

def test_find_knee():
    result = find_procedure("knee replacement")
    assert result is not None
    assert result["name"] == "Knee Replacement"

def test_find_mri():
    result = find_procedure("mri scan")
    assert result is not None

def test_find_no_match():
    result = find_procedure("something that doesnt exist xyz")
    assert result is None

def test_list_procedures():
    procedures = list_all_procedures()
    assert len(procedures) > 0
    assert "Knee Replacement" in procedures


# ── Finance Calculator Tests ──────────────────────────────────────────────────

def test_finance_no_interest():
    result = calculate_finance(principal=12000, apr=0, months=12)
    assert result["monthly_payment"] == 1000.0
    assert result["interest_paid"] == 0.0

def test_finance_with_interest():
    result = calculate_finance(principal=15000, apr=9.9, months=24)
    assert result["monthly_payment"] > 0
    assert result["total_repayable"] > 15000   # Should be more than principal
    assert result["interest_paid"] > 0


# ── Budget Assessment Tests ───────────────────────────────────────────────────

def test_budget_fully_covered():
    procedure = {"private_cost_min": 5000, "private_cost_max": 8000}
    result = assess_budget(user_budget=10000, procedure=procedure)
    assert result["status"] == "FULLY_COVERED"

def test_budget_not_covered():
    procedure = {"private_cost_min": 11000, "private_cost_max": 17000}
    result = assess_budget(user_budget=3000, procedure=procedure)
    assert result["status"] == "NOT_COVERED"
