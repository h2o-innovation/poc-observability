# ✅ Checklist de Validação - Observabilidade To-Do App

> **Lista de verificação para garantir que tudo está funcionando corretamente**

## 🎯 Objetivo
Este checklist garante que toda a stack de observabilidade está funcionando corretamente e pode ser usado pela equipe para validar deployments ou troubleshooting.

---

## ⚡ **Checklist Rápido (5 minutos)**

### ✅ **1. Serviços Básicos**
```bash
# ✅ Todos os containers estão rodando
docker-compose ps
# Status: deve mostrar todos como "Up"

# ✅ Aplicação To-Do responde
curl http://localhost:5001/health
# Resposta esperada: {"status": "healthy", ...}

# ✅ Grafana acessível
curl -I http://localhost:3000/api/health
# Status: HTTP/1.1 200 OK
```

### ✅ **2. Pipeline de Dados**
```bash
# ✅ Alloy recebendo dados OTLP
curl -I http://localhost:4318/v1/metrics
# Status: HTTP/1.1 200 OK (ou 405 Method Not Allowed - normal)

# ✅ Prometheus coletando métricas
curl http://localhost:9090/api/v1/query?query=up
# Deve retornar JSON com targets "up"

# ✅ Tempo acessível para traces
curl -I http://localhost:3200/api/traces
# Status: HTTP/1.1 200 OK
```

### ✅ **3. Teste End-to-End**
```bash
# ✅ Criar tarefa gera observabilidade completa
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Teste validação observabilidade"}'

# Deve retornar: {"id": X, "title": "Teste...", ...}
```

