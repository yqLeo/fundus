import React from 'react';
import './Home.css';
import SearchBar from '../SearchBar/SearchBar';
import SearchResults from '../SearchResults/SearchResults';
import SearchTarget from '../SearchTarget/SearchTarget';
import Dropzone from 'react-dropzone';
import { NavLink } from 'react-router-dom';
import Navigation from '../Navigation/Navigation';
import Basic from '../Dropzone/Dropzone';
import Backend from '../Backend/Backend';
import axios from 'axios'; 

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.onDrop = (files) => {
      this.setState({files})
      const uploadData = new FormData();
      console.log(files[0])
      this.setState({searchResults: files[0]['path']});
      this.setState({searchTarget: files[0]['path']});
      uploadData.append('image',files[0]);
      console.log(uploadData)
      fetch('http://localhost:8000/fundus/upload/',{
          method: 'POST',
          body:uploadData
      })
      .then( res => console.log(res))
      .catch( error => console.log(error))
    };
    this.state = {
      searchResults: [],
      searchTarget: [],
      details: [],
      files: []
    };
    this.search = this.search.bind(this);
  }
  search(term,wrong) {
      this.setState({searchResults: term});
      this.setState({searchTarget: term});
      this.setState({details: wrong});
  }

  

  render() {
    
    const files = this.state.files.map(file => (
      <li key={file.name}>
        {file.name} - {file.size} bytes
      </li>
    ));
    return (
      <div>
        <h1><span className="highlight">AI</span> fundus</h1>
        <NavLink to="/Images">Images</NavLink>
        <div className="Home">
          <SearchBar onSearch={this.search} />
          <Dropzone onDrop={this.onDrop}>
            {({getRootProps, getInputProps}) => (
              <section className="container">
                <div {...getRootProps({className: 'dropzone'})}>
                  <input {...getInputProps()} />
                  <p>Drag and drop some files here, or click to select files</p>
                </div>
                <aside>
                  <ul>{files}</ul>
                </aside>
              </section>
            )}
          </Dropzone>
          <div className="App-playlist">
          
          <SearchTarget searchTarget={this.state.searchTarget}
                           onAdd={this.addTrack} />
          
          

          <SearchResults searchResults={this.state.searchResults} wrong = {this.state.details}
                          onAdd={this.addTrack} />
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
