from flask import Flask, request, jsonify, render_template_string
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging
import time
import random
from datetime import datetime
from otel import CustomLogFW, CustomMetrics, CustomTracer, CustomPyroscope

# Configuração do Flask
app = Flask(__name__)

# Template HTML simples
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>📝 To-Do App - Observabilidade Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        .task { background: white; margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; }
        .completed { border-left-color: #28a745; opacity: 0.7; }
        .error { border-left-color: #dc3545; background: #ffe6e6; }
        input, button { padding: 10px; margin: 5px; }
        button { background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
        .error-btn { background: #dc3545; }
        .warning-btn { background: #ffc107; color: black; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 To-Do List - Demo Observabilidade</h1>
        
        <h2>Adicionar Nova Tarefa</h2>
        <input type="text" id="taskTitle" placeholder="Título da tarefa" style="width: 300px;">
        <button onclick="addTask()">Adicionar</button>
        
        <h2>Simulação de Erros</h2>
        <button class="error-btn" onclick="simulateError('db')">Simular Erro DB</button>
        <button class="error-btn" onclick="simulateError('timeout')">Simular Timeout</button>
        <button class="error-btn" onclick="simulateError('500')">Simular 500</button>
        <button class="warning-btn" onclick="simulateError('slow')">Simular Lentidão</button>
        
        <h2>Tarefas</h2>
        <div id="tasks"></div>
    </div>

    <script>
        // Carregar tarefas ao iniciar
        loadTasks();

        function addTask() {
            const title = document.getElementById('taskTitle').value;
            if (!title) return;
            
            fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: title})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('taskTitle').value = '';
                loadTasks();
            })
            .catch(error => console.error('Erro:', error));
        }

        function loadTasks() {
            fetch('/api/tasks')
            .then(response => response.json())
            .then(tasks => {
                const tasksDiv = document.getElementById('tasks');
                tasksDiv.innerHTML = tasks.map(task => 
                    `<div class="task ${task.completed ? 'completed' : ''}">
                        <strong>${task.title}</strong>
                        <br><small>ID: ${task.id} | Criado: ${task.created_at}</small>
                        <br>
                        ${!task.completed ? 
                            `<button onclick="completeTask(${task.id})">Completar</button>` : 
                            '<span style="color: green;">✓ Concluída</span>'
                        }
                        <button class="error-btn" onclick="deleteTask(${task.id})">Deletar</button>
                    </div>`
                ).join('');
            })
            .catch(error => console.error('Erro:', error));
        }

        function completeTask(id) {
            fetch(`/api/tasks/${id}/complete`, {method: 'POST'})
            .then(() => loadTasks())
            .catch(error => console.error('Erro:', error));
        }

        function deleteTask(id) {
            fetch(`/api/tasks/${id}`, {method: 'DELETE'})
            .then(() => loadTasks())
            .catch(error => console.error('Erro:', error));
        }

        function simulateError(type) {
            fetch(`/api/simulate-error/${type}`, {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                alert(`Erro simulado: ${data.message}`);
                loadTasks();
            })
            .catch(error => {
                alert(`Erro real capturado: ${error.message}`);
            });
        }

        // Auto-refresh a cada 30 segundos
        setInterval(loadTasks, 30000);
    </script>
</body>
</html>
"""

class TodoApp:
    def __init__(self):
        # Configurar observabilidade
        self.setup_observability()
        
        # Configurar banco de dados
        self.setup_database()
        
    def setup_observability(self):
        """Configura todas as ferramentas de observabilidade"""
        service_name = "todo-app"
        
        # Logs
        logFW = CustomLogFW(service_name=service_name)
        handler = logFW.setup_logging()
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Métricas
        metrics_service = CustomMetrics(service_name=service_name)
        self.meter = metrics_service.get_meter()
        
        # Traces
        tracer_service = CustomTracer(service_name=service_name)
        self.trace = tracer_service.get_trace()
        self.tracer = self.trace.get_tracer(service_name)
        
        # Profiling
        self.profiler = CustomPyroscope(service_name=service_name, application_name="todo-app")
        
        # Criar métricas customizadas
        self.setup_metrics()
        
        self.logger.info("Observabilidade configurada com sucesso")
    
    def setup_metrics(self):
        """Configura métricas específicas da aplicação"""
        # Contador de requests HTTP
        self.http_requests_counter = self.meter.create_counter(
            name="http_requests_total",
            description="Total de requests HTTP"
        )
        
        # Contador de operações no banco
        self.db_operations_counter = self.meter.create_counter(
            name="db_operations_total", 
            description="Total de operações no banco de dados"
        )
        
        # Histograma de tempo de resposta
        self.response_time_histogram = self.meter.create_histogram(
            name="http_request_duration_seconds",
            description="Tempo de resposta das requisições HTTP"
        )
        
        # Contador de erros
        self.error_counter = self.meter.create_counter(
            name="errors_total",
            description="Total de erros na aplicação"
        )
        
        # Métricas simples
        self.tasks_counter = self.meter.create_counter(
            name="tasks_total",
            description="Total de tarefas criadas",
            unit="1"
        )
        
        self.completed_tasks_counter = self.meter.create_counter(
            name="tasks_completed_total", 
            description="Total de tarefas completadas",
            unit="1"
        )
        
        # Métrica para duração das operações
        self.operation_duration = self.meter.create_histogram(
            name="operation_duration_seconds",
            description="Duração das operações em segundos",
            unit="s"
        )
    
    def update_task_metrics(self):
        """Atualiza métricas de tarefas manualmente"""
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Conta total de tarefas
                    cur.execute("SELECT COUNT(*) FROM tasks")
                    total_tasks = cur.fetchone()[0]
                    
                    # Conta tarefas completadas  
                    cur.execute("SELECT COUNT(*) FROM tasks WHERE completed = true")
                    completed_tasks = cur.fetchone()[0]
                    
                    self.logger.info(f"Métricas atualizadas - Total: {total_tasks}, Completadas: {completed_tasks}")
        except Exception as e:
            self.logger.error(f"Erro ao atualizar métricas: {e}")
    
    def setup_database(self):
        """Configura e inicializa o banco de dados"""
        self.db_config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'database': os.environ.get('DB_NAME', 'todoapp'),
            'user': os.environ.get('DB_USER', 'todouser'),
            'password': os.environ.get('DB_PASSWORD', 'todopass'),
            'port': os.environ.get('DB_PORT', '5432')
        }
        
        # Criar tabelas se não existirem
        self.create_tables()
        
    def get_db_connection(self):
        """Obtém conexão com o banco de dados"""
        return psycopg2.connect(**self.db_config)
    
    def create_tables(self):
        """Cria as tabelas necessárias"""
        with self.tracer.start_as_current_span("create_tables") as span:
            try:
                with self.get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS tasks (
                                id SERIAL PRIMARY KEY,
                                title VARCHAR(255) NOT NULL,
                                completed BOOLEAN DEFAULT FALSE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                        """)
                        conn.commit()
                        
                span.set_attribute("operation", "create_tables")
                span.set_attribute("success", True)
                self.logger.info("Tabelas criadas/verificadas com sucesso")
                
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                self.logger.error(f"Erro ao criar tabelas: {e}")
                raise

