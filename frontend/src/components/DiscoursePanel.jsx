import { Sparkles, ChevronRight, AlertCircle, Check } from './Icons'

export default function DiscoursePanel({ data }) {
  const coref = data.coreference_chains || data.discourse?.coreference_chains || []
  const relations = data.discourse_relations || data.discourse?.discourse_relations || []
  const pragmatics = data.pragmatic_inferences || data.discourse?.pragmatic_inferences || []

  return (
    <div className="grid2">
      {/* Coreference Resolution */}
      <div className="panel">
        <div className="panel-title">
          <div>
            <h3>Coreference Resolution</h3>
            <span>Agreement-constrained salience resolver with explicit ambiguity tracking</span>
          </div>
          <span className="pill">{coref.length} Chains Tracked</span>
        </div>

        {coref.length ? (
          coref.map((x, i) => (
            <div
              className="chain"
              key={i}
              style={{
                marginBottom: '12px',
                flexDirection: 'column',
                alignItems: 'stretch',
                padding: '12px',
                background: x.is_ambiguous ? '#fffbeb' : '#fafafa',
                borderRadius: '8px',
                border: `1px solid ${x.is_ambiguous ? '#fef3c7' : '#f0f0f0'}`
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                  <span className="mention-badge" style={{ background: '#e0f2fe', color: '#0369a1', padding: '3px 8px', borderRadius: '4px', fontWeight: 600 }}>
                    "{x.mention}"
                  </span>
                  <ChevronRight size={14} />
                  <b style={{ color: '#0f172a' }}>{x.antecedent}</b>
                </div>

                {x.is_ambiguous ? (
                  <span style={{ fontSize: '10px', color: '#b45309', background: '#fef3c7', padding: '2px 8px', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
                    <AlertCircle size={12} /> Ambiguous
                  </span>
                ) : (
                  <span style={{ fontSize: '10px', color: '#15803d', background: '#dcfce7', padding: '2px 8px', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
                    <Check size={12} /> Resolved
                  </span>
                )}
              </div>

              {x.candidates && x.candidates.length > 1 && (
                <div style={{ fontSize: '10px', color: '#92400e', marginTop: '6px' }}>
                  <b>Candidate Antecedents in Discourse:</b> {x.candidates.join(', ')}
                </div>
              )}

              <small style={{ display: 'block', marginTop: '6px', color: 'var(--text-muted)', fontSize: '10px' }}>
                {x.rule}
              </small>
            </div>
          ))
        ) : (
          <div className="muted">No coreference chains resolved.</div>
        )}
      </div>

      {/* Discourse Relations & Pragmatics */}
      <div className="panel">
        <div className="panel-title">
          <div>
            <h3>Discourse Connectives & Relations</h3>
            <span>Causal, contrastive, resultative, and temporal transitions</span>
          </div>
          <span className="pill">{relations.length} Connectives</span>
        </div>

        {relations.length ? (
          relations.map((x, i) => (
            <div className="relation" key={i} style={{ marginBottom: '10px', display: 'flex', flexDirection: 'column', alignItems: 'stretch', padding: '10px', background: '#fafaf9', borderRadius: '8px', border: '1px solid #f2f2ef' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <b style={{ color: '#1e293b' }}>"{x.connective}"</b>
                <span style={{ color: '#6366f1', fontWeight: 700, fontSize: '10px', background: '#eef2ff', padding: '2px 8px', borderRadius: '12px' }}>
                  {x.relation}
                </span>
              </div>
              {x.snippet && (
                <div style={{ margin: '6px 0 3px 0', fontSize: '11px', color: '#475569', fontStyle: 'italic' }}>
                  {x.snippet}
                </div>
              )}
              {x.description && (
                <small style={{ color: '#94a3b8', fontSize: '9px' }}>
                  {x.description}
                </small>
              )}
            </div>
          ))
        ) : (
          <div className="muted">No discourse connectives detected.</div>
        )}

        {/* Pragmatics */}
        <h3 className="mt" style={{ marginTop: '1.8rem', marginBottom: '0.8rem' }}>
          Pragmatic Speech Acts & Indirect Inferences
        </h3>
        {pragmatics.length ? (
          pragmatics.map((x, i) => (
            <div className="inference" key={i} style={{ marginBottom: '10px', background: '#f5f3ff', border: '1px solid #ddd6fe', padding: '12px', borderRadius: '8px' }}>
              <Sparkles size={16} style={{ color: '#7c3aed', flexShrink: 0, marginTop: '2px' }} />
              <div>
                <b style={{ color: '#5b21b6', fontSize: '12px' }}>{x.inference}</b>
                <span style={{ display: 'block', color: '#1e1b4b', fontWeight: 500, margin: '4px 0 2px 0', fontSize: '11px' }}>
                  "{x.pattern}"
                </span>
                {x.explanation && (
                  <small style={{ color: '#6d28d9', fontSize: '10px', display: 'block' }}>
                    {x.explanation}
                  </small>
                )}
              </div>
            </div>
          ))
        ) : (
          <div className="muted">No indirect requests or speech acts detected.</div>
        )}
      </div>
    </div>
  )
}

