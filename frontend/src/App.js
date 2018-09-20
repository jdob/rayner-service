import React, { Component } from 'react';

import EventsTable from './EventsTable.js';
import Status from './Status.js';


class App extends Component {
  render() {
    return (
        <div className="container">
            <div className="row">
                <div className="col-md-8"><EventsTable/></div>
                <div className="col-md-4"><Status/></div>
            </div>
        </div>
    );
  }
}

export default App;
