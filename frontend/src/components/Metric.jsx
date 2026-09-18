export default function Metric({n,label,sub}){return <div className="metric"><b>{n}</b><span>{label}</span>{sub&&<small>{sub}</small>}</div>}
