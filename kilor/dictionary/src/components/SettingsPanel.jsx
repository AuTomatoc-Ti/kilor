export default function SettingsPanel({ showModified, onToggleModified, showAudio, onToggleAudio, onClose }) {
  return (
    <div className="settings-overlay" onClick={onClose}>
      <div className="settings-dropdown" onClick={(e) => e.stopPropagation()}>
        <div className="settings-header">
          <h3>Settings</h3>
          <button className="settings-close-btn" onClick={onClose}>✕</button>
        </div>
        <label className="settings-row">
          <input
            type="checkbox"
            checked={showModified}
            onChange={onToggleModified}
          />
          <span>Show "Last Modified" column</span>
        </label>
        <label className="settings-row">
          <input
            type="checkbox"
            checked={showAudio}
            onChange={onToggleAudio}
          />
          <span>Audio pronunciation 🔊 (experimental)</span>
        </label>
      </div>
    </div>
  );
}