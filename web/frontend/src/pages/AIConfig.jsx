import { useEffect, useState } from 'react'
import { getServices } from '../api'
import { Card } from '../components/Card'
import { StatusBadge } from '../components/StatusBadge'

const MODELS = ['phi3:mini', 'llama3.2:3b', 'gemma2:2b', 'mistral:7b']

export default function AIConfig() {
  const [services, setServices] = useState(null)
  const [model, setModel] = useState('phi3:mini')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    getServices().then(r => setServices(r.data)).catch(() => {})
  }, [])

  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Configuración IA</h1>

      <Card title="Estado de servicios">
        <div className="space-y-3">
          {[
            { label: 'Ollama (LLM local)', key: 'ollama' },
            { label: 'Mosquitto (MQTT)', key: 'mosquitto' },
            { label: 'SAMP (asistente)', key: 'samp' },
          ].map(({ label, key }) => (
            <div key={key} className="flex justify-between items-center">
              <span className="text-sm text-gray-600">{label}</span>
              <StatusBadge active={services?.[key] === 'active'} />
            </div>
          ))}
        </div>
      </Card>

      <Card title="Modelo LLM">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Modelo activo
            </label>
            <div className="space-y-2">
              {MODELS.map(m => (
                <label key={m} className="flex items-center gap-3 cursor-pointer">
                  <input type="radio" name="model" value={m}
                    checked={model === m} onChange={() => setModel(m)}
                    className="accent-blue-600" />
                  <span className="text-sm font-mono">{m}</span>
                  {m === 'phi3:mini' && (
                    <span className="text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded-full">
                      recomendado 8GB
                    </span>
                  )}
                </label>
              ))}
            </div>
          </div>
          <button onClick={handleSave}
            className="w-full py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition">
            {saved ? '✓ Guardado' : 'Aplicar modelo'}
          </button>
        </div>
      </Card>
    </div>
  )
}
