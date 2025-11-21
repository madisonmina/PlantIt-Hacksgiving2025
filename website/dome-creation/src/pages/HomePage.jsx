import React from 'react';
import '../styles/App.css';

export default function HomePage({ onClick }) {

  return (
    <main className="container" style={{paddingTop: '4rem', paddingBottom: '4rem'}}>
      <div className="card" style={{textAlign: 'center', padding: '2.25rem'}}>
        <img src="/HomePage.png" alt="PLANT_IT Logo" style={{maxWidth: 800, width: '100%', height: 'auto', marginBottom: '1rem'}} />

        <h1 style={{fontFamily: 'var(--font-heading)', margin: '0.25rem 0'}}>PLANT IT!</h1>
        <p className="lead" style={{marginTop: 8}}>Plant planning reimagined for the Milwaukee Domes.</p>
        <p className="small" style={{marginTop: 8, color: 'var(--color-muted)'}}>
          Design seasonal layouts, explore plant compatibility, and build stunning displays with smart, data-driven tools made for horticulture teams.
        </p>

        <div style={{marginTop: '1.25rem'}}>
          <button className="btn btn-primary" onClick={onClick}>Start Planting</button>
        </div>
      </div>
    </main>
  );
}
