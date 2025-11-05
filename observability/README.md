# 可观测性配置

## 目标
提供开箱即用的监控、日志、追踪配置，帮助项目快速建立可观测性体系。

## 适用场景
- 需要监控应用性能和健康状态
- 需要集中收集和分析日志
- 需要追踪分布式请求链路
- 需要告警和通知机制

## 前置条件
- 已确定监控需求
- 已选择监控工具栈（Prometheus/Grafana/ELK/Jaeger等）

---

## 目录结构

```
observability/
├── README.md           # 本文件
├── logging/            # 日志配置
│   ├── logstash.conf      # Logstash 配置
│   ├── fluentd.yaml       # Fluentd 配置
│   └── python_logging.yaml # Python logging 配置
├── metrics/            # 指标配置
│   ├── prometheus.yml     # Prometheus 配置
│   └── grafana_dashboards/ # Grafana 仪表盘
│       └── app_dashboard.json
├── tracing/            # 链路追踪
│   ├── jaeger.yaml        # Jaeger 配置
│   └── opentelemetry.yaml # OpenTelemetry 配置
└── alerts/             # 告警配置
    ├── prometheus_alerts.yml
    └── alertmanager.yml
```

---

## 快速开始

### 1. 日志收集（ELK Stack）

#### 使用 Logstash
```yaml
# observability/logging/logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] {
    mutate {
      add_field => { "service" => "%{[fields][service]}" }
    }
  }
  
  # 解析 JSON 日志
  if [message] =~ /^\{.*\}$/ {
    json {
      source => "message"
    }
  }
  
  # 解析时间戳
  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "app-logs-%{+YYYY.MM.dd}"
  }
}
```

#### 使用 Fluentd
```yaml
# observability/logging/fluentd.yaml
<source>
  @type forward
  port 24224
</source>

<filter app.**>
  @type parser
  format json
  key_name message
  reserve_data true
</filter>

<match app.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name app-logs
  type_name _doc
  <buffer>
    flush_interval 10s
  </buffer>
</match>
```

#### Python logging 配置
```yaml
# observability/logging/python_logging.yaml
version: 1
formatters:
  json:
    format: '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}'
    datefmt: '%Y-%m-%dT%H:%M:%S'

handlers:
  console:
    class: logging.StreamHandler
    formatter: json
    level: INFO
    stream: ext://sys.stdout
  
  file:
    class: logging.handlers.RotatingFileHandler
    formatter: json
    level: INFO
    filename: /var/log/app/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

loggers:
  app:
    level: INFO
    handlers: [console, file]
    propagate: false

root:
  level: WARNING
  handlers: [console]
```

---

### 2. 指标收集（Prometheus）

#### Prometheus 配置
```yaml
# observability/metrics/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:8000']
        labels:
          service: 'api'
          version: 'v1.0.0'
  
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']
        labels:
          service: 'database'
  
  - job_name: 'redis'
    static_configs:
      - targets: ['redis_exporter:9121']
        labels:
          service: 'cache'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

#### 应用指标暴露（Python 示例）
```python
# modules/user/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# 定义指标
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'active_connections',
    'Active database connections'
)

# 启动指标服务器
start_http_server(8001)
```

---

### 3. 链路追踪（Jaeger）

#### Jaeger 配置
```yaml
# observability/tracing/jaeger.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-config
data:
  jaeger.yaml: |
    sampling:
      default_strategy:
        type: probabilistic
        param: 0.001  # 0.1% 采样率
    storage:
      type: elasticsearch
      elasticsearch:
        server_urls: http://elasticsearch:9200
        index_prefix: jaeger
        username: elastic
        password: changeme
```

#### OpenTelemetry 配置
```yaml
# observability/tracing/opentelemetry.yaml
exporter:
  jaeger:
    endpoint: jaeger:14250
    insecure: true

service:
  name: app-service
  version: 1.0.0

instrumentation:
  python:
    enabled: true
    packages:
      - flask
      - requests
      - sqlalchemy
```

#### Python 集成示例
```python
# modules/user/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# 配置追踪器
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# 使用示例
@tracer.start_as_current_span("create_user")
def create_user(email: str):
    with tracer.start_as_current_span("validate_email"):
        validate_email(email)
    with tracer.start_as_current_span("save_to_db"):
        save_user(email)
    return user
```

---

### 4. 告警配置

#### Prometheus 告警规则
```yaml
# observability/alerts/prometheus_alerts.yml
groups:
  - name: app_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "高错误率告警"
          description: "错误率超过 10% (当前值: {{ $value }})"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "高延迟告警"
          description: "P95 延迟超过 2 秒 (当前值: {{ $value }}s)"
      
      - alert: LowAvailability
        expr: up{job="app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "服务不可用"
          description: "服务 {{ $labels.instance }} 已下线超过 1 分钟"
```

#### Alertmanager 配置
```yaml
# observability/alerts/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'critical'
      continue: true
    - match:
        severity: warning
      receiver: 'warning'

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
  
  - name: 'critical'
    slack_configs:
      - channel: '#alerts-critical'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
  
  - name: 'warning'
    slack_configs:
      - channel: '#alerts-warning'
        title: '⚠️ WARNING: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

---

## 验证步骤

### 1. 日志验证
```bash
# 检查日志是否正常收集
curl http://elasticsearch:9200/app-logs-*/_search?q=level:ERROR

# 检查 Fluentd 状态
curl http://fluentd:24220/api/plugins.json
```

### 2. 指标验证
```bash
# 检查 Prometheus 目标
curl http://prometheus:9090/api/v1/targets

# 查询指标
curl 'http://prometheus:9090/api/v1/query?query=up'
```

### 3. 追踪验证
```bash
# 检查 Jaeger 服务
curl http://jaeger:16686/api/services

# 查询追踪
curl 'http://jaeger:16686/api/traces?service=app-service&limit=10'
```

---

## Docker Compose 集成

```yaml
# docker-compose.observability.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./observability/metrics/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./observability/alerts:/etc/prometheus/alerts
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana:latest
    volumes:
      - ./observability/metrics/grafana_dashboards:/var/lib/grafana/dashboards
    ports:
      - "3000:3000"
  
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "6831:6831/udp"
  
  elasticsearch:
    image: elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
  
  logstash:
    image: logstash:8.0.0
    volumes:
      - ./observability/logging/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"
```

---

## 相关文档
- 运维手册：`modules/example/RUNBOOK.md`
- 监控指标：`docs/process/ENV_SPEC.yaml`
- 日志规范：`docs/process/CONVENTIONS.md`

