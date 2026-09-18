import { Copy, Check, ChevronRight } from './Icons'

export default function SpellPanel({ data, onCopy, copied }) {
  const correctedText = data.corrected_text || data.corrected || ''
  const corrections = data.corrections || []
  const wordsScanned = data.words_scanned || 0

  return (
    <div className="grid2">
      <div className="panel correction">
        <div className="panel-title">
          <div>
            <h3>Cleaned writing</h3>
            <span>Conservative corrections only — valid technical and domain vocabulary is strictly preserved.</span>
          </div>
          <button className="iconbtn" onClick={onCopy} title="Copy cleaned text">
            {copied ? <Check size={16} /> : <Copy size={16} />}
          </button>
        </div>
        <div className="corrected">{correctedText}</div>
        {data.accuracy_impact && (
          <div style={{ marginTop: '12px', fontSize: '11px', color: '#16a34a', background: 'rgba(22,163,74,0.08)', padding: '8px 12px', borderRadius: '8px', border: '1px solid rgba(22,163,74,0.2)' }}>
            ✓ {data.accuracy_impact}
          </div>
        )}
      </div>

      <div className="panel">
        <div className="panel-title">
          <div>
            <h3>Correction ledger</h3>
            <span>{corrections.length} change{corrections.length === 1 ? '' : 's'} detected across {wordsScanned} scanned words</span>
          </div>
        </div>
        {corrections.length ? (
          <div className="table">
            {corrections.map((c, i) => (
              <div className="row" key={i}>
                <span className="bad">{c.original}</span>
                <ChevronRight size={14} />
                <span className="good">{c.replacement}</span>
                <small>
                  edit distance {c.edit_distance} · confidence: {c.confidence ? `${Math.round(c.confidence * 100)}%` : '100%'}
                  {c.position ? ` · pos [${c.position.start}-${c.position.end}]` : ''}
                  <br />
                  <b>Reason:</b> {c.reason}
                </small>
              </div>
            ))}
          </div>
        ) : (
          <div className="nochange">No spelling changes needed. All terms are valid or domain-protected.</div>
        )}
      </div>
    </div>
  )
}

