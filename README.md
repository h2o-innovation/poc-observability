# 📝 To-Do App - Demonstração Completa de Observabilidade

> **Demo prático dos três pilares da observabilidade usando OpenTelemetry e Grafana Stack**

## 📋 **Documentação Disponível**

| Documento | Público-Alvo | Descrição |
|-----------|--------------|-----------|
| 📖 **README.md** (este) | Todos | Visão geral e início rápido |
| 🔧 **README-TODO-APP.md** | Desenvolvedores/DevOps | Documentação técnica detalhada |
| 👥 **GUIA-EQUIPE.md** | Todos os perfis | Instruções específicas por função |
| ✅ **CHECKLIST-VALIDACAO.md** | DevOps/SRE | Lista de verificação completa |
| 🔥 **README-PYROSCOPE.md** | Performance Engineers | Guia específico de profiling |

**💡 Dica**: Comece por aqui, depois vá para o guia específico do seu perfil!

---

## 🎯 O que é este projeto?

Este é um **projeto educacional** que demonstra como implementar **observabilidade completa** em uma aplicação web real. Através de uma aplicação simples de To-Do List, você aprenderá:

- 📈 **Métricas** - Como coletar e visualizar KPIs de negócio e técnicos
- 📋 **Logs** - Logging estruturado com correlação de traces  
- 🔗 **Traces** - Distributed tracing para entender o fluxo das requisições
- 🔥 **Profiling** - Análise de performance em nível de código

## 🏗️ Arquitetura da Solução

```mermaid
graph TD
    A[� Usuário] --> B[🌐 To-Do App<br/>Flask + PostgreSQL]
    B --> C[📊 OpenTelemetry<br/>Instrumentação]
    C --> D[🔄 Grafana Alloy<br/>Coletor OTEL]
    
    D --> E[📈 Prometheus<br/>Métricas]
    D --> F[📋 Loki<br/>Logs]
    D --> G[🔗 Tempo<br/>Traces]
    D --> H[🔥 Pyroscope<br/>Profiling]
    
    E --> I[📊 Grafana<br/>Dashboards]
    F --> I
    G --> I
    H --> I
```

**Stack Tecnológico:**
- **Frontend**: HTML + JavaScript (interface web simples)
- **Backend**: Flask (Python) com OpenTelemetry
- **Database**: PostgreSQL 15
- **Observabilidade**: Grafana, Prometheus, Loki, Tempo, Pyroscope
- **Coletor**: Grafana Alloy (substituto moderno do OTEL Collector)

## 🚀 Início Rápido (5 minutos)

### Pré-requisitos
```bash
# Verificar se tem Docker instalado
docker --version
docker-compose --version
```

### 1. Baixar e Executar
```bash
# 1. Clonar o repositório
git clone https://github.com/grafana/adventure.git
cd adventure

# 2. Subir toda a stack (aguarde ~2-3 minutos)
docker-compose up -d

# 3. Verificar se tudo está funcionando
docker-compose ps
```

### 2. Acessar as Aplicações
| Serviço | URL | Credenciais |
|---------|-----|-------------|
| 🌐 **To-Do App** | http://localhost:5001 | - |
| 📊 **Grafana** | http://localhost:3000 | admin / admin |
| 📈 **Prometheus** | http://localhost:9090 | - |
| 🔥 **Pyroscope** | http://localhost:4040 | - |

### 3. Gerar Dados para Observar
```bash
# Instalar dependências para simulação (opcional)
pip install requests

# Gerar tráfego automático por 2 minutos
python simulate_traffic.py --mode continuous --duration 2

# OU criar tarefas manualmente na interface web
```

### 4. Explorar os Dashboards
1. **Acesse o Grafana**: http://localhost:3000 (admin/admin)
2. **Vá para Dashboards** → Browse → **"To-Do App - Observabilidade"**
3. **Observe os dados** sendo coletados em tempo real

## 📊 O que você vai aprender?

