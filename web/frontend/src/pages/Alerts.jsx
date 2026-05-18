import { useEffect, useState } from 'react'
import { getAlerts, clearAlerts } from '../api'
import { Card } from '../components/Card'

const LEVEL_STYLES = {
  emergency: 'bg-red-100 text-red-700 border-red-200',
  attention:  'bg-yellow-100 text-yellow-700 border-yellow-200',
}

const LEVEL_LABELS = {
  emergency: '🚨 Emergencia',
  attention:  '⚠️ Atención',
}

export default function Alerts() {
  const [alerts, setAlerts] = useState([])

  const fetch = () => getAlerts().then(r => setAlerts(r.data)).catch(() => {})

  useEffect(() => {
    fetch()
    const t = setInterval(fetch, 5000)
    return () => clearInterval(t)
  }, [])

  const handleClear = async () => {
    await clearAlerts()
    setAlerts([])
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Historial de alertas</h1>
        {alerts.length > 0 && (
          <button onClick={handleClear}
            className="text-sm text-red-500 hover:text-red-700">
            Limpiar historial
          </button>
        )}
      </div>

      {alerts.length === 0 ? (
        <Card>
          <p className="text-center text-gray-400 py-8">Sin alertas registradas</p>
        </Card>
      ) : (
        <div className="space-y-3">
          {alerts.map((a, i) => (
            <div key={i} className={`rounded-lg border p-4 ${LEVEL_STYLES[a.level] ?? ''}`}>
              <div className="flex justify-between items-start">
                <span className="font-semibold">{LEVEL_LABELS[a.level] ?? a.level}</span>
                <span className="text-xs opacity-70">
                  {new Date(a.timestamp * 1000).toLocaleString('es-AR')}
                </span>
              </div>
              <div className="mt-1 text-sm space-x-4">
                {a.heart_rate && <span>FC: {a.heart_rate} bpm</span>}
                {a.impact_detected && <span>Impacto detectado</span>}
                {a.fall_detected && <span>⚠️ Caída detectada</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
