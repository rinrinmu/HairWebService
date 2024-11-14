import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../style/style.css';

const Navbar = () => {
  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate('/ChoosePage');
  };

  const handleRecordsClick = () => {
    navigate('/RecordsPage'); // RecordsPage로 이동
  };

  return (
    <div className="navbar">
      <div className="navbar-left">
        <div className="navbar-item" onClick={handleHomeClick}>머리카락 보일라</div>
        <div className="navbar-item" onClick={handleRecordsClick}>기록 보기</div> 
      </div>
    </div>
  );
};

export default Navbar;