### 📈 **Métricas - "O que está acontecendo?"**
```promql
# Exemplos de queries que você vai usar:

# 1. Taxa de requests por segundo
rate(http_requests_total[5m])

# 2. Percentil 95 de tempo de resposta  
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 3. Taxa de erro da aplicação
rate(errors_total[5m]) / rate(http_requests_total[5m]) * 100

# 4. Tarefas pendentes no sistema
tasks_total - tasks_completed_total
```

### 📋 **Logs - "Por que aconteceu?"**
```json
{
  "level": "INFO",
  "message": "Tarefa criada: 123 - Estudar observabilidade",
  "trace_id": "abc123...",
  "span_id": "def456...",
  "operation": "create_task",
  "duration_ms": 45.2,
  "task_id": 123
}
```

**Correlação Automática**: Clique no `trace_id` no log e vá direto para o trace!

### 🔗 **Traces - "Como aconteceu?"**
```
📊 Exemplo de Trace Distribuído:

HTTP Request (200ms total)
├── Flask Handler (150ms)
│   ├── Database Query (120ms) 
│   │   ├── Connection Pool (5ms)
│   │   ├── SQL Execution (110ms)
│   │   └── Result Processing (5ms)
│   ├── Business Logic (20ms)
│   └── Response Serialization (10ms)
└── HTTP Response (50ms)
```

### 🔥 **Profiling - "Onde está gastando tempo?"**
- **Flamegraphs** - Visualização hierárquica do call stack
- **Function-level performance** - Tempo gasto em cada função
- **CPU hotspots** - Onde o código está mais lento

## 🎮 Cenários de Demonstração

### 🟢 **Cenário 1: Operação Normal**
```bash
# Gerar tráfego normal
python simulate_traffic.py --mode normal --duration 3

# 👀 O que observar:
# ✅ Métricas de sucesso aumentando
# ✅ Traces limpos sem erros  
# ✅ Logs de nível INFO
# ✅ CPU usage normal no profiling
```

### 🔴 **Cenário 2: Simulação de Erros**
```bash
# Na interface web, clique em "Simular Erro DB"
# OU use o script:
python simulate_traffic.py --mode errors

# 👀 O que observar:
# ❌ Métrica errors_total aumentando
# ❌ Traces com status ERROR  
# ❌ Logs de nível ERROR com stack traces
# ❌ Correlação entre logs e traces via trace_id
```

### ⚡ **Cenário 3: Teste de Performance**
```bash
# Gerar rajadas de tráfego
python simulate_traffic.py --mode burst --requests 50 --bursts 3

# 👀 O que observar:
# 📈 Picos nas métricas
# ⏱️ Aumento na latência (P95)
# 🔥 CPU spikes no profiling
# 🔗 Traces com maior duração
```

### 🐌 **Cenário 4: Operação Lenta**
```bash
# Na interface web, clique em "Simular Lentidão"

# 👀 O que observar:
# 🐌 Traces com spans de alta duração
# ⏰ Histograma de latência com outliers  
# 🔥 Wait time no profiling
# 📋 Logs indicando operação demorada
```

## 🔍 Como Investigar um Problema Real

### 🚨 **Passo 1: Detectar**
1. **Dashboard de overview** mostra anomalia (ex: error rate alto)
2. **Alertas automáticos** (se configurados)
3. **Usuários reportando lentidão**

### 🔍 **Passo 2: Investigar**
1. **Métricas** → Identificar quando e onde o problema começou
2. **Logs** → Filtrar por ERROR/WARN no período afetado  
3. **Trace ID** → Copiar do log para investigação detalhada

### 📊 **Passo 3: Analisar Root Cause**
1. **Tempo** → Abrir trace específico usando trace_id
2. **Span Analysis** → Encontrar span com erro ou alta latência
3. **Pyroscope** → Se for problema de performance, analisar profiling

### 💡 **Exemplo Prático:**
```
🔍 "Por que as requests estão lentas?"

1. Dashboard: P95 latency subiu de 100ms para 2s
   ↓
2. Métricas: Problema começou às 14:30  
   ↓
3. Logs: Filtrar por timestamp e encontrar errors
   ↓
4. Trace: Copiar trace_id de um log de erro
   ↓  
5. Tempo: Analisar trace → span "database_query" demorou 1.8s
   ↓
6. Root Cause: Query SQL específica está lenta
```

