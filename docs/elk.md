# ELK Logging Layer

InfraPulse includes an optional ELK stack for local log search and visualization.

## What It Adds

- Elasticsearch stores indexed log documents.
- Logstash consumes JSON events from the Kafka-compatible `application-logs` topic.
- Kibana provides a browser UI for searching and visualizing logs.

The default Docker Compose stack does not start ELK because it is heavier than the core demo. Use the `elk` profile when you want centralized log analytics.

## Start ELK

```powershell
.\scripts\start-elk.ps1
```

Or run the equivalent Docker Compose command:

```powershell
docker compose --profile elk up -d
```

Open:

- Kibana: http://localhost:5601
- Elasticsearch: http://localhost:9200

## Generate Logs

If the telemetry generator was stopped for deterministic screenshots, restart it:

```powershell
docker compose up -d telemetry-generator
```

The telemetry generator publishes application log events to Kafka. Logstash reads those events and writes them to Elasticsearch indexes named:

```text
infrapulse-logs-YYYY.MM.DD
```

## View Logs In Kibana

1. Open http://localhost:5601.
2. Go to Discover.
3. Create a data view for:

   ```text
   infrapulse-logs-*
   ```

4. Use `@timestamp` as the time field.
5. Search fields such as:
   - `service`
   - `level`
   - `message`
   - `device_id`
   - `pipeline`
   - `environment`

## Stop ELK

```powershell
.\scripts\stop-elk.ps1
```

To remove ELK data as well:

```powershell
docker compose --profile elk down -v
```

Only use `down -v` if you are okay deleting all local Compose volumes, including PostgreSQL and Elasticsearch data.
