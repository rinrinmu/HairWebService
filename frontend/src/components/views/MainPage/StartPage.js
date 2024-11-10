import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import Navbar from '../NavBar/NavBar';
import './StartPage.css';

const MainPage = () => {
  const navigate = useNavigate(); // Create a navigate function

  const handleStartClick = () => {
    navigate('/ChoosePage'); // Navigate to the new page
  };

  return (
    <div className="main-container">
      <Navbar />
      <div className="content">
        <div className="start-button" onClick={handleStartClick}>
          <p className="start-button-text">시작하기</p>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
