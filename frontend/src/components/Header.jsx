function Header() {
  return (
    <header className="site-header">
      <div className="brand">
        <div className="brand-icon">WSW</div>

        <div>
          <div className="logo">Who Said What</div>
          <div className="brand-subtitle">
            Cross-Source Media Analysis
          </div>
        </div>
      </div>

      <nav className="nav-links">
        <a href="#">Home</a>
        <a href="#compare">Compare</a>
        <a href="#timeline">Timeline</a>
        <a href="#coverage">Bias & Coverage</a>
      </nav>
    </header>
  )
}

export default Header