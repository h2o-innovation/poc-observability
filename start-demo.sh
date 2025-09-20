#!/bin/bash

# Script de inicialização da demonstração de observabilidade To-Do App
# Autor: Adventure Team
# Versão: 1.0

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Docker está rodando
check_docker() {
    print_status "Verificando Docker..."
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker não está rodando. Por favor, inicie o Docker e tente novamente."
        exit 1
    fi
    print_success "Docker está rodando"
}

# Verificar se Docker Compose está disponível
check_docker_compose() {
    print_status "Verificando Docker Compose..."
    if ! docker-compose --version >/dev/null 2>&1; then
        print_error "Docker Compose não está instalado."
        exit 1
    fi
    print_success "Docker Compose está disponível"
}

# Parar serviços existentes
stop_services() {
    print_status "Parando serviços existentes..."
    docker-compose down --remove-orphans >/dev/null 2>&1 || true
    print_success "Serviços parados"
}

# Construir e iniciar serviços
start_services() {
    print_status "Construindo e iniciando serviços..."
    docker-compose up --build -d
    
    if [ $? -eq 0 ]; then
        print_success "Serviços iniciados com sucesso"
    else
        print_error "Falha ao iniciar serviços"
        exit 1
    fi
}

# Aguardar serviços ficarem prontos
wait_for_services() {
    print_status "Aguardando serviços ficarem prontos..."
    
    # Aguardar PostgreSQL
    print_status "Aguardando PostgreSQL..."
    for i in {1..30}; do
        if docker-compose exec -T postgres pg_isready -U todouser -d todoapp >/dev/null 2>&1; then
            break
        fi
        sleep 2
    done
    
    # Aguardar To-Do App
    print_status "Aguardando To-Do App..."
    for i in {1..30}; do
        if curl -f http://localhost:5001/health >/dev/null 2>&1; then
            break
        fi
        sleep 3
    done
    
    # Aguardar Grafana
    print_status "Aguardando Grafana..."
    for i in {1..30}; do
        if curl -f http://localhost:3000/api/health >/dev/null 2>&1; then
            break
        fi
        sleep 2
    done
    
    print_success "Todos os serviços estão prontos!"
}

# Verificar se os serviços estão funcionando
verify_services() {
    print_status "Verificando serviços..."
    
    # Verificar To-Do App
    if curl -f http://localhost:5001/health >/dev/null 2>&1; then
        print_success "✅ To-Do App está funcionando (http://localhost:5001)"
    else
        print_warning "⚠️ To-Do App pode não estar pronto ainda"
    fi
    
    # Verificar Grafana
    if curl -f http://localhost:3000/api/health >/dev/null 2>&1; then
        print_success "✅ Grafana está funcionando (http://localhost:3000)"
    else
        print_warning "⚠️ Grafana pode não estar pronto ainda"
    fi
    
    # Verificar Prometheus
    if curl -f http://localhost:9090/-/healthy >/dev/null 2>&1; then
        print_success "✅ Prometheus está funcionando (http://localhost:9090)"
    else
        print_warning "⚠️ Prometheus pode não estar pronto ainda"
    fi
    
    # Verificar Pyroscope
    if curl -f http://localhost:4040/api/apps >/dev/null 2>&1; then
        print_success "✅ Pyroscope está funcionando (http://localhost:4040)"
    else
        print_warning "⚠️ Pyroscope pode não estar pronto ainda"
    fi
}

# Mostrar informações de acesso
show_access_info() {
    echo ""
    echo "🎉 Demonstração de Observabilidade - To-Do App"
    echo "=============================================="
    echo ""
    echo "📱 Aplicações disponíveis:"
    echo "   🌐 To-Do App:    http://localhost:5001"
    echo "   📊 Grafana:      http://localhost:3000 (admin/admin)"
    echo "   📈 Prometheus:   http://localhost:9090"
    echo "   🔥 Pyroscope:    http://localhost:4040"
    echo ""
    echo "🎯 Próximos passos:"
    echo "   1. Acesse a aplicação To-Do em http://localhost:5001"
    echo "   2. Crie algumas tarefas para gerar dados"
    echo "   3. Simule erros usando os botões vermelhos"
    echo "   4. Visualize métricas no Grafana (Dashboard: To-Do App)"
    echo ""
    echo "🔧 Scripts úteis:"
    echo "   • Tráfego normal:     python simulate_traffic.py --mode normal"
    echo "   • Tráfego contínuo:   python simulate_traffic.py --mode continuous --duration 5"
    echo "   • Teste de carga:     python simulate_traffic.py --mode burst --requests 20"
    echo "   • Simular erros:      python simulate_traffic.py --mode errors"
    echo ""
    echo "📋 Logs em tempo real:"
    echo "   docker-compose logs -f todo-app"
    echo ""
    echo "⏹️ Para parar tudo:"
    echo "   docker-compose down"
    echo ""
}

# Função principal
main() {
    echo "🚀 Iniciando demonstração de observabilidade..."
    echo ""
    
    check_docker
    check_docker_compose
    stop_services
    start_services
    wait_for_services
    verify_services
    show_access_info
    
    print_success "Demonstração iniciada com sucesso!"
}

# Verificar argumentos da linha de comando
case "${1:-start}" in
    start)
        main
        ;;
    stop)
        print_status "Parando demonstração..."
        docker-compose down --remove-orphans
        print_success "Demonstração parada"
        ;;
    restart)
        print_status "Reiniciando demonstração..."
        docker-compose down --remove-orphans
        main
        ;;
    logs)
        service=${2:-todo-app}
        print_status "Mostrando logs do serviço: $service"
        docker-compose logs -f $service
        ;;
    status)
        print_status "Status dos serviços:"
        docker-compose ps
        verify_services
        ;;
    clean)
        print_status "Limpando tudo (incluindo volumes)..."
        docker-compose down --remove-orphans --volumes
        docker system prune -f
        print_success "Limpeza concluída"
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|logs [service]|status|clean}"
        echo ""
        echo "Comandos:"
        echo "  start     - Iniciar demonstração (padrão)"
        echo "  stop      - Parar todos os serviços"
        echo "  restart   - Reiniciar demonstração"
        echo "  logs      - Mostrar logs (opcional: especificar serviço)"
        echo "  status    - Verificar status dos serviços"
        echo "  clean     - Parar e remover tudo (incluindo volumes)"
        exit 1
        ;;
esac
