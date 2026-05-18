import { useEffect, useRef, useState } from 'react'

export function useWebSocket() {
  const [data, setData] = useState(null)
  const [connected, setConnected] = useState(false)
  const ws = useRef(null)

  useEffect(() => {
    const connect = () => {
      ws.current = new WebSocket(`ws://${window.location.host}/ws`)
      ws.current.onopen  = () => setConnected(true)
      ws.current.onclose = () => { setConnected(false); setTimeout(connect, 3000) }
      ws.current.onmessage = (e) => setData(JSON.parse(e.data))
    }
    connect()
    return () => ws.current?.close()
  }, [])

  return { data, connected }
}
