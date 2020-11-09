import React from 'react';

import axios from 'axios';

class Backend extends React.Component {
  state = {
    result:""
  }

  componentDidMount() {
    
    axios.get(`http://localhost:8000/api/fundus/`)
      .then(res => {
        const persons = res.data;
        console.log(this.props.searchResults)
        let last = persons.filter(person => person.path === this.props.searchResults);
        this.setState( {result:last.title} );
        console.log(last.title)
      })
  }

  render() {
    return (
        <p>
        { this.state.result}
      </p>
    )
  }
}

export default Backend;