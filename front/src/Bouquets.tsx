import React, { FC, useState, useEffect } from 'react';
import { Spinner } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';
import './Bouquet.css';

interface Bouquet {
  bouquet_id: number;
  name: string;
  description: string;
  price: string;
  full_url: string;
}

const BouquetsPage: FC = () => {
  const navigateTo = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const searchParam = queryParams.get('q') || '';

  const [bouquets, setBouquets] = useState<Bouquet[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchValue, setSearchValue] = useState(searchParam);

  const fetchBouquets = (searchText: string) => {
    setLoading(true);
    // Fetch bouquet data using the relative path with query parameter
    fetch(`/bouquets/?q=${searchText}`)
      .then(response => response.json())
      .then(data => {
        setBouquets(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching bouquets:', error);
        setLoading(false);
      });
  };

  const handleSearchClick = () => {
    // Redirect to the same frontend page with the search query parameter
    navigateTo(`/bouquetss/?q=${searchValue}`);
    // Fetch data after navigating to the new URL
    fetchBouquets(searchValue);
  };

  useEffect(() => {
    // Fetch data when the component mounts for the first time or when search query changes
    fetchBouquets(searchValue);
  }, []); // Update the effect to run whenever searchValue changes

  return (
    <div className="album">
      <div className="container">
        <div className="row">
            <div className="search-bar">
              <input
                type="text"
                id="search-input"
                placeholder="Поиск"
                value={searchValue}
                onChange={(event => setSearchValue(event.target.value))}
              />
              <button type="button" id="search-button" onClick={handleSearchClick}>
                Искать
              </button>
            </div>

          {loading ? (
            <Spinner animation="border" role="status">
              <span className="sr-only">Loading...</span>
            </Spinner>
          ) : (
            bouquets.map(bouquet => (
              <div className="col" key={bouquet.bouquet_id}>
                <div className="card">
                  <img src={bouquet.full_url} alt={bouquet.name} className="card-img-top" />
                  <div className="card-body">
                    <h5 className="card-title">{bouquet.name}</h5>
                    <p className="card-text">{bouquet.description}</p>
                    <p className="card-text">Цена: {bouquet.price} рублей</p>
                    {/* Add more text elements here if needed */}
                    <a href={`/bouquetss/${bouquet.bouquet_id}/`} className="btn btn-primary">
                      Подробнее
                    </a>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default BouquetsPage;