## 📚 Conceitos Fundamentais

### 🎯 **Os Três Pilares da Observabilidade**

| Pilar | O que é? | Quando usar? |
|-------|----------|--------------|
| **📈 Métricas** | Agregações numéricas (CPU, requests/sec, erro %) | Alertas, SLIs, tendências |
| **📋 Logs** | Eventos discretos com contexto textual | Debug, audit trail, troubleshooting |
| **🔗 Traces** | Jornada de uma request pelo sistema | Performance, distributed debugging |

### 🔧 **OpenTelemetry (OTEL)**
- **Instrumentação automática**: Flask, PostgreSQL, HTTP clients
- **Instrumentação manual**: Spans customizados, métricas de negócio
- **Correlação**: trace_id conecta logs, métricas e traces
- **Padronização**: Um SDK para todas as linguagens

### 📊 **Grafana Observability Stack**
- **Alloy**: Coletor moderno, substitui OTEL Collector
- **Prometheus**: Time-series database para métricas
- **Loki**: Log aggregation (like Prometheus for logs)
- **Tempo**: Distributed tracing backend  
- **Pyroscope**: Continuous profiling platform

## 🛠️ Estrutura do Projeto

```
adventure/
├── 📝 todo_app.py              # Aplicação principal Flask
├── 🔧 otel.py                  # Configuração OpenTelemetry
├── ⚙️ config.alloy             # Configuração Grafana Alloy  
├── 🐳 docker-compose.yml       # Stack completa
├── 📊 grafana/                 # Dashboards e datasources
│   ├── dashboards/
│   │   ├── todo-app.json       # Dashboard principal
│   │   ├── profiling.json      # Dashboard de profiling
│   │   └── adventure.json      # Dashboard do jogo original
│   └── datasources/
│       └── default.yml         # Configuração dos datasources
├── 🔧 prometheus.yml           # Configuração Prometheus
├── 📋 loki-config.yaml         # Configuração Loki
├── 🔗 tempo.yaml               # Configuração Tempo
├── 📦 requirements.txt         # Dependências Python
├── 🚀 start-demo.sh            # Script de início rápido
├── 📈 simulate_traffic.py      # Gerador de tráfego
└── 📚 README.md                # Esta documentação
```

## 🎯 Funcionalidades da Aplicação

### 🌐 **Interface Web** (http://localhost:5001)
- ✅ **Criar tarefas** - Adicionar novas tarefas
- ✅ **Listar tarefas** - Ver todas as tarefas  
- ✅ **Completar tarefas** - Marcar como concluída
- ✅ **Deletar tarefas** - Remover tarefas
- ⚠️ **Simular erros** - Botões para testar observabilidade

### 🔌 **API REST** 
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Interface web |
| GET | `/api/tasks` | Listar tarefas |
| POST | `/api/tasks` | Criar tarefa |
| POST | `/api/tasks/{id}/complete` | Completar tarefa |
| DELETE | `/api/tasks/{id}` | Deletar tarefa |
| POST | `/api/simulate-error/{type}` | Simular erros |
| GET | `/health` | Health check |

### 💥 **Tipos de Erro para Demonstração**
- **`db`** - Erro de banco (SQL inválido)
- **`timeout`** - Timeout simulado  
- **`500`** - Erro interno do servidor
- **`slow`** - Operação lenta (2-5s)

## 🔧 Troubleshooting

### ❌ **Aplicação não inicia**
```bash
# Verificar logs da aplicação
docker-compose logs todo-app

# Verificar PostgreSQL
docker-compose logs postgres

# Restartar serviços
docker-compose restart todo-app postgres
```

### ❌ **Métricas não aparecem no Grafana**
```bash
# Verificar Alloy (coletor)
docker-compose logs alloy

# Verificar Prometheus
curl http://localhost:9090/api/v1/query?query=up

# Testar endpoint OTLP
curl http://localhost:4318/v1/metrics -X POST
```

### ❌ **Traces não aparecem no Tempo**  
```bash
# Verificar logs do Tempo
docker-compose logs tempo

# Verificar conectividade
curl http://localhost:3200/api/traces

# Verificar Alloy está enviando traces
docker-compose logs alloy | grep -i trace
```

