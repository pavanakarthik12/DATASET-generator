import React from 'react';

const HeroSection = () => {
  const goToApp = () => {
    window.location.hash = '#/app';
    setTimeout(() => {
      const el = document.getElementById('data');
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 0);
  };

  const learnMore = () => {
    const target = document.getElementById('learn-more');
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <section className="hero" role="region" aria-label="Smart Dataset Generator overview">
      <div className="hero-blob hero-blob-a" aria-hidden="true" />
      <div className="hero-blob hero-blob-b" aria-hidden="true" />
      <div className="hero-ring hero-ring-a" aria-hidden="true" />
      <div className="hero-ring hero-ring-b" aria-hidden="true" />
      <div className="hero-constellation" aria-hidden="true" />
      <div className="hero-bottom-fade" aria-hidden="true" />
      <div className="container">
        <div className="hero-grid">
          <div className="hero-content">
            <div className="hero-eyebrow">Smart Dataset Generator</div>
            <h1 className="hero-title">Build datasets in minutes, not days</h1>
            <p className="hero-subtitle">
              Fetch, combine, and export data from weather, stocks, news, and images—
              all in one streamlined workspace.
            </p>
            <div className="hero-features" aria-hidden="true">
              <span className="feature-pill">Weather</span>
              <span className="feature-pill">Stocks</span>
              <span className="feature-pill">News</span>
              <span className="feature-pill">Images</span>
            </div>
            <div className="hero-actions">
              <button className="hero-cta" onClick={goToApp}>Generate Dataset</button>
              <button className="hero-cta-secondary" onClick={learnMore}>Learn More</button>
            </div>
            <ul className="hero-stats" aria-label="Key stats">
              <li>
                <span className="stat-value">4+</span>
                <span className="stat-label">Data sources</span>
              </li>
              <li>
                <span className="stat-value">60s</span>
                <span className="stat-label">To first dataset</span>
              </li>
              <li>
                <span className="stat-value">Zero</span>
                <span className="stat-label">Setup required</span>
              </li>
            </ul>
          </div>
          <div className="hero-aside">
            <div className="hero-card" aria-hidden="true">
              <div className="card-header">Dataset Preview</div>
              <div className="card-table">
                <div className="card-row card-row-h">
                  <span>source</span>
                  <span>field</span>
                  <span>value</span>
                </div>
                <div className="card-row">
                  <span>weather</span>
                  <span>temp_c</span>
                  <span>27.4</span>
                </div>
                <div className="card-row">
                  <span>stocks</span>
                  <span>close</span>
                  <span>193.12</span>
                </div>
                <div className="card-row">
                  <span>news</span>
                  <span>sentiment</span>
                  <span>0.82</span>
                </div>
                <div className="card-row">
                  <span>images</span>
                  <span>keywords</span>
                  <span>ocean, sunrise</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Highlights */}
        <div className="hero-highlights" aria-label="Highlights">
          <div className="highlight-card">
            <div className="highlight-title">Unified workflow</div>
            <div className="highlight-sub">Fetch, preview, export in one place</div>
          </div>
          <div className="highlight-card">
            <div className="highlight-title">Flexible exports</div>
            <div className="highlight-sub">CSV, JSON, and Parquet ready</div>
          </div>
          <div className="highlight-card">
            <div className="highlight-title">AI assistant</div>
            <div className="highlight-sub">Chat to refine your dataset</div>
          </div>
        </div>

        {/* 3-step guide */}
        <div className="hero-steps" aria-label="How it works">
          <div className="step-item">
            <div className="step-num">1</div>
            <div className="step-content">
              <div className="step-title">Choose a source</div>
              <div className="step-desc">Weather, stocks, news, or images</div>
            </div>
          </div>
          <div className="step-item">
            <div className="step-num">2</div>
            <div className="step-content">
              <div className="step-title">Configure fields</div>
              <div className="step-desc">Set filters, locations, and ranges</div>
            </div>
          </div>
          <div className="step-item">
            <div className="step-num">3</div>
            <div className="step-content">
              <div className="step-title">Export instantly</div>
              <div className="step-desc">Download your dataset in one click</div>
            </div>
          </div>
        </div>

        {/* Logos strip (placeholders) */}
        <div className="logos-strip" aria-hidden="true">
          <div className="logos-grid">
            <span className="logo-dot" />
            <span className="logo-dot" />
            <span className="logo-dot" />
            <span className="logo-dot" />
            <span className="logo-dot" />
            <span className="logo-dot" />
          </div>
        </div>

        {/* Secondary block for Learn More anchor */}
        <section id="learn-more" className="hero-secondary" aria-label="Details">
          <div className="secondary-grid">
            <div className="secondary-copy">
              <h2>Why teams choose Smart Dataset Generator</h2>
              <p>
                Reduce switching costs, avoid brittle scripts, and keep your focus on insights.
                Powerful defaults with just enough flexibility for advanced users.
              </p>
              <ul className="secondary-points">
                <li className="secondary-point">Consistent schema across sources</li>
                <li className="secondary-point">Instant previews before export</li>
                <li className="secondary-point">No setup or credentials required to try</li>
              </ul>
              <div className="hero-actions">
                <button className="hero-cta" onClick={goToApp}>Start now</button>
                <button className="hero-cta-secondary" onClick={goToApp}>See examples</button>
              </div>
            </div>
            <div className="secondary-visual" aria-hidden="true">
              <div className="secondary-card" />
            </div>
          </div>
        </section>
      </div>
    </section>
  );
};

export default HeroSection;