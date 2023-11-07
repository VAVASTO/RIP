import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Breadcrumbs from './Breadcrumbs';
import './BouquetDetail.css';

const BouquetDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>(); // Accessing the bouquet_id from the URL
  const [bouquetData, setBouquetData] = useState({
    name: '',
    image_url: '',
    description: '',
    price: '',
    full_url: ''
  });

  const breadcrumbsItems = [
    { label: 'Все букеты', link: '/bouquetss' },
    { label: 'Подробнее', link: '' } 
  ];


  useEffect(() => {
    const fetchBouquetData = async () => {
      try {
        const response = await fetch(`/bouquets/${id}`); // Assuming your API endpoint is like 'bouquets/id'
        const data = await response.json();
        setBouquetData(data); // Update state with fetched data
      } catch (error) {
        console.error('Error fetching bouquet data:', error);
      }
    };

    fetchBouquetData(); // Call the fetchBouquetData function when the component mounts

    // Cleanup the effect when the component is unmounted (optional)
    return () => {
      // Cleanup code (if needed)
    };
  }, [id]); // Dependency array ensures the effect runs whenever 'id' changes

  return (
    <div className="container">
      {
        <div className="row">
          <Breadcrumbs items={breadcrumbsItems} /> {/* Include Breadcrumbs component */}
          <div className="col">
            <div className="card">
              <img src={bouquetData.full_url} alt={bouquetData.name} className="card-img-top" />
              <div className="card-body">
                <h5 className="card-title">{bouquetData.name}</h5>
                <p className="card-text">{bouquetData.description}</p>
                <p className="card-text">Цена: {bouquetData.price} рублей</p>
              </div>
            </div>
          </div>
        </div>
      }
    </div>
  );
};

export default BouquetDetailPage;
