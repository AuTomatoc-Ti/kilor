export default function Legend({ open, prefixInfo }) {
  return (
    <div className={'legend' + (open ? ' open' : '')}>
      <h3>Colour Prefixes</h3>
      <div className="legend-grid">
        {Object.entries(prefixInfo).map(([key, info]) => (
          <div className="legend-item" key={key}>
            <span className="legend-swatch" style={{ background: info.color, border: key === 'o-' ? '1px dashed #ccc' : 'none' }}></span>
            <b>{key}</b> {info.cls} · {info.emotion}
          </div>
        ))}
      </div>
      <h3 style={{ marginTop: 10 }}>Section Codes</h3>
      <div className="legend-grid">
        <span>A — Worlds & Elements</span><span>B — Living Things</span>
        <span>C — Physical Objects</span><span>D — Actions & Motion</span>
        <span>E — Qualities & States</span><span>F — Mind & Emotion</span>
        <span>G — Time & Space</span><span>H — Social & Relational</span>
        <span>I — Abstract</span><span>J — Sensation</span>
      </div>
      <h3 style={{ marginTop: 10 }}>NVAD Mask</h3>
      <div>Each letter = word can function as: <b>N</b>oun, <b>V</b>erb, <b>A</b>djective, <b>D</b>adverb. &ldquo;closed-class&rdquo; = function word.</div>
    </div>
  );
}