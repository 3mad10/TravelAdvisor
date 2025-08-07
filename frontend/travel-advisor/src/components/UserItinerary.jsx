import { useEffect, useState } from "react";
import './Itinerary.css';
import PublicItinerary from "./PublicItinerary";
import api from "../api";

const UserItinerary = ({activities, userSpecificItineraryInfo, isSaved, onSave, onDelete, isLoggedIn}) => {
    const [errorState, setErrorState] = useState(false);
    const [errorMessage, setErrorMessage] = useState();

    const deleteHandler = async () => {
        if(userSpecificItineraryInfo) {
            const token = localStorage.getItem("token");
            const response = await api.delete(`/api/itinerary/${userSpecificItineraryInfo.id}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            });
            onDelete(userSpecificItineraryInfo.id);
        }
    }

    const saveHandler = async () => {
        if(userSpecificItineraryInfo && activities) {
            const token = localStorage.getItem("token");
            console.log(activities)
            try {
                    const request = {
                        'destination': userSpecificItineraryInfo.destination,
                        'interests': userSpecificItineraryInfo.interests,
                        'activities': activities,
                        'start_date': userSpecificItineraryInfo.start_date,
                        'end_date': userSpecificItineraryInfo.end_date
                    }
                    const response = await api.post("/api/itinerary/", request, {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        }
                    });
                    setErrorState(false);
                    setErrorMessage("");
                    onSave(userSpecificItineraryInfo.id);
            } catch(error) {
                if(error.status===403) {
                    setErrorState(true);
                    setErrorMessage("Login to be able to save a new plan");
                }
            }

        }
    }

    useEffect( () => {
        console.log("entered useEffect")
        if(isLoggedIn && errorState) {
            setErrorState(false);
            setErrorMessage("");
        }
    }, [isLoggedIn]);

    if(activities && userSpecificItineraryInfo) {
        return (
            <div className="flex flex-col justify-center shadow-2xl pb-2 border-cyan-300 rounded-md border-b-2 shadow-2xl">
                <div className="text-cyan-700 self-center-safe text-center uppercase p-6 bg-white shadow-2xl border-b-2 w-full max-w-2xl">
                    {userSpecificItineraryInfo.destination}
                </div>
                <div className="text-cyan-600 text-center p-6 bg-white rounded-lg shadow-md w-full max-w-2xl">
                    Staring {userSpecificItineraryInfo.start_date}
                </div>
                <div>
                    {isSaved ? <PublicItinerary activities={[activities[0]]}/> : <PublicItinerary activities={activities}/>}
                    {isSaved && (<button className="w-full rounded-2xl cursor-pointer hover:bg-cyan-500 border-2 hover:text-white text-cyan-500 border-cyan-500" onClick={deleteHandler}>Delete</button>)}
                </div>
                <div>
                    {!isSaved && (<button className="w-full rounded-2xl cursor-pointer hover:bg-cyan-500 border-2 hover:text-white text-cyan-500 border-cyan-500" onClick={saveHandler}>Save plan</button>)}
                </div>
                <div>
                    {errorState && (<div className="text-red-500 text-sm">{errorMessage}</div>)}
                </div>
            </div>
        )   
    }
}
export default UserItinerary
