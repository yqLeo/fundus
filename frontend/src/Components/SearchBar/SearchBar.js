import React from 'react';

import './SearchBar.css';
import axios from 'axios';
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

class SearchBar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      term: '',
      wrong: 'processing'
    };

    this.handleTermChange = this.handleTermChange.bind(this);
    this.search = this.search.bind(this);
  }

  handleTermChange(event) {
    this.setState({term: event.target.value});
  }

  search() {
    this.props.onSearch(this.state.term,this.state.wrong);
  }

  handleSubmit = event => {
    event.preventDefault();
    const user = {
      title: "a",
      path: this.state.term
    };
    axios.post("http://localhost:8000/fundus/path/",  user )
    .then(res => {
    }).catch((error) => {
      this.setState({wrong: "invalid path >_<"});
      this.search();
  })
  }

  render() {
    return (
      <div className="SearchBar">
        <form onSubmit={this.handleSubmit}>
          <input placeholder="Enter An fundus image path" onChange={this.handleTermChange} />
          <button type = "submit" className="SearchButton" onClick={this.search}>SEARCH</button>
        </form>
      </div>
    );
  }
}

export default SearchBar;