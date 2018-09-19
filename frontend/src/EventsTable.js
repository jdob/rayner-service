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
            let events = data.results.map((e) => {
                return(
                    <tr key={e.id}>
                        <td>{e.service_ip}</td>
                        <td>{e.client_id}</td>
                        <td>{e.client_ip})</td>
                        <td>{e.color}</td>
                        <td>{e.timestamp}</td>
                    </tr>
                )
            })
            this.setState({events: events})
            console.log('events', this.state.events)
        })
    }

    render() {
        return(
            <table>
            <tbody>
            {this.state.events}
            </tbody>
            </table>
        )
    }
}

export default EventsTable;
