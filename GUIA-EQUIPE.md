# 👥 Guia de Uso por Perfil - Equipe DevOps

> **Instruções específicas para diferentes perfis de usuário na equipe**

## 🎯 Para quem é este guia?

Este documento orienta diferentes perfis da equipe sobre como usar o projeto de demonstração de observabilidade de acordo com suas necessidades específicas.

---

## 👨‍💻 **Desenvolvedor Backend/Frontend**

### 🎯 **Objetivo**: Entender instrumentação de código

#### 🚀 **Start Rápido** (10 minutos)
```bash
# 1. Subir ambiente
./start-demo.sh

# 2. Ver código instrumentado
code todo_app.py otel.py

# 3. Gerar dados
python simulate_traffic.py --mode normal --duration 3

# 4. Ver traces no Grafana
# http://localhost:3000 → Explore → Tempo → Search
```

#### 📝 **O que focar**
- **OpenTelemetry SDK**: Como instrumentar Flask + PostgreSQL
- **Traces manuais**: Criação de spans customizados
- **Métricas de negócio**: Contadores de tarefas criadas/completadas
- **Logs correlacionados**: Como incluir `trace_id` nos logs
- **Profiling**: Instrumentação de performance de código

#### 🔍 **Código-chave para estudar**
```python
# todo_app.py - linhas 180-200 (setup de métricas)
# otel.py - linhas 30-80 (configuração OTEL)
# Veja spans customizados em todo_app.py:350+
```

#### 🎮 **Exercícios práticos**
1. **Adicionar nova métrica**: Contador de tarefas deletadas
2. **Criar span customizado**: Instrumentar validação de dados
3. **Testar erro handling**: Simular falha de conexão DB
4. **Correlação logs**: Adicionar contexto extra nos logs

---

## 🔧 **DevOps/SRE**

### 🎯 **Objetivo**: Configurar stack de observabilidade

#### 🚀 **Start Rápido** (15 minutos)
```bash
# 1. Analisar arquitetura
cat docker-compose.yml
cat config.alloy

# 2. Subir stack
./start-demo.sh

# 3. Verificar conectividade
curl http://localhost:4318/v1/metrics  # Alloy OTLP
curl http://localhost:9090/api/v1/query?query=up  # Prometheus

# 4. Monitorar logs do pipeline
docker-compose logs -f alloy tempo prometheus
```

#### 📝 **O que focar**
- **Grafana Alloy**: Configuração de receivers/exporters
- **Grafana Stack**: Integração Prometheus/Loki/Tempo/Pyroscope  
- **Data Pipeline**: Fluxo de dados OTLP → Alloy → Backends
- **Health Checks**: Monitoramento dos próprios componentes
- **Storage**: Configuração de retenção e volumes

#### 🔍 **Arquivos-chave para estudar**
```yaml
# config.alloy - Pipeline de telemetria
# docker-compose.yml - Orquestração completa
# grafana/datasources/ - Configuração dos datasources
# prometheus.yml - Configuração de scraping
```

#### 🎮 **Exercícios práticos**
1. **Configurar alerting**: Regras no Prometheus
2. **Otimizar Alloy**: Ajustar sampling e buffering
3. **Backup/Restore**: Configurar volumes persistentes
4. **High Availability**: Replicar componentes críticos
5. **Security**: Adicionar TLS e autenticação

---

## 📊 **Analista de Dados/Observabilidade**

### 🎯 **Objetivo**: Criar dashboards e alertas efetivos

#### 🚀 **Start Rápido** (20 minutos)
```bash
# 1. Subir ambiente
./start-demo.sh

# 2. Gerar dados variados
python simulate_traffic.py --mode continuous --duration 5 &
python simulate_traffic.py --mode errors &

# 3. Explorar dados
# Grafana → Explore → Prometheus/Loki/Tempo

# 4. Importar dashboards
# Grafana → Dashboards → Browse → "To-Do App"
```

#### 📝 **O que focar**
- **PromQL**: Queries para métricas e alertas
- **LogQL**: Consultas estruturadas de logs
- **TraceQL**: Busca e análise de traces
- **Dashboard Design**: Visualizações efetivas
- **Alerting**: SLI/SLO e regras de alerta

