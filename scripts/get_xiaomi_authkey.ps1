# Extrae la auth_key del Xiaomi Smart Band — version Windows PowerShell.
# Versión parcheada con diagnóstico de 2FA/captcha.
#
# Uso (desde PowerShell):
#   cd C:\Users\CYANEZ\huami-token
#   powershell -ExecutionPolicy Bypass -File scripts\get_xiaomi_authkey.ps1
#
# O directamente:
#   .\scripts\get_xiaomi_authkey.ps1

$ErrorActionPreference = "Stop"

$HuamiDir = "$env:USERPROFILE\huami-token"

Write-Host "==> Verificando huami-token en $HuamiDir..." -ForegroundColor Cyan
if (-not (Test-Path "$HuamiDir\main.py")) {
    Write-Host "    No existe. Clonando..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/argrento/huami-token.git $HuamiDir
}

Write-Host "==> Aplicando parche de diagnóstico..." -ForegroundColor Cyan
$xiaomiPy = "$HuamiDir\huami_token\xiaomi.py"
$content = Get-Content $xiaomiPy -Raw

$old = @'
        if not self._ssecurity or not location:
            raise AuthenticationError(
                code="missing-auth-data",
                message="Missing ssecurity or location in auth response",
            )
'@

$new = @'
        if not self._ssecurity or not location:
            logger.error(f"Respuesta completa del server: {data}")
            notification_url = data.get("notificationUrl")
            if notification_url:
                logger.error(
                    f"Xiaomi requiere verificacion adicional (2FA/captcha). "
                    f"Abri esta URL en el navegador y completa la verificacion, "
                    f"despues corre el script de nuevo:\n  {notification_url}"
                )
            raise AuthenticationError(
                code="missing-auth-data",
                message=f"Missing ssecurity or location. Server response: {data}",
            )
'@

if ($content.Contains($old)) {
    $content = $content.Replace($old, $new)
    Set-Content -Path $xiaomiPy -Value $content -NoNewline
    Write-Host "    Parche aplicado OK" -ForegroundColor Green
} elseif ($content.Contains("Respuesta completa del server")) {
    Write-Host "    Parche ya estaba aplicado" -ForegroundColor Yellow
} else {
    Write-Host "    WARN: bloque original no encontrado, sigo sin parche" -ForegroundColor Yellow
}

Write-Host "==> Instalando dependencias..." -ForegroundColor Cyan
python -m pip install --quiet pycryptodome loguru requests cryptography

Write-Host ""
$email = Read-Host "Email Xiaomi"
$securePwd = Read-Host "Password Xiaomi" -AsSecureString
$pwd = [System.Net.NetworkCredential]::new("", $securePwd).Password

Write-Host ""
Write-Host "==> Ejecutando huami-token (parcheado)..." -ForegroundColor Cyan
Set-Location $HuamiDir
python main.py -m xiaomi -e $email -p $pwd -b
