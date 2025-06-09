# 🔌 API DOCUMENTATION - ChaosGenius Empire

## 🌩️💜 BROSKI ULTRA SERVER API REFERENCE

Complete API documentation for the ChaosGenius Empire ecosystem.

## 🎯 Base Configuration

- **Base URL**: `http://your-domain:8080/api/v1`
- **Authentication**: Bearer Token / API Key
- **Content-Type**: `application/json`
- **Rate Limit**: 1000 requests/hour per API key

## 🔐 Authentication

### API Key Authentication

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://your-domain:8080/api/v1/status
```

### Token Configuration

```json
{
  "headers": {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
    "X-API-Version": "1.0"
  }
}
```

## 🤖 Agent Army Endpoints

### GET /api/v1/agents

Get all deployed agents status

```bash
curl -X GET "http://localhost:8080/api/v1/agents" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "status": "success",
  "agents": [
    {
      "id": "code_quality_agent",
      "name": "CodeQualityAgent",
      "status": "active",
      "last_run": "2025-06-09T10:30:00Z",
      "success_rate": 98.5,
      "next_scheduled": "2025-06-09T10:35:00Z"
    },
    {
      "id": "security_fortress_agent",
      "name": "SecurityFortressAgent",
      "status": "active",
      "last_run": "2025-06-09T10:00:00Z",
      "success_rate": 99.2,
      "next_scheduled": "2025-06-09T12:00:00Z"
    }
  ]
}
```

### POST /api/v1/agents/deploy

Deploy new agent

```bash
curl -X POST "http://localhost:8080/api/v1/agents/deploy" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "security_fortress",
    "schedule": "0 */2 * * *",
    "enabled": true,
    "config": {
      "scan_depth": "deep",
      "alert_threshold": "medium"
    }
  }'
```

### PUT /api/v1/agents/{agent_id}/execute

Execute agent immediately

```bash
curl -X PUT "http://localhost:8080/api/v1/agents/code_quality_agent/execute" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 🧠 Neural Overseer Endpoints

### GET /api/v1/neural/pulse

Get current brain pulse status

```bash
curl -X GET "http://localhost:8080/api/v1/neural/pulse" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "status": "healthy",
  "pulse_rate": 72,
  "memory_usage": 45.2,
  "cpu_usage": 23.8,
  "active_connections": 15,
  "learning_rate": 0.001,
  "neural_activity": "optimal",
  "last_update": "2025-06-09T10:35:42Z"
}
```

### POST /api/v1/neural/learn

Submit learning data

```bash
curl -X POST "http://localhost:8080/api/v1/neural/learn" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data_type": "performance_metrics",
    "metrics": {
      "response_time": 150,
      "error_rate": 0.02,
      "user_satisfaction": 4.8
    },
    "timestamp": "2025-06-09T10:35:00Z"
  }'
```

## 🛡️ Security Fortress Endpoints

### GET /api/v1/security/status

Get security system status

```bash
curl -X GET "http://localhost:8080/api/v1/security/status" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "status": "secure",
  "threat_level": "low",
  "active_monitors": 12,
  "blocked_attempts": 0,
  "last_scan": "2025-06-09T10:30:00Z",
  "firewall_status": "active",
  "intrusion_detection": "enabled",
  "ssl_certificates": "valid"
}
```

### POST /api/v1/security/scan

Initiate security scan

```bash
curl -X POST "http://localhost:8080/api/v1/security/scan" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "scan_type": "full",
    "priority": "high",
    "notify_on_completion": true
  }'
```

### GET /api/v1/security/reports

Get security reports

```bash
curl -X GET "http://localhost:8080/api/v1/security/reports?limit=10&type=vulnerability" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📊 Analytics Endpoints

### GET /api/v1/analytics/dashboard

Get dashboard analytics

```bash
curl -X GET "http://localhost:8080/api/v1/analytics/dashboard" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "overview": {
    "total_requests": 15420,
    "active_users": 89,
    "system_uptime": "99.98%",
    "response_time_avg": 145
  },
  "performance": {
    "cpu_usage": 23.8,
    "memory_usage": 45.2,
    "disk_usage": 67.1,
    "network_io": 125.4
  },
  "security": {
    "threat_level": "low",
    "blocked_attempts": 0,
    "security_score": 98.5
  }
}
```

### POST /api/v1/analytics/track

Track custom event

```bash
curl -X POST "http://localhost:8080/api/v1/analytics/track" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "user_action",
    "action": "dashboard_view",
    "user_id": "user_123",
    "metadata": {
      "page": "guardian_hud",
      "session_duration": 1250
    }
  }'
```

## ☁️ Cloudflare Integration Endpoints

### GET /api/v1/cloudflare/zones

Get Cloudflare zones

```bash
curl -X GET "http://localhost:8080/api/v1/cloudflare/zones" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### POST /api/v1/cloudflare/purge-cache

Purge Cloudflare cache

```bash
curl -X POST "http://localhost:8080/api/v1/cloudflare/purge-cache" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "purge_everything": true
  }'
```

### GET /api/v1/cloudflare/analytics

Get Cloudflare analytics

