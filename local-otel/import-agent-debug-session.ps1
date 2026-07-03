param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

# Windows equivalent of import-agent-debug-session.sh. Imports a VS Code Agent
# Debug Logs session export (OTLP JSON) into the local Frontier Cockpit stack,
# enriching it with the current Git workspace attribution so the session shows
# up grouped by workspace and is inspectable in the mini app's Inspector view.
#
# Usage:
#   pwsh -File local-otel/import-agent-debug-session.ps1 -Path exported-session.json
#
# Everything stays local: the file is posted to the local OTel Collector only.

$ErrorActionPreference = "Stop"

if (!(Test-Path $Path)) {
    Write-Error "File not found: $Path. Export the session from the VS Code Agent Debug Logs panel (Export icon) first."
    exit 2
}

function Get-Endpoint([string]$Name, [string]$Fallback) {
    $value = [Environment]::GetEnvironmentVariable($Name, "Process")
    if ([string]::IsNullOrWhiteSpace($value)) { return $Fallback }
    return $value
}

$TracesEndpoint = Get-Endpoint "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT" "http://localhost:4318/v1/traces"
$MetricsEndpoint = Get-Endpoint "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT" "http://localhost:4318/v1/metrics"
$LogsEndpoint = Get-Endpoint "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT" "http://localhost:4318/v1/logs"

$workspacePath = ""
$workspaceName = ""
$branch = ""
$remote = ""
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    $inside = & git rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -eq 0 -and $inside -eq "true") {
        $workspacePath = & git rev-parse --show-toplevel
        $workspaceName = Split-Path -Leaf $workspacePath
        $branch = (& git branch --show-current 2>$null)
        $remote = (& git config --get remote.origin.url 2>$null)
    }
}

$pathHash = ""
if ($workspacePath) {
    $hashBytes = [System.Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($workspacePath))
    $pathHash = -join ($hashBytes | ForEach-Object { $_.ToString('x2') })
}

function New-Attr([string]$Key, [string]$Value) {
    return @{ key = $Key; value = @{ stringValue = $Value } }
}

function Get-Enrichment {
    $attrs = @()
    if ($workspaceName) {
        $attrs += New-Attr "workspace.name" $workspaceName
        $attrs += New-Attr "workspace.kind" "git"
    }
    if ($pathHash) { $attrs += New-Attr "workspace.path_hash" $pathHash }
    if ($branch) { $attrs += New-Attr "git.branch" $branch }
    if ($remote) { $attrs += New-Attr "github.copilot.git.repository" $remote }
    $attrs += New-Attr "frontier.import.source" "vscode-agent-debug-export"
    return $attrs
}

$payload = Get-Content -Raw -Path $Path | ConvertFrom-Json -AsHashtable -Depth 100

$sections = @(
    @{ Key = "resourceSpans"; Endpoint = $TracesEndpoint },
    @{ Key = "resourceMetrics"; Endpoint = $MetricsEndpoint },
    @{ Key = "resourceLogs"; Endpoint = $LogsEndpoint }
)

$postedAny = $false
foreach ($section in $sections) {
    $items = $payload[$section.Key]
    if (!$items -or @($items).Count -eq 0) { continue }
    $items = @($items)
    foreach ($item in $items) {
        if (!$item.ContainsKey("resource")) { $item["resource"] = @{} }
        if (!$item["resource"].ContainsKey("attributes")) { $item["resource"]["attributes"] = @() }
        $existing = @($item["resource"]["attributes"] | ForEach-Object { $_["key"] })
        foreach ($attr in Get-Enrichment) {
            if ($existing -notcontains $attr["key"]) {
                $item["resource"]["attributes"] = @($item["resource"]["attributes"]) + @($attr)
            }
        }
    }
    # Post in batches so very large exports do not exceed collector limits.
    $batchSize = 50
    for ($start = 0; $start -lt $items.Count; $start += $batchSize) {
        $end = [Math]::Min($start + $batchSize, $items.Count) - 1
        $body = @{ $section.Key = @($items[$start..$end]) } | ConvertTo-Json -Depth 100 -Compress
        Invoke-RestMethod -Method Post -Uri $section.Endpoint -ContentType "application/json" -Body $body | Out-Null
    }
    Write-Host "Imported $($items.Count) $($section.Key) batch(es) to $($section.Endpoint)"
    $postedAny = $true
}

if (!$postedAny) {
    Write-Error "The file contains no resourceSpans, resourceMetrics, or resourceLogs. Is this an Agent Debug Logs OTLP export?"
    exit 1
}

if ($workspaceName) {
    Write-Host "Attributed to workspace $workspaceName (branch $(if ($branch) { $branch } else { 'unknown' }))."
}
else {
    Write-Host "No Git workspace detected; the session was imported without workspace attribution. Run from inside the project repository to attribute it."
}
Write-Host "The session lands in local Tempo/Prometheus. It appears in the mini app after the next materializer pass (up to 5 minutes) and is inspectable in the Inspector view via its trace id."
