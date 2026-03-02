# 🏥 NHS vs Private: UK Healthcare Decision Engine
🌐 **Live Demo: [https://nhs-vs-private.onrender.com](https://nhs-vs-private.onrender.com)**
A free, open-source Python tool that helps UK residents make an **informed, data-driven decision** about whether to wait on the NHS, go private, or explore medical tourism — based on their real situation.

> **7 million people** are currently on NHS waiting lists. Every one of them faces the same question with no honest, free tool to help them answer it. This is that tool.

---

## 🎯 What It Does

You answer 3 questions:
1. What procedure do you need?
2. How long have you already been waiting?
3. What is your budget?

The tool gives you a **complete, transparent report** covering:

- Your NHS waiting position and estimated time remaining
- Private UK costs with full finance breakdown (monthly payments, total repayable, interest)
- Medical tourism options where applicable (Poland, Hungary, Turkey)
- A plain English recommendation based on your specific situation

---

## 💡 Why This Exists

Every existing "comparison" tool is either:
- A commercial site pushing private health insurance
- A basic NHS page with no cost context
- A form that collects your data and calls you

This tool is **fully offline, fully transparent, and completely free**. No data collected. No calls. No sales pitch.

---

## 🚀 Getting Started

### Requirements
- Python 3.8 or higher
- No external libraries needed for core functionality

### Installation

```bash
git clone https://github.com/yourusername/nhs-vs-private.git
cd nhs-vs-private
python main.py
```

### Running Tests

```bash
pip install pytest
pytest tests/test_modules.py -v
```

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
  2. Hungary (Budapest) offers this at £5,800 — close to your
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
├── main.py                    ← Entry point
├── data/
│   └── procedures.json        ← Procedure database
├── modules/
│   ├── procedure_finder.py    ← Matches user input to procedures
│   ├── wait_parser.py         ← Converts days/weeks/months + urgency
│   ├── private_costs.py       ← Cost + finance calculator
│   ├── recommendation.py      ← Decision engine
│   └── report.py              ← Output formatter
├── tests/
│   └── test_modules.py        ← Unit tests
└── requirements.txt
```

---

## 🔮 Planned Features

- [ ] Live NHS waiting time data via NHS England RTT API
- [ ] Postcode-based nearest private provider lookup
- [ ] Export report as PDF
- [ ] Web interface (Flask)
- [ ] More procedures (target: 50)
- [ ] NHS e-Referral Trust comparison by specialty

---

## 🤝 Contributing

Contributions welcome. If you work in healthcare or have access to better cost data, please open a PR or issue. Accuracy matters here — real people use this.

---

## ⚠️ Disclaimer

This tool provides general guidance only and is **not medical or financial advice**. Always consult a qualified medical professional and/or Independent Financial Adviser before making healthcare decisions.

---

## 📄 Licence

MIT Licence — free to use, share, and build on.