# Instância global da aplicação
todo_app = TodoApp()

@app.before_request
def before_request():
    """Middleware para capturar início das requisições"""
    request.start_time = time.time()
    
    # Incrementar contador de requests
    todo_app.http_requests_counter.add(1, {
        "method": request.method,
        "endpoint": request.endpoint or "unknown"
    })

@app.after_request
def after_request(response):
    """Middleware para capturar fim das requisições"""
    duration = time.time() - request.start_time
    
    # Registrar tempo de resposta
    todo_app.response_time_histogram.record(duration, {
        "method": request.method,
        "status_code": str(response.status_code),
        "endpoint": request.endpoint or "unknown"
    })
    
    # Log da requisição
    todo_app.logger.info(
        f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s",
        extra={
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration": duration,
            "user_agent": request.headers.get('User-Agent', '')
        }
    )
    
    return response

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Listar todas as tarefas"""
    with todo_app.tracer.start_as_current_span("get_tasks") as span:
        with todo_app.profiler.tag_wrapper({"operation": "list_tasks"}):
            try:
                with todo_app.get_db_connection() as conn:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
                        tasks = cur.fetchall()
                        
                        # Converter datetime para string
                        for task in tasks:
                            if task['created_at']:
                                task['created_at'] = task['created_at'].isoformat()
                            if task['updated_at']:
                                task['updated_at'] = task['updated_at'].isoformat()
                
                todo_app.db_operations_counter.add(1, {"operation": "select", "table": "tasks"})
                span.set_attribute("tasks_count", len(tasks))
                span.set_attribute("success", True)
                
                todo_app.logger.info(f"Listadas {len(tasks)} tarefas")
                return jsonify(tasks)
                
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                todo_app.error_counter.add(1, {"operation": "get_tasks", "error_type": "database"})
                todo_app.logger.error(f"Erro ao listar tarefas: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Criar uma nova tarefa"""
    with todo_app.tracer.start_as_current_span("create_task") as span:
        with todo_app.profiler.tag_wrapper({"operation": "create_task"}):
            try:
                data = request.get_json()
                title = data.get('title', '').strip()
                
                if not title:
                    span.set_attribute("success", False)
                    span.set_attribute("error", "missing_title")
                    return jsonify({"error": "Título é obrigatório"}), 400
                
                with todo_app.get_db_connection() as conn:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute(
                            "INSERT INTO tasks (title) VALUES (%s) RETURNING *",
                            (title,)
                        )
                        task = cur.fetchone()
                        conn.commit()
                
                todo_app.db_operations_counter.add(1, {"operation": "insert", "table": "tasks"})
                todo_app.tasks_counter.add(1, {"operation": "created"})
                span.set_attribute("task_id", task['id'])
                span.set_attribute("success", True)
                
                todo_app.logger.info(f"Tarefa criada: {task['id']} - {title}")
                
                # Converter datetime para string
                if task['created_at']:
                    task['created_at'] = task['created_at'].isoformat()
                if task['updated_at']:
                    task['updated_at'] = task['updated_at'].isoformat()
                
                return jsonify(task), 201
                
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                todo_app.error_counter.add(1, {"operation": "create_task", "error_type": "database"})
                todo_app.logger.error(f"Erro ao criar tarefa: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Marcar tarefa como completada"""
    with todo_app.tracer.start_as_current_span("complete_task") as span:
        with todo_app.profiler.tag_wrapper({"operation": "complete_task"}):
            try:
                with todo_app.get_db_connection() as conn:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute(
                            "UPDATE tasks SET completed = true, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
                            (task_id,)
                        )
                        task = cur.fetchone()
                        conn.commit()
                        
                        if not task:
                            span.set_attribute("success", False)
                            span.set_attribute("error", "task_not_found")
                            return jsonify({"error": "Tarefa não encontrada"}), 404
                
                todo_app.db_operations_counter.add(1, {"operation": "update", "table": "tasks"})
                todo_app.completed_tasks_counter.add(1, {"operation": "completed"})
                span.set_attribute("task_id", task_id)
                span.set_attribute("success", True)
                
                todo_app.logger.info(f"Tarefa completada: {task_id}")
                
                # Converter datetime para string
                if task['created_at']:
                    task['created_at'] = task['created_at'].isoformat()
                if task['updated_at']:
                    task['updated_at'] = task['updated_at'].isoformat()
                
                return jsonify(task)
                
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                todo_app.error_counter.add(1, {"operation": "complete_task", "error_type": "database"})
                todo_app.logger.error(f"Erro ao completar tarefa {task_id}: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deletar uma tarefa"""
    with todo_app.tracer.start_as_current_span("delete_task") as span:
        with todo_app.profiler.tag_wrapper({"operation": "delete_task"}):
            try:
                with todo_app.get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                        
                        if cur.rowcount == 0:
                            span.set_attribute("success", False)
                            span.set_attribute("error", "task_not_found")
                            return jsonify({"error": "Tarefa não encontrada"}), 404
                        
                        conn.commit()
                
                todo_app.db_operations_counter.add(1, {"operation": "delete", "table": "tasks"})
                span.set_attribute("task_id", task_id)
                span.set_attribute("success", True)
                
                todo_app.logger.info(f"Tarefa deletada: {task_id}")
                return jsonify({"message": "Tarefa deletada com sucesso"})
                
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                todo_app.error_counter.add(1, {"operation": "delete_task", "error_type": "database"})
                todo_app.logger.error(f"Erro ao deletar tarefa {task_id}: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/simulate-error/<error_type>', methods=['POST'])
def simulate_error(error_type):
    """Simular diferentes tipos de erros para demonstração"""
    with todo_app.tracer.start_as_current_span("simulate_error") as span:
        span.set_attribute("error_type", error_type)
        
        try:
            if error_type == "db":
                # Simular erro de banco de dados
                with todo_app.get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT * FROM tabela_inexistente")
                        
            elif error_type == "timeout":
                # Simular timeout
                time.sleep(10)
                return jsonify({"message": "Não deveria chegar aqui"})
                
            elif error_type == "500":
                # Simular erro 500
                raise Exception("Erro simulado intencionalmente")
                
            elif error_type == "slow":
                # Simular operação lenta
                with todo_app.profiler.tag_wrapper({"operation": "slow_operation"}):
                    time.sleep(random.uniform(2, 5))
                    span.set_attribute("slow_operation", True)
                    span.set_attribute("sleep_time", 3)
                    todo_app.logger.warning("Operação lenta simulada")
                    return jsonify({"message": "Operação lenta concluída"})
            
            else:
                return jsonify({"error": "Tipo de erro desconhecido"}), 400
                
        except Exception as e:
            span.set_attribute("success", False)
            span.set_attribute("error", str(e))
            todo_app.error_counter.add(1, {
                "operation": "simulate_error", 
                "error_type": error_type,
                "simulated": "true"
            })
            todo_app.logger.error(f"Erro simulado ({error_type}): {e}")
            return jsonify({"error": f"Erro simulado: {str(e)}"}), 500

@app.route('/health')
def health_check():
    """Health check para monitoramento"""
    try:
        # Testar conexão com banco
        with todo_app.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "todo-app"
        })
    except Exception as e:
        todo_app.logger.error(f"Health check falhou: {e}")
        return jsonify({
            "status": "unhealthy", 
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 503

if __name__ == '__main__':
    # Configurar nível de log
    logging.basicConfig(level=logging.INFO)
    
    # Iniciar aplicação
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )
