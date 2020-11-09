import React from 'react';
import './App.css';
import SearchBar from '../SearchBar/SearchBar';
import SearchResults from '../SearchResults/SearchResults';
import SearchTarget from '../SearchTarget/SearchTarget';
import Backend from '../Backend/Backend';
import axios from 'axios'; 

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      searchResults: [],
      details: []
    };
    this.search = this.search.bind(this);
  }
  search(term) {
      this.setState({searchResults: term});
  }


  render() {
    return (
      <div>
        <h1><span className="highlight">AI</span> fundus</h1>
        <div className="App">
          <SearchBar onSearch={this.search} />
          <div className="App-playlist">
          <SearchTarget searchTarget={this.state.searchResults}
                           onAdd={this.addTrack} />
            <SearchResults searchResults={this.state.searchResults}
                           onAdd={this.addTrack} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