#### 🔍 **Queries importantes**
```promql
# SLI - Error Rate
rate(errors_total[5m]) / rate(http_requests_total[5m]) * 100

# SLI - Latency P99
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Business KPI - Task Creation Rate
rate(tasks_total[5m])

# Infra - Database Connections
db_connections_active
```

#### 🎮 **Exercícios práticos**
1. **Dashboard de SLIs**: Error rate, latency, throughput
2. **Business Dashboard**: KPIs de negócio (tarefas/hora)
3. **Alertas críticos**: Configurar alertas no Grafana
4. **Derived Fields**: Correlacionar logs → traces
5. **Explore Correlation**: Template de investigação

---

## 🏢 **Gerente Técnico/Arquiteto**

### 🎯 **Objetivo**: Entender ROI e estratégia de observabilidade

#### 🚀 **Start Rápido** (25 minutos)
```bash
# 1. Overview da arquitetura
./start-demo.sh status

# 2. Demonstração end-to-end
python simulate_traffic.py --mode burst --requests 20

# 3. Simular incident response
# - Detectar problema (Dashboard)
# - Investigar causa (Traces)
# - Quantificar impacto (Métricas)

# 4. Analisar custos
docker stats  # Resource usage
```

#### 📝 **O que focar**
- **Business Value**: MTTR, customer impact, SLA compliance
- **Cost vs Benefit**: Resource usage vs insights gained
- **Team Productivity**: Developer experience, debugging efficiency
- **Scalability**: Como escalar observabilidade
- **Standards**: OpenTelemetry como padrão da indústria

#### 🔍 **Métricas de valor**
```
📊 KPIs de Observabilidade:

• MTTR (Mean Time To Resolution)
• MTTD (Mean Time To Detection) 
• False Positive Rate de alertas
• Developer Productivity (time to debug)
• SLA Compliance %
• Customer Satisfaction Score

💰 Cost Analysis:
• Storage costs (metrics/logs/traces retention)
• Compute costs (collection, processing)
• Team time investment
• Tool licensing costs
```

#### 🎮 **Exercícios estratégicos**
1. **ROI Analysis**: Calcular benefício vs custo
2. **Rollout Plan**: Estratégia de adoção por equipes
3. **Training Plan**: Capacitação da equipe
4. **Vendor Selection**: Comparar soluções (OSS vs SaaS)
5. **Compliance**: Auditoria e governance

---

## 🧪 **QA/Tester**

### 🎯 **Objetivo**: Usar observabilidade para testing

#### 🚀 **Start Rápido** (15 minutos)
```bash
# 1. Subir ambiente
./start-demo.sh

# 2. Testar cenários de erro
# Interface web → Botões "Simular Erro"

# 3. Validar comportamento
# Grafana → Dashboards → "To-Do App" 
# Verificar se erros aparecem nas métricas

# 4. Performance testing
python simulate_traffic.py --mode burst --requests 50
```

#### 📝 **O que focar**
- **Error Detection**: Como erros aparecem em métricas/logs/traces
- **Performance Testing**: Usar métricas para validar SLAs
- **Synthetic Monitoring**: Testes automatizados
- **Chaos Testing**: Simular falhas e verificar observabilidade
- **Test Observability**: Instrumentar próprios testes

#### 🔍 **Scenarios de teste**
```
🧪 Test Cases com Observabilidade:

1. Functional Tests:
   ✅ Happy path → traces limpos
   ❌ Error paths → spans com erro
   
2. Performance Tests:
   📊 Load test → métricas de latência
   🔥 Stress test → profiling de CPU
   
3. Reliability Tests:
   💥 Chaos engineering → alertas funcionando
   🔄 Recovery tests → métricas voltando ao normal
```

#### 🎮 **Exercícios práticos**
1. **Error Validation**: Verificar se todos os erros são observáveis
2. **Performance SLA**: Validar se P95 < 200ms
3. **Monitoring Tests**: Testar próprios alertas
4. **End-to-end Traces**: Validar trace completo de um fluxo
5. **Test Data**: Gerar dados sintéticos para dashboards

---

## 🔒 **Security Engineer**

### 🎯 **Objetivo**: Observabilidade para segurança

