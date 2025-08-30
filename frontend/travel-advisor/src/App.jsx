import { useState, useEffect } from 'react'
import './App.css'
import ItineraryGenerationForm from './components/ItineraryGenerationForm'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import UserItinerariesContainer from './components/UserItinerariesContainer'
import UserItinerary from './components/UserItinerary'

function App() {
  const [generationResponse, setGenerationResponse] = useState([]);
  const [generationReady, setGenerationReady] = useState(false);
  const [generationInput, setGenerationInput] = useState();
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [savedPlacesContainerRefresh, setSavedPlacesContainerRefresh] = useState(false);
  const [generatedItinerarySaveState, setGeneratedItinerarySaveState] = useState(false);
  const [generatedItiniraryID, setGeneratedItiniraryID] = useState(0);

  function generationResponseCallback(response, generationInput) {
    setGenerationResponse(response);
    setGenerationInput(generationInput);
    console.log(generationResponse);
    setGenerationReady(true);
  }
  
  function handleLoginCallback() {
    setShowLoginForm(false);
    setLoggedIn(true);
  }

  function handleStateChange(id) {
    setGeneratedItinerarySaveState(false);
    setGenerationReady(false);
    setSavedPlacesContainerRefresh(prevState => !prevState);
  }

  function handleRegisterationCallback() {
    setShowLoginForm(true);
    setShowRegisterForm(false);
  }

  function handleClosureCallback() {
    setShowLoginForm(false);
    setShowRegisterForm(false);
  }

  function handleLogOut() {
    localStorage.removeItem("token");
    setLoggedIn(false);
  }
  
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setLoggedIn(true);
    } else {
      setLoggedIn(false);
    }
  }, []);

  return (
    <>
    <div className="flex justify-center items-center min-h-screen w-full">
      <div className="px-2 max-w-8xl">
        <div className="flex flex-col justify-center items-center gap-4 text-2xl">
          <div className="text-6xl text-cyan-950">Travelling without a plan?</div>
          <div className="text-2xl text-cyan-700">AI is here to help</div>
          <ItineraryGenerationForm responseCallback={generationResponseCallback} />
          {generationReady && (
            <UserItinerary
              userSpecificItineraryInfo={generationInput}
              activities={generationResponse}
              isSaved={generatedItinerarySaveState}
              onSave={handleStateChange}
              isLoggedIn={loggedIn}
            />
          )}
        </div>
      </div>
    </div>
      <div>
        {
          !loggedIn && <button className='auth-button top-5 right-5' onClick={() => {setShowLoginForm(true)}}>Login</button>
        }
      </div>
      <div>
        {
          !loggedIn && <button className='auth-button top-5 right-30' onClick={() => {setShowRegisterForm(true)}}>Register</button>
        }
      </div>
      {
        loggedIn && <UserItinerariesContainer loggInState={loggedIn} refreshFlagFromApp={savedPlacesContainerRefresh}/>
      }
      {
        loggedIn && <button className="auth-button top-5 right-5" onClick={() => {handleLogOut()}}>Logout</button>
      }
      {showLoginForm && (
        <LoginForm onLoginSuccess={handleLoginCallback} onClosure={handleClosureCallback}/>
      )}

      {showRegisterForm && (
        <RegisterForm onRegisterationSuccess={handleRegisterationCallback} onClosure={handleClosureCallback}/>
      )}
    </>
  )
}

export default App
