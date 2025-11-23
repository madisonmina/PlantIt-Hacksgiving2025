import React, { useState } from 'react';
import './styles/App.css';
import HomePage from './pages/HomePage';
import PlanningDashboard from './pages/PlanningDashboard';



function App() {
  const [isPlanting, setIsPlanting] = useState(false);
  function switchPages() {
  if(!isPlanting) {
    setIsPlanting(true);
  } else {
    setIsPlanting(false);
  }
}  
  return (
    <div className="App">
      {!isPlanting && (
          <HomePage onClick={switchPages} />
        )}
      {isPlanting && (
          <PlanningDashboard onClick={switchPages} />
        )}
    </div>
  );
}



export default App;
