import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Link } from 'react-router-dom'
import './index.css'
import ITunesPage from './ITunesPage'
import BouquetsPage from './Bouquets'
import Services from './Services'
import 'bootstrap/dist/css/bootstrap.min.css'

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
    path: '/itunes',
    element: <ITunesPage />,
  },
  {
    path: '/bouquetss',
    element: <BouquetsPage />,
  },
]);


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <hr />
    <RouterProvider router={router} />
  </React.StrictMode>,
)