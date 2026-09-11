$ErrorActionPreference = "Stop"

$results = @()

function Add-Check {
    param(
        [string]$Name,
        [bool]$Available,
        [string]$Detail
    )
    $script:results += [pscustomobject]@{
        Name = $Name
        Available = $Available
        Detail = $Detail
    }
}

$uv = Get-Command uv -ErrorAction SilentlyContinue
Add-Check "uv" ($null -ne $uv) $(if ($uv) { (& uv --version) } else { "Install uv" })

$python = Get-Command python -ErrorAction SilentlyContinue
$pythonVersion = if ($python) { (& python --version 2>&1) }
$pythonAvailable = ($null -ne $python) -and ($LASTEXITCODE -eq 0)
Add-Check "Python" $pythonAvailable $(if ($pythonAvailable) { $pythonVersion } else { "Install Python 3 or let uv manage Python" })

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
Add-Check "ffmpeg" ($null -ne $ffmpeg) $(if ($ffmpeg) { (& ffmpeg -version | Select-Object -First 1) } else { "Install FFmpeg" })

$ffprobe = Get-Command ffprobe -ErrorAction SilentlyContinue
Add-Check "ffprobe" ($null -ne $ffprobe) $(if ($ffprobe) { (& ffprobe -version | Select-Object -First 1) } else { "Install FFmpeg tools" })

$chromeCandidates = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
Add-Check "Chrome" ($null -ne $chrome) $(if ($chrome) { $chrome } else { "Install Google Chrome or adjust the recorder executable" })

try {
    Add-Type -AssemblyName System.Speech
    $synth = [System.Speech.Synthesis.SpeechSynthesizer]::new()
    $voices = @($synth.GetInstalledVoices() | Where-Object Enabled | ForEach-Object VoiceInfo | ForEach-Object Name)
    $synth.Dispose()
    Add-Check "Windows narration voices" ($voices.Count -gt 0) ($voices -join ", ")
}
catch {
    Add-Check "Windows narration voices" $false $_.Exception.Message
}

$results | Format-Table -AutoSize
if ($results.Where({ -not $_.Available }).Count -gt 0) {
    exit 1
}
