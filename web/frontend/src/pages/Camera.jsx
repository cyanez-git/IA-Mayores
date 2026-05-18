import { useEffect, useState } from 'react'
import { getCameraStatus, updateCamera } from '../api'
import { Card } from '../components/Card'
import { StatusBadge } from '../components/StatusBadge'

export default function Camera() {
  const [status, setStatus] = useState(null)
  const [rtspUrl, setRtspUrl] = useState('')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    getCameraStatus().then(r => {
      setStatus(r.data)
      setRtspUrl(r.data.rtsp_url)
    }).catch(() => {})
  }, [])

  const handleSave = async () => {
    await updateCamera({ rtsp_url: rtspUrl })
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Cámara IP</h1>

      <Card title="Estado">
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Conexión RTSP</span>
            <StatusBadge active={status?.reachable ?? false} />
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">MediaPipe activo</span>
            <StatusBadge active={status?.mediapipe_active ?? false} />
          </div>
        </div>
      </Card>

      <Card title="Configuración">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">URL RTSP</label>
            <input
              type="text"
              value={rtspUrl}
              onChange={e => setRtspUrl(e.target.value)}
              placeholder="rtsp://usuario:contraseña@192.168.1.x:554/stream"
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-gray-400 mt-1">
              Ejemplo Seisa: rtsp://admin:contraseña@192.168.1.X:554/stream1
            </p>
          </div>
          <button onClick={handleSave}
            className="w-full py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition">
            {saved ? '✓ Guardado' : 'Guardar configuración'}
          </button>
        </div>
      </Card>
    </div>
  )
}
