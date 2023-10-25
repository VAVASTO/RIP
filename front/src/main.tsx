import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider, Routes, Route, Link } from 'react-router-dom';
import BouquetsPage from './Bouquets';
import BouquetDetailPage from './BouquetDetail';  // Import your BouquetDetail component

const router = createBrowserRouter([
  {
    path: '/',
    element: <h1>Это наша стартовая страница</h1>,
  },
  {
    path: '/new',
    element: <h1>Это наша страница с чем-то новеньким</h1>,
  },
  {
    path: '/bouquetss',
    element: <BouquetsPage />,
  },
  {
    path: '/bouquetss/:id/',
    element: <BouquetDetailPage />,
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <hr />
    <RouterProvider router={router} />
  </React.StrictMode>,
);
