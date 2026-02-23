"""
report.py
---------
Formats and prints the final report the user sees.
Also saves it as a .txt file they can keep.
"""

from datetime import date   # For adding today's date to the report


def print_divider(char="═", width=60):
    """ Prints a line of repeated characters — purely for visual formatting """
    print(char * width)


def print_section(title):
    """ Prints a section header """
    print(f"\n─── {title} {'─' * (54 - len(title))}")


def format_currency(amount):
    """ Formats a number as £1,234 """
    return f"£{amount:,.0f}"


def generate_report(procedure, wait_data, urgency_data, budget_data, recommendation):
    """
    Prints the full formatted report to the terminal.
    Returns the report as a string (for saving to file).
    """

    lines = []   # We'll collect all lines here, then print them

    def add(line=""):
        """ Adds a line to our report and prints it """
        lines.append(line)
        print(line)

    today = date.today().strftime("%d %B %Y")

    # ── Header ────────────────────────────────────────────────────────────────
    add("═" * 60)
    add("   NHS vs PRIVATE: YOUR HEALTHCARE DECISION")
    add(f"   Generated: {today}")
    add("═" * 60)

    # ── Procedure & Input Summary ─────────────────────────────────────────────
    add(f"\n  Procedure  : {procedure['name']}")
    add(f"  Waited     : {wait_data['display']}")
    add(f"  Budget     : {format_currency(budget_data['user_budget'])}")

    # ── NHS Section ───────────────────────────────────────────────────────────
    add("\n─── NHS " + "─" * 52)
    add(f"  NHS average wait     : {procedure['nhs_avg_wait_weeks']} weeks")
    add(f"  You have waited      : {wait_data['display']}")
    add(f"  Estimated remaining  : ~{urgency_data['weeks_remaining']} weeks ({urgency_data['months_remaining']} months)")
    add(f"  Urgency level        : {urgency_data['urgency']}")
    add(f"  {urgency_data['urgency_reason']}")
    add(f"  Cost to you          : £0 (free at point of use)")

    # ── Private UK Section ────────────────────────────────────────────────────
    add("\n─── PRIVATE (UK) " + "─" * 43)
    add(f"  Cost range           : {format_currency(budget_data['min_cost'])} – {format_currency(budget_data['max_cost'])}")
    add(f"  Average cost         : {format_currency(budget_data['avg_cost'])}")
    add(f"  Typical wait         : 2–4 weeks")
    add(f"  Providers            : {', '.join(procedure['private_providers'])}")
    add(f"\n  Budget status        : {budget_data['status'].replace('_', ' ')}")
    add(f"  {budget_data['message']}")

    # Finance options
    add(f"\n  Finance options (at 9.9% APR):")
    for plan in budget_data["finance_options"]:
        add(
            f"    {plan['months']} months → "
            f"£{plan['monthly_payment']:.2f}/month | "
            f"Total: {format_currency(plan['total_repayable'])} | "
            f"Interest: {format_currency(plan['interest_paid'])}"
        )

    # ── Abroad Section ────────────────────────────────────────────────────────
    if procedure["suitable_for_abroad"] and procedure["abroad"]:
        add("\n─── MEDICAL TOURISM " + "─" * 40)
        add("  (All costs below are approximate all-in estimates including flights)")
        for option in procedure["abroad"]:
            saving = budget_data["avg_cost"] - option["cost"]
            add(
                f"  {option['country']} ({option['city']})  →  "
                f"{format_currency(option['cost'])}  |  "
                f"Quality: {option['quality']}  |  "
                f"Saving vs UK avg: {format_currency(saving)}"
            )
    else:
        add("\n─── MEDICAL TOURISM " + "─" * 40)
        add("  Not recommended for this procedure.")

    # ── Recommendation ────────────────────────────────────────────────────────
    add("\n─── RECOMMENDATION " + "─" * 41)
    add(f"\n  {recommendation['primary']}\n")
    for i, rec in enumerate(recommendation["recommendations"], 1):
        # Word wrap at 55 chars for readability
        add(f"  {i}. {rec}")

    # ── Footer ────────────────────────────────────────────────────────────────
    add("\n" + "═" * 60)
    add("  ⚠️  This tool provides guidance only and is not medical")
    add("  or financial advice. Always consult a qualified professional.")
    add("═" * 60)

    return "\n".join(lines)


def save_report(report_text, procedure_name):
    """
    Saves the report to a .txt file in the current directory.
    """
    filename = f"report_{procedure_name.lower().replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n  Report saved to: {filename}")
