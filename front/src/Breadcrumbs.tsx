import React from 'react';
import { Link } from 'react-router-dom';

interface BreadcrumbsProps {
  items: { label: string; link: string }[];
  className?: string;
}

const Breadcrumbs: React.FC<BreadcrumbsProps> = ({ items, className }) => {
  return (
    <div className={`breadcrumbs ${className || ''}`}>
      {items.map((item, index) => (
        <React.Fragment key={item.link}>
          {index > 0 && <span className="breadcrumb-separator"> &gt; </span>}
          <Link to={item.link} className="breadcrumb-link">
            {item.label}
          </Link>
        </React.Fragment>
      ))}
    </div>
  );
};

export default Breadcrumbs;
