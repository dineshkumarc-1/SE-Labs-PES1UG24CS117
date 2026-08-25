# Software Engineering Laboratory (UE23CS352A)

**PES University, Department of Computer Science & Engineering**

---

### Student Details
- **Name:** C Dinesh Kumar
- **SRN:** PES1UG24CS117
- **Section:** 5B
- **Course:** Software Engineering Lab (UE23CS352A)

---

## Lab Index

| Lab | Topic / Title | Deliverables | Status |
| :---: | :--- | :--- | :---: |
| **Lab 1** | **Requirements Engineering & UML Use-Case Modelling** | [Lab-1 Folder](Lab-1/) &bull; [PDF Report](Lab-1/PES1UG24CS117_Lab1_Report.pdf) | `Completed` |

---

# Lab 1: Community Solar Credit Allocation Manager

## 1. Problem Statement & Context
A clean energy sharing portal ingesting rooftop solar generation metrics, facilitating peer-to-peer solar credit transfers within a neighborhood microgrid, and tracking monthly utility billing offsets.

- **Primary Stakeholders & Actors:** Prosumer Resident (Co-op Member), Co-op Manager, Smart Meter System, External Utility / Billing System.
- **Goal:** Provide a dependable, transparent accounting and allocation platform for residential microgrids.

---

## 2. Requirements Traceability Table

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **FR-001** | Functional | The system shall record solar generation units (kWh) from smart meter feeds and allow prosumers to transfer surplus credits to neighbor accounts. | **High** | **Pass:** Transferred credits deduct from the prosumer balance and apply to the neighbor billing statement.<br>**Fail:** Transfer exceeding balance. | Enables accurate recording of solar generation and sharing of surplus solar credits. |
| **FR-002** | Functional | The system shall allow prosumer residents to view their available solar credit balance and transaction history. | **High** | **Pass:** The system displays the current credit balance and previous transactions.<br>**Fail:** Incorrect or unavailable balance information is displayed. | Allows prosumers to monitor their available credits and previous transactions. |
| **FR-003** | Functional | The system shall verify that a recipient account is eligible to receive transferred solar credits before completing a credit transfer. | **High** | **Pass:** A transfer proceeds only when the recipient account is valid and eligible.<br>**Fail:** The system rejects transfers to invalid or ineligible recipient accounts. | Prevents credits from being transferred to unauthorized or ineligible community accounts. |
| **FR-004** | Functional | The system shall track monthly utility billing offsets resulting from allocated solar credits. | **High** | **Pass:** The system records and displays the correct billing offset based on allocated solar credits.<br>**Fail:** The displayed billing offset does not reflect the allocated credits. | Enables tracking of the financial benefit obtained through solar credit allocation. |
| **FR-005** | Functional | The system shall allow the Co-op Manager to generate reports on solar generation, credit allocations, and billing offsets. | **Medium** | **Pass:** The Co-op Manager can generate reports containing solar generation, credit allocation, and billing offset information.<br>**Fail:** Required information is missing or inaccurate. | Helps the Co-op Manager monitor and manage community solar activities. |
| **NFR-001** | Performance & Security | The smart meter telemetry processing pipeline must validate and store hourly generation data for 500 households with 99.9% uptime. | **High** | **Pass:** Benchmarking tests confirm the required latency and security standards under simulated peak load.<br>**Fail:** The system fails to meet the required performance or uptime. | Ensures reliable processing of solar generation data at the required scale. |
| **NFR-002** | Non-functional / Security | The system shall ensure that only authorized users can access solar generation, credit, and billing information and perform credit allocation operations. | **High** | **Pass:** All tested unauthorized access attempts to protected information and credit allocation operations are denied.<br>**Fail:** Any unauthorized user can access protected information or perform a restricted operation. | Protects user data and prevents unauthorized credit transactions. |

---

## 3. UML Use-Case Model

### Actors
1. **Prosumer Resident (Co-op Member):** Primary actor who views solar credit balance, monitors history, submits meter generation data, and initiates credit transfers to neighbors.
2. **Co-op Manager:** Administrative actor who monitors cooperative activities, oversees user accounts, and generates aggregate reports.
3. **Smart Meter System:** Telemetry actor automatically transmitting hourly solar generation data.
4. **External System (Utility / Billing):** External integration partner responsible for applying solar offsets to monthly consumer utility statements.

