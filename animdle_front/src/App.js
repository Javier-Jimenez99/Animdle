import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Game from "./components/Game";
import Results from "./components/Results";
import { createContext, useContext, useState, useEffect } from "react";
import { getPlayedModes } from "./api/apiCalls";
import './styles/utils.css';
import ReactGA from 'react-ga4';

ReactGA.initialize("G-DXNQ33D5NK");

export const appContext = createContext();

export function usePlayedModes() {
  return useContext(appContext);
}

function App() {
  const modes = ["opening", "hardcore-opening", "ending", "hardcore-ending"];

  const [playedModes, setPlayedModes] = useState([]);
  useEffect(() => {
    getPlayedModes().then((data) => { setPlayedModes(data) });
  }, []);

  const value = {
    playedModes,
    setPlayedModes,
  };

  return (
    <appContext.Provider value={value}>
      <Routes>
        <Route path="/" element={<Navbar actual_mode="opening" />}>
          <Route index element={<Game mode="opening" />} />
          <Route path="results" element={<Results mode="opening" />} />
          <Route path="results/:date" element={<Results mode="opening" />} />
          <Route path=":date" element={<Game mode="opening" />} />
        </Route>
        {modes.map(mode =>
          <Route path={"/" + mode} element={<Navbar actual_mode={mode} />} key={mode}>
            <Route index element={<Game mode={mode} />} />
            <Route path="results" element={<Results mode={mode} />} />
            <Route path="results/:date" element={<Results mode={mode} />} />
            <Route path=":date" element={<Game mode={mode} />} />
          </Route>
        )}
      </Routes>
    </appContext.Provider>
  );
}

export default App;
