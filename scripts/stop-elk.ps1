Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker compose --profile elk stop logstash kibana elasticsearch
