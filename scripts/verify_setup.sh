#!/bin/bash
# Verifica que todos los componentes de SAMP estén funcionando

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; }
warn() { echo -e "  ${YELLOW}~${NC} $1"; }

echo ""
echo "=== Verificación SAMP Mini PC ==="
echo ""

# Python
echo "[ Python ]"
if python3.11 --version &>/dev/null; then
    ok "Python 3.11: $(python3.11 --version)"
else
    fail "Python 3.11 no encontrado"
fi

# Entorno virtual
PROJECT_DIR="$HOME/IA-Mayores"
if [ -f "$PROJECT_DIR/.venv/bin/activate" ]; then
    ok "Entorno virtual presente"
else
    fail "Entorno virtual no encontrado en $PROJECT_DIR/.venv"
fi

echo ""
echo "[ Servicios ]"

# Mosquitto
if systemctl is-active --quiet mosquitto; then
    ok "Mosquitto MQTT: activo"
    if mosquitto_pub -t test -m ping -q 0 2>/dev/null; then
        ok "Mosquitto responde en localhost:1883"
    else
        warn "Mosquitto activo pero no responde al pub"
    fi
else
    fail "Mosquitto: inactivo"
fi

# Ollama
if systemctl is-active --quiet ollama; then
    ok "Ollama: activo"
    if ollama list 2>/dev/null | grep -q "phi3"; then
        ok "Modelo phi3:mini descargado"
    else
        warn "Ollama activo pero phi3:mini no encontrado — ejecutá: ollama pull phi3:mini"
    fi
else
    fail "Ollama: inactivo"
fi

# Bluetooth
echo ""
echo "[ Hardware ]"
if systemctl is-active --quiet bluetooth; then
    ok "Bluetooth: activo"
else
    warn "Bluetooth: inactivo (necesario para Fase 5)"
fi

# RAM disponible
RAM_TOTAL=$(free -m | awk '/^Mem:/{print $2}')
RAM_FREE=$(free -m | awk '/^Mem:/{print $7}')
if [ "$RAM_FREE" -gt 2000 ]; then
    ok "RAM disponible: ${RAM_FREE}MB / ${RAM_TOTAL}MB"
else
    warn "RAM disponible baja: ${RAM_FREE}MB / ${RAM_TOTAL}MB"
fi

# Disco
DISK_FREE=$(df -BG "$HOME" | awk 'NR==2{print $4}' | tr -d 'G')
if [ "$DISK_FREE" -gt 20 ]; then
    ok "Espacio en disco: ${DISK_FREE}GB disponibles"
else
    warn "Espacio en disco bajo: ${DISK_FREE}GB disponibles"
fi

echo ""
echo "[ Proyecto ]"
if [ -f "$PROJECT_DIR/src/chat.py" ]; then
    ok "Código fuente presente"
else
    fail "No se encontró el proyecto en $PROJECT_DIR"
fi

if [ -f "$PROJECT_DIR/data/profile.json" ]; then
    ok "Perfil de usuario configurado"
else
    warn "Falta data/profile.json — copiá el perfil del usuario"
fi

echo ""
echo "================================="
echo ""
