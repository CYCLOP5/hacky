import axios from 'axios'

export type RunInputs = {
  asset_value_millions: number
  shielding_level: 'Standard' | 'Hardened' | 'Light/Legacy'
  years_in_orbit: number
  adjustment_factor: number
}

export async function runWorkflow(inputs: RunInputs) {
  const { data } = await axios.post('/api/run', inputs)
  return data
}

export type HistoricalRunInputs = RunInputs & {
  historical_kp: number
  historical_event_name: string
  historical_date: string
}

export async function runHistoricalWorkflow(inputs: HistoricalRunInputs) {
  const { data } = await axios.post('/api/run-historical', inputs, {
    timeout: 120000 // 2 minutes timeout to prevent hanging
  })
  return data
}

export async function getPortfolio() {
  const { data } = await axios.get('/api/portfolio')
  return data as { items: any[] }
}

export type DailyGeomagDay = {
  date: string
  ap: number | null
  kp_values: number[]
  kp_max: number | null
  kp_avg: number | null
}

export async function getDailyGeomag(limit = 30) {
  const { data } = await axios.get(`/api/daily-geomag?limit=${limit}`)
  return data as { days: DailyGeomagDay[] }
}

export type ThreeDayBreakdownRow = { period: string; values: number[] }
export type ThreeDayForecast = {
  issued: string | null
  observed_max_kp: number | null
  expected_max_kp: number | null
  days: string[]
  breakdown: ThreeDayBreakdownRow[]
  rationale: string
}

export async function getThreeDayForecast() {
  const { data } = await axios.get('/api/forecast-3day')
  return data as ThreeDayForecast
}
