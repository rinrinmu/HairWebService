import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../NavBar/NavBar';
import './StartPage.css';

const MainPage = () => {
  const navigate = useNavigate();

  const handleStartClick = () => {
    navigate('/ChoosePage');
  };

  return (
    <div className="main-container">
      <Navbar />
      <div className="content">
        <div className="title-section">
          <h1 className="main-title">머리카락 보일라</h1>
          <p className="sub-title">
            AI 기반 두피 분석으로 당신의 두피 건강을 체크하세요.
            <br />
            간단한 사진 한 장으로 시작해보세요.
          </p>
        </div>
        <div className="start-button" onClick={handleStartClick}>
          <p className="start-button-text">시작하기</p>
        </div>
      </div>
    </div>
  );
};

export default MainPage;