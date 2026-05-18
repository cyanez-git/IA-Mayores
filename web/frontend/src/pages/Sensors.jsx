import { useEffect, useState } from 'react'
import { getSensors } from '../api'
import { Card } from '../components/Card'
import { StatusBadge } from '../components/StatusBadge'

export default function Sensors() {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    const fetch = () => getSensors().then(r => setStatus(r.data)).catch(() => {})
    fetch()
    const t = setInterval(fetch, 3000)
    return () => clearInterval(t)
  }, [])

  const latest = status?.latest

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Sensores mmWave</h1>

      <Card title="Estado del sensor">
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Sensor activo</span>
            <StatusBadge active={status?.mmwave_active ?? false} />
          </div>
          {status?.last_seen_seconds_ago != null && (
            <p className="text-xs text-gray-400">
              Última lectura: hace {status.last_seen_seconds_ago}s
            </p>
          )}
        </div>
      </Card>

      {latest && (
        <div className="grid grid-cols-2 gap-4">
          <Card>
            <p className="text-xs text-gray-500 mb-1">Presencia</p>
            <p className={`text-2xl font-bold ${latest.presence_detected ? 'text-green-600' : 'text-gray-400'}`}>
              {latest.presence_detected ? 'Detectada' : 'No detectada'}
            </p>
          </Card>
          <Card>
            <p className="text-xs text-gray-500 mb-1">Caída detectada</p>
            <p className={`text-2xl font-bold ${latest.fall_detected ? 'text-red-600' : 'text-green-600'}`}>
              {latest.fall_detected ? 'SÍ ⚠️' : 'No'}
            </p>
          </Card>
          <Card>
            <p className="text-xs text-gray-500 mb-1">Distancia</p>
            <p className="text-2xl font-bold text-blue-600">{latest.distance_cm} cm</p>
          </Card>
          <Card>
            <p className="text-xs text-gray-500 mb-1">Velocidad</p>
            <p className="text-2xl font-bold text-blue-600">{latest.movement_speed} m/s</p>
          </Card>
        </div>
      )}
    </div>
  )
}
