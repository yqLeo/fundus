import React from 'react';
import axios from 'axios';
import './SearchResults.css';
import Backend from '../Backend/Backend';
//import TrackList from '../TrackList/TrackList';

class SearchResults extends React.Component {
  state = {
    result:""
  }
  
  componentDidUpdate() {
    
    axios.get(`http://localhost:8000/api/fundus/`)
      .then(res => {
        const persons = res.data;
        let last = persons.pop();
        this.setState( {result:last.title} );
        
      })
  }

  render() {
    return (
      <div className="SearchResults">
        <h2>Results</h2>
        <h2>{this.props.searchResults} </h2>
        <li><span className="highlight">camera:</span>  {this.state.result} </li>
        <li><span className="highlight">symptom:</span> TBD </li>
        <li><span className="highlight">label:</span> TBD </li>
      </div>
    );
  }
}

export default SearchResults;