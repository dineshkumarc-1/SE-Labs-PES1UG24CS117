# Use-Case Flow Specification

**Course:** Software Engineering  
**Lab:** Lab 1  
**Name:** C Dinesh Kumar  
**SRN:** PES1UG24CS117  
**Section:** 5B  

---

## Use Case: Transfer Solar Credits

| Attribute | Details |
| :--- | :--- |
| **Use Case ID** | `UC-03` |
| **Use Case Name** | Transfer Solar Credits |
| **Primary Actor** | Prosumer Resident (Co-op Member) |
| **Supporting System** | Community Solar Credit Allocation Manager |
| **Goal** | Transfer available solar credits from the prosumer's account to an eligible neighbor's account. |

---

### Preconditions
1. The Prosumer Resident must be registered and logged into the system.
2. The Prosumer Resident must have available solar credits in their account.
3. The recipient account must be provided by the Prosumer Resident.
4. The requested transfer amount must be greater than zero.

---

### Postconditions
1. The transferred credits are deducted from the sender's credit balance.
2. The transferred credits are added to the recipient's account.
3. The credit transfer transaction is recorded in the system.
4. The recipient's billing statement is updated with the transferred credits.
5. A transfer confirmation is displayed to the Prosumer Resident.

---

### Main Success Scenario (MSS)
1. The Prosumer Resident selects **Transfer Solar Credits**.
2. The system displays the prosumer's available credit balance.
3. The Prosumer Resident enters the recipient account and the amount of solar credits to transfer.
4. The system verifies that the recipient account is valid and eligible to receive credits.
5. The system checks whether the prosumer has sufficient available credits.
6. The system deducts the specified credits from the sender's balance.
7. The system applies the transferred credits to the recipient's account.
8. The system records the credit transfer transaction.
9. The system updates the recipient's billing statement.
10. The system displays a successful transfer confirmation to the Prosumer Resident.

---

### Alternate Flow – Insufficient Credit Balance (A1)
1. **At Step 5**, the system determines that the requested transfer amount exceeds the prosumer's available credit balance.
2. The system rejects the transfer request.
3. The system displays an **Insufficient Credit Balance** error message.
4. No credits are deducted from the sender's account.
5. No credits are added to the recipient's account.
6. The transaction is not recorded as a successful transfer.
