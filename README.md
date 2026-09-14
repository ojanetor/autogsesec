# autogsesec
Autonomous GSE Cybersecurity Tabletop Exercise Platform

A web-based security training platform for professionals responsible for securing autonomous ground service equipment operating on active airfields in U.S. aviation critical infrastructure.

---

## The Problem

Self-driving vehicles move cargo across active airfields at major U.S. airports today. A cyberattack on these systems does not produce a data breach — it produces a vehicle in motion near aircraft and people.

The frameworks that exist were built for IT networks and industrial control systems. Jiang et al. (2025) reviewed 417 publications on MITRE ATT&CK and confirmed documented gaps in cyber-physical and ICS coverage. Security teams working with autonomous airside systems have nothing purpose-built to train against.

AutoGSESec fills that gap.

---

## What It Does

| Component | Function |
|-----------|----------|
| **Scenario Library** | Interactive threat scenarios mapped to MITRE ATT&CK for ICS tactics |
| **Exercise Delivery Engine** | Branching decision prompts with session state management |
| **Scoring Engine** | Rule-based evaluation against NIST SP 800-82 control families |
| **After-Action Reports** | Gaps, recommended controls, and prioritized implementation timelines |

---

## Scenario Modules

1. **Initial Access (TA0108)** — insider threat and social engineering
2. **Command and Control (TA0101)** — GPS spoofing
3. **Impact (TA0106)** — physical consequence and response

---

## Tech Stack

- **Backend:** Python 3.11 + Flask
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Database:** SQLite via SQLAlchemy
- **Hosting:** Render.com

---

## Setup

```bash
git clone https://github.com/ojanetor/autogsesec.git
cd autogsesec
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

---

## ⚠️ Disclaimer

AutoGSESec is an **educational and preparedness tool only**. It does not constitute a formal security assessment, compliance certification, or guarantee of protection. It should be used alongside qualified security professionals and regulatory compliance programs — never as a substitute for them.

All scenario content is derived from publicly available NIST and MITRE documentation. No proprietary operational data is used.

---

## Project Context

Applied project for CISC 699 — Applied Project in Computer Information Sciences
Harrisburg University of Science and Technology | Fall 2026

Extends thesis research completed in GRAD 695: *Securing the Airside — A Cybersecurity Risk and Threat-Modeling Framework for Autonomous Ground Service Equipment in U.S. Aviation Critical Infrastructure*

---

## License

MIT
