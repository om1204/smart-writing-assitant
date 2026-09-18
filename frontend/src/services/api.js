const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function processText(text) {
  const response = await fetch(`${API}/api/process`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({text})
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || 'Pipeline failed')
  return data
}

export async function healthCheck() {
  const response = await fetch(`${API}/api/health`)
  return response.ok
}
