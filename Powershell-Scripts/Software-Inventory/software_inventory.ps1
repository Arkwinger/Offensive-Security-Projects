Write-Host ""
Write-Host "==============================="
Write-Host " Software Inventory"
Write-Host "==============================="
Write-Host ""

$software = Get-ItemProperty `
HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* `
-ErrorAction SilentlyContinue |
Where-Object {$_.DisplayName} |
Select-Object DisplayName, DisplayVersion

$software |
Sort-Object DisplayName |
Format-Table -AutoSize

Write-Host ""
Write-Host "[+] Total Applications Found: $($software.Count)"
