import React, { FC, useState, useEffect } from 'react';
import { Card, Spinner } from 'react-bootstrap';
import './Bouquet.css'

interface Bouquet {
  bouquet_id: number;
  name: string;
  description: string;
  price: string;
  full_url: string; // Update the interface to include the full_url field
}

const BouquetsPage: FC = () => {
  const [bouquets, setBouquets] = useState<Bouquet[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  // Fetch bouquet data using the relative path
  fetch('/bouquets')
    .then(response => response.json())
    .then(data => {
      setBouquets(data);
      setLoading(false);
    })
    .catch(error => console.error('Error fetching bouquets:', error));
}, []);

  return (
    <div className="album">
      <div className="container">
        <div className="row">
          {loading ? (
            <Spinner animation="border" role="status">
              <span className="sr-only">Loading...</span>
            </Spinner>
          ) : (
            bouquets.map(bouquet => (
              <div className="col" key={bouquet.bouquet_id}>
                <div className="card" data-url="https://google.com">
                  {/* Add form and other elements here */}
                  <img src={bouquet.full_url} alt={bouquet.name} className="card-img-top" /> {/* Update the src attribute */}
                  <div className="card-body">
                    <h5 className="card-title">{bouquet.name}</h5>
                    <p className="card-text">{bouquet.description}</p>
                    <p className="card-text">Цена: {bouquet.price} рублей</p>
                  </div>
                  <div className="card-button">
                    <a href={`/bouquets/${bouquet.bouquet_id}`} className="btn btn-primary">
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
