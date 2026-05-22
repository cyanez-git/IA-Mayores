#!/bin/bash
# Extrae la auth_key del Xiaomi Smart Band desde la API de Xiaomi.
# Versión parcheada con diagnóstico de 2FA/captcha.
#
# Uso:
#   bash scripts/get_xiaomi_authkey.sh
#
# Te pide email y password de forma interactiva (no quedan en historial).

set -e

WORKDIR="/tmp/huami-token-patched"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Verificando venv del proyecto..."
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "ERROR: no se encuentra $PROJECT_ROOT/.venv"
    exit 1
fi
source "$PROJECT_ROOT/.venv/bin/activate"

echo "==> Clonando huami-token (limpio)..."
rm -rf "$WORKDIR"
git clone --depth 1 https://github.com/argrento/huami-token.git "$WORKDIR" 2>&1 | tail -3

echo "==> Aplicando parche de diagnóstico..."
python3 - <<PYEOF
import re
p = "$WORKDIR/huami_token/xiaomi.py"
with open(p) as f:
    src = f.read()
old = '''        if not self._ssecurity or not location:
            raise AuthenticationError(
                code="missing-auth-data",
                message="Missing ssecurity or location in auth response",
            )'''
new = '''        if not self._ssecurity or not location:
            logger.error(f"Respuesta completa del server: {data}")
            notification_url = data.get("notificationUrl")
            if notification_url:
                logger.error(
                    f"Xiaomi requiere verificacion adicional (2FA/captcha). "
                    f"Abri esta URL en el navegador y completa la verificacion, "
                    f"despues corre el script de nuevo:\\n  {notification_url}"
                )
            raise AuthenticationError(
                code="missing-auth-data",
                message=f"Missing ssecurity or location. Server response: {data}",
            )'''
if old in src:
    src = src.replace(old, new)
    with open(p, "w") as f:
        f.write(src)
    print("  Parche aplicado OK")
else:
    print("  WARN: bloque original no encontrado, sigo con version sin parche")
PYEOF

echo "==> Instalando dependencias..."
pip install -q pycryptodome loguru requests cryptography 2>&1 | tail -2

echo ""
read -rp "Email Xiaomi: " EMAIL
read -rsp "Password Xiaomi: " PASSWORD
echo ""
echo ""

echo "==> Ejecutando huami-token (parcheado)..."
cd "$WORKDIR"
python3 main.py -m xiaomi -e "$EMAIL" -p "$PASSWORD" -b
