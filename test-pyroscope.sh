#!/bin/bash

echo "🔥 Adventure Game - Teste de Profiling com Pyroscope"
echo "=================================================="

# Verificar se o Docker está rodando
if ! docker info &> /dev/null; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

echo "✅ Docker está rodando"

# Subir a stack
echo "🚀 Iniciando stack de observabilidade..."
docker-compose up -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 30

# Verificar se todos os serviços estão rodando
echo "🔍 Verificando status dos serviços..."

services=("alloy" "prometheus" "loki" "grafana" "tempo" "pyroscope")
all_healthy=true

for service in "${services[@]}"; do
    if docker-compose ps $service | grep -q "Up"; then
        echo "✅ $service está rodando"
    else
        echo "❌ $service não está rodando"
        all_healthy=false
    fi
done

if $all_healthy; then
    echo ""
    echo "🎉 Todos os serviços estão rodando!"
    echo ""
    echo "📊 Acesse os dashboards:"
    echo "   • Grafana: http://localhost:3000"
    echo "   • Pyroscope: http://localhost:4040"
    echo "   • Prometheus: http://localhost:9090"
    echo ""
    echo "🎮 Para iniciar o jogo e gerar profiles:"
    echo "   docker-compose exec alloy python main.py"
    echo ""
    echo "🔍 Para ver logs do Pyroscope:"
    echo "   docker-compose logs -f pyroscope"
else
    echo ""
    echo "❌ Alguns serviços não estão funcionando. Verifique os logs:"
    echo "   docker-compose logs"
fi