### ❌ **Dashboards vazios no Grafana**
```bash
# Verificar datasources
curl http://admin:admin@localhost:3000/api/datasources

# Restartar Grafana
docker-compose restart grafana

# Verificar tempo de retenção dos dados
```

## 🚀 Próximos Passos

### 📖 **Para Aprofundar Conhecimento**
- [ ] Configurar **alertas** no Prometheus/Grafana
- [ ] Implementar **SLI/SLO** dashboards  
- [ ] Estudar **sampling strategies** no tracing
- [ ] Explorar **custom metrics** de negócio
- [ ] Adicionar **cache layer** (Redis) com observabilidade

### 🏢 **Para Ambiente de Produção**
- [ ] Configurar **retenção** adequada de dados
- [ ] Implementar **high availability** dos componentes
- [ ] Adicionar **security** (TLS, autenticação)
- [ ] Configurar **backup** e **disaster recovery**
- [ ] Implementar **cost optimization**

### 🔬 **Para Experimentos Avançados**
- [ ] **Chaos Engineering** - Simular falhas reais
- [ ] **Synthetic Monitoring** - Testes automatizados
- [ ] **Multi-service tracing** - Adicionar mais serviços
- [ ] **Custom OpenTelemetry Collector** - Configurações avançadas

## 🎉 Conclusão

Este projeto é uma **implementação completa e realista** dos três pilares da observabilidade usando **ferramentas modernas de mercado**.

**🎯 O que você consegue fazer após este projeto:**
- ✅ Implementar observabilidade em qualquer aplicação
- ✅ Usar Grafana Stack em produção
- ✅ Troubleshoot problemas usando traces correlacionados
- ✅ Criar dashboards efetivos para monitoramento
- ✅ Entender OpenTelemetry na prática

**💼 Skills desenvolvidas:**
- **Observabilidade** - Métricas, logs, traces, profiling
- **Grafana Stack** - Prometheus, Loki, Tempo, Pyroscope, Alloy
- **OpenTelemetry** - Instrumentação automática e manual
- **Troubleshooting** - Investigação de problemas em produção
- **Performance** - Análise e otimização de aplicações

---

## 📖 Documentação Adicional

- 📝 **README-TODO-APP.md** - Documentação técnica detalhada
- 🎮 **Projeto Adventure Game** - Demo alternativa (main.py)
- 🔥 **README-PYROSCOPE.md** - Específico sobre profiling

---

**🚀 Pronto para começar? Execute os comandos do "Início Rápido" e comece a explorar!**

---

> 💡 **Dica**: Este projeto é opensource e está sempre evoluindo. Contribuições são bem-vindas!

---

# 🎮 Adventure Game (Projeto Original)

<!-- INTERACTIVE ignore START -->

<div align="center">
<img src="https://raw.githubusercontent.com/grafana/adventure/main/img/logo.png" alt="Quest" width="200"/>
</div>

<!-- INTERACTIVE ignore END -->

Quest World é um jogo de aventura em texto com observabilidade integrada. Neste jogo, você embarca em uma jornada através de um mundo místico, interagindo com personagens, explorando locais e fazendo escolhas que moldam seu destino. O jogo foi projetado para ensinar conceitos de observabilidade enquanto você embarca em uma aventura emocionante.

