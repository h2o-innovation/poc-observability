# 📝 To-Do App - Demonstração de Observabilidade

## 🎯 Visão Geral

Este projeto é uma **demonstração completa de observabilidade** usando uma aplicação web simples de To-Do List. Foi desenvolvido para ensinar e demonstrar os **três pilares da observabilidade** (métricas, logs e traces) usando **OpenTelemetry** e **Grafana Alloy**.

### 🏗️ Arquitetura da Solução

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (HTML/JS)     │◄──►│   (Flask)       │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Observabilidade Stack                        │
├─────────────────┬─────────────────┬─────────────────┬──────────┤
│   Grafana       │   Prometheus    │      Loki       │  Tempo   │
│   (Dashboards)  │   (Métricas)    │     (Logs)      │ (Traces) │
└─────────────────┴─────────────────┴─────────────────┴──────────┘
                              ▲
                              │
                    ┌─────────────────┐
                    │ Grafana Alloy   │
                    │ (Coletor OTEL)  │
                    └─────────────────┘
                              ▲
                              │
                    ┌─────────────────┐
                    │ OpenTelemetry   │
                    │ (Instrumentação)│
                    └─────────────────┘
```

## 🚀 Como Executar

### **Pré-requisitos**
- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)

### **1. Executar a Stack Completa**
```bash
# Clonar o repositório
git clone <repository-url>
cd adventure

# Iniciar todos os serviços
docker-compose up -d

# Verificar se todos os serviços estão rodando
docker-compose ps
```

### **2. Acessar as Aplicações**
- **To-Do App**: http://localhost:5000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Pyroscope**: http://localhost:4040

### **3. Gerar Tráfego para Demonstração**
```bash
# Instalar dependências para simulação
pip install requests

# Tráfego normal por 5 minutos
python simulate_traffic.py --mode continuous --duration 5

# Teste de rajada (stress test)
python simulate_traffic.py --mode burst --requests 20 --bursts 5

# Simular apenas erros
python simulate_traffic.py --mode errors
```

## 📊 Funcionalidades da Aplicação

### **🎮 Interface Web**
- ✅ Criar tarefas
- ✅ Listar todas as tarefas
- ✅ Marcar tarefas como completadas
- ✅ Deletar tarefas
- ⚠️ Simular diferentes tipos de erros

### **🔧 Endpoints da API**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Interface web principal |
| GET | `/api/tasks` | Listar todas as tarefas |
| POST | `/api/tasks` | Criar nova tarefa |
| POST | `/api/tasks/{id}/complete` | Completar tarefa |
| DELETE | `/api/tasks/{id}` | Deletar tarefa |
| POST | `/api/simulate-error/{type}` | Simular erros |
| GET | `/health` | Health check |

### **💥 Tipos de Erros Simulados**

1. **`db`** - Erro de banco de dados (consulta inválida)
2. **`timeout`** - Timeout de requisição (operação lenta)
3. **`500`** - Erro interno do servidor (exceção)
4. **`slow`** - Operação lenta (2-5 segundos)

## 🔍 Observabilidade Implementada

### **📈 Métricas (Prometheus)**

#### **Métricas de HTTP**
- `http_requests_total` - Total de requests por método/endpoint
- `http_request_duration_seconds` - Histograma de tempo de resposta

#### **Métricas de Aplicação**
- `tasks_total` - Total de tarefas no sistema
- `tasks_completed_total` - Total de tarefas completadas
- `db_operations_total` - Operações no banco por tipo
- `errors_total` - Total de erros por tipo

#### **Exemplos de Queries**
```promql
# Taxa de requests por segundo
rate(http_requests_total[5m])

# Percentil 95 de tempo de resposta
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Taxa de erro
rate(errors_total[5m])

