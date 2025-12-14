# Beta Infrastructure Setup Guide

**Date:** December 13, 2025
**Purpose:** Deploy HUMMBL beta environment with SY19 production capabilities, user authentication, and monitoring systems.

## Prerequisites

- GCP Project with Vertex AI enabled
- Domain name for beta.hummbl.dev
- SSL certificate
- Docker and Kubernetes cluster
- Monitoring tools (DataDog or similar)

## Architecture Overview

```
User → Cloud Load Balancer → API Gateway → App Engine
                                      ↓
                                Cloud SQL (PostgreSQL)
                                      ↓
                            Vertex AI (SY19 Models)
                                      ↓
                         Cloud Storage (Logs/Backups)
```

## Deployment Steps

### 1. GCP Project Setup

```bash
# Create GCP project
gcloud projects create hummbl-beta-2025

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable logging.googleapis.com

# Set project
gcloud config set project hummbl-beta-2025
```

### 2. Database Setup

```bash
# Create Cloud SQL instance
gcloud sql instances create hummbl-beta-db \
  --database-version=POSTGRES_15 \
  --cpu=2 \
  --memory=4GB \
  --region=us-central1

# Create database
gcloud sql databases create hummbl_beta --instance=hummbl-beta-db

# Create user
gcloud sql users create beta_user \
  --instance=hummbl-beta-db \
  --password=$(openssl rand -base64 12)
```

### 3. Vertex AI Setup

```bash
# Create Vertex AI endpoint
gcloud ai endpoints create hummbl-sy19-endpoint \
  --display-name="HUMMBL SY19 Recommender" \
  --region=us-central1

# Deploy SY19 model
gcloud ai models upload \
  --region=us-central1 \
  --display-name=hummbl-sy19-v1 \
  --container-image-uri=gcr.io/hummbl-beta-2025/sy19-model:latest \
  --model-id=sy19-v1
```

### 4. Application Deployment

```bash
# Build and push container
docker build -t gcr.io/hummbl-beta-2025/hummbl-beta:latest .
docker push gcr.io/hummbl-beta-2025/hummbl-beta:latest

# Deploy to Cloud Run
gcloud run deploy hummbl-beta \
  --image=gcr.io/hummbl-beta-2025/hummbl-beta:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DATABASE_URL=postgresql://beta_user:password@db-host/hummbl_beta" \
  --set-env-vars="VERTEX_AI_PROJECT=hummbl-beta-2025" \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=hummbl-beta-2025"
```

### 5. Authentication Setup

```bash
# Enable Identity Platform
gcloud services enable identitytoolkit.googleapis.com

# Configure OAuth providers
gcloud identitytoolkit config update \
  --project=hummbl-beta-2025 \
  --oauth-client-id=your-oauth-client-id \
  --oauth-client-secret=your-oauth-client-secret

# Set up custom domain
gcloud identitytoolkit config update \
  --project=hummbl-beta-2025 \
  --custom-domain=beta.hummbl.dev
```

### 6. Monitoring Setup

```bash
# Create monitoring dashboard
gcloud monitoring dashboards create hummbl-beta-dashboard \
  --config-from-file=dashboard-config.json

# Set up alerts
gcloud alpha monitoring policies create hummbl-beta-alerts \
  --policy-from-file=alerts-config.json

# Enable logging
gcloud logging sinks create hummbl-beta-logs \
  storage.googleapis.com/hummbl-beta-logs \
  --log-filter='resource.type="cloud_run_revision" AND resource.labels.service_name="hummbl-beta"'
```

## Configuration Files

