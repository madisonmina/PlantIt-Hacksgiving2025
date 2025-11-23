import React from 'react';
import '../styles/ShowDome.css';
export default function ShowDome(){
    return (
        <div className="show-dome">
            <img src={require('../images/show_dome_map.png')} alt="Dome Map" style={{width: '100%', height: 'auto'}}/>
        </div>
    );       
}     