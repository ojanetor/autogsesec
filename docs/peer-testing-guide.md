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

## For testers T2, T3, and T4: rubric check

**Do this only after finishing your two scenarios**, because these tables show the answer key.

Each of you reviews different decisions, so together you cover all 36 rubric entries. For each row, decide whether you **agree** with the rating, the controls, and the "fix by" timeline. Reply with the row ID, **Agree** or **Disagree**, and a short comment if you disagree. Example: `SC02-D1-b Disagree: should be Incorrect, because ...`

- **Ratings:** Correct = 2 points, Partial = 1, Incorrect = 0.
- **Fix by:** the timeline the report gives for a gap: Immediate (within 30 days), Short-term (30–90 days), Long-term (over 90 days).

| Tester | Your rows | Time |
|---|---|---|
| T4 | 20 rows: all of Drifting Positions, and Dark Screens decisions 1 and 3 | about 25 minutes |
| T2 | 8 rows: The Helpful Caller decisions 1 and 2 | about 10 minutes |
| T3 | 8 rows: The Helpful Caller decision 3, and Dark Screens decision 2 | about 10 minutes |

### T4: 20 entries

**Drifting Positions: GPS Spoofing on the Ramp — Decision 1: What is your first action?**

*Situation:* During the early morning departure bank, the fleet dashboard shows one autonomous baggage tractor about 15 meters from where the ramp agent can see it. The vehicle is still moving and its route planner is adjusting to the reported position.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC01-D1-a | Treat it as a sensor glitch and let the tractor finish its run. | Incorrect | SI-4 System Monitoring | Immediate | An unexplained position mismatch is a monitoring alert, not something to ignore. |
| SC01-D1-b | Command a safe stop and tell the operations supervisor. | Partial | IR-4 Incident Handling | Short-term | Safe stop and escalation are right, but evidence is not preserved. |
| SC01-D1-c | Command a safe stop and restart the navigation system right away. | Incorrect | IR-4 Incident Handling | Immediate | Restarting before preserving logs can destroy the evidence incident handling needs. |
| SC01-D1-d | Command a safe stop, tell the supervisor, and preserve the logs. | Correct | IR-4 Incident Handling; SI-4 System Monitoring | — | Contains the hazard, escalates, and preserves evidence. |

**Drifting Positions: GPS Spoofing on the Ramp — Decision 2: Who needs to know, and how?**

*Situation:* Within ten minutes two more tractors in the same area show the same drift. Vehicles on the far side of the ramp look normal.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC01-D2-a | Keep it within the ramp team to avoid alarming anyone. | Incorrect | IR-6 Incident Reporting | Immediate | A multi-vehicle anomaly must be reported to the people responsible for response. |
| SC01-D2-b | Report to the security team and airport operations through the incident process. | Correct | IR-6 Incident Reporting; IR-8 Incident Response Plan | — | Uses the defined incident reporting path to the right parties. |
| SC01-D2-c | Contact only the vehicle vendor's support line. | Partial | IR-6 Incident Reporting | Short-term | The vendor matters, but internal security and operations must also be told. |
| SC01-D2-d | Post a heads-up in the shift group chat. | Incorrect | IR-6 Incident Reporting | Immediate | An informal channel is not an incident report and may spread unverified information. |

**Drifting Positions: GPS Spoofing on the Ramp — Decision 3: How do you return to operations?**

*Situation:* After forty minutes the reported positions look normal again. Operations wants the fleet back in service for the next bank.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC01-D3-a | Resume normal autonomous operations since the drift has stopped. | Incorrect | CP-10 System Recovery and Reconstitution | Immediate | The drift stopping does not show the cause is gone; recovery needs verification. |
| SC01-D3-b | Resume under supervised mode in the affected zone and hold a lessons-learned review. | Correct | CP-10 System Recovery and Reconstitution; IR-4 Incident Handling; SI-4 System Monitoring | — | Controlled recovery with continued monitoring and lessons learned. |
| SC01-D3-c | Ground the whole fleet until the vendor confirms the cause. | Partial | CP-10 System Recovery and Reconstitution | Long-term | Safe but not proportionate; recovery planning should allow controlled restoration. |
| SC01-D3-d | Resume normally and add the event to next quarter's review list. | Incorrect | IR-4 Incident Handling | Short-term | Lessons learned should follow the incident promptly, not wait for a scheduled review. |

**Dark Screens: Loss of View Across the Fleet — Decision 1: What is your first action?**

*Situation:* During a busy arrival bank, the fleet monitoring dashboard stops updating. Vehicle icons are frozen in place, but ramp staff can see tractors still moving near aircraft.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC03-D1-a | Wait a few minutes for the dashboard to recover. | Incorrect | SI-4 System Monitoring; IR-4 Incident Handling | Immediate | Vehicles are moving with no one watching; waiting accepts a safety risk. |
| SC03-D1-b | Trigger the fleet-wide safe stop and post staff to watch the vehicles directly. | Correct | IR-4 Incident Handling; CP-2 Contingency Plan | — | Removes the hazard first and replaces the lost view with direct observation, as a contingency plan should. |
| SC03-D1-c | Open an IT ticket and keep operating while IT investigates. | Incorrect | IR-4 Incident Handling | Immediate | Treats a safety event as a routine IT fault while vehicles keep moving unwatched. |
| SC03-D1-d | Stop only the vehicles closest to aircraft and let the rest continue. | Partial | IR-4 Incident Handling | Short-term | Reduces the worst risk, but other vehicles still move with no one watching. |

**Dark Screens: Loss of View Across the Fleet — Decision 3: How do you return to operations?**

