import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from '../Home/Home';
import Navigation from '../Navigation/Navigation';

class App extends Component {
    render() {
      return (      
         <BrowserRouter>
          <div>
              <Switch>
               <Route path="/" component={Home} exact/>
              <Route component={Error}/>
             </Switch>
          </div> 
        </BrowserRouter>
      );
    }
  }
   
  export default App;