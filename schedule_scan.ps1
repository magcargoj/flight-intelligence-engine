# Nomad Flight Intelligence - Automation Script
# Use this script to set up a Windows Scheduled Task

$PythonPath = "python" # Change this to your full python.exe path if needed
$ProjectDir = "C:\Users\jerem\.gemini\antigravity\scratch"
$ScriptPath = "nomad_flight_finder.main"

Write-Host "Running Daily Flight Scan..." -ForegroundColor Cyan

Set-Location $ProjectDir
& $PythonPath -m $ScriptPath

Write-Host "Scan Complete." -ForegroundColor Green
