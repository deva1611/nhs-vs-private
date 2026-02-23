"""
main.py
-------
NHS vs Private: UK Healthcare Decision Engine
---------------------------------------------
Run this file to start the tool:  python main.py

This is the entry point. It:
1. Welcomes the user
2. Asks 3 questions
3. Calls all the modules
4. Prints the report
"""

# ── Import our modules ────────────────────────────────────────────────────────
# Each import pulls in a file we created in the modules/ folder
from modules.procedure_finder import find_procedure, list_all_procedures
from modules.wait_parser import parse_wait_time, calculate_urgency
from modules.private_costs import assess_budget
from modules.recommendation import generate_recommendation
from modules.report import generate_report, save_report


def ask_question(prompt, example=None):
    """
    Helper function: prints a question and returns the user's answer.
    Keeps the input logic clean and consistent throughout.
    """
    if example:
        print(f"\n  {prompt}")
        print(f"  Example: {example}")
        answer = input("  → ").strip()
    else:
        print(f"\n  {prompt}")
        answer = input("  → ").strip()
    return answer


def get_procedure():
    """
    Asks the user what procedure they need.
    Keeps asking until we find a match or they give up.
    """
    while True:
        user_input = ask_question(
            "What procedure do you need?",
            example="knee replacement, MRI scan, cataract surgery"
        )

        procedure = find_procedure(user_input)

        if procedure:
            print(f"\n  ✓ Found: {procedure['name']}")
            return procedure
        else:
            print(f"\n  Sorry, we couldn't find '{user_input}' in our database.")
            print("  Available procedures:")
            for name in list_all_procedures():
                print(f"    - {name}")
            print("\n  Please try again.")


def get_wait_time(procedure):
    """
    Asks how long the user has already waited.
    Your suggestion — takes days/weeks/months and converts internally.
    """
    while True:
        user_input = ask_question(
            "How long have you already been waiting?",
            example="3 days, 2 weeks, 4 months"
        )

        wait_data = parse_wait_time(user_input)

        if wait_data:
            print(f"\n  ✓ Got it: {wait_data['display']}")
            return wait_data
        else:
            print("\n  Sorry, I didn't understand that. Please use a format like:")
            print("  '3 days', '2 weeks', or '4 months'")


def get_budget():
    """
    Asks the user their budget for private treatment.
    Handles common input errors gracefully.
    """
    while True:
        user_input = ask_question(
            "What is your budget for private treatment? (enter 0 if you have no budget)",
            example="5000   or   15000   or   0"
        )

        # Remove £ sign and commas in case user typed them
        cleaned = user_input.replace("£", "").replace(",", "").strip()

        try:
            budget = int(float(cleaned))   # Convert to a whole number
            if budget < 0:
                print("\n  Budget can't be negative. Please enter 0 or more.")
                continue
            print(f"\n  ✓ Budget: £{budget:,}")
            return budget
        except ValueError:
            print("\n  Please enter a number, e.g. 5000")


def main():
    """
    The main function — runs the whole tool from start to finish.
    """

    # ── Welcome Screen ────────────────────────────────────────────────────────
    print("\n" + "═" * 60)
    print("   🏥 NHS vs PRIVATE: UK HEALTHCARE DECISION ENGINE")
    print("═" * 60)
    print("\n  This tool helps you decide whether to wait on the NHS,")
    print("  go private, or explore medical tourism — based on your")
    print("  real situation, with real numbers.")
    print("\n  Answer 3 simple questions to get your personalised report.")

    # ── Step 1: Get the procedure ─────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  STEP 1 of 3: Your Procedure")
    print("─" * 60)
    procedure = get_procedure()

    # ── Step 2: Get wait time ─────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  STEP 2 of 3: Your Wait So Far")
    print("─" * 60)
    wait_data = get_wait_time(procedure)

    # ── Step 3: Get budget ────────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("  STEP 3 of 3: Your Budget")
    print("─" * 60)
    budget = get_budget()

    # ── Process everything ────────────────────────────────────────────────────
    print("\n  Calculating your personalised report...")
    print("─" * 60)

    # Calculate urgency from wait time + NHS average
    urgency_data = calculate_urgency(
        days_waited=wait_data["days_waited"],
        nhs_avg_wait_weeks=procedure["nhs_avg_wait_weeks"]
    )

    # Assess how budget compares to private costs
    budget_data = assess_budget(
        user_budget=budget,
        procedure=procedure
    )

    # Get the best abroad option (cheapest) if available
    abroad_option = None
    if procedure["suitable_for_abroad"] and procedure["abroad"]:
        abroad_option = min(procedure["abroad"], key=lambda x: x["cost"])

    # Generate recommendation
    recommendation = generate_recommendation(
        procedure=procedure,
        urgency_data=urgency_data,
        budget_data=budget_data,
        abroad_option=abroad_option
    )

    # ── Print the report ──────────────────────────────────────────────────────
    print()
    report_text = generate_report(
        procedure=procedure,
        wait_data=wait_data,
        urgency_data=urgency_data,
        budget_data=budget_data,
        recommendation=recommendation
    )

    # ── Ask if they want to save it ───────────────────────────────────────────
    print()
    save = input("  Would you like to save this report as a .txt file? (yes/no): ").strip().lower()
    if save in ["yes", "y"]:
        save_report(report_text, procedure["name"])

    print("\n  Thank you for using the NHS vs Private Decision Engine.")
    print("  Stay well.")


# ── This runs main() when you type: python main.py ────────────────────────────
# The if __name__ check means main() won't run if another file imports this one
if __name__ == "__main__":
    main()
