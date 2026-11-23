# AutoGSESec Peer Testing Guide

Thank you for testing AutoGSESec. It takes about **20 minutes**, and you need only a web browser.

**Testing window:** now until **Saturday, November 28, 2026**.

## Before you start

- You will receive a **tester ID** (T1, T2, T3, or T4) in my message. Use it in your reply instead of your name.
- **Please don't open the `data/mappings` folder in this repository before testing.** It contains the answer key.
- **Answer from general knowledge only.** Do not describe your employer's systems, procedures, or any confidential information in the app or in your reply.
- The app stores **no names or personal data**: only your answers, three 1–5 ratings, and timestamps, under a random session number.

## Steps

1. **Open** https://autogsesec.onrender.com
   - The first load can take **up to a minute** if the site has been idle. That is expected; please wait.
2. **Complete the two scenarios assigned to your tester ID:**

   | Tester ID | First scenario | Second scenario |
   |---|---|---|
   | T1 | Drifting Positions | The Helpful Caller |
   | T2 | The Helpful Caller | Dark Screens |
   | T3 | Dark Screens | Drifting Positions |
   | T4 | Drifting Positions | Dark Screens |

   For each scenario:
   - answer the **"Before you start"** rating on the first decision;
   - make your three decisions;
   - answer the **two quick questions** on the summary page;
   - open the **after-action report** and click **Download report (.txt)** to check the download works.
3. **Please don't ask for help while testing.** If you get stuck, write down where. That is useful data.
4. **Reply to my message** with the five answers below.

## Your reply (copy, fill in, send)

```
Tester ID:
1. Did you finish both scenarios without help? (yes / no; if no, where did you get stuck?)
2. Did anything break, look wrong, or feel slow? (describe it; a screenshot helps)
3. Did the report download work? (yes / no)
4. How realistic were the scenarios? (1 = not at all, 5 = very realistic)
5. One thing you would change:
```

## For tester T4 only: rubric check (about 15 extra minutes)

**After** finishing your scenarios, please review these 12 entries from the scoring rubric (12 of 36, which is 33%). For each one, mark whether you **agree** with the rating and controls, and add a short comment if you disagree. Reply with the row number, Agree or Disagree, and any comment.

Ratings: Correct = 2 points, Partial = 1, Incorrect = 0. "Fix by" is the timeline the report gives for a gap: Immediate (within 30 days), Short-term (30–90 days), Long-term (over 90 days).

| Row | Decision | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|---|
| **Drifting Positions: GPS Spoofing on the Ramp** | | | | | | |
| R01 | 1. What is your first action? | Command a safe stop, tell the supervisor, and preserve the logs. | Correct | IR-4 Incident Handling; SI-4 System Monitoring | — | Contains the hazard, escalates, and preserves evidence. |
| R02 | 2. Who needs to know, and how? | Report to the security team and airport operations through the incident process. | Correct | IR-6 Incident Reporting; IR-8 Incident Response Plan | — | Uses the defined incident reporting path to the right parties. |
| R03 | 3. How do you return to operations? | Resume under supervised mode in the affected zone and hold a lessons-learned review. | Correct | CP-10 System Recovery and Reconstitution; IR-4 Incident Handling; SI-4 System Monitoring | — | Controlled recovery with continued monitoring and lessons learned. |
| R04 | 3. How do you return to operations? | Ground the whole fleet until the vendor confirms the cause. | Partial | CP-10 System Recovery and Reconstitution | Long-term | Safe but not proportionate; recovery planning should allow controlled restoration. |
| **The Helpful Caller: Social Engineering at the Fleet Console** | | | | | | |
| R05 | 1. What do you do? | Refuse, call the vendor back on the number in the support contract, and report the call to security. | Correct | AT-2 Literacy Training and Awareness; IR-6 Incident Reporting | — | Verifies the request through a known channel and reports the attempt so others can be warned. |
| R06 | 1. What do you do? | Refuse, hang up, and carry on with the shift. | Partial | AT-2 Literacy Training and Awareness | Short-term | Refusing stops the attempt, but security never hears about it, so other staff stay exposed. |
| R07 | 2. How do you handle the account? | Disable the account now, preserve the sign-in records, and review what it accessed. | Correct | PS-4 Personnel Termination; AC-2 Account Management; AU-6 Audit Record Review, Analysis, and Reporting | — | Closes access at once, keeps the evidence, and finds out what the account did. |
| R08 | 3. What do you recommend? | Role-based social-engineering training for ramp and operations staff, least-privilege console roles, and an offboarding step that closes accounts when contracts end. | Correct | AT-3 Role-Based Training; AC-6 Least Privilege; PS-4 Personnel Termination | — | Fixes the human, access, and process causes together. |
| **Dark Screens: Loss of View Across the Fleet** | | | | | | |
| R09 | 1. What is your first action? | Trigger the fleet-wide safe stop and post staff to watch the vehicles directly. | Correct | IR-4 Incident Handling; CP-2 Contingency Plan | — | Removes the hazard first and replaces the lost view with direct observation, as a contingency plan should. |
| R10 | 1. What is your first action? | Stop only the vehicles closest to aircraft and let the rest continue. | Partial | IR-4 Incident Handling | Short-term | Reduces the worst risk, but other vehicles still move with no one watching. |
| R11 | 2. What do you do next? | Preserve the logs, check the change records, report it as a possible incident, then restore a known-good configuration. | Correct | IR-4 Incident Handling; AU-6 Audit Record Review, Analysis, and Reporting; CM-3 Configuration Change Control | — | Keeps the evidence, finds out who made the change, and recovers safely. |
| R12 | 3. How do you return to operations? | Keep the fleet grounded until a full vendor audit is complete. | Partial | CP-10 System Recovery and Reconstitution | Long-term | Safe but not proportionate; recovery planning should allow controlled restoration. |

## How your input is used

Results are reported anonymously by tester ID in the project report: whether each scenario was finished without help, the 1–5 ratings, any problems found, and (for T4) agreement with the rubric. Nothing you send is published with your name.