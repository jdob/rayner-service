import React, { Component } from 'react';

import EventsTable from './EventsTable.js';


class App extends Component {
  render() {
    return (
        <div className="container">
            <EventsTable/>
        </div>
    );
  }
}

export default App;
