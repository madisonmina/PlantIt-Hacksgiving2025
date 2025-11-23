import React from 'react';
import '../styles/RightPane.css';
export default function RightPane({selectedPlants, removePlant, generatePlan}){
    return (
        <div className="right-pane">
            <div className="title">
                <h2>Selected</h2>
            </div>
            <div className="pane-content">
                {selectedPlants.map((plant, index) => (
                    <p key={index} onClick={() => removePlant(plant)}>{plant}</p>
                ))}
            </div>
            <div className="generate" onClick={() => generatePlan()}>
                <h2>Generate Plan</h2>
            </div>
        </div>
    );       
}     