"""
app.py
------
Flask Web Application - NHS vs Private Decision Engine
-------------------------------------------------------
Run this file to start the web app: python app.py
Then open your browser and go to: http://localhost:5000
"""

from flask import Flask, render_template, request
from modules.procedure_finder import find_procedure, list_all_procedures
from modules.wait_parser import parse_wait_time, calculate_urgency
from modules.private_costs import assess_budget
from modules.recommendation import generate_recommendation

app = Flask(__name__)

@app.route("/")
def index():
    procedures = list_all_procedures()
    return render_template("index.html", procedures=procedures)

@app.route("/results", methods=["POST"])
def results():
    procedure_input = request.form.get("procedure", "").strip()
    wait_input      = request.form.get("wait_time", "").strip()
    budget_input    = request.form.get("budget", "0").strip()

    errors = []

    procedure = find_procedure(procedure_input)
    if not procedure:
        errors.append(f"Sorry, we couldn't find '{procedure_input}'. Please try a different procedure.")

    wait_data = parse_wait_time(wait_input)
    if not wait_data:
        errors.append("Please enter your wait time as '3 days', '2 weeks', or '4 months'.")

    try:
        budget = int(float(budget_input.replace("£", "").replace(",", "")))
        if budget < 0:
            errors.append("Budget cannot be negative.")
    except ValueError:
        errors.append("Please enter a valid budget amount, e.g. 5000")
        budget = 0

    if errors:
        procedures = list_all_procedures()
        return render_template("index.html", procedures=procedures, errors=errors)

    urgency_data = calculate_urgency(
        days_waited=wait_data["days_waited"],
        nhs_avg_wait_weeks=procedure["nhs_avg_wait_weeks"]
    )

    budget_data = assess_budget(
        user_budget=budget,
        procedure=procedure
    )

    abroad_option = None
    if procedure["suitable_for_abroad"] and procedure["abroad"]:
        abroad_option = min(procedure["abroad"], key=lambda x: x["cost"])

    recommendation = generate_recommendation(
        procedure=procedure,
        urgency_data=urgency_data,
        budget_data=budget_data,
        abroad_option=abroad_option
    )

    return render_template(
        "results.html",
        procedure=procedure,
        wait_data=wait_data,
        urgency_data=urgency_data,
        budget_data=budget_data,
        abroad_option=abroad_option,
        recommendation=recommendation
    )

if __name__ == "__main__":
    app.run(debug=True)