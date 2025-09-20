#!/usr/bin/env python3
"""
Script para simular tráfego e erros na aplicação To-Do
para demonstrar funcionalidades de observabilidade.
"""

import requests
import time
import random
import threading
import json
from datetime import datetime

class TodoTrafficSimulator:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.running = False
        
        # Lista de tarefas de exemplo
        self.sample_tasks = [
            "Implementar dashboard de métricas",
            "Configurar alertas do Prometheus", 
            "Documentar arquitetura da aplicação",
            "Revisar logs de erro da aplicação",
            "Otimizar consultas no banco de dados",
            "Implementar cache para consultas frequentes",
            "Configurar backup automático",
            "Atualizar dependências do projeto",
            "Implementar testes de integração",
            "Configurar CI/CD pipeline",
            "Revisar segurança da aplicação",
            "Implementar rate limiting",
            "Configurar monitoramento de rede",
            "Otimizar imagens Docker",
            "Implementar health checks"
        ]
    
    def check_health(self):
        """Verifica se a aplicação está rodando"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Aplicação não está acessível: {e}")
            return False
    
    def create_random_task(self):
        """Cria uma tarefa aleatória"""
        try:
            task_title = random.choice(self.sample_tasks)
            response = self.session.post(
                f"{self.base_url}/api/tasks",
                json={"title": task_title},
                timeout=10
            )
            
            if response.status_code == 201:
                task = response.json()
                print(f"✅ Tarefa criada: {task['id']} - {task_title}")
                return task['id']
            else:
                print(f"❌ Erro ao criar tarefa: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na requisição de criação: {e}")
            return None
    
    def list_tasks(self):
        """Lista todas as tarefas"""
        try:
            response = self.session.get(f"{self.base_url}/api/tasks", timeout=10)
            if response.status_code == 200:
                tasks = response.json()
                print(f"📋 Listadas {len(tasks)} tarefas")
                return tasks
            else:
                print(f"❌ Erro ao listar tarefas: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erro na requisição de listagem: {e}")
            return []
    
    def complete_random_task(self, tasks):
        """Completa uma tarefa aleatória"""
        incomplete_tasks = [t for t in tasks if not t['completed']]
        if not incomplete_tasks:
            return False
            
        try:
            task = random.choice(incomplete_tasks)
            response = self.session.post(
                f"{self.base_url}/api/tasks/{task['id']}/complete",
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Tarefa completada: {task['id']}")
                return True
            else:
                print(f"❌ Erro ao completar tarefa: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição de completar: {e}")
            return False
    
    def delete_random_task(self, tasks):
        """Deleta uma tarefa aleatória"""
        if not tasks:
            return False
            
        try:
            task = random.choice(tasks)
            response = self.session.delete(
                f"{self.base_url}/api/tasks/{task['id']}",
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"🗑️ Tarefa deletada: {task['id']}")
                return True
            else:
                print(f"❌ Erro ao deletar tarefa: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição de deletar: {e}")
            return False
    
    def simulate_error(self, error_type):
        """Simula um tipo específico de erro"""
        try:
            print(f"🔥 Simulando erro: {error_type}")
            response = self.session.post(
                f"{self.base_url}/api/simulate-error/{error_type}",
                timeout=15
            )
            
            if response.status_code >= 500:
                print(f"💥 Erro simulado com sucesso: {error_type}")
            else:
                result = response.json()
                print(f"⚠️ Resposta da simulação: {result.get('message', 'N/A')}")
                
        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout simulado com sucesso: {error_type}")
        except Exception as e:
            print(f"💥 Erro capturado durante simulação: {e}")
    
    def normal_workflow(self):
        """Simula um fluxo normal de trabalho"""
        print("\n🔄 Iniciando fluxo normal de trabalho...")
        
        # Listar tarefas existentes
        tasks = self.list_tasks()
        
        # Criar algumas tarefas
        for _ in range(random.randint(1, 3)):
            self.create_random_task()
            time.sleep(random.uniform(0.5, 2))
        
        # Listar novamente
        tasks = self.list_tasks()
        
        # Completar algumas tarefas
        if tasks and random.random() > 0.3:
            self.complete_random_task(tasks)
        
        # Deletar algumas tarefas ocasionalmente
        if tasks and random.random() > 0.7:
            self.delete_random_task(tasks)
    
    def error_simulation_workflow(self):
        """Simula vários tipos de erros"""
        print("\n💥 Iniciando simulação de erros...")
        
        error_types = ["db", "timeout", "500", "slow"]
        selected_errors = random.sample(error_types, random.randint(1, 2))
        
        for error_type in selected_errors:
            self.simulate_error(error_type)
            time.sleep(random.uniform(1, 3))
    
    def continuous_traffic(self, duration_minutes=10):
        """Gera tráfego contínuo por um período específico"""
        print(f"\n🚀 Iniciando tráfego contínuo por {duration_minutes} minutos...")
        
        if not self.check_health():
            print("❌ Aplicação não está acessível. Verifique se ela está rodando.")
            return
        
        self.running = True
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        request_count = 0
        error_count = 0
        
        while self.running and time.time() < end_time:
            try:
                # 70% fluxo normal, 30% simulação de erros
                if random.random() < 0.7:
                    self.normal_workflow()
                else:
                    self.error_simulation_workflow()
                
                request_count += 1
                
                # Pausa entre operações
                time.sleep(random.uniform(2, 8))
                
            except KeyboardInterrupt:
                print("\n⏹️ Interrompido pelo usuário")
                break
            except Exception as e:
                error_count += 1
                print(f"❌ Erro durante simulação: {e}")
                time.sleep(5)  # Pausa maior em caso de erro
        
        self.running = False
        elapsed = time.time() - start_time
        
        print(f"\n📊 Simulação concluída:")
        print(f"   ⏱️ Tempo total: {elapsed:.1f}s")
        print(f"   📈 Requests executados: {request_count}")
        print(f"   ❌ Erros encontrados: {error_count}")
    
    def burst_test(self, requests_per_burst=10, bursts=3):
        """Executa um teste de rajada para estressar a aplicação"""
        print(f"\n⚡ Teste de rajada: {requests_per_burst} requests x {bursts} rajadas")
        
        if not self.check_health():
            return
        
        for burst in range(bursts):
            print(f"\n🔥 Rajada {burst + 1}/{bursts}")
            
            # Criar threads para requisições simultâneas
            threads = []
            for i in range(requests_per_burst):
                if i % 3 == 0:
                    # Erro simulado
                    thread = threading.Thread(
                        target=self.simulate_error, 
                        args=(random.choice(["db", "500", "slow"]),)
                    )
                else:
                    # Operação normal
                    thread = threading.Thread(target=self.create_random_task)
                
                threads.append(thread)
                thread.start()
            
            # Aguardar todas as threads
            for thread in threads:
                thread.join()
            
            if burst < bursts - 1:
                print(f"⏳ Aguardando próxima rajada...")
                time.sleep(5)
        
        print("⚡ Teste de rajada concluído!")
    
    def stop(self):
        """Para a simulação"""
        self.running = False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Simulador de tráfego para To-Do App")
    parser.add_argument("--url", default="http://localhost:5001", help="URL base da aplicação")
    parser.add_argument("--mode", choices=["normal", "continuous", "burst", "errors"], 
                       default="normal", help="Modo de operação")
    parser.add_argument("--duration", type=int, default=10, 
                       help="Duração em minutos (para modo continuous)")
    parser.add_argument("--bursts", type=int, default=3, 
                       help="Número de rajadas (para modo burst)")
    parser.add_argument("--requests", type=int, default=10, 
                       help="Requests por rajada (para modo burst)")
    
    args = parser.parse_args()
    
    simulator = TodoTrafficSimulator(args.url)
    
    print(f"🎯 Simulador de Tráfego - To-Do App")
    print(f"📡 URL: {args.url}")
    print(f"🎮 Modo: {args.mode}")
    print(f"🕐 Timestamp: {datetime.now().isoformat()}")
    print("=" * 50)
    
    try:
        if args.mode == "normal":
            simulator.normal_workflow()
            
        elif args.mode == "continuous":
            simulator.continuous_traffic(args.duration)
            
        elif args.mode == "burst":
            simulator.burst_test(args.requests, args.bursts)
            
        elif args.mode == "errors":
            simulator.error_simulation_workflow()
    
    except KeyboardInterrupt:
        print("\n⏹️ Simulação interrompida pelo usuário")
        simulator.stop()
    
    print("\n✅ Simulação finalizada!")

if __name__ == "__main__":
    main()
