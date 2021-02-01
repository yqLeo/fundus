import React from 'react';
import './Navigation.css';
import { NavLink } from 'react-router-dom';
 
const Navigation = () => {
    return (
       <div>
          <NavLink to="/">Home</NavLink>
          <NavLink to="/Images">Images</NavLink>
       </div>
    );
}
 
export default Navigation;