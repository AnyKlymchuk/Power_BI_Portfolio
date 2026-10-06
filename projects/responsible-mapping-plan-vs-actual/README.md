# Responsible Mapping – Plan vs Actual

## Project goal
Create one clear mapping for responsible persons and use the same logic for Plan and Actual data.

## Problem
The report used the current responsible person for a doctor or counterparty.

There was no history for responsible persons. If the responsible person changed, old sales could also show the new person. For example, sales from 2024 could be changed to the person who is responsible today.

## Solution
I created a separate dataflow called `DF_ResponsibleMapping`.

The mapping keeps the fields needed to define the responsible person:

- Doctor
- Doctor Responsible
- Counterparty ID
- Counterparty
- Counterparty Responsible
- Branch
- Project

The final responsible person can depend on the doctor, counterparty, branch, project, and business exception rules.

## Historical tracking
The next part of the model is historical tracking with fields such as:

- `ValidFrom`
- `ValidTo`
- `IsCurrent`
- `FinalResponsible`

This will allow old sales to stay connected to the person who was responsible at that time.

Example: a sale from 2024 should stay with the person who was responsible in 2024, even if another person is responsible today.

This design can be developed into an **SCD Type 2** model.

## Model idea

```text
DF_ResponsibleMapping
        |
        v
Dim_Responsible
      /      \
     v        v
Fact Sales   Fact Plan
```

## Current stage
The dataflow for the mapping layer is created. It selects and cleans the fields needed for the responsibility rules and removes duplicate combinations.

The historical logic and final responsibility rule are the next steps.

## STAR interview answer

### Situation
We had no history for responsible persons. The report always used the current responsible person. Old sales could change when the responsible person changed.

### Task
I needed to create a separate mapping table and use the same logic for Plan and Actual data.

### Action
I created `DF_ResponsibleMapping`. I added doctor, counterparty, branch, project, and responsible-person fields. I prepared the structure for historical tracking with `ValidFrom`, `ValidTo`, `IsCurrent`, and `FinalResponsible`.

### Result
Old sales can stay connected to the person who was responsible at that time. The mapping can also be reused for Plan and Actual reports.

## Tools
- Power BI
- Power Query
- Dataflows
- Dimensional modeling
- SCD Type 2 design
