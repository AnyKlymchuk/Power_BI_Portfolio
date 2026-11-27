# Validation record

Validated 2026-11-27 using Python 3.12.14.

`python -m unittest discover -s tests -v`: 15 tests passed. Coverage includes Decimal precision, exact and date matching, amount/fee differences, duplicate references on either side, account/currency isolation, ambiguous and unique blank-reference candidates, candidate date limits, offsetting errors, source row-ID errors, period mismatch, rejected amounts, independent count/balance failures and deterministic report generation.

`python reconcile.py --month 2026-10`: generated the synthetic monthly reports successfully. EUR closing difference 392.00 with review required. USD closing difference 0.00 with no detected exceptions; ready for human review. Both sample account roll-forwards and expected row counts passed.

The HTML dashboard is generated from these tested outputs. Its JavaScript was checked with a DOM test harness for rendering and filter behavior. A browser visual check could not be completed because the available Chromium launcher has no installed browser binary. Layout screenshots and real-browser compatibility are therefore still to be reviewed before using the dashboard in a client delivery. The Python reconciliation is independent of the HTML renderer.

No live bank connection, client data, live accounting posting, performance benchmark or native Power BI file was tested.
