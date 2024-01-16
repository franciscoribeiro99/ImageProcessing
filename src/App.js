import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Landing from './components/Landing/Landing';
import Embed from './components/Embed/Embed';
import Reveal from './components/Reveal/Reveal';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Landing />} />
        <Route path='/embed' element={<Embed />} />
        <Route path='/reveal' element={<Reveal />} />
        <Route path='*' element={<Navigate to='/'/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
