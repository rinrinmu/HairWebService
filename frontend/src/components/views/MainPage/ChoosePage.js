import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import Navbar from '../NavBar/NavBar';
import './ChoosePage.css';

const ChoosePage = () => {
    const navigate = useNavigate();

    const handleAnalyzeCLick = () => {
        navigate('/AnalyzePage');
    };

    const handleRecordClick = () => {
        navigate('/RecordsPage');
    };

    return (
        <div className="main-container">
            <Navbar />
            <div className="welcome-message">
                <p>환영합니다!</p>
            </div>
            <div className="buttons-container">
                <div className="button analyze-button" onClick={handleAnalyzeCLick}>
                    <p>분석하기</p>
                </div>
                <p className="footer-text">두피 분석하기</p> {/* 분석하기 버튼 아래 텍스트 */}
                
                <div className="button record-button" onClick={handleRecordClick}>
                    <p>기록하기</p>
                </div>
                <p className="footer-text">분석 결과 확인하기</p> {/* 기록하기 버튼 아래 텍스트 */}
            </div>
        </div>
    );
};

export default ChoosePage;
