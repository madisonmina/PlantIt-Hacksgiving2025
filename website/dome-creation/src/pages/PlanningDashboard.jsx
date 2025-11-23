import React from 'react';
import LeftPane from '../components/LeftPane.jsx';
import RightPane from '../components/RightPane.jsx';
import ShowDome from '../components/ShowDome.jsx';
import { useState } from 'react';


export default function PlanningDashboard({ onClick }){
    let plantTypes = [
      "Rose",
      "Tulip",
      "Daisy",
      "Sunflower",
      "Lavender",
      "Fern",
      "Bamboo",
      "Orchid",
      "Succulent",
      "Cactus",
      "Marigold",
      "Pansy",
      "Begonia",
      "Hydrangea",
      "Peony",
      "Azalea",
      "Jasmine",
      "Lily",
      "Snapdragon",
      "Iris",
      "Zinnia",
      "Petunia",
      "Geranium",
      "Fuchsia",
      "Rosemary",
      "Thyme",
      "Basil",
      "Mint",
      "Sage",
      "Oregano",
      "Aloe Vera",
      "Monstera",
      "Ficus",
      "Rubber Plant",
      "Philodendron",
      "Hosta",
      "Camellia",
      "Daffodil",
      "Bluebell",
      "Cherry Blossom"
    ];
    const [selectedPlants, setSelectedPlants] = useState([]);
    function selectPlant(plant) {
        setSelectedPlants(prev => {
            if (prev.includes(plant)) return prev;
            return [...prev, plant];
        });
    }
    function removePlant(plant) {
        setSelectedPlants(prev => prev.filter(p => p !== plant));
    }
    function generatePlan() {
        
    }    
    return (
        <div className="home-row">
            <LeftPane plantTypes={plantTypes} selectPlant={selectPlant}></LeftPane>
            <ShowDome></ShowDome>
            <RightPane selectedPlants={selectedPlants} removePlant={removePlant} generatePlan={generatePlan}></RightPane>
        </div>
    );
}

    