```bash
curl -X GET "http://localhost:8080/api/v1/cloudflare/analytics?since=2025-06-08" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 🎮 Discord Bot Endpoints

### GET /api/v1/discord/status

Get Discord bot status

```bash
curl -X GET "http://localhost:8080/api/v1/discord/status" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### POST /api/v1/discord/message

Send Discord message

```bash
curl -X POST "http://localhost:8080/api/v1/discord/message" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "123456789",
    "message": "🌩️💜 System status update: All systems operational!",
    "embed": {
      "title": "Status Update",
      "description": "All systems running smoothly",
      "color": 9442302
    }
  }'
```

## 🔄 System Management Endpoints

### GET /api/v1/system/health

Get system health status

```bash
curl -X GET "http://localhost:8080/api/v1/system/health" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "status": "healthy",
  "uptime": 2847392,
  "version": "2.0.0",
  "environment": "production",
  "database": {
    "status": "connected",
    "response_time": 12
  },
  "services": {
    "discord_bot": "running",
    "neural_overseer": "running",
    "security_fortress": "running",
    "analytics_engine": "running"
  }
}
```

### POST /api/v1/system/restart

Restart system services

```bash
curl -X POST "http://localhost:8080/api/v1/system/restart" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "discord_bot",
    "force": false
  }'
```

### GET /api/v1/system/logs

Get system logs

```bash
curl -X GET "http://localhost:8080/api/v1/system/logs?limit=100&level=error" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📈 Performance Monitoring Endpoints

### GET /api/v1/performance/metrics

Get performance metrics

```bash
curl -X GET "http://localhost:8080/api/v1/performance/metrics" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### GET /api/v1/performance/load

Get current system load

```bash
curl -X GET "http://localhost:8080/api/v1/performance/load" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 🔧 Configuration Endpoints

### GET /api/v1/config

Get system configuration

```bash
curl -X GET "http://localhost:8080/api/v1/config" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### PUT /api/v1/config

Update system configuration

```bash
curl -X PUT "http://localhost:8080/api/v1/config" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "neural_overseer": {
      "learning_rate": 0.002,
      "memory_threshold": 80
    },
    "security": {
      "scan_frequency": "hourly",
      "alert_threshold": "medium"
    }
  }'
```

## 📡 WebSocket Endpoints

### Real-time Neural Pulse

```javascript
const ws = new WebSocket("ws://localhost:8080/ws/neural-pulse");
ws.onmessage = function (event) {
  const pulseData = JSON.parse(event.data);
  console.log("Neural pulse:", pulseData);
};
```

### Real-time Security Alerts

```javascript
const ws = new WebSocket("ws://localhost:8080/ws/security-alerts");
ws.onmessage = function (event) {
  const alert = JSON.parse(event.data);
  console.log("Security alert:", alert);
};
```

## 🚨 Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid or expired",
    "details": {
      "timestamp": "2025-06-09T10:35:00Z",
      "request_id": "req_123456789"
    }
  }
}
```

### Common Error Codes

- `INVALID_API_KEY` (401) - Invalid or expired API key
- `RATE_LIMIT_EXCEEDED` (429) - Too many requests
- `RESOURCE_NOT_FOUND` (404) - Requested resource not found
- `VALIDATION_ERROR` (400) - Invalid request data
- `INTERNAL_ERROR` (500) - Internal server error
- `SERVICE_UNAVAILABLE` (503) - Service temporarily unavailable

## 📚 SDK Examples

### Python SDK

```python
import requests

class ChaosGeniusAPI:
    def __init__(self, api_key, base_url="http://localhost:8080/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def get_system_health(self):
        response = requests.get(f"{self.base_url}/system/health", headers=self.headers)
        return response.json()

    def deploy_agent(self, agent_config):
        response = requests.post(f"{self.base_url}/agents/deploy",
                               json=agent_config, headers=self.headers)
        return response.json()

# Usage
api = ChaosGeniusAPI("your_api_key")
health = api.get_system_health()
print(health)
```

### JavaScript SDK

```javascript
class ChaosGeniusAPI {
  constructor(apiKey, baseUrl = "http://localhost:8080/api/v1") {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
    this.headers = {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    };
  }

  async getSystemHealth() {
    const response = await fetch(`${this.baseUrl}/system/health`, {
      headers: this.headers,
    });
    return response.json();
  }

  async deployAgent(agentConfig) {
    const response = await fetch(`${this.baseUrl}/agents/deploy`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(agentConfig),
    });
    return response.json();
  }
}

// Usage
const api = new ChaosGeniusAPI("your_api_key");
api.getSystemHealth().then((health) => console.log(health));
```

## 🔗 Integration Examples

### Webhook Integration

```bash
# Register webhook
curl -X POST "http://localhost:8080/api/v1/webhooks" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.com/webhook",
    "events": ["security.alert", "agent.completed", "system.error"],
    "secret": "webhook_secret_key"
  }'
```

### Monitoring Integration

```bash
# Prometheus metrics endpoint
curl -X GET "http://localhost:8080/metrics" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 📞 API Support

For API support and questions:

- Documentation: https://docs.chaosgenius.com/api
- Support: api-support@chaosgenius.com
- Status: https://status.chaosgenius.com

**API Version**: 1.0
**Last Updated**: June 9, 2025
**Rate Limits**: 1000 requests/hour per API key

🌩️💜 **Your ChaosGenius Empire API is IMMORTAL!**
