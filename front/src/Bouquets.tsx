import { FC, useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Breadcrumbs from './Breadcrumbs';
import './Bouquet.css';
import logoImage from './logo.png'; 

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
  const priceParam = queryParams.get('price') || '';

  const [bouquets, setBouquets] = useState<Bouquet[]>([]);
  const [searchValue, setSearchValue] = useState(searchParam);
  const [priceValue, setPriceValue] = useState(priceParam);

  const fetchBouquets = (searchText: string, price: string) => {
    // Fetch bouquet data using the relative path with query parameter
    fetch(`/bouquets/?q=${searchText}&price=${price}`)
      .then(response => response.json())
      .then(data => {
        setBouquets(data);
      })
      .catch(error => {
        console.error('Error fetching bouquets:', error);
      });
  };

  const breadcrumbsItems = [
    { label: 'Все букеты', link:'' } // Link to the current page
  ];

  const handleSearchClick = () => {
    // Redirect to the same frontend page with the search query parameter
    navigateTo(`/bouquetss/?q=${searchValue}&price=${priceValue}`);
    // Fetch data after navigating to the new URL
    fetchBouquets(searchValue, priceValue);
  };

  useEffect(() => {
    // Fetch data when the component mounts for the first time or when search query changes
    fetchBouquets(searchValue, priceValue);
  }, []); // Update the effect to run whenever searchValue changes

  return (
    <div className="album">
      <div className="container">
        <div className="row">
        <Breadcrumbs items={breadcrumbsItems} /> {/* Include Breadcrumbs component */}
            <div className="search-bar">
              <input
                type="text"
                id="search-input"
                placeholder="Поиск"
                value={searchValue}
                onChange={(event => setSearchValue(event.target.value))}
              />
              <input
              type="number"
              id="price-input"
              placeholder="Цена"
              value={priceValue}
              onChange={(event => setPriceValue(event.target.value))}
              />
              <button type="button" id="search-button" onClick={handleSearchClick}>
                Искать
              </button>
            </div>

            {bouquets.map((bouquet) => (
            <div className="col" key={bouquet.bouquet_id}>
              <div className="card">
              <img
                  src={(bouquet.full_url != '' && bouquet.full_url !== 'http://localhost:9000/images/images/None') ? bouquet.full_url : logoImage} // Use bouquet.full_url or default logoImage
                  alt={bouquet.name}
                  className="card-img-top"
                />
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
          ))}
        </div>
      </div>
    </div>
  );
};

export default BouquetsPage;
