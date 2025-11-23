import React from 'react';
import '../styles/App.css';

export default function HomePage({ onClick }) {

  return (
    <main className="container">
      <div className="home-row" style={{marginBottom: '2rem'}}>
        <div className="home-left">
          <img src={require('../images/PLANT_IT.png')} alt="Plant It Logo" style={{width: '100%', height: 'auto', marginBottom: '5rem'}}/>
          <button style={{backgroundColor: 'var(--color-secondary)', width: '35%', height: '3.5rem', fontWeight: '800', fontSize: '1.25rem'}} className="btn btn-primary" onClick={onClick}>Start Planting</button>
        </div>
      </div>
      <div className="dome-cut" aria-hidden>
        <img src={require('../images/domes_image.jpg')} alt="" />
      </div>
    </main>
  );
}
