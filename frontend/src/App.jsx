import { useEffect, useState } from 'react';

const featureCards = [
  {
    title: 'Search and filter',
    description: 'Explore products by category, country, ingredients, labels, and nutrition grade.',
  },
  {
    title: 'Compare products',
    description: 'Line up two or more items and inspect nutrition, additives, and score deltas.',
  },
  {
    title: 'Analyze trends',
    description: 'Use charts and summaries to spot nutrition patterns across the dataset.',
  },
];

export default function App() {
  const [health, setHealth] = useState('checking');

  useEffect(() => {
    let active = true;

    fetch('/api/health')
      .then((response) => response.json())
      .then((data) => {
        if (active) {
          setHealth(data.status === 'ok' ? 'connected' : 'offline');
        }
      })
      .catch(() => {
        if (active) {
          setHealth('offline');
        }
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <main className="app-shell">
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Open Food Facts dashboard</p>
          <h1>Start with a clean product intelligence workspace.</h1>
          <p className="lead">
            This scaffold connects a Flask API to a React frontend and gives you a base for search,
            comparison, and nutrition analytics.
          </p>
          <div className="status-row">
            <span className={`status-dot ${health}`}></span>
            <span>API status: {health}</span>
          </div>
        </div>

        <div className="hero-panel">
          <div className="metric-card">
            <span className="metric-label">Dataset</span>
            <strong>Open Food Facts TSV</strong>
          </div>
          <div className="metric-card accent">
            <span className="metric-label">Backend</span>
            <strong>Flask on :5000</strong>
          </div>
          <div className="metric-card">
            <span className="metric-label">Frontend</span>
            <strong>Vite on :3000</strong>
          </div>
        </div>
      </section>

      <section className="feature-grid" aria-label="Project starter features">
        {featureCards.map((card) => (
          <article key={card.title} className="feature-card">
            <h2>{card.title}</h2>
            <p>{card.description}</p>
          </article>
        ))}
      </section>
    </main>
  );
}