import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DataUploadComponent from './views/upload.js';
import MapDisplayComponent from './views/mapComponent.js';
function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<DataUploadComponent />} />
        <Route path="/map" element={<MapDisplayComponent />} />
      </Routes>
    </Router>
  );
}

export default App;