import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import { router } from './router';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Toaster
      position="top-right"
      containerStyle={{
        top: 80, // avoids navbar overlap
        right: 20,
      }}
    />

    <RouterProvider router={router} />
  </StrictMode>,
);