**🚨 Se algum item falhou**: Vá para [Troubleshooting Detalhado](#-troubleshooting-detalhado)

---

## 🔍 **Checklist Completo (15 minutos)**

### 📊 **Métricas (Prometheus/Grafana)**

#### ✅ **Prometheus Targets**
1. Acesse http://localhost:9090/targets
2. ✅ Verifique se todos os targets estão "UP":
   - prometheus (localhost:9090)
   - alloy (alloy:12345)

#### ✅ **Métricas da Aplicação**
Execute no Prometheus (http://localhost:9090):
```promql
# ✅ Métricas HTTP estão sendo coletadas
sum(rate(http_requests_total[5m])) > 0

# ✅ Métricas de banco de dados
sum(rate(db_operations_total[5m])) > 0

# ✅ Métricas customizadas de tarefas
tasks_total > 0
```

#### ✅ **Dashboard do Grafana**
1. Acesse http://localhost:3000 (admin/admin)
2. Vá para Dashboards → Browse → "To-Do App - Observabilidade"
3. ✅ Verifique se há dados nos painéis:
   - HTTP Requests Rate
   - Response Time (P95)
   - Tasks Total vs Completed
   - Database Operations

### 📋 **Logs (Loki/Grafana)**

#### ✅ **Loki Ingestion**
1. No Grafana, vá para Explore
2. Selecione datasource "Loki"
3. Query: `{service_name="todo-app"}`
4. ✅ Deve mostrar logs da aplicação com timestamps recentes

#### ✅ **Correlação Logs-Traces**
1. No resultado dos logs, procure por `trace_id`
2. ✅ Clique no trace_id (deve estar linkado)
3. ✅ Deve abrir o trace correspondente no Tempo

### 🔗 **Traces (Tempo/Grafana)**

#### ✅ **Tempo Data**
1. No Grafana, vá para Explore
2. Selecione datasource "Tempo"
3. ✅ Execute search sem filtros - deve mostrar traces recentes

#### ✅ **Trace Quality**
1. Abra um trace específico
2. ✅ Verifique se contém spans de:
   - HTTP request (Flask)
   - Database operation (PostgreSQL)
   - Custom spans (create_task, etc.)
3. ✅ Spans devem ter atributos relevantes (success, task_id, etc.)

### 🔥 **Profiling (Pyroscope)**

#### ✅ **Pyroscope Data**
1. Acesse http://localhost:4040
2. ✅ Deve mostrar "todo-app" na lista de aplicações
3. ✅ Selecione a aplicação e verifique se há dados de profiling
4. ✅ Flamegraph deve mostrar call stack da aplicação

#### ✅ **Grafana Integration**
1. No Grafana, vá para Explore
2. Selecione datasource "Pyroscope"
3. ✅ Query por "todo-app" deve retornar perfis

---

## 🎮 **Validação Funcional (20 minutos)**

### 🟢 **Cenário 1: Operação Normal**
```bash
# 1. Gerar tráfego normal
python simulate_traffic.py --mode normal --duration 2

# 2. ✅ Validar no Grafana Dashboard:
#    - HTTP Requests aumentando
#    - Error Rate próximo de 0%
#    - Latência P95 < 500ms
#    - Tasks Total aumentando

# 3. ✅ Validar logs:
#    - Logs de nível INFO aparecendo
#    - Sem logs de ERROR/WARNING

# 4. ✅ Validar traces:
#    - Traces limpos sem erros
#    - Spans com status SUCCESS
```

### 🔴 **Cenário 2: Simulação de Erros**
```bash
# 1. Interface web: clicar em "Simular Erro DB"
# OU via API:
curl -X POST http://localhost:5001/api/simulate-error/db

# 2. ✅ Validar métricas:
#    - errors_total aumentando
#    - Error rate > 0%

# 3. ✅ Validar logs:
#    - Logs de ERROR aparecendo
#    - Stack traces visíveis

# 4. ✅ Validar traces:
#    - Spans com status ERROR
#    - Error details nos attributes
```

### ⚡ **Cenário 3: Teste de Performance**
```bash
# 1. Gerar carga
python simulate_traffic.py --mode burst --requests 20

# 2. ✅ Validar métricas:
#    - Pico nas requests/sec
#    - Aumento na latência P95
#    - CPU usage aumentando

# 3. ✅ Validar profiling:
#    - Pyroscope mostra CPU spikes
#    - Hotspots identificados

# 4. ✅ Validar traces:
#    - Traces com duração alta
#    - Database spans mais lentos
```

### 🐌 **Cenário 4: Operação Lenta**
```bash
# 1. Interface web: clicar em "Simular Lentidão"
# OU via API:
curl -X POST http://localhost:5001/api/simulate-error/slow

# 2. ✅ Validar métricas:
#    - Latência P95 > 2s
#    - Histograma mostra outliers

# 3. ✅ Validar traces:
#    - Spans com duração 2-5s
#    - Root span reflete lentidão total

# 4. ✅ Validar profiling:
#    - Wait time visível no flamegraph
```

---

## 🔍 **Validação de Correlação**

### 🔗 **Teste de Correlação End-to-End**
```bash
# 1. Criar tarefa específica para teste
task_response=$(curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "CORRELACAO-TEST-'$(date +%s)'"}')

echo "Task criada: $task_response"

# 2. ✅ No Grafana Loki, buscar por:
#    {service_name="todo-app"} |= "CORRELACAO-TEST"

# 3. ✅ Copiar trace_id do log

# 4. ✅ No Grafana Tempo, colar o trace_id

# 5. ✅ Verificar se abre o trace correto

# 6. ✅ No trace, verificar se tem span com task_id correspondente
```

### 📊 **Métricas → Traces**
```bash
# 1. No Dashboard do Grafana, clicar em "HTTP Requests"
# 2. ✅ Deve haver link/botão para "Explore traces"
# 3. ✅ Deve filtrar traces do período selecionado
```

---

## 🛠️ **Troubleshooting Detalhado**

### ❌ **Serviços não sobem**
```bash
# Diagnostic completo
./start-demo.sh status

# Logs por serviço
docker-compose logs postgres
docker-compose logs todo-app  
docker-compose logs alloy
docker-compose logs grafana

# Resource usage
docker stats

# Restart total
./start-demo.sh restart
```

### ❌ **Métricas não aparecem**
```bash
# 1. Verificar Alloy está recebendo dados
docker-compose logs alloy | grep -i "metrics\|error"

# 2. Verificar Prometheus está fazendo scrape
curl http://localhost:9090/api/v1/targets

# 3. Verificar se aplicação está enviando métricas
curl http://localhost:5001/api/tasks  # Gera métrica
curl http://localhost:9090/api/v1/query?query=http_requests_total

# 4. Debug do pipeline
docker-compose logs alloy | grep -A5 -B5 "metrics"
```

### ❌ **Traces não aparecem**
```bash
# 1. Verificar endpoint OTLP está funcionando
curl -X POST http://localhost:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# 2. Verificar Alloy está processando traces  
docker-compose logs alloy | grep -i "trace"

# 3. Verificar Tempo está recebendo
docker-compose logs tempo | grep -i "trace"

# 4. Forçar criação de trace
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Força trace"}'

# 5. Verificar no Grafana após 30s
```

### ❌ **Dashboards vazios**
```bash
# 1. Verificar datasources no Grafana
curl http://admin:admin@localhost:3000/api/datasources

# 2. Testar queries individuais
# Grafana → Explore → Prometheus → Query: up

# 3. Verificar timerange
# Grafana → Last 5 minutes

# 4. Forçar geração de dados
python simulate_traffic.py --mode normal --duration 1

# 5. Aguardar scrape interval (15-30s)
```

### ❌ **Logs sem correlação**
```bash
# 1. Verificar se trace_id está nos logs
docker-compose logs todo-app | grep "trace_id"

# 2. Verificar configuração do derived field
# Grafana → Data sources → Loki → Derived fields

# 3. Testar regex do trace_id
# Deve capturar: "trace_id": "abc123..."

# 4. Verificar se Tempo datasource está configurado
```

---

## 📋 **Checklist de Produção**

### 🔒 **Segurança**
- [ ] Credenciais padrão alteradas (admin/admin)
- [ ] TLS configurado para endpoints externos
- [ ] Autenticação configurada no Grafana
- [ ] PII removido de logs e traces
- [ ] Rate limiting configurado

### 📊 **Performance**
- [ ] Retenção de dados configurada adequadamente
- [ ] Sampling rate ajustado para traces
- [ ] Resource limits definidos para containers
- [ ] Storage persistente configurado
- [ ] Backup strategy implementada

### 🚨 **Alerting**
- [ ] Regras de alerta configuradas no Prometheus
- [ ] Notification channels configurados
- [ ] SLI/SLO dashboards criados
- [ ] Runbooks documentados
- [ ] Escalation procedures definidos

### 📈 **Monitoring**
- [ ] Self-monitoring da stack de observabilidade
- [ ] Resource usage monitorado
- [ ] Cost tracking implementado
- [ ] Capacity planning documentado
- [ ] DR procedures testados

---

## 🎉 **Conclusão**

**✅ Se todos os checks passaram**: Parabéns! Sua stack de observabilidade está funcionando perfeitamente.

**❌ Se alguns checks falharam**: Use o troubleshooting detalhado ou consulte:
- **GUIA-EQUIPE.md** para orientações específicas por função
- **README-TODO-APP.md** para documentação técnica detalhada
- Logs dos serviços: `docker-compose logs [service]`

**📚 Próximos passos:**
1. Explore o GUIA-EQUIPE.md para seu perfil específico
2. Pratique cenários de troubleshooting
3. Personalize dashboards para suas necessidades
4. Implemente alerting personalizado

---

**🔄 Recomendação**: Execute este checklist sempre que:
- Fazer deploy de mudanças
- Suspeitar de problemas na observabilidade  
- Onboarding de novos membros da equipe
- Validar ambiente após atualizações

---

**Vamos DevOpear! 🚀**
