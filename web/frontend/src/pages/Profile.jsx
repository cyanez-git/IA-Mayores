import { useEffect, useState } from 'react'
import { getProfile, updateProfile } from '../api'
import { Card } from '../components/Card'

export default function Profile() {
  const [profile, setProfile] = useState(null)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    getProfile().then(r => setProfile(r.data)).catch(() => {})
  }, [])

  const handleSave = async () => {
    await updateProfile(profile)
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  const update = (key, value) => setProfile(p => ({ ...p, [key]: value }))
  const updateNested = (parent, key, value) =>
    setProfile(p => ({ ...p, [parent]: { ...p[parent], [key]: value } }))

  if (!profile) return <div className="text-gray-400">Cargando perfil...</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Perfil del usuario</h1>

      <Card title="Datos personales">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { label: 'Nombre', key: 'name' },
            { label: 'Edad', key: 'age', type: 'number' },
            { label: 'Condición médica', key: 'condition' },
          ].map(({ label, key, type = 'text' }) => (
            <div key={key}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
              <input type={type} value={profile[key] ?? ''}
                onChange={e => update(key, type === 'number' ? +e.target.value : e.target.value)}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          ))}
        </div>
      </Card>

      <Card title="Contacto familiar">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { label: 'Nombre', key: 'name' },
            { label: 'Teléfono', key: 'phone' },
            { label: 'Relación', key: 'relation' },
          ].map(({ label, key }) => (
            <div key={key}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
              <input type="text" value={profile.family_contact?.[key] ?? ''}
                onChange={e => updateNested('family_contact', key, e.target.value)}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          ))}
        </div>
      </Card>

      <Card title="Preferencias">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Temas de conversación (separados por coma)
            </label>
            <input type="text"
              value={profile.preferences?.topics?.join(', ') ?? ''}
              onChange={e => updateNested('preferences', 'topics', e.target.value.split(',').map(t => t.trim()))}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Horario de medicación
            </label>
            <input type="text"
              value={profile.preferences?.medication_schedule ?? ''}
              onChange={e => updateNested('preferences', 'medication_schedule', e.target.value)}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>
      </Card>

      <button onClick={handleSave}
        className="w-full py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition">
        {saved ? '✓ Perfil guardado' : 'Guardar perfil'}
      </button>
    </div>
  )
}
