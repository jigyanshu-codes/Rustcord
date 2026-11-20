<#
.SYNOPSIS
Installs or uninstalls Serein for the current Windows user without elevation.
Preserves write permissions for seamless in-app autoupdates.
#>
param(
    [switch]$Uninstall,
    [switch]$Quiet
)

$ErrorActionPreference = 'Stop'
$appName = 'RustCord'
$publisher = 'RustCord contributors'
$website = 'https://github.com/jigyanshu-codes/Rustcord'
$installDir = Join-Path $env:LOCALAPPDATA "Programs\$appName"
$uninstallKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$appName"
$shortcut = Join-Path ([Environment]::GetFolderPath('Programs')) "$appName.lnk"

# Check if RustCord is currently running
$running = Get-Process rustcord, serein -ErrorAction SilentlyContinue
if ($running) {
    if ($Quiet) {
        $running | Stop-Process -Force
    } else {
        throw "RustCord is currently running. Please close RustCord before running setup."
    }
}

if ($Uninstall) {
    if (Test-Path -LiteralPath $shortcut) {
        Remove-Item -LiteralPath $shortcut -Force
    }
    if (Test-Path -LiteralPath $uninstallKey) {
        Remove-Item -LiteralPath $uninstallKey -Recurse -Force
    }
    $runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
    if ((Get-ItemProperty -LiteralPath $runKey -Name $appName -ErrorAction SilentlyContinue)) {
        Remove-ItemProperty -LiteralPath $runKey -Name $appName -Force
    }
    if (Test-Path -LiteralPath $installDir) {
        Remove-Item -LiteralPath $installDir -Recurse -Force
    }
    if (!$Quiet) {
        Write-Host "RustCord was successfully uninstalled."
    }
    return
}

# Install
$distDir = $PSScriptRoot
$executable = Join-Path $distDir 'rustcord.exe'
if (!(Test-Path -LiteralPath $executable)) {
    $executable = Join-Path $distDir 'serein.exe'
}
if (!(Test-Path -LiteralPath $executable)) {
    $candidate = Join-Path (Join-Path $distDir '..\..\dist') 'rustcord.exe'
    if (!(Test-Path -LiteralPath $candidate)) {
        $candidate = Join-Path (Join-Path $distDir '..\..\dist') 'serein.exe'
    }
    if (Test-Path -LiteralPath $candidate) {
        $distDir = (Resolve-Path (Join-Path $distDir '..\..\dist')).Path
        $executable = $candidate
    } else {
        throw "rustcord.exe not found in $distDir. Run this script from the release package directory or build the project first."
    }
}

[IO.Directory]::CreateDirectory($installDir) | Out-Null

# Copy payload
Copy-Item -Path "$distDir\*" -Destination $installDir -Recurse -Force
if ($PSCommandPath -and (Test-Path -LiteralPath $PSCommandPath)) {
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $installDir 'setup.ps1') -Force
}

# Create Start Menu shortcut with AUMID
$notificationScript = Join-Path $installDir 'install-notifications.ps1'
if (Test-Path -LiteralPath $notificationScript) {
    & $notificationScript -Force
}

# Determine version
$version = '0.1.0'
$installedExe = if (Test-Path -LiteralPath (Join-Path $installDir 'rustcord.exe')) { 'rustcord.exe' } else { 'serein.exe' }
try {
    $versionInfo = (Get-Item -LiteralPath (Join-Path $installDir $installedExe)).VersionInfo.ProductVersion
    if ($versionInfo) { $version = $versionInfo }
} catch {}

# Register in Windows Add/Remove Programs
if (!(Test-Path -LiteralPath $uninstallKey)) {
    New-Item -Path $uninstallKey -Force | Out-Null
}

$uninstallCmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$installDir\setup.ps1`" -Uninstall"
Set-ItemProperty -LiteralPath $uninstallKey -Name 'DisplayName' -Value $appName
Set-ItemProperty -LiteralPath $uninstallKey -Name 'DisplayVersion' -Value $version
Set-ItemProperty -LiteralPath $uninstallKey -Name 'Publisher' -Value $publisher
Set-ItemProperty -LiteralPath $uninstallKey -Name 'DisplayIcon' -Value "$installDir\$installedExe,0"
Set-ItemProperty -LiteralPath $uninstallKey -Name 'InstallLocation' -Value $installDir
Set-ItemProperty -LiteralPath $uninstallKey -Name 'UninstallString' -Value $uninstallCmd
Set-ItemProperty -LiteralPath $uninstallKey -Name 'QuietUninstallString' -Value "$uninstallCmd -Quiet"
Set-ItemProperty -LiteralPath $uninstallKey -Name 'URLInfoAbout' -Value $website
Set-ItemProperty -LiteralPath $uninstallKey -Name 'NoModify' -Value 1 -Type DWord
Set-ItemProperty -LiteralPath $uninstallKey -Name 'NoRepair' -Value 1 -Type DWord

if (!$Quiet) {
    Write-Host "RustCord $version installed successfully to $installDir"
}
