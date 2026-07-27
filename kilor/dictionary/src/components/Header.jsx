import SettingsPanel from './SettingsPanel';

export default function Header({ total, exportedAt, settingsOpen, onSettingsToggle, showModified, onToggleModified }) {
  return (
    <header className="header">
      <div className="header-left">
        <h1>Kilor Dictionary</h1>
        <p>{total} words{exportedAt ? ' · ' + exportedAt : ''}</p>
      </div>
      <div className="header-right">
        <button
          className="settings-gear-btn"
          onClick={onSettingsToggle}
          title="Settings"
        >
          ⚙
        </button>
        {settingsOpen && (
          <SettingsPanel
            showModified={showModified}
            onToggleModified={onToggleModified}
            onClose={onSettingsToggle}
          />
        )}
      </div>
    </header>
  );
}
