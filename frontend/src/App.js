import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import StartPage from './components/views/MainPage/StartPage';
import ChoosePage from './components/views/MainPage/ChoosePage';
import AnalyzePage from './components/views/AnalyzePage/AnalyzePage';
import ResultPage1 from './components/views/ResultPage/ResultPage1';
import RecordsPage from './components/views/RecordsPage/RecordsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/ChoosePage" element={<ChoosePage />} />
        <Route path="/RecordsPage" element={<RecordsPage />} />
        <Route path="/AnalyzePage" element={<AnalyzePage />} />
        <Route path="/ResultPage1" element={<ResultPage1 />} />
      </Routes>
    </Router>
  );
}

export default App;