# Tarefas pendentes
tasks_total - tasks_completed_total
```

### **📋 Logs (Loki)**

#### **Estrutura dos Logs**
```json
{
  "level": "INFO",
  "message": "POST /api/tasks - 201 - 0.123s",
  "method": "POST",
  "path": "/api/tasks",
  "status_code": 201,
  "duration": 0.123,
  "user_agent": "Mozilla/5.0...",
  "trace_id": "abc123...",
  "span_id": "def456..."
}
```

#### **Correlação Automática**
- Logs incluem `trace_id` para correlação com traces
- Derived fields configurados no Grafana para navegação

### **🔗 Traces (Tempo)**

#### **Spans Capturados**
- HTTP requests (automático via Flask instrumentation)
- Operações de banco de dados (automático via psycopg2)
- Operações customizadas (`create_task`, `complete_task`, etc.)
- Simulação de erros

#### **Atributos dos Spans**
```python
span.set_attribute("operation", "create_task")
span.set_attribute("task_id", task_id)
span.set_attribute("success", True)
span.set_attribute("error", str(e))  # em caso de erro
```

### **🔥 Profiling (Pyroscope)**

#### **Configuração**
- Profiling contínuo de CPU habilitado
- Tags contextuais por operação
- Integração com Grafana para visualização

#### **Tags Disponíveis**
```python
{
    "service.name": "todo-app",
    "operation": "create_task",
    "environment": "development"
}
```

## 🎛️ Dashboards do Grafana

### **📊 Dashboard Principal - To-Do App**
- **Taxa de Requests HTTP** - Requests por segundo por endpoint
- **Tempo de Resposta** - P95 e P50 de latência
- **Tarefas no Sistema** - Total vs completadas
- **Taxa de Erros** - Erros por tipo e operação
- **Operações do Banco** - Queries por tipo

### **🔥 Dashboard de Profiling**
- **Flamegraph** - Visualização hierárquica do call stack
- **Operações da Aplicação** - Profiling por operação
- **Function Call Tree** - Distribuição de tempo por função

### **📋 Dashboard de Logs**
- **Volume de Logs** - Logs por nível e serviço
- **Logs de Erro** - Filtrados por ERROR/WARNING
- **Trace Correlation** - Links diretos para traces

## ⚙️ Configuração Técnica

### **🔧 Grafana Alloy**
```alloy
// OTLP Receiver
otelcol.receiver.otlp "default" {
  http { endpoint = "0.0.0.0:4318" }
  grpc { endpoint = "0.0.0.0:4317" }
  
  output {
    metrics = [otelcol.exporter.otlphttp.metrics.input]
    logs    = [otelcol.exporter.otlphttp.logs.input]
    traces  = [otelcol.exporter.otlphttp.traces.input]
  }
}

// Pyroscope Receiver
pyroscope.receive_http "default" {
  http {
    listen_address = "0.0.0.0"
    listen_port    = 4040
  }
  forward_to = [pyroscope.write.default.receiver]
}
```

### **🐍 Instrumentação Python**
```python
# Instrumentação automática
from otel import CustomLogFW, CustomMetrics, CustomTracer, CustomPyroscope

# Setup completo
logFW = CustomLogFW(service_name="todo-app")
metrics = CustomMetrics(service_name="todo-app") 
tracer = CustomTracer(service_name="todo-app")
profiler = CustomPyroscope(service_name="todo-app")

# Instrumentação automática Flask + PostgreSQL
auto_instrument = AutoInstrumentation()
auto_instrument.instrument_all(app)
```

### **🗄️ PostgreSQL**
```sql
-- Estrutura da tabela
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 Cenários de Demonstração

### **📈 Cenário 1: Operação Normal**
```bash
# Gerar tráfego normal
python simulate_traffic.py --mode normal

# O que observar:
# ✅ Métricas de requests aumentando
# ✅ Traces sendo criados para cada operação
# ✅ Logs estruturados com correlação
# ✅ Profiles de CPU sendo coletados
```

### **💥 Cenário 2: Simulação de Erros**
```bash
# Simular erros diversos
python simulate_traffic.py --mode errors

# O que observar:
# ❌ Aumento na métrica errors_total
# ❌ Spans com status ERROR
# ❌ Logs de nível ERROR com stack traces
# ❌ Correlação trace_id entre logs e traces
```

### **⚡ Cenário 3: Teste de Carga**
```bash
# Gerar rajadas de tráfego
python simulate_traffic.py --mode burst --requests 50

# O que observar:
# 📊 Picos nas métricas de requests
# ⏱️ Aumento no tempo de resposta (P95)
# 🔥 CPU usage aumentando no profiling
# 🔗 Traces com maior latência
```

### **🐌 Cenário 4: Operações Lentas**
```bash
# Através da interface web, clicar em "Simular Lentidão"

# O que observar:
# 🐌 Spans com duração alta
# ⏰ Histograma de latência com outliers
# 🔥 Profiling mostrando wait time
# 📋 Logs indicando operação lenta
```

## 🔍 Como Investigar Problemas

### **🚨 Passo 1: Detectar o Problema**
1. **Dashboards** - Alertas visuais de anomalias
2. **Métricas** - Aumentos em `errors_total` ou latência
3. **Logs** - Mensagens de ERROR no volume

