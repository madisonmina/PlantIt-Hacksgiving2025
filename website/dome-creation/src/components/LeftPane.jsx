import React from 'react';
import '../styles/LeftPane.css';
export default function LeftPane({plantTypes, selectPlant}){
    
    return (
        <div className="left-pane">
            <div className="title">
                <h2>Plant Types</h2>
            </div>
            <div className="pane-content">
                {plantTypes.map((plant, index) => (
                    <p key={index} onClick={() => selectPlant(plant)}>{plant}</p>
                ))}
            </div>
        </div>
    );       
}     