import React, { Component } from 'react';


class Status extends Component {
    constructor(props) {
        super(props);
        this.current_color = "ffffff";
    }

    render() {
        return(
            <div align="center">
                <div>Current Light Color</div>
                <div className="status-box"></div>
            </div>
        )
    }

}

export default Status;