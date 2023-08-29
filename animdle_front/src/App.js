import React from "react";
import { Routes, Route } from "react-router-dom";
import OpeningPage from "./pages/OpeningPage";
import OpeningHardcorePage from "./pages/OpeningHardcorePage";
import EndingPage from "./pages/EndingPage";
import EndingHardcorePage from "./pages/EndingHardcorePage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<OpeningPage />} />
      <Route path="/openings-hardcore" element={<OpeningHardcorePage />} />
      <Route path="/endings" element={<EndingPage />} />
      <Route path="/endings-hardcore" element={<EndingHardcorePage />} />
    </Routes>
  );
}

export default App;
