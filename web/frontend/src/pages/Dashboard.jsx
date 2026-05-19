import { useEffect, useState } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'
import { getCameraStatus } from '../api'
import { Card } from '../components/Card'
import { StatusBadge } from '../components/StatusBadge'
import { Activity, Cpu, MemoryStick, Watch, Camera, Radio } from 'lucide-react'

function MetricBar({ label, value, color }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-gray-600">{label}</span>
        <span className="font-semibold">{value}%</span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-2">
        <div className={`h-2 rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  )
}

function DeviceCard({ icon: Icon, label, connected, value }) {
  return (
    <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
      <div className={`p-2 rounded-lg ${connected ? 'bg-blue-100' : 'bg-gray-200'}`}>
        <Icon size={20} className={connected ? 'text-blue-600' : 'text-gray-400'} />
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium">{label}</p>
        {value && <p className="text-xs text-gray-500">{value}</p>}
      </div>
      <StatusBadge active={connected} />
    </div>
  )
}

export default function Dashboard() {
  const { data, connected } = useWebSocket()
  const [cameraStatus, setCameraStatus] = useState(null)

  useEffect(() => {
    const fetch = () => getCameraStatus().then(r => setCameraStatus(r.data)).catch(() => {})
    fetch()
    const t = setInterval(fetch, 10000)
    return () => clearInterval(t)
  }, [])

  const hr = data?.wearable?.heart_rate
  const cpu = data?.cpu ?? 0
  const ram = data?.ram ?? 0

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <StatusBadge active={connected} labelOn="En línea" labelOff="Sin conexión" />
      </div>

      {/* Métricas del sistema */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <div className="flex items-center gap-3 mb-3">
            <Cpu size={18} className="text-blue-500" />
            <span className="font-semibold">CPU</span>
          </div>
          <p className="text-3xl font-bold text-blue-600">{cpu.toFixed(0)}%</p>
          <div className="mt-2 w-full bg-gray-100 rounded-full h-2">
            <div className="h-2 rounded-full bg-blue-500" style={{ width: `${cpu}%` }} />
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-3 mb-3">
            <MemoryStick size={18} className="text-purple-500" />
            <span className="font-semibold">RAM</span>
          </div>
          <p className="text-3xl font-bold text-purple-600">{ram.toFixed(0)}%</p>
          <div className="mt-2 w-full bg-gray-100 rounded-full h-2">
            <div className="h-2 rounded-full bg-purple-500" style={{ width: `${ram}%` }} />
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-3 mb-3">
            <Activity size={18} className="text-red-500" />
            <span className="font-semibold">Frecuencia cardíaca</span>
          </div>
          <p className="text-3xl font-bold text-red-600">
            {hr ? `${hr} bpm` : '—'}
          </p>
          <p className="text-xs text-gray-400 mt-1">Última lectura del wearable</p>
        </Card>
      </div>

      {/* Estado de dispositivos */}
      <Card title="Dispositivos">
        <div className="space-y-3">
          <DeviceCard
            icon={Watch}
            label="Wearable"
            connected={data?.wearable_connected ?? false}
            value={hr ? `FC: ${hr} bpm` : 'Sin datos'}
          />
          <DeviceCard
            icon={Camera}
            label="Cámara IP"
            connected={cameraStatus?.reachable ?? false}
            value={cameraStatus?.rtsp_url ? 'RTSP configurado' : 'Sin configurar'}
          />
          <DeviceCard
            icon={Radio}
            label="Sensor mmWave"
            connected={data?.mmwave_active ?? false}
            value={data?.mmwave?.presence_detected ? 'Presencia detectada' : 'Sin presencia'}
          />
        </div>
      </Card>
    </div>
  )
}
