# Beginner entry point; never installs system software or runs as administrator.
[CmdletBinding()]
param(
    [ValidateSet('install', 'verify', 'uninstall')]
    [string] $Action = 'install',
    [ValidateSet('tr', 'en')]
    [string] $Language = 'tr',
    [switch] $NonInteractive
)

function Say([string] $Turkish, [string] $English) {
    if ($Language -eq 'en') { Write-Host $English } else { Write-Host $Turkish }
}

$root = Split-Path -Parent $PSScriptRoot
$state = Join-Path $root '.agentlab'
$systemName = if ($env:OS -eq 'Windows_NT') { 'Windows' } else { 'Unix' }

# Both launchers may otherwise offer or initiate installation when no runtime exists.
# These changes apply only to this process and are restored before the script exits.
$oldOutputEncoding = [Console]::OutputEncoding
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
$oldAgentLanguage = [Environment]::GetEnvironmentVariable('AGENTLAB_LANGUAGE', 'Process')
[Environment]::SetEnvironmentVariable('AGENTLAB_LANGUAGE', $Language, 'Process')
$oldAutoInstall = [Environment]::GetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', 'Process')
$oldLegacyInstall = [Environment]::GetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', 'Process')
[Environment]::SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', '0', 'Process')
[Environment]::SetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', $null, 'Process')
try {
    Say "Algılanan ortam: $systemName (PowerShell)." "Detected environment: $systemName (PowerShell)."
    if ($Action -eq 'uninstall') {
        $stateItem = Get-Item -Force -LiteralPath $state -ErrorAction SilentlyContinue
        if (-not (Test-Path -LiteralPath $state) -and $null -eq $stateItem) {
            Say 'Kaldırılacak AgentLab ortamı bulunmuyor.' 'There is no AgentLab environment to remove.'
            exit 0
        }
        Say "Otomatik kaldırma kapalı; hiçbir dosya silinmedi. $state klasörünü inceleyin, güvenliyse kendiniz kaldırın." "Automatic removal is disabled; no files were deleted. Inspect $state and remove it yourself only if safe."
        Say 'Sonra kurulumu veya kaldırmayı tekrar çalıştırabilirsiniz.' 'You can then rerun install or uninstall.'
        exit 1
    }
    $selected = $null
    $candidates = @(
        @{ Name = 'py'; Prefix = @('-3') },
        @{ Name = 'python3'; Prefix = @() },
        @{ Name = 'python'; Prefix = @() }
    )
    foreach ($candidate in $candidates) {
        $command = Get-Command $candidate.Name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $command) { continue }
        # The Windows Store python alias can open the Store even when no Python is installed.
        if ($candidate.Name -ne 'py' -and $command.Source -match '[\\/]WindowsApps[\\/]') { continue }
        try {
            & $command.Source @($candidate.Prefix) -B -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>$null
            if ($LASTEXITCODE -eq 0) {
                $selected = @{ Path = $command.Source; Prefix = @($candidate.Prefix) }
                break
            }
        } catch { continue }
    }

    if (-not $selected) {
        $url = 'https://www.python.org/downloads/windows/'
        Say 'Python 3.10 veya yenisi bulunamadı. Python kurulumunu kendiniz başlatmalısınız.' 'Python 3.10 or newer was not found. You must start Python installation yourself.'
        Say "Resmî kurulum sayfası: $url" "Official installation page: $url"
        Say 'Python kurulduktan sonra PowerShell penceresini kapatıp açın ve komutu yeniden çalıştırın.' 'After installing Python, restart PowerShell and run the command again.'
        Say 'Yalnızca Python Install Manager kurulduysa kurulum rehberindeki py install adımını inceleyin.' 'If only Python Install Manager was installed, review the py install step in the setup guide.'
        if (-not $NonInteractive) {
            if ($Language -eq 'en') { $answer = Read-Host 'Open the official page? [y/N]' }
            else { $answer = Read-Host 'Resmî sayfa açılsın mı? [e/H]' }
            if ($answer -match '^(?i:e|evet|y|yes)$') {
                try { Start-Process $url -ErrorAction Stop }
                catch { Say 'Tarayıcı açılamadı; bağlantıyı elle açın.' 'Could not open the browser; open the link manually.' }
            }
        }
        exit 2
    }

    if ($Action -eq 'install') {
        try {
            & $selected.Path @($selected.Prefix) -B -c 'import venv' 2>$null
            $hasVenv = ($LASTEXITCODE -eq 0)
        } catch { $hasVenv = $false }
        if (-not $hasVenv) {
            Say 'Python bulundu, ancak venv bileşeni kullanılamıyor. Python kurulumunuzu gözden geçirin.' 'Python was found, but venv is unavailable. Review your Python installation.'
            Say 'Script sistem paketi kurmaz; seçimi ve onayı siz verirsiniz.' 'The script does not install system packages; that choice and approval are yours.'
            exit 3
        }
    }

    & $selected.Path @($selected.Prefix) -X utf8 -B (Join-Path $root 'setup/manage.py') $Action
    $status = $LASTEXITCODE
    if ($status -eq 0 -and $Action -eq 'install') {
        & $selected.Path @($selected.Prefix) -X utf8 -B (Join-Path $root 'setup/manage.py') verify
        $status = $LASTEXITCODE
    }
    if ($status -ne 0) {
        Say 'İşlem durdu. Yukarıdaki ayrıntıları ve kurulum rehberini inceleyin.' 'The operation stopped. Review the details above and the setup guide.'
    }
    exit $status
} finally {
    [Console]::OutputEncoding = $oldOutputEncoding
    [Environment]::SetEnvironmentVariable('AGENTLAB_LANGUAGE', $oldAgentLanguage, 'Process')
    [Environment]::SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', $oldAutoInstall, 'Process')
    [Environment]::SetEnvironmentVariable('PYLAUNCHER_ALLOW_INSTALL', $oldLegacyInstall, 'Process')
}
