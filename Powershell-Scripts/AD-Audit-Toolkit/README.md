# AD Audit Toolkit

A PowerShell-based Active Directory auditing utility designed to collect and summarize common security and administrative information from a Windows domain environment.

The script performs a series of basic Active Directory checks and generates a consolidated report that can be reviewed during lab exercises, security assessments, and environment reviews.

## Features

* Domain Admin enumeration
* Password Never Expires account discovery
* Disabled account enumeration
* Locked account discovery
* User and computer statistics
* Automated report generation

## Requirements

* Windows PowerShell
* Active Directory PowerShell Module
* Appropriate permissions to query Active Directory

## Usage

Run the script from PowerShell:

```powershell
.\ad_audit.ps1
```

A report will be generated in the current directory:

```text
ad_audit_report.txt
```

## Example Findings

```text
Domain Admins
-------------
Administrator
svc_backup

Password Never Expires
----------------------
svc_sql

Disabled Accounts
-----------------
testuser

Environment Statistics
----------------------
Total Users: 215
Total Computers: 178
```

## Disclaimer

This project is intended for educational purposes, lab environments, and authorized security assessments only.
