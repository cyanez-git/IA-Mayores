import { useEffect, useState } from 'react'
import { getWearable, updateThresholds } from '../api'
import { Card } from '../components/Card'
import { StatusBadge } from '../components/StatusBadge'

export default function Wearable() {
  const [status, setStatus] = useState(null)
  const [hrMin, setHrMin] = useState(50)
  const [hrMax, setHrMax] = useState(140)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    const fetch = () => getWearable().then(r => setStatus(r.data)).catch(() => {})
    fetch()
    const t = setInterval(fetch, 3000)
    return () => clearInterval(t)
  }, [])

  const handleSave = async () => {
    await updateThresholds({ hr_min: hrMin, hr_max: hrMax })
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  const latest = status?.latest

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Wearable</h1>

      <Card title="Estado de conexión">
        <div className="flex items-center justify-between">
          <StatusBadge active={status?.connected ?? false} />
          {status?.last_seen_seconds_ago != null && (
            <span className="text-sm text-gray-400">
              Última lectura: hace {status.last_seen_seconds_ago}s
            </span>
          )}
        </div>
      </Card>

      {latest && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Frecuencia cardíaca', value: `${latest.heart_rate} bpm`, color: 'text-red-600' },
            { label: 'Acelerómetro X', value: `${latest.accel_x} g`, color: 'text-blue-600' },
            { label: 'Acelerómetro Y', value: `${latest.accel_y} g`, color: 'text-blue-600' },
            { label: 'Impacto detectado', value: latest.impact_detected ? 'SÍ' : 'No', color: latest.impact_detected ? 'text-red-600' : 'text-green-600' },
          ].map(({ label, value, color }) => (
            <Card key={label}>
              <p className="text-xs text-gray-500 mb-1">{label}</p>
              <p className={`text-2xl font-bold ${color}`}>{value}</p>
            </Card>
          ))}
        </div>
      )}

      <Card title="Umbrales de alerta">
        <div className="space-y-5">
          <div>
            <div className="flex justify-between text-sm mb-1">
              <label className="font-medium">FC mínima</label>
              <span className="text-blue-600 font-bold">{hrMin} bpm</span>
            </div>
            <input type="range" min={30} max={70} value={hrMin}
              onChange={e => setHrMin(+e.target.value)}
              className="w-full accent-blue-600" />
          </div>
          <div>
            <div className="flex justify-between text-sm mb-1">
              <label className="font-medium">FC máxima</label>
              <span className="text-blue-600 font-bold">{hrMax} bpm</span>
            </div>
            <input type="range" min={100} max={180} value={hrMax}
              onChange={e => setHrMax(+e.target.value)}
              className="w-full accent-blue-600" />
          </div>
          <button onClick={handleSave}
            className="w-full py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition">
            {saved ? '✓ Guardado' : 'Guardar umbrales'}
          </button>
        </div>
      </Card>
    </div>
  )
}
