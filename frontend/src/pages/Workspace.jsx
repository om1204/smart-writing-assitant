import { useState } from 'react'
import Sidebar from '../components/Sidebar'
import Editor from '../components/Editor'
import Metric from '../components/Metric'
import SpellPanel from '../components/SpellPanel'
import SyntaxPanel from '../components/SyntaxPanel'
import SemanticPanel from '../components/SemanticPanel'
import DiscoursePanel from '../components/DiscoursePanel'
import OverviewPanel from '../components/OverviewPanel'
import { AlertCircle, Activity } from '../components/Icons'
import { stages, samples } from '../data/samples'
import { usePipeline } from '../hooks/usePipeline'

export default function Workspace() {
  const [text, setText] = useState(samples[0])
  const [tab, setTab] = useState('spell')
  const [copied, setCopied] = useState(false)
  const { result, loading, error, run, setResult } = usePipeline()

  async function execute() {
    const ok = await run(text)
    if (ok) setTab('spell')
  }

  async function copy() {
    await navigator.clipboard?.writeText(result?.corrected_text || '')
    setCopied(true)
    setTimeout(() => setCopied(false), 1200)
  }

  // Stage-isolated metrics: each stage panel shows ONLY its own verified metrics
  const getStageMetrics = () => {
    if (!result) return []
    const spell = result.spell || {}
    const syntax = result.syntax || {}
    const semantics = result.semantics || {}
    const discourse = result.discourse || {}
    const overview = result.overview || {}

    if (tab === 'spell') {
      return [
        { label: 'Words Scanned', n: spell.words_scanned || 0 },
        { label: 'Flagged Typos', n: (spell.corrections || []).length },
        { label: 'Cleaned Words', n: (spell.corrections || []).length }
      ]
    }
    if (tab === 'syntax') {
      return [
        { label: 'Sentences', n: syntax.total_sentences || (syntax.sentences || []).length },
        { label: 'SVO Triples', n: syntax.total_svo_triples || 0 },
        { label: 'CFG Rules', n: (syntax.grammar_rules || []).length || 14 }
      ]
    }
    if (tab === 'semantic') {
      return [
        { label: 'Entities (NER)', n: (semantics.named_entities || []).length },
        { label: 'Domain Concepts', n: (semantics.domain_concepts || []).length },
        { label: 'WSD Targets', n: (semantics.wsd_disambiguations || []).length }
      ]
    }
    if (tab === 'discourse') {
      return [
        { label: 'Coref Chains', n: (discourse.coreference_chains || []).length },
        { label: 'Connectives', n: (discourse.discourse_relations || []).length },
        { label: 'Pragmatic Acts', n: (discourse.pragmatic_inferences || []).length }
      ]
    }
    // Full overview tab: holistic KPI overview
    return [
      { label: 'Latency (ms)', n: overview.execution_time_ms || 0 },
      { label: 'Total Errors', n: overview.summary_metrics?.spelling_errors || 0 },
      { label: 'Sentences', n: overview.summary_metrics?.sentences || 0 },
      { label: 'Entities & Terms', n: overview.summary_metrics?.entities_and_concepts || 0 }
    ]
  }

  return (
    <div className="app">
      <Sidebar tab={tab} setTab={setTab} />
      <main className="main">
        <header>
          <div>
            <div className="eyebrow">NLP PIPELINE / LIVE WORKSPACE</div>
            <h1>Make messy writing <em>make sense.</em></h1>
            <p>Inspect every transformation from raw student text to structured linguistic insight.</p>
          </div>
          <div className="status"><i />API workspace</div>
        </header>

        <Editor
          text={text}
          setText={setText}
          run={execute}
          loading={loading}
          onClear={() => { setText(''); setResult(null); }}
        />

        {error && (
          <div className="error">
            <AlertCircle size={18} />
            <div>
              <b>Pipeline error</b>
              <span>{error}</span>
            </div>
          </div>
        )}

        {!result && !error && (
          <section className="empty">
            <Activity size={24} />
            <h3>Ready for analysis</h3>
            <p>Run the pipeline to inspect spelling, syntax, semantics, discourse and the final structured output.</p>
          </section>
        )}

        {result && (
          <section className="workspace">
            <div className="result-head">
              <div>
                <span className="pill">ANALYSIS RESULT</span>
                <h2>{stages.find(x => x[0] === tab)?.[1]}</h2>
              </div>
              <div className="metrics">
                {getStageMetrics().map(m => (
                  <Metric key={m.label} n={m.n} label={m.label} />
                ))}
              </div>
            </div>

            {tab === 'spell' && <SpellPanel data={result.spell || result} onCopy={copy} copied={copied} />}
            {tab === 'syntax' && <SyntaxPanel data={result.syntax || result} />}
            {tab === 'semantic' && <SemanticPanel data={result.semantics || result} />}
            {tab === 'discourse' && <DiscoursePanel data={result.discourse || result} />}
            {tab === 'full' && <OverviewPanel data={result} />}
          </section>
        )}
      </main>
    </div>
  )
}

