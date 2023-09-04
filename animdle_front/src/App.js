import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Game from "./components/Game";
import Results from "./components/Results";
import { Helmet } from "react-helmet";

function App() {
  const modes = ["opening", "hardcore-opening", "ending", "hardcore-ending"];
  return (
    <>
      <Helmet>
        <title>Animdle</title>
        <meta name="description" content="Animdle is a game where you have to guess the anime opening or ending song." />
        <meta name="keywords" content="animdle, anime, opening, ending, wordle, song, guess, game, quiz, anime quiz, anime game, anime quiz game, anime guess game, anime guess quiz, anime opening, anime ending, anime opening quiz, anime ending quiz, anime opening game, anime ending game, anime opening guess, anime ending guess, anime opening quiz game, anime ending quiz game, anime opening guess game, anime ending guess game, anime opening guess quiz, anime ending guess quiz" />
        <link rel="canonical" href="https://animdle.com" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta charset="UTF-8" />
        <meta name="theme-color" content="#dd6559" />

        <meta property="og:title" content="Animdle" />
        <meta property="og:description" content="Animdle is a game where you have to guess the anime opening or ending song." />
        <meta property="og:url" content="https://animdle.com" />
        <meta property="og:image" content="https://animdle.com/assets/logo.png" />
        <meta property="og:type" content="website" />
        <meta property="og:locale" content="es" />
        <meta property="og:site_name" content="Animdle" />

        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:site" content="@animdle" />
        <meta name="twitter:title" content="Animdle" />
        <meta name="twitter:description" content="Animdle is a game where you have to guess the anime opening or ending song." />
        <meta name="twitter:image" content="https://animdle.com/assets/logo.png" />
      </Helmet>
      <Routes>
        <Route path="/" element={<Navbar actual_mode="opening" />}>
          <Route index element={<Game mode="opening" />} />
          <Route path="results" element={<Results mode="opening" />} />
          <Route path="results/:date" element={<Results mode="opening" />} />
          <Route path=":date" element={<Game mode="opening" />} />
        </Route>
        {modes.map(mode =>
          <Route path={"/" + mode} element={<Navbar actual_mode={mode} />}>
            <Route index element={<Game mode={mode} />} />
            <Route path="results" element={<Results mode={mode} />} />
            <Route path="results/:date" element={<Results mode={mode} />} />
            <Route path=":date" element={<Game mode={mode} />} />
          </Route>
        )}
      </Routes>
    </>
  );
}

export default App;
