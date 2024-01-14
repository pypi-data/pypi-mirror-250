mds-cashbook-report
===================
Tryton module to add reports to cashbook.

Install
=======

pip install mds-cashbook-report

Requires
========
- Tryton 6.0

Info
====
Module cashbook_report adds the following evaluations:
- account balance as amount,
- price difference according to stock exchange price as amount,
- exchange rate difference in percent,
- current value according to stock exchange price,
- total yield

The displayed data is selected according to cash books,
types of cash books and cash books by category.
The presentation can be done as pie, bar and line chart.
For each evaluation, a dashboard view is also created,
so that you can display several evaluations at the same time.

Changes
=======

*6.0.10 - 13.01.2024*

- add: multiple data sources in evaluations

*6.0.9 - 10.12.2023*

- fix: selection of lines in dashboard-view

*6.0.8 - 06.12.2023*

- optimized code

*6.0.7 - 11.03.2023*

- add: type of evaluation 'total yield' for cashbook/type/category

*6.0.6 - 06.02.2023*

- add: profit/loss-values for btype-selection of cashbooks

*6.0.5 - 06.02.2023*

- fix: values on non-asset-cashbooks

*6.0.4 - 05.02.2023*

- add: investment to evaluation-types

*6.0.3 - 08.11.2022*

- add: cashbook-categories for evaluation
- updt: optimized update of evaluation with existing dashboard-actions
- updt: limit bookings in evaluation-result to today

*6.0.2 - 05.11.2022*

- evaluation-line: permissions optimized
- evaluation: sorting by sequence

*6.0.1 - 05.11.2022*

- works

*6.0.0 - 28.10.2022*

- init
