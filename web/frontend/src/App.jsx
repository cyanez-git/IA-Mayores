import { BrowserRouter, NavLink, Routes, Route, Navigate } from 'react-router-dom'
import { LayoutDashboard, Watch, Camera, Radio, User, Bell, Bot } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Wearable  from './pages/Wearable'
import CameraPage from './pages/Camera'
import Sensors   from './pages/Sensors'
import Profile   from './pages/Profile'
import Alerts    from './pages/Alerts'
import AIConfig  from './pages/AIConfig'

const NAV = [
  { to: '/',        icon: LayoutDashboard, label: 'Dashboard'  },
  { to: '/wearable',icon: Watch,           label: 'Wearable'   },
  { to: '/camera',  icon: Camera,          label: 'Cámara'     },
  { to: '/sensors', icon: Radio,           label: 'Sensores'   },
  { to: '/profile', icon: User,            label: 'Perfil'     },
  { to: '/alerts',  icon: Bell,            label: 'Alertas'    },
  { to: '/ai',      icon: Bot,             label: 'Config IA'  },
]

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <aside className="w-56 bg-white border-r border-gray-100 flex flex-col">
          <div className="px-5 py-5 border-b border-gray-100">
            <h1 className="text-lg font-bold text-blue-600">SAMP</h1>
            <p className="text-xs text-gray-400">Panel de administración</p>
          </div>
          <nav className="flex-1 py-4 space-y-1 px-3">
            {NAV.map(({ to, icon: Icon, label }) => (
              <NavLink key={to} to={to} end={to === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition
                  ${isActive
                    ? 'bg-blue-50 text-blue-700 font-semibold'
                    : 'text-gray-600 hover:bg-gray-50'}`
                }>
                <Icon size={17} />
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="px-5 py-4 border-t border-gray-100">
            <p className="text-xs text-gray-300">v1.0.0</p>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto p-8">
          <Routes>
            <Route path="/"         element={<Dashboard />} />
            <Route path="/wearable" element={<Wearable />} />
            <Route path="/camera"   element={<CameraPage />} />
            <Route path="/sensors"  element={<Sensors />} />
            <Route path="/profile"  element={<Profile />} />
            <Route path="/alerts"   element={<Alerts />} />
            <Route path="/ai"       element={<AIConfig />} />
            <Route path="*"         element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
