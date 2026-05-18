export function StatusBadge({ active, labelOn = 'Activo', labelOff = 'Inactivo' }) {
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium
      ${active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-green-500' : 'bg-red-500'}`} />
      {active ? labelOn : labelOff}
    </span>
  )
}
