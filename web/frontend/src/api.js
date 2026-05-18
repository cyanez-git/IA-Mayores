import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getSystemStatus  = () => api.get('/system/status')
export const getServices      = () => api.get('/system/services')
export const getWearable      = () => api.get('/wearable/status')
export const updateThresholds = (data) => api.put('/wearable/thresholds', data)
export const getCameraStatus  = () => api.get('/camera/status')
export const getCameraConfig  = () => api.get('/camera/config')
export const updateCamera     = (data) => api.put('/camera/config', data)
export const getSensors       = () => api.get('/sensors/status')
export const getProfile       = () => api.get('/profile')
export const updateProfile    = (data) => api.put('/profile', data)
export const getAlerts        = () => api.get('/alerts')
export const clearAlerts      = () => api.delete('/alerts')