#### 🚀 **Start Rápido** (20 minutos)
```bash
# 1. Analisar configuração de segurança
grep -r "password\|secret\|token" . --exclude-dir=.git

# 2. Verificar logs de auditoria
docker-compose logs todo-app | grep -E "(POST|DELETE)"

# 3. Testar attack scenarios
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "<script>alert(1)</script>"}'

# 4. Monitorar behavior
# Grafana → Explore → Loki → {service_name="todo-app"} |= "POST"
```

#### 📝 **O que focar**
- **Audit Logs**: Rastreamento de ações críticas
- **Anomaly Detection**: Padrões anômalos de acesso
- **Attack Visibility**: Como ataques aparecem em logs/metrics
- **Data Privacy**: PII em logs e traces
- **Compliance**: Logging para auditoria

#### 🔍 **Security observability**
```
🔒 Security Metrics:

• Authentication failures
• Authorization denials  
• Suspicious user agents
• Unusual request patterns
• Error rate spikes (potential DoS)
• Database injection attempts

📋 Audit Trail:
• User actions (create/update/delete)
• Admin operations
• Configuration changes
• Access patterns
```

#### 🎮 **Exercícios de segurança**
1. **Attack Detection**: Simular SQL injection, verificar logs
2. **Anomaly Alerting**: Configurar alertas para padrões suspeitos  
3. **PII Sanitization**: Verificar se dados sensíveis vazam em logs
4. **Compliance Dashboard**: Métricas para auditoria
5. **Incident Response**: Usar observabilidade para forensics

---

## 🆘 **Troubleshooting Rápido**

### ❌ **Problema**: "Não consigo acessar http://localhost:5001"
```bash
# 1. Verificar se serviços estão rodando
docker-compose ps

# 2. Verificar logs da aplicação
docker-compose logs todo-app

# 3. Verificar conectividade interna
docker-compose exec todo-app curl http://localhost:5001/health

# 4. Restart se necessário
./start-demo.sh restart
```

### ❌ **Problema**: "Dashboards vazios no Grafana"
```bash
# 1. Verificar datasources
curl http://admin:admin@localhost:3000/api/datasources

# 2. Verificar se dados estão chegando
curl http://localhost:9090/api/v1/query?query=up

# 3. Gerar tráfego
python simulate_traffic.py --mode normal --duration 2

# 4. Aguardar scrape interval (15s)
```

### ❌ **Problema**: "Traces não aparecem"
```bash
# 1. Verificar logs do Alloy
docker-compose logs alloy | grep -i trace

# 2. Verificar Tempo
docker-compose logs tempo

# 3. Testar endpoint OTLP
curl -X POST http://localhost:4318/v1/traces

# 4. Gerar traces
curl -X POST http://localhost:5001/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test trace"}'
```

---

## 📚 **Recursos Adicionais**

### 📖 **Documentação**
- **README-TODO-APP.md** - Documentação técnica detalhada
- **README-PYROSCOPE.md** - Guia específico de profiling
- **config.alloy** - Configuração comentada do pipeline

### 🔗 **Links Úteis**
- **OpenTelemetry Docs**: https://opentelemetry.io/docs/
- **Grafana Alloy**: https://grafana.com/docs/alloy/
- **PromQL Guide**: https://prometheus.io/docs/prometheus/latest/querying/basics/
- **LogQL Guide**: https://grafana.com/docs/loki/latest/logql/

### 🎓 **Próximos Estudos**
- **Distributed Tracing Patterns**
- **SLI/SLO Implementation**  
- **Cost Optimization for Observability**
- **OpenTelemetry Collector vs Alloy**
- **Production Best Practices**

---

## 🤝 **Contribuindo**

### 📝 **Melhorias Sugeridas**
- [ ] Adicionar mais cenários de erro
- [ ] Implementar alerting rules
- [ ] Criar dashboard de SLIs
- [ ] Adicionar synthetic monitoring
- [ ] Documentar patterns avançados

### 🐛 **Reportar Problemas**
Se encontrar problemas ou tiver sugestões:
1. Verifique logs: `./start-demo.sh logs`
2. Documente o erro e contexto
3. Abra issue no repositório

---

**🚀 Agora cada pessoa da equipe tem um caminho claro para aproveitar ao máximo este projeto!**

Vamos DevOpear! 🚀
