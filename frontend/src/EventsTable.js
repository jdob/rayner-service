import React, { Component } from 'react';


class EventsTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            events: [],
        };
    }

    componentDidMount() {
        fetch('http://localhost:8000/changes/')
        .then(results => {
            return results.json();
        }).then(data => {
            let events = data.map((e) => {
                return(
                    <div>{e.color}</div>
                )
            })
            this.setState({events: events})
            console.log('events', this.state.events)
        })
    }

    render() {
        return(
            <div>{this.state.events}</div>
        )
    }
}

export default EventsTable;
