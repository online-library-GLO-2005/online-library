import { useEffect } from 'react';
import { initAuth } from './services/initService';
import { Outlet } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';

function App() {
  useEffect(() => {
    initAuth();
  }, []);

  return (
    <>
      <Toaster position="top-right" />
      <Navbar />
      <Outlet />
    </>
  );
}

export default App;
