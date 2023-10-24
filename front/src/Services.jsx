import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios'; // You might need Axios or Fetch API to handle API requests

const Services = () => {  
  const [searchValue, setSearchValue] = useState('');
  const [filteredData, setFilteredData] = useState([]);

  // Fetch and filter data logic here (using useEffect and useState)

  return (
    <div className="album">
      <div className="container">
        <div className="row">
          <form>
            <div className="search-bar">
              <input
                type="text"
                placeholder="Поиск"
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
              />
              <button type="submit">Искать</button>
            </div>
          </form>

          {filteredData.map((model) => (
            <div key={model.bouquet_id} className="col">
              {/* Render your data here */}
              <div className="card" data-url="https://google.com">
                {/* Card content */}
                <button className="close-button">✖</button>
                <img src={model.image_url} alt={model.name} className="card-img-top" />
                <div className="card-body">
                  <h5 className="card-title">{model.name}</h5>
                  <p className="card-text">{model.description}</p>
                  <p className="card-text">Цена: {model.price} рублей</p>
                </div>
                <div className="card-button">
                  <Link to={`/services/${model.bouquet_id}`} className="btn btn-primary">
                    Подробнее
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Services;
