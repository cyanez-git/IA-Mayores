# SAMP — Registro de Progreso
**Sistema de Acompañamiento y Monitoreo Proactivo**

---

## 2026-05-06

### Sesión inicial — Diseño + Fase 1 completa

**Arquitectura definida:**
- Tres agentes concurrentes: Vigilancia, Empatía, Triaje
- Stack: Python 3.11+ / LangGraph / Claude Haiku / Whisper / ElevenLabs
- Hub: Raspberry Pi 5 (prototipo) → tablet Android (producto)
- Sensores: wearable BLE + mmWave + cámara RTSP

**Modelo de negocio:**
- B2C primario: adultos mayores solos + familia como comprador real
- Segmento adicional: hipocondría y ataques de pánico
- B2B secundario: hogares de ancianos, clínicas
- Revenue: kit hardware + suscripción mensual cloud

**Código entregado (Fase 1):**

| Archivo | Descripción |
|---------|-------------|
| `src/simulator/data_simulator.py` | Genera lecturas simuladas de wearable (5 escenarios) |
| `src/router/alert_router.py` | Clasifica lecturas: normal / attention / emergency |
| `src/agents/empathy_agent.py` | Agente de compañía y contención emocional |
| `src/agents/triage_agent.py` | Agente de emergencia con relato para familiar |
| `src/graph.py` | Grafo LangGraph que orquesta los agentes |
| `src/main.py` | Demo completa de los 4 escenarios |

**Resultado de la demo:**
- Normal → respuesta de compañía cálida ✅
- FC elevada → pregunta empática sobre estado ✅
- Ataque de pánico → contención + alerta al familiar ✅
- Caída detectada → aviso al usuario + relato con datos de impacto ✅

**Repositorio:** https://github.com/cyanez-git/IA-Mayores
**Commits:** 2 (feat: Fase 1 DataSimulator + AlertRouter / feat: Fase 1 agentes LangGraph)

**Pendiente para próxima sesión:**
- Fase 2: loop de conversación interactiva + memoria de sesión
- Fase 3: tests unitarios del AlertRouter

---
