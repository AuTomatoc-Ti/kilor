export default function Header({ total, exportedAt }) {
  return (
    <header className="header">
      <div className="header-left">
        <h1>Kilor Dictionary</h1>
        <p>{total} words{exportedAt ? ' · ' + exportedAt : ''}</p>
      </div>
    </header>
  );
}