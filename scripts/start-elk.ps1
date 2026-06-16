Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker compose --profile elk up -d
docker compose ps

Write-Host ""
Write-Host "Kibana: http://localhost:5601"
Write-Host "Elasticsearch: http://localhost:9200"
Write-Host "Run 'docker compose up -d telemetry-generator' to generate fresh application logs."
