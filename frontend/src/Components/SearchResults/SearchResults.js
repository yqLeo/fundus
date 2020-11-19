import React from 'react';
import axios from 'axios';
import './SearchResults.css';

class SearchResults extends React.Component {
  state = {
    result:"",
    complete:""
  }
  
  componentDidUpdate() {
    
    axios.get(`http://localhost:8000/api/fundus/`)
      .then(res => {
        const persons = res.data;
        let last = persons.filter(d => d.path === this.props.searchResults);
        let lasts = last[last.length-1]
        if (typeof lasts !== 'undefined'){
          this.setState( {result:lasts.title.substring(2,lasts.title.length-3)} );
        }
        else{
          this.setState({result:""});
        }
      })  
      if(this.props.wrong === "invalid path >_<" && this.state.complete === "" || this.props.wrong === "invalid path >_<" && this.state.complete === "processing..."){
        this.setState( {complete:"invalid path >_<"} );
      }
      else if(this.props.wrong === "processing" && this.state.complete === ""){
        console.log("2")
        this.setState( {complete:"processing..."} );
      }
      if(this.state.complete === "processing..." && this.state.result != ""){
        this.setState( {complete:"done!"} );
      }  
  }

  componentDidMount() {
    this.setState( {complete:""} );
  }


  render() {
    return (
      <div className="SearchResults">
        <h2>Results</h2>
        <h2>{this.state.complete} </h2>
        <li><span className="highlight">camera:</span>  {this.state.result} </li>
        <li><span className="highlight">symptom:</span> TBD </li>
        <li><span className="highlight">label:</span> TBD </li>
      </div>
    );
  }
}

export default SearchResults;