### Use-Case Diagram
![UML Use-Case Diagram](Lab-1/use_case_diagram.png)

### Key Stereotypes
- **`«include»` Relationships:**
  - `Transfer Solar Credits` $\rightarrow$ `Validate Credit Balance`
  - `Transfer Solar Credits` $\rightarrow$ `Verify Recipient Eligibility`
  - `Transfer Solar Credits` $\rightarrow$ `Record Credit Transaction`
- **`«extend»` Relationship:**
  - `Generate Monthly Billing Statement` $\xrightarrow{\text{«extend»}}$ `View Billing Offset & Statements`

---

## 4. Use-Case Flow Specification (`UC-03`)

### Use Case: Transfer Solar Credits
- **Use Case ID:** `UC-03`
- **Primary Actor:** Prosumer Resident
- **Supporting System:** Community Solar Credit Allocation Manager
- **Goal:** Transfer available solar credits from the prosumer's balance to an eligible neighbor's account.

#### Preconditions
1. The Prosumer Resident must be registered and authenticated in the system.
2. The Prosumer Resident must have an active positive solar credit balance.
3. The recipient account identifier must be provided by the sender.
4. The requested transfer amount must be greater than zero.

#### Postconditions
1. The transferred solar credit units are deducted from the sender's balance.
2. The transferred credits are credited to the recipient's account.
3. The credit transfer transaction is logged with a unique transaction reference and timestamp.
4. The recipient's next billing statement reflects the transferred offset credits.
5. A success confirmation receipt is displayed to the sender.

#### Main Success Scenario (MSS)
1. The Prosumer Resident navigates to and selects **Transfer Solar Credits**.
2. The system retrieves and displays the prosumer's current credit balance.
3. The Prosumer Resident enters the recipient account ID and the quantity of credits to transfer.
4. The system validates that the recipient account exists and is eligible to receive credits.
5. The system verifies that the sender has sufficient available balance (`balance >= requested_credits`).
6. The system deducts the specified solar credits from the sender's account.
7. The system applies the transferred credits to the recipient's account.
8. The system records and persists the transaction in the ledger.
9. The system updates the billing statement record for the recipient.
10. The system displays a transfer confirmation message with transaction summary details.

#### Alternate Flow: Insufficient Credit Balance (A1)
1. **At Step 5:** The system identifies that the requested transfer amount exceeds the prosumer's available balance.
2. The system rejects the transfer request.
3. The system displays an **"Insufficient Credit Balance"** error prompt.
4. No credit balance is deducted from the sender.
5. No credits are added to the recipient.
6. The transaction is aborted without recording a completed transfer.

---

## 5. Lab 1 Deliverables Summary

All deliverables for Lab 1 are available directly inside the [`Lab-1/`](Lab-1/) directory:

| Deliverable | File Link | Description |
| :--- | :--- | :--- |
| **Consolidated PDF Report** | [`PES1UG24CS117_Lab1_Report.pdf`](Lab-1/PES1UG24CS117_Lab1_Report.pdf) | Formal compiled 3-page submission report |
| **Requirements Table (Word)** | [`Requirements_Traceability_Table.docx`](Lab-1/Requirements_Traceability_Table.docx) | Full editable requirements document (`.docx`) |
| **Requirements Table (Excel)** | [`Requirements_Table.xlsx`](Lab-1/Requirements_Table.xlsx) | Structured spreadsheet version (`.xlsx`) |
| **UML Diagram (Vector PDF)** | [`use_case_diagram.pdf`](Lab-1/use_case_diagram.pdf) | High-definition vector PDF diagram |
| **UML Diagram (Image)** | [`use_case_diagram.png`](Lab-1/use_case_diagram.png) | High-resolution PNG image |
| **Use-Case Flow Document** | [`UseCase_Flow_Specification_UC03.docx`](Lab-1/UseCase_Flow_Specification_UC03.docx) | 1-page Word document for `UC-03` |
