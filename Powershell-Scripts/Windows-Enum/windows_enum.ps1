Write-Host ""
Write-Host "==============================="
Write-Host " Windows Enumeration Script"
Write-Host "==============================="
Write-Host ""

Write-Host "[+] Current User"
whoami

Write-Host ""
Write-Host "[+] Hostname"
hostname

Write-Host ""
Write-Host "[+] Operating System"
Get-CimInstance Win32_OperatingSystem |
Select-Object Caption, Version

Write-Host ""
Write-Host "[+] IP Addresses"
Get-NetIPAddress -AddressFamily IPv4 |
Select-Object IPAddress

Write-Host ""
Write-Host "[+] Local Administrators"

try {
    Get-LocalGroupMember Administrators
}
catch {
    Write-Host "Unable to enumerate local administrators."
}

Write-Host ""
Write-Host "[+] Running Processes"

Get-Process |
Sort-Object CPU -Descending |
Select-Object -First 10 Name, CPU

Write-Host ""
Write-Host "[+] Installed Software"

Get-ItemProperty `
HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* `
-ErrorAction SilentlyContinue |
Select-Object DisplayName |
Where-Object {$_.DisplayName}

Write-Host ""
Write-Host "[+] Enumeration Complete"
