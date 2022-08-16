# Automated Login Scripts to Keep Accounts Active

## Objective

Cloud service providers have been known to delete the contents of personal accounts or 
close the accounts themselves after a period of inactivity, sometimes without the end-user's knowledge.
This project aims to prevent that from happening by automating logins at regular intervals.

Each login process is recorded in a csv log file. 
Because it contains personally identifiable information, this log file is saved to a private repository.

## Process Workflow and Code Organisation

```mermaid
flowchart LR
    A([login-platform-auto.yml]) -->|Call workflow| B([reusable-autolog.yml])
    F[[Run keep-platform-active.py]] 
    F ==>|output|G[("[Year] platform_account log.csv"<br/><em>Private Repository</em>)]
    B -->|login job| F
    B -.->|schedule-maintenance job| C{{Login and Logging Successful?}}
    C ==>|Yes| D[[Run reset-schedule.py]]
    C ==>|No| E[[Run reschedule-next-run.py]]
    D -->|next run back at usual time tomorrow| A
    E -->|next run in one hour| A
    
  ```
