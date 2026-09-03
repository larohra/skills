param(
    [Parameter(Mandatory = $true)]
    [string]$Manifest,

    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Speech

$document = Get-Content $Manifest -Raw | ConvertFrom-Json
$voice = if ($document.voice) { [string]$document.voice } else { "Microsoft Mark" }
$rate = if ($null -ne $document.rate) { [int]$document.rate } else { 0 }
$volume = if ($null -ne $document.volume) { [int]$document.volume } else { 100 }

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$probe = Get-Command ffprobe -ErrorAction SilentlyContinue
$results = @()
foreach ($segment in $document.segments) {
    $id = [string]$segment.id
    $text = [string]$segment.text
    if (-not $id -or -not $text) {
        throw "Each narration segment requires non-empty id and text."
    }
    $path = Join-Path $OutputDirectory ("narration-{0}.wav" -f $id)
    $synth = [System.Speech.Synthesis.SpeechSynthesizer]::new()
    try {
        $synth.SelectVoice($voice)
        $synth.Rate = $rate
        $synth.Volume = $volume
        $synth.SetOutputToWaveFile($path)
        $synth.Speak($text)
    }
    finally {
        $synth.Dispose()
    }
    $duration = $null
    if ($probe) {
        $duration = [math]::Round(
            [double](& ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 $path),
            2
        )
    }
    $results += [pscustomobject]@{
        Id = $id
        Path = $path
        DurationSeconds = $duration
    }
}

$results | ConvertTo-Json -Depth 4
