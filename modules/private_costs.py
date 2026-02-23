"""
private_costs.py
----------------
Calculates private healthcare costs, finance payment plans,
and compares against the user's budget.
"""


def calculate_finance(principal, apr, months):
    """
    Calculates monthly payment for a medical finance plan.

    principal = amount borrowed (e.g. 15000)
    apr       = annual interest rate as percentage (e.g. 9.9)
    months    = number of months to repay (e.g. 24)

    Formula used: standard loan amortisation formula
    Monthly rate = APR / 12 / 100
    Monthly payment = principal * (monthly_rate) / (1 - (1 + monthly_rate)^-months)
    """

    if apr == 0:
        # No interest — just divide evenly
        monthly = principal / months
        total = principal
    else:
        monthly_rate = apr / 12 / 100
        monthly = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)
        total = monthly * months

    interest_paid = total - principal

    return {
        "monthly_payment": round(monthly, 2),
        "total_repayable": round(total, 2),
        "interest_paid": round(interest_paid, 2),
        "months": months,
        "apr": apr
    }


def get_finance_options(cost):
    """
    Returns 3 finance plan options for a given procedure cost.
    Uses typical UK medical finance rates.
    """
    average_cost = (cost["min"] + cost["max"]) / 2

    options = [
        calculate_finance(average_cost, apr=9.9, months=12),
        calculate_finance(average_cost, apr=9.9, months=24),
        calculate_finance(average_cost, apr=9.9, months=36),
    ]

    return options


def assess_budget(user_budget, procedure):
    """
    Compares user budget against private procedure costs.
    Returns a clear assessment.
    """
    min_cost = procedure["private_cost_min"]
    max_cost = procedure["private_cost_max"]
    avg_cost = (min_cost + max_cost) / 2

    if user_budget >= max_cost:
        status = "FULLY_COVERED"
        message = f"Your budget of £{user_budget:,} fully covers private treatment (max £{max_cost:,})."

    elif user_budget >= min_cost:
        status = "PARTIALLY_COVERED"
        shortfall = avg_cost - user_budget
        message = f"Your budget covers the lower end. You may need an extra £{shortfall:,.0f} for the average cost."

    else:
        shortfall = min_cost - user_budget
        status = "NOT_COVERED"
        message = f"Your budget is £{shortfall:,} below the minimum private cost of £{min_cost:,}."

    return {
        "status": status,
        "message": message,
        "min_cost": min_cost,
        "max_cost": max_cost,
        "avg_cost": avg_cost,
        "user_budget": user_budget,
        "finance_options": get_finance_options({"min": min_cost, "max": max_cost})
    }


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Finance calculator test ===")
    result = calculate_finance(principal=15000, apr=9.9, months=24)
    print(f"  £15,000 over 24 months @ 9.9% APR:")
    print(f"  Monthly payment : £{result['monthly_payment']}")
    print(f"  Total repayable : £{result['total_repayable']}")
    print(f"  Interest paid   : £{result['interest_paid']}")

    print("\n=== Budget assessment test ===")
    fake_procedure = {
        "private_cost_min": 11000,
        "private_cost_max": 17000
    }
    assessment = assess_budget(user_budget=5000, procedure=fake_procedure)
    print(f"  Status  : {assessment['status']}")
    print(f"  Message : {assessment['message']}")
