import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Game from "./components/Game";

function App() {
  const modes = ["opening", "hardcore-opening", "ending", "hardcore-ending"];
  return (
    <>
      <Routes>
        <Route path="/" element={<Navbar actual_mode={"opening"} />}>
          <Route index element={<Game mode={"opening"} />} />
          <Route path=":date" element={<Game mode={"opening"} />} />
        </Route>
        {modes.map(mode =>
          <Route path={"/" + mode} element={<Navbar actual_mode={mode} />}>
            <Route index element={<Game mode={mode} />} />
            <Route path=":date" element={<Game mode={mode} />} />
          </Route>
        )}
      </Routes>
    </>
  );
}

export default App;
