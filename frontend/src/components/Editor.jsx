import {Play, RotateCcw} from './Icons'
import {samples, sampleLabels} from '../data/samples'

export default function Editor({text, setText, run, loading, onClear}) {
  return (
    <section className="editor-card">
      <div className="card-head">
        <div>
          <span className="pill">INPUT</span>
          <h2>Write or paste a paragraph</h2>
        </div>
        <select 
          value={Math.max(-1, samples.indexOf(text))} 
          onChange={e => setText(samples[Number(e.target.value)] || '')}
        >
          <option value={-1}>Choose a test sample…</option>
          {samples.map((_, i) => (
            <option value={i} key={i}>
              {sampleLabels[i] || `Sample ${i + 1}`}
            </option>
          ))}
        </select>
      </div>
      <textarea 
        value={text} 
        onChange={e => setText(e.target.value)} 
        placeholder="Paste student writing here…"
        rows={6}
      />
      <div className="editor-foot">
        <span>{text.length} characters · {text.trim() ? text.trim().split(/\s+/).length : 0} words</span>
        <div>
          <button className="ghost" onClick={onClear}>
            <RotateCcw size={14}/>Clear
          </button>
          <button className="run" onClick={run} disabled={loading || !text.trim()}>
            {loading ? <span className="loader"/> : <Play size={15} fill="currentColor"/>}
            {loading ? 'Processing…' : 'Run pipeline'}
          </button>
        </div>
      </div>
    </section>
  )
}
