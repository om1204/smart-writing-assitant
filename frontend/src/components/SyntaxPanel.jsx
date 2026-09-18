export default function SyntaxPanel({ data }) {
  const sentences = data.sentences || (Array.isArray(data.syntax) ? data.syntax : data.syntax?.sentences) || []
  const grammarRules = data.grammar_rules || data.syntax?.grammar_rules || [
    "S -> NP VP", "S -> S CONJ", "S -> CONJ S", "NP -> DET N", "NP -> ADJ N",
    "NP -> N N", "NP -> NP PP", "NP -> PRON N", "VP -> V NP", "VP -> V PP",
    "VP -> AUX VP", "VP -> V ADV", "VP -> V S", "PP -> P NP"
  ]

  return (
    <div className="stack">
      {/* Hand-written CFG Grammar Specification */}
      <div className="panel" style={{ borderLeft: '4px solid #7c5df5' }}>
        <div className="panel-title">
          <div>
            <h3>Hand-Written Context-Free Grammar (CFG)</h3>
            <span>Small 14-rule canonical grammar executed via Cocke-Younger-Kasami (CKY) dynamic programming parser</span>
          </div>
          <span className="pill" style={{ background: '#eee9ff', color: '#6d43ff', borderColor: '#c4b5fd' }}>
            {grammarRules.length} Production Rules
          </span>
        </div>
        <div className="chips" style={{ gap: '6px' }}>
          {grammarRules.map((rule, idx) => (
            <span key={idx} style={{ background: '#faf9fe', borderColor: '#e4dcfb', fontFamily: 'DM Mono' }}>
              <small style={{ color: '#8b5cf6', marginRight: '4px' }}>R{idx + 1}:</small>
              <b>{rule}</b>
            </span>
          ))}
        </div>
      </div>

      {/* Sentence-level syntactic analyses */}
      {sentences.map((s, i) => (
        <div className="panel" key={i}>
          <div className="panel-title">
            <div>
              <h3>Sentence {i + 1}</h3>
              <span>{s.sentence}</span>
            </div>
          </div>
          
          {s.svo_triples && s.svo_triples.length > 0 && (
            <>
              <h4>Subject / Object Relationships (SVO Triples)</h4>
              <div className="chips" style={{ marginBottom: '1rem' }}>
                {s.svo_triples.map((t, k) => (
                  <span key={k} style={{ background: 'rgba(59, 130, 246, 0.08)', borderColor: 'rgba(59, 130, 246, 0.3)', padding: '8px 12px' }}>
                    <b style={{ color: '#1d4ed8' }}>{t.subject}</b>
                    <span style={{ margin: '0 6px', color: '#6b7280' }}>→</span>
                    <i style={{ color: '#7c3aed', fontWeight: 600 }}>{t.verb}</i>
                    <span style={{ margin: '0 6px', color: '#6b7280' }}>→</span>
                    <b style={{ color: '#047857' }}>{t.object}</b>
                  </span>
                ))}
              </div>
            </>
          )}

          <h4>Part of Speech (POS) Sequence</h4>
          <div className="chips">
            {s.pos.map((x, j) => (
              <span key={j}>
                <b>{x.token}</b>
                <small>{x.pos}</small>
              </span>
            ))}
          </div>

          <h4>Dependency Arcs (spaCy Head/Relation)</h4>
          <div className="depgrid">
            {s.dependencies.map((x, j) => (
              <div key={j}>
                <b>{x.token}</b>
                <span>{x.dep}</span>
                <small>→ {x.head}</small>
              </div>
            ))}
          </div>

          <h4>Hand-written CKY / Constituent Parse Tree</h4>
          <pre>{Array.isArray(s.cky_tree) ? s.cky_tree.join('\n') : s.cky_tree}</pre>
        </div>
      ))}
    </div>
  )
}

