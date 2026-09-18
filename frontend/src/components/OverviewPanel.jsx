import { useState } from 'react'
import { Copy, Check, Sparkles } from './Icons'

export default function OverviewPanel({ data }) {
  const [copied, setCopied] = useState(false)
  const overview = data.overview || {}
  const metrics = overview.summary_metrics || {}

  async function copyJson() {
    await navigator.clipboard?.writeText(JSON.stringify(data, null, 2))
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <div className="stack">
      {/* Side-by-side Text Comparison */}
      <div className="overview-grid">
        <div style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ font: '600 10px DM Mono', color: '#64748b', letterSpacing: '1px' }}>RAW INPUT TEXT</span>
            <span className="pill" style={{ fontSize: '9px' }}>Original</span>
          </div>
          <p style={{ margin: 0, fontSize: '13px', lineHeight: 1.6, color: '#334155' }}>
            {data.raw_text}
          </p>
        </div>

        <div style={{ background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '12px', padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ font: '600 10px DM Mono', color: '#0369a1', letterSpacing: '1px' }}>CORRECTED TEXT (NLP INPUT)</span>
            <span className="pill" style={{ background: '#e0f2fe', color: '#0369a1', borderColor: '#bae6fd', fontSize: '9px' }}>
              Cleaned
            </span>
          </div>
          <p style={{ margin: 0, fontSize: '13px', lineHeight: 1.6, color: '#0f172a', fontWeight: 500 }}>
            {data.corrected_text}
          </p>
        </div>
      </div>

      {/* Holistic 5-Stage Metrics Grid */}
      <div className="panel" style={{ borderLeft: '4px solid #10b981' }}>
        <div className="panel-title">
          <div>
            <h3>Pipeline Summary & Latency</h3>
            <span>Integrated multi-stage NLP execution telemetry</span>
          </div>
          {overview.execution_time_ms && (
            <span className="pill" style={{ background: '#ecfdf5', color: '#059669', borderColor: '#a7f3d0' }}>
              ⚡ {overview.execution_time_ms} ms Latency
            </span>
          )}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '12px', marginTop: '10px' }}>
          <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
            <span style={{ font: '500 9px DM Mono', color: '#71717a', display: 'block' }}>STAGE 1: SPELL</span>
            <b style={{ fontSize: '18px', color: '#e11d48' }}>{metrics.spelling_errors || 0}</b>
            <span style={{ fontSize: '10px', color: '#a1a1aa', display: 'block' }}>Typos Flagged</span>
          </div>

          <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
            <span style={{ font: '500 9px DM Mono', color: '#71717a', display: 'block' }}>STAGE 2: SYNTAX</span>
            <b style={{ fontSize: '18px', color: '#2563eb' }}>{metrics.svo_triples || 0}</b>
            <span style={{ fontSize: '10px', color: '#a1a1aa', display: 'block' }}>SVO Triples</span>
          </div>

          <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
            <span style={{ font: '500 9px DM Mono', color: '#71717a', display: 'block' }}>STAGE 3: CONCEPTS</span>
            <b style={{ fontSize: '18px', color: '#7c3aed' }}>{metrics.entities_and_concepts || 0}</b>
            <span style={{ fontSize: '10px', color: '#a1a1aa', display: 'block' }}>Entities & Terms</span>
          </div>

          <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
            <span style={{ font: '500 9px DM Mono', color: '#71717a', display: 'block' }}>STAGE 3: WSD</span>
            <b style={{ fontSize: '18px', color: '#0284c7' }}>{metrics.wsd_terms || 0}</b>
            <span style={{ fontSize: '10px', color: '#a1a1aa', display: 'block' }}>WordNet Targets</span>
          </div>

          <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
            <span style={{ font: '500 9px DM Mono', color: '#71717a', display: 'block' }}>STAGE 4: COREF</span>
            <b style={{ fontSize: '18px', color: '#d97706' }}>{metrics.coref_chains || 0}</b>
            <span style={{ fontSize: '10px', color: '#a1a1aa', display: 'block' }}>Chains Tracked</span>
          </div>

          <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
            <span style={{ font: '500 9px DM Mono', color: '#71717a', display: 'block' }}>STAGE 4: RELATIONS</span>
            <b style={{ fontSize: '18px', color: '#4f46e5' }}>{metrics.discourse_relations || 0}</b>
            <span style={{ fontSize: '10px', color: '#a1a1aa', display: 'block' }}>Connectives</span>
          </div>

          <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
            <span style={{ font: '500 9px DM Mono', color: '#71717a', display: 'block' }}>STAGE 4: PRAGMATICS</span>
            <b style={{ fontSize: '18px', color: '#9333ea' }}>{metrics.pragmatic_acts || 0}</b>
            <span style={{ fontSize: '10px', color: '#a1a1aa', display: 'block' }}>Speech Acts</span>
          </div>
        </div>
      </div>

      {/* JSON Payload Viewer */}
      <div className="panel">
        <div className="panel-title">
          <div>
            <h3>Structured Pipeline Output</h3>
            <span>Full 5-stage partitioned JSON response payload</span>
          </div>
          <button className="iconbtn" onClick={copyJson} title="Copy full JSON">
            {copied ? <Check size={16} /> : <Copy size={16} />}
            <span style={{ fontSize: '11px', marginLeft: '4px' }}>{copied ? 'Copied' : 'Copy JSON'}</span>
          </button>
        </div>
        <pre className="json" style={{ maxHeight: '450px' }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  )
}

