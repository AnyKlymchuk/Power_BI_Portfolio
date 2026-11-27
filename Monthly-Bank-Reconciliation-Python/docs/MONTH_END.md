# Monthly close: investigation and review

## Confirmed scope versus assumptions

Confirmed by the project request: monthly reconciliation, Python, bank statement versus an internal ledger from another system, and a freelance portfolio deliverable.

Demo assumptions requiring client agreement: matching cash-account perspective, two decimal places, common references, calendar-day date window of 3 days, no FX conversion, one-to-one settlements, same monthly period, sign convention of inflows positive/outflows negative. These are not confirmed rules from the interview bank.

## Roles and handoff

| Step | Responsible role | Evidence / outcome |
| --- | --- | --- |
| Export and verify coverage | Source system owner | Full statement period, account list, independent row counts and opening/closing balances |
| Run and validate | Analyst / data engineer | Run hashes, source controls, validation errors |
| Investigate settlement gaps | Operations | Payment/settlement evidence; next-period confirmation |
| Investigate amounts, fees, timing | Finance analyst | Ledger entry, invoice, fee agreement, posting dates |
| Fix extract/duplicate issue | Data team + source owner | Source correction or approved mapping; rerun |
| Approve accounting correction | Authorized finance reviewer | Approved adjustment and posting ID |
| Review close | Team lead / controller | Cleared controls, reviewed cases, documented outstanding items |

Suggested owners in the generated report are routing hints, not real assignments. The report does not modify systems or approve transactions.

## Monthly algorithm in plain English

Start with the same account, currency and month. Check that the files are complete. Match shared references once each, compare amounts and dates, and send differences to the work queue. Check blank-reference candidates manually. Then explain closing bank minus ledger using the opening difference and all transaction differences. Review each case even when the total difference is zero.

## Investigation register to maintain outside the prototype

Record run ID (input hashes + period), case ID, both source IDs, owner, reason, supporting evidence, proposed action, due date, investigation state, approver, approval date, posting reference and next-run result. Case IDs are local to one run and may change when inputs change; use source IDs plus run hashes to track lineage. Never mark a new run cleared just because an old case ID was cleared.

## Suggested team-lead controls

Track completeness failures, open cases by reason and owner, exception age at month end, unresolved absolute transaction differences within each currency, and monthly close approval. Set escalation deadlines with the client. Record approved timing items separately from true errors; retain evidence for both. The dashboard's age is calendar days from the earliest case date to month end, not days since assignment.

## Example EUR bridge

Bank opening 10,000.00 + bank movement 1,225.00 = 11,225.00.
Ledger opening 10,000.00 + ledger movement 833.00 = 10,833.00.
Closing difference 392.00 = opening difference 0.00 + transaction difference 392.00.

The bridge proves all loaded differences are represented, not that source data is complete or all cases are resolved. Counts, roll-forwards and individual exceptions provide separate controls.
