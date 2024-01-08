import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Embed from './components/Embed/Embed';
import Landing from './components/Landing/Landing';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />}>
          <Route path='/embed' element={<Embed />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
