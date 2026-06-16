param(
  [switch]$ResumeTelemetry
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker compose up -d postgres kafka backend
docker compose stop telemetry-generator | Out-Null
docker compose exec backend python -m app.scripts.reset_demo

if ($ResumeTelemetry) {
  docker compose up -d telemetry-generator
  Write-Host "Demo data reset. Telemetry generator restarted."
}
else {
  Write-Host "Demo data reset. Telemetry generator is stopped so screenshots remain deterministic."
  Write-Host "Run 'docker compose up -d telemetry-generator' to resume live data."
}