### **🔍 Passo 2: Investigar a Causa**
1. **Correlação** - Usar `trace_id` dos logs para encontrar traces
2. **Traces** - Analisar spans com erro ou alta latência
3. **Profiling** - Verificar hot paths no código

### **📊 Passo 3: Analisar o Impacto**
1. **Métricas** - Quantificar o impacto (% de erro, usuários afetados)
2. **Logs** - Frequência e padrões dos erros
3. **Traces** - Quais operações são mais afetadas

### **⚡ Passo 4: Correlacionar Dados**
```
🔍 Exemplo de Investigação:

1. Dashboard mostra aumento em errors_total
   ↓
2. Filtrar logs por ERROR level
   ↓  
3. Copiar trace_id de um log de erro
   ↓
4. Abrir trace no Tempo usando o trace_id
   ↓
5. Identificar span com erro
   ↓
6. Analisar stack trace e atributos
   ↓
7. Correlacionar com profiling se necessário
```

## 🛠️ Troubleshooting

### **❌ Problema: Aplicação não inicia**
```bash
# Verificar logs
docker-compose logs todo-app

# Verificar PostgreSQL
docker-compose logs postgres

# Verificar conectividade
docker-compose exec todo-app python -c "import psycopg2; print('OK')"
```

### **❌ Problema: Métricas não aparecem**
```bash
# Verificar Alloy
docker-compose logs alloy

# Verificar endpoint OTLP
curl http://localhost:4318/v1/metrics

# Verificar Prometheus
curl http://localhost:9090/api/v1/query?query=up
```

### **❌ Problema: Traces não aparecem**
```bash
# Verificar Tempo
docker-compose logs tempo

# Verificar endpoint traces
curl http://localhost:3200/api/traces

# Verificar instrumentação
docker-compose exec todo-app python -c "from opentelemetry import trace; print(trace.get_tracer_provider())"
```

### **❌ Problema: Dashboards em branco**
```bash
# Verificar datasources
curl http://admin:admin@localhost:3000/api/datasources

# Verificar queries
curl http://admin:admin@localhost:3000/api/dashboards/uid/todo-app-main

# Restartar Grafana
docker-compose restart grafana
```

## 📚 Conceitos Aprendidos

### **🎯 Observabilidade**
- **Métricas**: Agregações numéricas ao longo do tempo
- **Logs**: Eventos discretos com contexto
- **Traces**: Jornada de uma requisição através do sistema
- **Profiling**: Performance de código em nível de função

### **🔧 OpenTelemetry**
- **Instrumentação automática** vs manual
- **Spans** e **attributes** para contexto
- **Correlação** entre sinais de observabilidade
- **Sampling** e configuração de exporters

### **📊 Grafana Stack**
- **Alloy** como coletor universal
- **Prometheus** para métricas time-series
- **Loki** para logs agregados
- **Tempo** para distributed tracing
- **Pyroscope** para continuous profiling

### **🏗️ Arquitetura**
- **Separation of concerns** na observabilidade
- **Push vs Pull** models
- **Service mesh** observability
- **Exemplars** conectando métricas a traces

## 🎯 Próximos Passos

### **🚀 Melhorias Possíveis**
- [ ] Implementar alertas no Prometheus/Grafana
- [ ] Adicionar SLI/SLO dashboards
- [ ] Configurar retenção de dados
- [ ] Implementar distributed tracing entre serviços
- [ ] Adicionar instrumentação de cache (Redis)
- [ ] Configurar log aggregation por múltiplos serviços

### **📖 Estudos Adicionais**
- [ ] Implementar chaos engineering
- [ ] Estudar OpenTelemetry Collector vs Alloy
- [ ] Explorar custom metrics e business KPIs
- [ ] Implementar synthetic monitoring
- [ ] Estudar cost optimization para observabilidade

---

## 🎉 Conclusão

Este projeto demonstra uma implementação completa e prática dos **três pilares da observabilidade** usando ferramentas modernas como **OpenTelemetry** e **Grafana Alloy**. 

Através de uma aplicação simples porém realista, você pode:
- ✅ **Aprender** conceitos fundamentais de observabilidade
- ✅ **Praticar** com ferramentas reais de mercado
- ✅ **Experimentar** diferentes cenários de erro e performance
- ✅ **Entender** correlação entre métricas, logs, traces e profiling

**O conhecimento adquirido aqui é diretamente aplicável em ambientes de produção!**

---
**Happy Observing! 📊🔍🚀**
