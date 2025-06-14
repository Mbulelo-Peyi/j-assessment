import React from 'react';
import {BrowserRouter as Router, Routes,Route} from 'react-router-dom';
import Home from './Home';
import StringForm from './StringForm';
import AppForm from './AppForm';


function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />}></Route>
        <Route path='/string' element={<StringForm />}></Route>
        <Route path='/form' element={<AppForm />}></Route>
      </Routes>
    </Router>
  )
}

export default App
