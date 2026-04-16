import { useEffect } from 'react';
import { Outlet } from 'react-router-dom';

import Navbar from './components/Navbar';
import { useAuthStore } from './store/authStore';
import { initAuth } from './services/initService';

function App() {
  const setAuthReady = useAuthStore((s) => s.setAuthReady);
  const authReady = useAuthStore((s) => s.authReady);

  useEffect(() => {
    const run = async () => {
      try {
        await initAuth();
      } finally {
        setAuthReady(true);
      }
    };

    run();
  }, [setAuthReady]);

  if (!authReady) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <Navbar />
      <Outlet />
    </>
  );
}

export default App;
