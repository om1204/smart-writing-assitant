export default function SemanticPanel({ data }) {
  const sentences = data.sentences || (Array.isArray(data.semantics) ? data.semantics : data.semantics?.sentences) || []

  return (
    <div className="stack">
      {sentences.map((s, i) => (
        <div className="panel" key={i}>
          <div className="panel-title">
            <h3>Sentence {i + 1}</h3>
          </div>

          <div className="semgrid">
            {/* Entities & Concepts */}
            <div>
              <h4>Entities & Domain Terminology</h4>
              {s.entities && s.entities.length ? (
                <div>
                  {s.entities.map((e, j) => {
                    const isNER = e.category && e.category.includes('Named Entity')
                    return (
                      <div
                        className="entity"
                        key={j}
                        title={e.description || e.label}
                        style={{
                          background: isNER ? 'rgba(59, 130, 246, 0.07)' : 'rgba(147, 51, 234, 0.07)',
                          borderColor: isNER ? 'rgba(59, 130, 246, 0.3)' : 'rgba(147, 51, 234, 0.3)'
                        }}
                      >
                        <b>{e.text}</b>
                        <span style={{ color: isNER ? '#2563eb' : '#9333ea', fontWeight: 600 }}>
                          {e.label}
                        </span>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div className="muted">No entities identified.</div>
              )}
            </div>

            {/* Semantic Role Frames */}
            <div>
              <h4>Semantic Role Frames (Agent · Action · Patient)</h4>
              {s.semantic_frames && s.semantic_frames.length ? (
                s.semantic_frames.map((f, j) => (
                  <div className="frame" key={j} style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '5px', padding: '10px' }}>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                      <span style={{ background: '#e0f2fe', color: '#0369a1', padding: '2px 6px', borderRadius: '4px', fontSize: '10px' }}>Agent</span>
                      <b>{f.agent || '—'}</b>
                      <span style={{ color: '#6b7280' }}>→</span>
                      <span style={{ background: '#f3e8ff', color: '#7e22ce', padding: '2px 6px', borderRadius: '4px', fontSize: '10px' }}>Action</span>
                      <b>{f.action}</b>
                      <span style={{ color: '#6b7280' }}>→</span>
                      <span style={{ background: '#dcfce7', color: '#15803d', padding: '2px 6px', borderRadius: '4px', fontSize: '10px' }}>Patient</span>
                      <b>{f.patient || '—'}</b>
                    </div>
                    {f.explanation && (
                      <small style={{ color: 'var(--text-muted)', fontSize: '10px', marginTop: '2px' }}>
                        {f.explanation}
                      </small>
                    )}
                  </div>
                ))
              ) : (
                <div className="muted">No frames extracted.</div>
              )}
            </div>
          </div>

          {/* Word Sense Disambiguation */}
          {s.word_senses && s.word_senses.length > 0 && (
            <div style={{ marginTop: '20px' }}>
              <h4>Word-Sense Disambiguation (WordNet Lesk Algorithm)</h4>
              <div className="sensegrid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>
                {s.word_senses.map((w, j) => (
                  <div key={j} style={{ borderLeft: '3px solid #0284c7', background: '#f8fafc', padding: '14px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <b style={{ fontSize: '14px', color: '#0f172a' }}>"{w.word}"</b>
                      <span className="pill" style={{ background: '#e0f2fe', color: '#0369a1', borderColor: '#bae6fd' }}>
                        {w.synset}
                      </span>
                    </div>

                    <span style={{ color: '#0284c7', fontWeight: 700, fontSize: '0.85rem', display: 'block', margin: '6px 0' }}>
                      {w.sense_label}
                    </span>

                    <p style={{ margin: '4px 0 8px 0', fontSize: '11px', color: '#475569', lineHeight: 1.5 }}>
                      {w.definition}
                    </p>

                    <div style={{ fontSize: '10px', color: '#64748b', background: '#fff', padding: '6px 8px', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                      <b>Evidence:</b> {w.reason}
                    </div>

                    {w.all_candidates && w.all_candidates.length > 1 && (
                      <div style={{ marginTop: '8px', fontSize: '9px', color: '#94a3b8' }}>
                        <b>Alternative Synsets Tested:</b>{' '}
                        {w.all_candidates.slice(1, 3).map(c => `${c.synset} (score ${c.score})`).join(' · ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

