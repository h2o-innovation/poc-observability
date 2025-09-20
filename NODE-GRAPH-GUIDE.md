# 🕸️ Guia Completo: Node Graph no Grafana Tempo

## 📊 O que é o Node Graph?

O **Node Graph** é uma visualização que mostra a **topologia de serviços** baseada nos traces coletados. Ele revela:

- **Dependências entre serviços**
- **Fluxo de requests**
- **Performance de comunicação**
- **Gargalos e pontos de falha**

## 🎯 Como Acessar

### 1. **Via Service Map (Mais Comum)**
```
Grafana → Explore → Tempo → Service Map tab
```

### 2. **Via Trace Individual**
```
Grafana → Explore → Tempo → Search → [Selecionar trace] → Node Graph tab
```

### 3. **Via Dashboard Panel**
```
Dashboard → Add Panel → Node Graph visualization → Tempo datasource
```

## 🔧 Configurações Importantes

### **Datasource Tempo (já configurado)**
```yaml
jsonData:
  nodeGraph: 
    enabled: true
  serviceMap:
    datasourceUid: 'prometheus'  # Para métricas adicionais
```

### **Métricas Correlacionadas**
O Node Graph fica mais rico quando correlacionado com:
- **Prometheus**: Rate, errors, duration (RED metrics)
- **Loki**: Logs de erro por serviço
- **Pyroscope**: Performance profiling

## 📈 Elementos Visuais

### **Nós (Serviços)**
- **Tamanho**: Volume de requests
- **Cor**: Taxa de erro
  - 🟢 Verde: Baixa taxa de erro
  - 🟡 Amarelo: Taxa média de erro
  - 🔴 Vermelho: Alta taxa de erro

### **Arestas (Conexões)**
- **Espessura**: Volume de comunicação
- **Cor**: Latência
  - Azul: Baixa latência
  - Laranja: Alta latência

### **Informações Exibidas**
- **Request Rate**: Requests por segundo
- **Error Rate**: Porcentagem de erros
- **Duration**: Latência média/percentis

## 🎮 Interações

### **Clique em Nó**
- Mostra detalhes do serviço
- Acesso rápido a traces
- Navegação para dashboards específicos

### **Clique em Aresta**
- Detalhes da comunicação
- Traces da comunicação específica
- Métricas de latência

### **Filtros Disponíveis**
- **Time Range**: Período de análise
- **Service Name**: Filtrar por serviço
- **Operation**: Filtrar por operação
- **Tag Filters**: Filtros customizados

## 🚀 Casos de Uso

### **1. Identificar Dependências**
- Mapear arquitetura real vs documentada
- Descobrir dependências não documentadas
- Entender fluxo de dados

### **2. Performance Analysis**
- Identificar gargalos
- Spots de alta latência
- Serviços com erro

### **3. Troubleshooting**
- Rastrear origem de problemas
- Impacto cascata de falhas
- Análise de root cause

### **4. Capacity Planning**
- Volume de tráfego por serviço
- Padrões de comunicação
- Crescimento de dependências

## 📋 Requisitos para Funcionar

### **1. Traces com Spans Corretos**
```python
# Spans devem ter service.name definido
with tracer.start_span("operation_name") as span:
    span.set_attribute("service.name", "todo-app")
    span.set_attribute("http.method", "GET")
```

### **2. Instrumentação Adequada**
- **HTTP requests**: Cliente e servidor
- **Database calls**: Queries SQL
- **Message queues**: Producers/consumers
- **RPC calls**: gRPC, etc.

### **3. Correlação de Serviços**
- Cada serviço deve ter nome único
- Spans parent-child corretos
- Propagação de trace context

## 🔍 Nossa Configuração Atual

### **Serviços Detectados**
- `todo-app`: Aplicação Flask principal
- `postgres`: Database PostgreSQL
- `alloy`: Collector OpenTelemetry

### **Traces Gerados**
- HTTP requests para API
- Queries SQL para PostgreSQL
- Instrumentação automática Flask

### **Para Melhorar o Node Graph**

1. **Adicionar mais serviços**:
```python
# Exemplo: serviço de cache
with tracer.start_span("cache_get") as span:
    span.set_attribute("service.name", "redis-cache")
```

2. **Enriquecer spans**:
```python
span.set_attribute("http.status_code", 200)
span.set_attribute("db.statement", "SELECT * FROM todos")
span.set_attribute("user.id", user_id)
```

3. **Correlacionar com métricas**:
- RED metrics no Prometheus
- SLI/SLO dashboards
- Alert correlation

## 🎯 Demo Rápido

1. **Gere tráfego**:
```bash
python3 simulate_traffic.py
```

2. **Acesse Grafana**:
```
http://localhost:3000 → Explore → Tempo → Service Map
```

3. **Configure time range**: "Last 15 minutes"

4. **Explore o grafo**:
- Clique nos nós
- Analise conexões
- Investigue traces

## 🔧 Troubleshooting

### **Node Graph vazio?**
- ✅ Verificar se traces estão chegando no Tempo
- ✅ Confirmar instrumentação dos serviços
- ✅ Validar time range adequado
- ✅ Gerar tráfego suficiente

### **Poucos nós/conexões?**
- ✅ Melhorar instrumentação
- ✅ Adicionar spans de comunicação
- ✅ Verificar service.name nos spans

### **Performance lenta?**
- ✅ Reduzir time range
- ✅ Aplicar filtros de serviço
- ✅ Otimizar queries no Tempo
