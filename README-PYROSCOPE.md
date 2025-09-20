# 🔥 Adventure Game - Profiling com Pyroscope

Este documento descreve como usar o **Pyroscope** para profiling contínuo na aplicação Adventure Game.

## 🚀 O que foi adicionado

### 1. **Serviço Pyroscope**
```yaml
# docker-compose.yml
pyroscope:
  image: grafana/pyroscope:latest
  ports:
    - "4040:4040"
  command:
    - "server"
  environment:
    - PYROSCOPE_LOG_LEVEL=debug
```

### 2. **Configuração do Alloy**
```alloy
# config.alloy
pyroscope.receive_http "default" {
  http {
    listen_address = "0.0.0.0"
    listen_port    = 4040
  }
  forward_to = [pyroscope.write.default.receiver]
}

pyroscope.write "default" {
  endpoint {
    url = "http://pyroscope:4040"
  }
}
```

### 3. **Instrumentação Python**
- ✅ Biblioteca `pyroscope-io==0.8.7` adicionada
- ✅ Classe `CustomPyroscope` implementada
- ✅ Profiling contextual com tags personalizadas

### 4. **Dashboard do Grafana**
- ✅ Datasource Pyroscope configurado
- ✅ Dashboard específico para profiling criado
- ✅ Visualizações: Flamegraph, Stats e Pie Chart

## 🎯 Como funciona

### **Profiling Automático**
```python
# Configuração automática no início da aplicação
self.profiler = CustomPyroscope(service_name="adventure")
```

### **Profiling Contextual**
```python
# Exemplo de uso com tags específicas
with self.profiler.tag_wrapper({
    "operation": "forge_heating", 
    "adventurer": self.adventurer_name
}):
    # Código que será profileado com essas tags
    if self.is_heating_forge:
        self.heat += 1
```

## 🛠️ Como executar

### 1. **Iniciar a stack completa**
```bash
docker-compose up -d
```

### 2. **Executar o jogo**
```bash
docker-compose exec alloy python main.py
```

### 3. **Acessar dashboards**
- **Grafana**: http://localhost:3000
- **Pyroscope direto**: http://localhost:4040

## 📊 Visualizações disponíveis

### **Dashboard Adventure Game - Profiling**
- **Flamegraph**: Visualização hierárquica do call stack
- **Forge Operations**: Métricas específicas das operações da forja
- **Function Call Tree**: Distribuição de tempo por função

### **Filtros disponíveis**
- **Adventurer**: Filtrar por nome do jogador
- **Operation**: Filtrar por tipo de operação
- **Time Range**: Ajustar período de análise

## 🔍 Informações coletadas

### **Tags automáticas**
```python
{
    "service.name": "adventure",
    "environment": "development", 
    "version": "1.0.0"
}
```

### **Tags contextuais**
```python
{
    "operation": "forge_heating",
    "adventurer": "nome_do_jogador"
}
```

## 🎮 Casos de uso práticos

### **1. Identificar gargalos**
- Detectar funções que consomem mais CPU
- Analisar performance por jogador
- Comparar operações diferentes

### **2. Otimização**
- Profiles antes/depois de mudanças
- Correlação com traces do OpenTelemetry
- Análise de memory leaks

### **3. Correlação com observabilidade**
- Profiles ↔ Traces (via Tempo)
- Profiles ↔ Logs (via Loki)  
- Profiles ↔ Metrics (via Prometheus)

## 🔧 Configurações avançadas

### **Ajustar frequência de sampling**
```python
pyroscope.configure(
    application_name="adventure-game",
    server_address="http://pyroscope:4040",
    sample_rate=100,  # Hz (padrão: 100)
    detect_subprocesses=True
)
```

### **Adicionar mais tags contextuais**
```python
# Em diferentes funções do jogo
with self.profiler.tag_wrapper({
    "action": "combat",
    "enemy_type": "dragon",
    "player_level": str(self.level)
}):
    # Lógica de combate
    pass
```

## 🚨 Troubleshooting

### **Pyroscope não aparece no Grafana**
1. Verificar se o serviço está rodando: `docker-compose ps pyroscope`
2. Checar logs: `docker-compose logs pyroscope`
3. Validar conexão: `curl http://localhost:4040/api/apps`

### **Sem dados de profiling**
1. Verificar se a biblioteca está instalada: `pip list | grep pyroscope`
2. Checar configuração: logs da aplicação Python
3. Validar endpoint do Alloy: `curl http://localhost:4040`

## 📈 Próximos passos

- [ ] Adicionar profiling de memória
- [ ] Implementar alertas baseados em CPU usage
- [ ] Integração com traces para correlação
- [ ] Profiling de operações de I/O

---

**Happy Profiling! 🔥🎮**
