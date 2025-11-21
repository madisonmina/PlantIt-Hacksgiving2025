import React from 'react';

export default function PlanningDashboard({ onClick }){
  return (
    <main className="container" style={{paddingTop: '3rem', paddingBottom: '3rem'}}>
      <div className="card">
        <h1 style={{fontFamily: 'var(--font-heading)'}}>Planning Dashboard</h1>
        <p className="lead">This is the planning dashboard placeholder. Replace with your planning UI.</p>
        <div style={{marginTop: 12}}>
          <button className="btn btn-outline" onClick={onClick}>Back</button>
        </div>
      </div>
    </main>
  );
}