Confira nosso blog post [aqui](https://grafana.com/blog/2024/11/20/metrics-logs-traces-and-mayhem-introducing-an-observability-adventure-game-powered-by-grafana-alloy-and-otel/) para saber mais sobre o jogo.

<!-- INTERACTIVE ignore START -->
## Executar em Ambiente Sandbox

Você pode jogar Quest World em um ambiente sandbox. A VM online é pré-configurada com todos os componentes necessários para executar o jogo. Clique no botão abaixo para iniciar a VM e começar a jogar.

<div align="center">
  <a href="https://killercoda.com/grafana-labs/course/workshops/adventure">
    <img src="https://raw.githubusercontent.com/grafana/adventure/main/img/launch.png" alt="Quest" width="200"/>
  </a>
</div>

E siga as instruções [aqui](killercoda-sandbox.md).

## Executar com Docker

Você pode executar Quest World em sua máquina local usando Docker. Siga as instruções abaixo para começar.

1. Clone o repositório

   ```bash
   git clone https://github.com/grafana/adventure.git
   ```

2. Navegue para o diretório `adventure`

   ```bash
   cd adventure
   ```

3. Suba a Stack de Observabilidade usando Docker Compose

   ```bash
   docker compose up -d
   ```

Em vez de usar um [ambiente virtual python](#instalação-com-python), você pode executar o jogo em um container Docker com os seguintes passos.

1. Primeiro construa a imagem Docker:

   ```bash
   docker build -t adventure:latest .
   ```
   
   **Nota**: Certifique-se de estar no nível superior do diretório `adventure`.

1. Execute o container:

   ```bash
   docker run -it --network=adventure_adventure --name adventure -e SETUP=docker adventure:latest
   ```

Uma vez iniciado, confira as [instruções de jogo](#instruções-de-jogo)

Quando você **terminar de jogar**, para limpar seu ambiente execute:

```bash
docker stop adventure
docker compose down
```

<!-- INTERACTIVE ignore END -->

## Instalação com Python

Se você preferir usar um ambiente virtual python, siga as instruções abaixo.

1. Clone o repositório

   ```bash
   git clone https://github.com/grafana/adventure.git
   ```

2. Navegue para o diretório `adventure`

   ```bash
   cd adventure
   ```

3. Suba a Stack de Observabilidade usando Docker Compose

   ```bash
   docker compose up -d
   ```

Quest World roda como uma aplicação python. Nossa forma recomendada de instalá-lo é usando um ambiente virtual.

1. Crie um ambiente virtual

   ```bash
   python3.12 -m venv .venv
   ```

2. Ative o ambiente virtual

   ```bash
   source .venv/bin/activate
   ```

3. Atualize o pip

   ```bash
   pip install --upgrade pip
   ```

4. Instale as dependências necessárias

   ```bash
   pip install -r requirements.txt
   ```

5. Execute a aplicação

   ```bash
   python main.py
   ```

## Instruções de Jogo

- Ao iniciar o jogo, você receberá uma descrição de sua localização atual e uma lista de ações disponíveis.
- Digite o comando correspondente à ação que deseja realizar e pressione **Enter**.
- O jogo continua baseado em suas entradas e escolhas.
- Este jogo envolve verificar dashboards do Grafana para progredir. Você pode acessar o dashboard do Grafana em `http://localhost:3000`. Verifique o dashboard para dicas e pistas.

### Comandos Disponíveis

A qualquer momento, você pode digitar `list actions` para ver os comandos disponíveis em sua localização atual.

Alguns comandos universais incluem:

- `quit` ou `exit`: Encerrar o jogo.
- `list actions`: Exibir ações disponíveis.

**Ações de Exemplo**:

- **Movimento**:
  - `go north`
  - `go south`
  - `go to town`
- **Interações**:
  - `request sword`
  - `pick herb`
  - `explore`
  - `accept quest`
  - `look at sword`
  - `pray`
- **Comandos Especiais**:
  - `cheat` (para obter uma espada imediatamente; não recomendado).

*Nota*: Nem todas as ações estão disponíveis em todos os locais. Algumas ações podem exigir certas condições a serem atendidas ou pré-requisitos a serem cumpridos.

### Dicas para Jogar

- **Explore Completamente**: Não hesite em tentar diferentes ações para descobrir elementos ocultos.
- **Gerencie Seus Itens**: Mantenha o controle de itens como espadas e ervas; eles podem afetar suas interações.
- **Interaja com Personagens**: Conversar com NPCs como o ferreiro, mago ou padre pode abrir novos caminhos.
- **Monitore o Calor da Forja**: Quando no ferreiro, você precisará gerenciar o calor da forja para obter sua espada.
- **Cuidado com as Escolhas**: Algumas decisões, como aceitar a oferta do mago, têm consequências.

Lembre-se, o jogo é dinâmico e suas escolhas podem levar a diferentes resultados. Aproveite a aventura!


<!-- INTERACTIVE page intro.md END -->

<!-- INTERACTIVE page step1.md START -->

## Installation with Python

If you prefer to use a python virtual environment, follow the instructions below.

1. Clone the repository

   ```bash
   git clone https://github.com/grafana/adventure.git
   ```

2. Navigate to the `adventure` directory

   ```bash
   cd adventure
   ```

3. Spin up the Observability Stack using Docker Compose

   ```bash
   docker compose up -d
   ```

Quest World runs as a python application our recommended way to install it is to use a virtual environment.

1. Create a virtual environment

   ```bash
   python3.12 -m venv .venv
   ```

2. Activate the virtual environment

   ```bash
   source .venv/bin/activate
   ```

3. Upgrade pip

   ```bash
   pip install --upgrade pip
   ```

4. Install the required dependencies

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application

   ```bash
   python main.py
   ```

<!-- INTERACTIVE page step1.md END -->

<!-- INTERACTIVE page step2.md START -->

## Gameplay Instructions

- Upon starting the game, you will receive a description of your current location and a list of available actions.
- Type the command corresponding to the action you want to take and press **Enter**.
- The game continues based on your inputs and choices.
- This game involves checking Grafana dashboards to progress. You can access the Grafana dashboard at `http://localhost:3000`. Check the dashboard for hints and clues.

### Available Commands

At any point, you can type `list actions` to see the available commands in your current location.

Some universal commands include:

- `quit` or `exit`: End the game.
- `list actions`: Display available actions.

**Sample Actions**:

- **Movement**:
  - `go north`
  - `go south`
  - `go to town`
- **Interactions**:
  - `request sword`
  - `pick herb`
  - `explore`
  - `accept quest`
  - `look at sword`
  - `pray`
- **Special Commands**:
  - `cheat` (to obtain a sword immediately; not recommended).

*Note*: Not all actions are available in every location. Some actions may require certain conditions to be met or prerequisites to be fulfilled.

### Tips for Playing

- **Explore Thoroughly**: Don't hesitate to try different actions to discover hidden elements.
- **Manage Your Items**: Keep track of items like swords and herbs; they can affect your interactions.
- **Interact with Characters**: Talking to NPCs like the blacksmith, wizard, or priest can open new paths.
- **Monitor Forge Heat**: When at the blacksmith, you'll need to manage the forge's heat to get your sword.
- **Beware of Choices**: Some decisions, like accepting the wizard's offer, have consequences.

### Sample Gameplay Flow

1. **Starting Out**:
   - You're at the starting point with the option to `go north` or `cheat`.
   - Typing `go north` takes you to the forest.

2. **In the Forest**:
   - Options include `go north` to the cave, `go south` back to start, `go to town`, or `pick herb`.
   - You might choose to `pick herb` and then `go to town`.

3. **In the Town**:
   - Several locations to explore: `blacksmith`, `mysterious man`, `quest giver`, `chapel`.
   - Visit the `blacksmith` to `request sword`.

4. **At the Blacksmith**:
   - After requesting a sword, you'll need to `heat forge` and `check sword` periodically.
   - Adjust the forge heat using `heat forge` and `cool forge` until the sword is ready.

5. **Getting the Sword**:
   - Once the forge is at the correct temperature, `check sword` will let you obtain it.
   - With the sword, you can interact with other characters differently.

6. **Meeting the Wizard**:
   - Return to town and choose `mysterious man` to meet the wizard (requires having a sword).
   - Decide whether to `accept his offer` or `decline his offer`.

7. **Accepting a Quest**:
   - Visit the `quest giver` to `accept quest`.
   - Your ability to complete the quest may depend on previous choices.

8. **Visiting the Chapel**:
   - Go to the `chapel` and `look at sword` to interact with the priest.
   - The priest can bless your sword, especially if it's been cursed.

<!-- INTERACTIVE page step2.md END -->

<!-- INTERACTIVE page finish.md START -->

Remember, the game is dynamic, and your choices can lead to different outcomes. Enjoy the adventure!

<!-- INTERACTIVE page finish.md END -->
