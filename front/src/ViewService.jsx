import React from 'react';
import { useParams } from 'react-router-dom';
import axios from "axios"; // <-- Correct import statement

const ViewService = () => {
  const { id } = useParams();
  // Fetch data for the specific service using id

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <div className="card">
            {/* Render detailed service content here */}
            <img src="{service.image_url}" alt="{service.name}" className="card-img-top" />
            <div className="card-body">
              <h5 className="card-title">{service.name}</h5>
              <p className="card-text">{service.description}</p>
              <p className="card-text">Цена: {service.price} рублей</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewService;
