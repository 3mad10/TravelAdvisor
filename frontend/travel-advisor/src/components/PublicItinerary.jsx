import { useEffect, useState } from "react";
import './Itinerary.css';
import Activity from "./Activity"
import api from "../api";

const PublicItinerary = ({showActivitiesOnly, activities}) => {
  if(activities) {
    return (
    <div>
      {activities.map(
        (activity, index) => {
          return <Activity key={index} activity={activity} />
        }
      )}
    </div>
  ) 
  }
  
}
export default PublicItinerary


