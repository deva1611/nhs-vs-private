"""
wait_parser.py
--------------
Converts whatever the user types (days, weeks, months)
into a standard number of days, then determines urgency.

Example inputs it handles:
  "3 days", "2 weeks", "4 months", "6 weeks", "1 month"
"""

import re  # re = regular expressions, helps us find patterns in text


def parse_wait_time(user_input):
    """
    Takes a string like "3 weeks" or "2 months"
    Returns a dictionary with:
      - days_waited  : total days already waited (int)
      - display      : clean string like "3 weeks (21 days)"
    """

    # Convert to lowercase so "3 Weeks" and "3 weeks" both work
    text = user_input.strip().lower()

    # Look for a number followed by a time unit
    # re.search finds the pattern anywhere in the string
    match = re.search(r'(\d+)\s*(day|days|week|weeks|month|months)', text)

    if not match:
        # If we couldn't understand the input, return None
        return None

    # Extract the number and the unit from what we found
    number = int(match.group(1))   # e.g. 3
    unit = match.group(2)          # e.g. "weeks"

    # Convert everything to days
    if 'day' in unit:
        days = number
        display = f"{number} day{'s' if number != 1 else ''} ({days} days)"

    elif 'week' in unit:
        days = number * 7
        display = f"{number} week{'s' if number != 1 else ''} ({days} days)"

    elif 'month' in unit:
        days = number * 30          # we use 30 as average days per month
        display = f"{number} month{'s' if number != 1 else ''} ({days} days)"

    return {
        "days_waited": days,
        "display": display
    }


def calculate_urgency(days_waited, nhs_avg_wait_weeks):
    """
    Takes how long someone has waited + NHS average wait for the procedure
    Returns urgency level and a plain English explanation.

    Logic:
    - Convert NHS average wait to days for fair comparison
    - See how far through the wait they are
    - Assign urgency based on remaining wait
    """

    nhs_avg_days = nhs_avg_wait_weeks * 7
    days_remaining = max(0, nhs_avg_days - days_waited)
    weeks_remaining = round(days_remaining / 7)
    months_remaining = round(days_remaining / 30)

    # Calculate what percentage of the wait is still ahead
    percent_remaining = (days_remaining / nhs_avg_days) * 100 if nhs_avg_days > 0 else 0

    # Assign urgency
    if days_remaining <= 0:
        urgency = "CRITICAL"
        urgency_reason = "You have already exceeded the NHS average wait. You should chase your referral immediately."

    elif percent_remaining >= 75:
        urgency = "HIGH"
        urgency_reason = f"You still have approximately {weeks_remaining} weeks ({months_remaining} months) to go. Most of your wait is still ahead."

    elif percent_remaining >= 40:
        urgency = "MODERATE"
        urgency_reason = f"You're roughly halfway through. Approximately {weeks_remaining} weeks remaining."

    else:
        urgency = "LOW"
        urgency_reason = f"You're nearing the end of the typical wait. Only around {weeks_remaining} weeks likely remaining."

    return {
        "urgency": urgency,
        "days_remaining": days_remaining,
        "weeks_remaining": weeks_remaining,
        "months_remaining": months_remaining,
        "percent_remaining": round(percent_remaining),
        "urgency_reason": urgency_reason
    }


# ── Quick test (only runs if you run this file directly) ──────────────────────
if __name__ == "__main__":
    # Test parse_wait_time
    tests = ["3 days", "2 weeks", "4 months", "6 Weeks", "1 month"]
    print("=== Testing wait time parser ===")
    for t in tests:
        result = parse_wait_time(t)
        print(f"  Input: '{t}' → {result}")

    # Test urgency calculation
    print("\n=== Testing urgency calculator ===")
    print("  Waited 2 weeks, NHS avg 38 weeks:")
    print(" ", calculate_urgency(14, 38))

    print("  Waited 20 weeks, NHS avg 38 weeks:")
    print(" ", calculate_urgency(140, 38))
