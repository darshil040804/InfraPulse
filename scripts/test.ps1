Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker compose run --rm `
  -e DATABASE_URL=postgresql+psycopg://infrapulse:infrapulse_password@postgres:5432/infrapulse `
  -e ENABLE_KAFKA_CONSUMER=false `
  backend python -m pytest -vv

Push-Location frontend
try {
  npm audit --audit-level=moderate
  npm run build
}
finally {
  Pop-Location
}

docker compose config --quiet
