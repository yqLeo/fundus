import React from 'react';
import axios from 'axios';
import './SearchResults.css';
import Backend from '../Backend/Backend';
//import TrackList from '../TrackList/TrackList';

class SearchResults extends React.Component {
  state = {
    result:"",
    complete:"",
    analysis:"",
    similar:"",
  }
  
  componentDidUpdate() {
    
    axios.get(`http://localhost:8000/api/fundus/`)
      .then(res => {
        const persons = res.data;
        let last = persons.filter(d => d.path === this.props.searchResults);
        let lasts = last[last.length-1]
        if (typeof lasts !== 'undefined'){
        //  if(this.state.result !== lasts.title.substring(2,lasts.title.length-3)){
              this.setState( {result:lasts.title.substring(2,lasts.title.length-3)} );
         // }
          let ana = lasts.analysis
          let advice = ana.substring(ana.indexOf("advice"),ana.indexOf("observationStates"))
          let advices = advice.substring(advice.indexOf(":")+3,advice.indexOf("}")-1)
          if(advices.length == 0){
              advices = "processing..."
          }
          if(this.state.analysis.length < 15){
              //this.setState( {analysis:advices} );
          }
          let sim = lasts.similar
          let sims = sim.substring(2,lasts.similar.length-3)
          if(this.state.similar.length < 15){
             // this.setState( {similar:sims} );
          }
        }
        else{
          this.setState({result:""});
          this.setState({analysis:""});
          this.setState({similar:""});
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

  render() {
    return (
      <div className="SearchResults">
        <h2>Results</h2>
        <h2>{this.state.complete} </h2>
        <li><span className="highlight">camera:</span>  {this.state.result} </li>
        <li><span className="highlight">symptom:</span> {this.state.analysis} </li>
        <li><span className="highlight">similar Images:</span> {this.state.similar} </li>
      </div>
    );
  }
}

export default SearchResults;