*Situation:* Monitoring is back and the cause is still being investigated. Operations wants to return to full autonomous operations.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC03-D3-a | Resume normally now that the dashboard works. | Incorrect | CP-10 System Recovery and Reconstitution | Immediate | A working dashboard does not show that the cause is gone; recovery needs verification. |
| SC03-D3-b | Resume in supervised mode, test the manual fallback procedure, and update and exercise the contingency plan. | Correct | CP-2 Contingency Plan; CP-4 Contingency Plan Testing; CP-10 System Recovery and Reconstitution | — | Controlled recovery, and the contingency plan is tested before it is needed again. |
| SC03-D3-c | Keep the fleet grounded until a full vendor audit is complete. | Partial | CP-10 System Recovery and Reconstitution | Long-term | Safe but not proportionate; recovery planning should allow controlled restoration. |
| SC03-D3-d | Add a second monitoring screen and resume normally. | Incorrect | CP-2 Contingency Plan | Short-term | More screens do not help when the monitoring data itself fails. |

### T2: 8 entries

**The Helpful Caller: Social Engineering at the Fleet Console — Decision 1: What do you do?**

*Situation:* Shortly before the morning departure bank, the shift lead gets a call from someone who says they are from the vehicle vendor's support team. They say a critical update must go out before the bank and ask the shift lead to turn on remote access to the fleet console and read back the one-time access code.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC02-D1-a | Turn on remote access and read the code, since the update sounds urgent. | Incorrect | AT-2 Literacy Training and Awareness; AC-17 Remote Access | Immediate | Urgency and authority are classic social-engineering pressure; remote access went to an unverified caller. |
| SC02-D1-b | Refuse, hang up, and carry on with the shift. | Partial | AT-2 Literacy Training and Awareness | Short-term | Refusing stops the attempt, but security never hears about it, so other staff stay exposed. |
| SC02-D1-c | Refuse, call the vendor back on the number in the support contract, and report the call to security. | Correct | AT-2 Literacy Training and Awareness; IR-6 Incident Reporting | — | Verifies the request through a known channel and reports the attempt so others can be warned. |
| SC02-D1-d | Turn on remote access but watch the session closely. | Incorrect | AC-17 Remote Access | Immediate | Watching the session does not stop an unverified party from acting on the fleet. |

**The Helpful Caller: Social Engineering at the Fleet Console — Decision 2: How do you handle the account?**

*Situation:* Security reviews fleet console sign-ins after the call. They find that the account of a maintenance contractor whose contract ended three weeks ago signed in late last night.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC02-D2-a | Disable the account now, preserve the sign-in records, and review what it accessed. | Correct | PS-4 Personnel Termination; AC-2 Account Management; AU-6 Audit Record Review, Analysis, and Reporting | — | Closes access at once, keeps the evidence, and finds out what the account did. |
| SC02-D2-b | Disable the account and move on. | Partial | PS-4 Personnel Termination | Short-term | Closes the door but leaves the question of what happened unanswered. |
| SC02-D2-c | Leave the account active and email the contractor's former manager to ask about it. | Incorrect | PS-4 Personnel Termination | Immediate | The account of someone who has left must be closed at once, not after an email. |
| SC02-D2-d | Reset the password but keep the account in case the contractor comes back. | Incorrect | AC-2 Account Management | Immediate | Accounts of people who have left should be removed, not kept in reserve. |

### T3: 8 entries

**The Helpful Caller: Social Engineering at the Fleet Console — Decision 3: What do you recommend?**

*Situation:* The review shows no changes were made to the vehicles, but the account could see fleet routes and schedules. Leadership asks what should change.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC02-D3-a | Send a reminder email about phishing to all staff. | Partial | AT-2 Literacy Training and Awareness | Short-term | Awareness helps, but one email does not build skills or close the account gap. |
| SC02-D3-b | Role-based social-engineering training for ramp and operations staff, least-privilege console roles, and an offboarding step that closes accounts when contracts end. | Correct | AT-3 Role-Based Training; AC-6 Least Privilege; PS-4 Personnel Termination | — | Fixes the human, access, and process causes together. |
| SC02-D3-c | Ban all vendor remote access permanently. | Partial | AC-17 Remote Access | Long-term | Removes the risk but also legitimate support; controlled remote access is the proportionate fix. |
| SC02-D3-d | No change, since nothing was damaged. | Incorrect | AT-2 Literacy Training and Awareness; AC-6 Least Privilege | Short-term | Two failures happened; no damage this time was luck, not control. |

**Dark Screens: Loss of View Across the Fleet — Decision 2: What do you do next?**

*Situation:* The vendor reports that the monitoring server restarted after a configuration change that nobody on the change calendar made.

| Row | Option | Rating | NIST SP 800-53 Rev. 5 controls | Fix by | Rationale |
|---|---|---|---|---|---|
| SC03-D2-a | Restore the last good configuration and resume, without further investigation. | Partial | CP-10 System Recovery and Reconstitution | Short-term | Restores service but treats an unexplained change as routine. |
| SC03-D2-b | Preserve the logs, check the change records, report it as a possible incident, then restore a known-good configuration. | Correct | IR-4 Incident Handling; AU-6 Audit Record Review, Analysis, and Reporting; CM-3 Configuration Change Control | — | Keeps the evidence, finds out who made the change, and recovers safely. |
| SC03-D2-c | Wait for the vendor's written report before doing anything. | Incorrect | IR-6 Incident Reporting | Immediate | Incident handling and reporting are the operator's job too, not only the vendor's. |
| SC03-D2-d | Wipe and rebuild the server right away. | Incorrect | IR-4 Incident Handling | Immediate | Rebuilding first destroys the evidence of who made the change. |

## How your input is used

Results are reported anonymously by tester ID in the project report: whether each scenario was finished without help, the 1–5 ratings, any problems found, and (for T2, T3, and T4) agreement with the rubric. Nothing you send is published with your name.