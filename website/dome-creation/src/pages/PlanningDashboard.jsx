import React from 'react';
import LeftPane from '../components/LeftPane.jsx';
import RightPane from '../components/RightPane.jsx';
import ShowDome from '../components/ShowDome.jsx';

export default function PlanningDashboard({ onClick }){
  return (
    <div className="home-row">
        <LeftPane></LeftPane>
        <ShowDome></ShowDome>
        <RightPane></RightPane>
    </div>
  );
}