### dashboard-config.json
```json
{
  "displayName": "HUMMBL Beta Dashboard",
  "gridLayout": {
    "widgets": [
      {
        "title": "API Response Time",
        "xyChart": {
          "dataSets": [{
            "timeSeriesQuery": {
              "timeSeriesFilter": {
                "filter": "metric.type=\"run.googleapis.com/request_latencies\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"hummbl-beta\"",
                "aggregator": "AGGREGATE_PERCENTILE_95"
              }
            }
          }]
        }
      },
      {
        "title": "Active Users",
        "xyChart": {
          "dataSets": [{
            "timeSeriesQuery": {
              "timeSeriesFilter": {
                "filter": "metric.type=\"custom.googleapis.com/active_users\"",
                "aggregator": "AGGREGATE_COUNT"
              }
            }
          }]
        }
      }
    ]
  }
}
```

### alerts-config.json
```json
{
  "displayName": "HUMMBL Beta Alerts",
  "conditions": [
    {
      "displayName": "High Error Rate",
      "conditionThreshold": {
        "filter": "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"hummbl-beta\"",
        "aggregator": "AGGREGATE_COUNT",
        "comparison": "COMPARISON_GT",
        "thresholdValue": 0.05,
        "duration": "300s"
      }
    },
    {
      "displayName": "Slow Response Time",
      "conditionThreshold": {
        "filter": "metric.type=\"run.googleapis.com/request_latencies\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"hummbl-beta\"",
        "aggregator": "AGGREGATE_PERCENTILE_95",
        "comparison": "COMPARISON_GT",
        "thresholdValue": 5000,
        "duration": "300s"
      }
    }
  ]
}
```

## Security Configuration

### Firewall Rules
```bash
# Allow Cloud Run access to Cloud SQL
gcloud sql instances patch hummbl-beta-db \
  --authorized-networks=$(gcloud run services describe hummbl-beta --region=us-central1 --format="value(status.url)" | sed 's|https://||;s|/.*||')/32

# Set up VPC for secure communication
gcloud compute networks create hummbl-beta-vpc --subnet-mode=custom
gcloud compute networks subnets create hummbl-beta-subnet \
  --network=hummbl-beta-vpc \
  --region=us-central1 \
  --range=10.0.0.0/24
```

### Secrets Management
```bash
# Create secret for database password
echo -n "database-password" | gcloud secrets create hummbl-db-password --data-file=-

# Create secret for API keys
echo -n "vertex-ai-key" | gcloud secrets create hummbl-vertex-key --data-file=-
```

## Testing Deployment

### Health Checks
```bash
# Test API endpoint
curl -X GET "https://hummbl-beta-[hash]-uc.a.run.app/health"

# Test SY19 recommendation
curl -X POST "https://hummbl-beta-[hash]-uc.a.run.app/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{"problem": "test problem", "detail_level": "medium"}'

# Test authentication
curl -X GET "https://hummbl-beta-[hash]-uc.a.run.app/api/user" \
  -H "Authorization: Bearer [token]"
```

### Load Testing
```bash
# Install hey for load testing
go install github.com/rakyll/hey@latest

# Run load test
hey -n 1000 -c 10 https://hummbl-beta-[hash]-uc.a.run.app/api/recommend
```

## Rollback Procedures

### Emergency Rollback
```bash
# Rollback to previous version
gcloud run revisions list --service=hummbl-beta --region=us-central1
gcloud run services update-traffic hummbl-beta \
  --to-revisions=[previous-revision]=100 \
  --region=us-central1
```

### Data Rollback
```bash
# Restore from backup
gcloud sql backups list --instance=hummbl-beta-db
gcloud sql backups restore [backup-id] --restore-instance=hummbl-beta-db
```

## Monitoring and Maintenance

### Daily Checks
- [ ] API response times <2 seconds
- [ ] Error rate <1%
- [ ] Database connections healthy
- [ ] Vertex AI endpoints responding

### Weekly Maintenance
- [ ] Update dependencies
- [ ] Review logs for anomalies
- [ ] Backup verification
- [ ] Performance optimization

### Monthly Reviews
- [ ] Cost analysis
- [ ] User growth metrics
- [ ] Feature usage analytics
- [ ] Security audit

This setup provides a production-ready beta environment supporting 100+ concurrent users with full SY19 capabilities, authentication, and comprehensive monitoring.