import { useEffect, useState } from "react";
import './Itinerary.css';
import UserItinerary from "./UserItinerary"
import api from "../api";
import axios from "axios";

const UserItinerariesContainer = ({loggInState, refreshFlagFromApp}) => {
    const [publicItinrariesResponseState, setPublicItinrariesResponseState] = useState(false);
    const [userItinraries, setUserItinraries] = useState([]);
    const [publicItinraries, setPublicItinraries] = useState([]);
    const [itinerarySaveState, setItinerarySaveState] = useState({});
    const [refreshFlag, setRefreshFlag] = useState(false);

    const getAssociatedPublicItineraries = async (responseItineraries) => {
        // console.log("entereeed getAssociatedPublicItineraries");
        const itineraries = [];
        const newStates = { ...itinerarySaveState };
        if (responseItineraries) {
            for (const itinirary of responseItineraries) {
                try{
                    const token = localStorage.getItem("token");
                    
                    const response = await api.get(`/api/itinerary/${itinirary.itinerary_id}`, {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    });
                    itineraries.push(response.data);
                    if (!(itinirary.id in newStates)) 
                    {
                        newStates[itinirary.id] = true;
                    }
                   
                } catch(error) {
                    console.error(`Error fetching itinerary ${itinirary.itinerary_id} : ${error}`);
                }
            }

            setItinerarySaveState(newStates);
            setUserItinraries(responseItineraries);
            setPublicItinraries(itineraries);
            setPublicItinrariesResponseState(true);
        }
    };

    const getUserItineraries = async () => {
        // console.log("entereeed getUserItineraries");
        try{
            const token = localStorage.getItem("token");
            const response = await api.get("/api/itinerary/", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            // console.log(response.data);
            getAssociatedPublicItineraries(response.data);
        } catch(error) {
            console.error("Error fetching itineraries:", error);
        }
    };

    const refreshCoontainer = () => {
        setRefreshFlag(true);
    }

    const saveHandler = (id) => {
        setItinerarySaveState(prev => ({
            ...prev, [id]: !prev[id]
        }
        ));
        refreshCoontainer();
    }

    const deleteHandler = (id) => {
        setItinerarySaveState(prev => ({
            ...prev, [id]: !prev[id]
        }
        ));
        refreshCoontainer();
    }

    useEffect( () => {
            if (loggInState) {
                getUserItineraries().then(() => {
                    setRefreshFlag(false);
                });
            }
        }, 
        [loggInState, refreshFlag, refreshFlagFromApp]
    )
    
    return (
        <div className="border-l-2 shadow-cyan-700 border-t-2 fixed top-20 right-5 h-screen overflow-y-auto w-[350px] bg-white border-gray-200 shadow-2xl p-4">
            <div className="text-cyan-900 text-2xl font-semibold text-center mb-4">Saved Planes</div>
            {publicItinrariesResponseState && publicItinraries.map(itinerary => {
                const userSpecificItinerary = userItinraries.find(itin => itin.itinerary_id === itinerary.id);
                const updatedItinerary = {...userSpecificItinerary};
                updatedItinerary['destination'] = itinerary.destination;
                updatedItinerary['interests'] = itinerary.interests;
                return userSpecificItinerary && (
                    <UserItinerary 
                        key={itinerary.id}
                        isSaved={itinerarySaveState[userSpecificItinerary.id]} 
                        userSpecificItineraryInfo={updatedItinerary} 
                        activities={itinerary.activities} 
                        onSave={saveHandler}
                        onDelete={deleteHandler}
                        isLoggedIn={loggInState}
                    />
                );
            })}
        </div>
    )
}

export default UserItinerariesContainer