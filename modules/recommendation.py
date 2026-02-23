"""
recommendation.py
-----------------
The brain of the tool.
Takes all the data and produces a clear, honest recommendation.
"""


def generate_recommendation(procedure, urgency_data, budget_data, abroad_option=None):
    """
    Takes all computed data and returns a recommendation.

    Logic:
    1. If urgency is CRITICAL → strongly push private or abroad
    2. If budget covers private → recommend private
    3. If abroad is available and saves >40% → flag it
    4. If none of the above → recommend NHS with tips to speed it up
    """

    urgency = urgency_data["urgency"]
    budget_status = budget_data["status"]
    weeks_remaining = urgency_data["weeks_remaining"]

    recommendations = []
    primary = ""

    # ── CRITICAL: Already exceeded NHS average wait ───────────────────────────
    if urgency == "CRITICAL":
        primary = "🚨 CHASE YOUR NHS REFERRAL IMMEDIATELY"
        recommendations.append(
            "You have already waited longer than the NHS average. "
            "Contact your GP today and ask them to escalate your referral. "
            "You are entitled to ask for the NHS e-Referral Service to choose a different Trust with shorter waits."
        )
        if budget_status == "FULLY_COVERED":
            recommendations.append(
                f"You can afford private treatment. Given your situation, we strongly recommend booking privately. "
                f"Contact {', '.join(procedure['private_providers'][:2])} for availability."
            )
        elif abroad_option:
            recommendations.append(
                f"Consider {abroad_option['country']} ({abroad_option['city']}) at £{abroad_option['cost']:,} — "
                f"significantly cheaper than UK private and at {abroad_option['quality']} standards."
            )

    # ── HIGH urgency + budget covers private ─────────────────────────────────
    elif urgency == "HIGH" and budget_status == "FULLY_COVERED":
        primary = "✅ GO PRIVATE — YOUR BUDGET COVERS IT"
        recommendations.append(
            f"With {weeks_remaining} weeks still to wait on the NHS and a budget that covers private treatment, "
            f"going private is your best option. You'll be seen within 2–4 weeks."
        )
        recommendations.append(
            f"Recommended providers: {', '.join(procedure['private_providers'])}."
        )

    # ── HIGH urgency + budget partially covers ────────────────────────────────
    elif urgency == "HIGH" and budget_status == "PARTIALLY_COVERED":
        primary = "⚠️ CONSIDER FINANCE OR ABROAD"
        recommendations.append(
            f"Your urgency is high ({weeks_remaining} weeks remaining) but your budget only partially covers private UK costs. "
            f"Consider a medical finance plan to bridge the gap."
        )
        if abroad_option:
            recommendations.append(
                f"Alternatively, {abroad_option['country']} offers this procedure at £{abroad_option['cost']:,} "
                f"which may fit your budget better."
            )

    # ── MODERATE urgency ──────────────────────────────────────────────────────
    elif urgency == "MODERATE":
        primary = "🔄 WEIGH YOUR OPTIONS — NO IMMEDIATE RUSH"
        recommendations.append(
            f"You're roughly halfway through your NHS wait ({weeks_remaining} weeks remaining). "
            f"You have time to make a considered decision."
        )
        if budget_status == "FULLY_COVERED":
            recommendations.append(
                "Since your budget covers private treatment, going private would eliminate the remaining wait. "
                "It's worth getting a private consultation quote before deciding."
            )
        elif abroad_option:
            abroad_saving = budget_data["avg_cost"] - abroad_option["cost"]
            if abroad_saving > 0:
                recommendations.append(
                    f"Going abroad to {abroad_option['country']} could save you approximately "
                    f"£{abroad_saving:,.0f} compared to UK private costs."
                )
        recommendations.append(
            "If staying on the NHS: ask your GP about the NHS e-Referral Service — "
            "you may be able to switch to a Trust with a shorter waiting list."
        )

    # ── LOW urgency ───────────────────────────────────────────────────────────
    else:
        primary = "🟢 STICK WITH NHS — YOU'RE NEARLY THERE"
        recommendations.append(
            f"You're close to the end of the typical NHS wait ({weeks_remaining} weeks remaining). "
            f"Unless your symptoms have significantly worsened, waiting is likely the right call."
        )
        recommendations.append(
            "Keep your GP updated on any changes to your symptoms in case escalation is needed."
        )

    return {
        "primary": primary,
        "recommendations": recommendations
    }


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fake_procedure = {
        "name": "Knee Replacement",
        "private_providers": ["Spire Healthcare", "Nuffield Health"]
    }
    fake_urgency = {
        "urgency": "HIGH",
        "weeks_remaining": 24,
        "months_remaining": 6,
        "urgency_reason": "Most of your wait is still ahead."
    }
    fake_budget = {
        "status": "FULLY_COVERED",
        "avg_cost": 14000,
        "user_budget": 16000
    }
    result = generate_recommendation(fake_procedure, fake_urgency, fake_budget)
    print(f"Primary: {result['primary']}")
    for r in result["recommendations"]:
        print(f"  - {r}")
