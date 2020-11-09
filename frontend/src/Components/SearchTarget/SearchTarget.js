import React from 'react';
import axios from 'axios';
import './SearchTarget.css';





class SearchTarget extends React.Component {

  state = {
    src: "",
  };

  componentDidUpdate() {
    axios.get(`http://localhost:8000/api/fundus/`)
      .then(res => {
        const persons = res.data;
        let last = persons.pop();
        this.setState( {src:last.fundus_Img} );
      })
    
  }

  render() {
    return (
      <div className="SearchTarget">
        <h2>Input</h2>
        <img src={this.state.src}
        width = "400px" />
      </div>
    );
  }
}

export default SearchTarget;