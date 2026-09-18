import {Sparkles, SpellCheck, Network, Brain, MessageSquareText, BarChart3, ChevronRight} from './Icons'
import {stages} from '../data/samples'
const icons=[SpellCheck,Network,Brain,MessageSquareText,BarChart3]
export default function Sidebar({tab,setTab}){return <aside className="sidebar">
  <div className="brand"><div className="logo"><Sparkles size={18}/></div><div><b>LexiFlow</b><span>NLP Writing Lab</span></div></div>
  <div className="side-label">WORKSPACE</div>
  {stages.map(([id,label],i)=>{const Icon=icons[i]; return <button className={`nav ${tab===id?'active':''}`} onClick={()=>setTab(id)} key={id}><span className="navicon"><Icon size={16}/></span><span><strong>0{i+1}</strong>{label}</span><ChevronRight size={14}/></button>})}
  <div className="side-card"><Sparkles size={17}/><div><b>Pipeline ready</b><p>Five visible NLP stages, designed for inspection and demo.</p></div></div>
  <div className="side-footer">Smart Reading & Writing Assistant<br/><span>React workspace · v3</span></div>
</aside>}
