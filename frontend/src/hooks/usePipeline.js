import {useState} from 'react'
import {processText} from '../services/api'

export function usePipeline() {
  const [result,setResult]=useState(null)
  const [loading,setLoading]=useState(false)
  const [error,setError]=useState('')
  async function run(text){
    setLoading(true); setError('')
    try { setResult(await processText(text)); return true }
    catch(e){ setError(e.message); return false }
    finally { setLoading(false) }
  }
  return {result, setResult, loading, error, run}
}
