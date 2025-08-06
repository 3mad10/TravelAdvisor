import { useEffect, useState } from "react";
import './Itinerary.css';
import api from "../api";


const Activity = ({activity}) => {
    // console.log(activity);
  if (!activity || !activity.location) return null;
  return (
    <div className="text-xs">
        <span>Day {activity.day}</span>
        <span>&#8943;</span>
        <span>{activity.location}</span>
        <div>{activity.short_name}</div>
    </div>
  )
}
export default Activity
