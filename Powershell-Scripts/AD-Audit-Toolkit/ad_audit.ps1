Write-Host ""
Write-Host "================================="
Write-Host " Active Directory Audit Toolkit"
Write-Host "================================="
Write-Host ""

Import-Module ActiveDirectory -ErrorAction Stop

$ReportPath = "ad_audit_report.txt"

"=================================" | Out-File $ReportPath
" Active Directory Audit Report" | Out-File $ReportPath -Append
" Generated: $(Get-Date)" | Out-File $ReportPath -Append
"=================================" | Out-File $ReportPath -Append
"" | Out-File $ReportPath -Append

# Domain Admins

"Domain Admins" | Out-File $ReportPath -Append
"-------------" | Out-File $ReportPath -Append

$DomainAdmins = Get-ADGroupMember "Domain Admins" |
Select-Object -ExpandProperty Name

$DomainAdmins | Out-File $ReportPath -Append

"" | Out-File $ReportPath -Append

# Password Never Expires

"Password Never Expires" | Out-File $ReportPath -Append
"----------------------" | Out-File $ReportPath -Append

$NeverExpires = Get-ADUser `
-Filter {PasswordNeverExpires -eq $true} `
-Properties PasswordNeverExpires

$NeverExpires |
Select-Object Name |
Out-File $ReportPath -Append

"" | Out-File $ReportPath -Append

# Disabled Accounts

"Disabled Accounts" | Out-File $ReportPath -Append
"-----------------" | Out-File $ReportPath -Append

$DisabledUsers = Get-ADUser `
-Filter {Enabled -eq $false}

$DisabledUsers |
Select-Object Name |
Out-File $ReportPath -Append

"" | Out-File $ReportPath -Append

# Locked Accounts

"Locked Accounts" | Out-File $ReportPath -Append
"---------------" | Out-File $ReportPath -Append

$LockedUsers = Search-ADAccount `
-LockedOut

$LockedUsers |
Select-Object Name |
Out-File $ReportPath -Append

"" | Out-File $ReportPath -Append

# Statistics

$UserCount = (
    Get-ADUser -Filter *
).Count

$ComputerCount = (
    Get-ADComputer -Filter *
).Count

"Environment Statistics" | Out-File $ReportPath -Append
"----------------------" | Out-File $ReportPath -Append

"Total Users: $UserCount" |
Out-File $ReportPath -Append

"Total Computers: $ComputerCount" |
Out-File $ReportPath -Append

"" | Out-File $ReportPath -Append

Write-Host ""
Write-Host "[+] Report Generated"
Write-Host "[+] Saved as: $ReportPath"
Write-Host ""
