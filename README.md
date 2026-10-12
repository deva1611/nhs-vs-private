# 🏥 NHS vs Private: UK Healthcare Decision Engine

[![CI](https://github.com/deva1611/nhs-vs-private/actions/workflows/ci.yml/badge.svg)](https://github.com/deva1611/nhs-vs-private/actions/workflows/ci.yml)

🌐 **Live demo: [nhs-vs-private.onrender.com](https://nhs-vs-private.onrender.com)** (free hosting, so the first load can take up to a minute while it wakes up)

A free, open-source Python tool that helps UK residents make an informed decision about whether to wait on the NHS, go private, or look at treatment abroad, based on their own situation.

> Around 7 million cases are on the NHS waiting list in England. Everyone on it faces the same question, and there is no honest, free tool to help them answer it. This is that tool.

---

## 🎯 What It Does

You answer 3 questions:
1. What procedure do you need?
2. How long have you already been waiting?
3. What is your budget?

The tool gives you a clear, transparent report covering:

- Your NHS waiting position and estimated time remaining
- Private UK costs with a full finance breakdown (monthly payments, total repayable, interest)
- Treatment abroad options where suitable (Poland, Hungary, Turkey)
- A plain English recommendation based on your answers

It runs two ways: as a **Flask web app** (the live demo) or as a **command-line tool**.

---

## 💡 Why This Exists

Most existing "comparison" tools are one of these:
- A commercial site pushing private health insurance
- A basic NHS page with no cost context
- A form that collects your details so someone can call you

This tool is free and transparent. It has no accounts, no database and no sales pitch. Nothing you enter is stored. The command-line version runs entirely offline on your own machine.

---

## 🚀 Getting Started

### Requirements
- Python 3.8 or higher
- The command-line tool uses only the Python standard library
- The web app needs Flask (installed from `requirements.txt`)

### Run the web app locally

```bash
git clone https://github.com/deva1611/nhs-vs-private.git
cd nhs-vs-private
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in your browser.

### Run the command-line version

```bash
python main.py
```

### Run the tests

```bash
pip install pytest
pytest tests/ -v
```

Tests also run automatically on every push through GitHub Actions.

---

## 📋 Supported Procedures

| Procedure | NHS Avg Wait | Private Cost Range |
|---|---|---|
| Knee Replacement | 38 weeks | £11,000 – £17,000 |
| Hip Replacement | 40 weeks | £12,000 – £18,000 |
| MRI Scan | 12 weeks | £350 – £800 |
| Cataract Surgery | 20 weeks | £2,000 – £4,000 |
| Hernia Repair | 24 weeks | £3,000 – £6,000 |
| Colonoscopy | 10 weeks | £1,500 – £3,000 |
| Carpal Tunnel Surgery | 18 weeks | £1,500 – £3,500 |
| Tonsil Removal | 22 weeks | £2,500 – £5,000 |
| Physiotherapy | 8 weeks | £50 – £120/session |
| Dermatology Consultation | 16 weeks | £200 – £500 |

### Where the figures come from

All figures are indicative averages compiled in February 2026 and stored in `data/procedures.json`. NHS waits are based on NHS England Referral to Treatment (RTT) waiting time statistics. Private prices are typical self-pay ranges from published UK provider price lists. Treatment abroad prices are typical package prices from clinics in each country.

Real costs and waits vary by hospital, region and individual case, and these figures will drift over time. Always get a direct quote before deciding.

---

## 📊 Sample Output

```
════════════════════════════════════════════════════════════
   NHS vs PRIVATE: YOUR HEALTHCARE DECISION
   Generated: 23 February 2026
════════════════════════════════════════════════════════════

  Procedure  : Knee Replacement
  Waited     : 6 weeks (42 days)
  Budget     : £5,000

─── NHS ────────────────────────────────────────────────────
  NHS average wait     : 38 weeks
  You have waited      : 6 weeks (42 days)
  Estimated remaining  : ~32 weeks (8 months)
  Urgency level        : HIGH
  Most of your wait is still ahead.
  Cost to you          : £0 (free at point of use)

─── PRIVATE (UK) ───────────────────────────────────────────
  Cost range           : £11,000 – £17,000
  Average cost         : £14,000
  Typical wait         : 2–4 weeks

  Finance options (at 9.9% APR):
    12 months → £1,231.12/month | Total: £14,773 | Interest: £773
    24 months →   £644.48/month | Total: £15,467 | Interest: £1,467
    36 months →   £451.09/month | Total: £16,239 | Interest: £2,239

─── MEDICAL TOURISM ────────────────────────────────────────
  Poland (Warsaw)   →  £6,500  |  EU Accredited  |  Saving: £7,500
  Hungary (Budapest)→  £5,800  |  EU Accredited  |  Saving: £8,200
  Turkey (Istanbul) →  £4,500  |  JCI Accredited |  Saving: £9,500

─── RECOMMENDATION ─────────────────────────────────────────

  ⚠️ CONSIDER FINANCE OR ABROAD

  1. Your urgency is high (32 weeks remaining) but your budget
     only partially covers private UK costs.
  2. Hungary (Budapest) offers this at £5,800, close to your
     budget and at EU Accredited standards.

════════════════════════════════════════════════════════════
  ⚠️  This tool provides guidance only and is not medical
  or financial advice. Always consult a qualified professional.
════════════════════════════════════════════════════════════
```

---

## 🗂️ Project Structure

```
nhs-vs-private/
│
├── app.py                     ← Flask web app (live demo)
├── main.py                    ← Command-line entry point
├── Procfile                   ← Render start command (gunicorn)
├── requirements.txt
├── data/
│   └── procedures.json        ← Procedure database
├── modules/
│   ├── procedure_finder.py    ← Matches user input to procedures
│   ├── wait_parser.py         ← Converts days/weeks/months + urgency
│   ├── private_costs.py       ← Cost + finance calculator
│   ├── recommendation.py      ← Decision engine
│   └── report.py              ← Output formatter
├── templates/                 ← HTML pages for the web app
├── static/                    ← CSS and assets
├── tests/
│   └── test_modules.py        ← Unit tests (pytest)
├── .github/workflows/ci.yml   ← GitHub Actions CI
└── LICENSE
```

---

## 🔮 Planned Features

- [x] Web interface (Flask), deployed on Render
- [x] Automated tests with GitHub Actions
- [ ] Live NHS waiting time data via NHS England RTT data
- [ ] Postcode-based nearest private provider lookup
- [ ] Export report as PDF
- [ ] More procedures (target: 50)
- [ ] NHS trust comparison by specialty

---

## 🤝 Contributing

Contributions are welcome. If you work in healthcare or have access to better cost data, please open a PR or issue. Accuracy matters here because real people may use this.

---

## ⚠️ Disclaimer

This tool provides general guidance only and is **not medical or financial advice**. Always consult a qualified medical professional and/or an Independent Financial Adviser before making healthcare decisions.

---

## 📄 Licence

MIT Licence. Free to use, share, and build on.
