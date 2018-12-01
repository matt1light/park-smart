import React, { Component } from 'react';
import './App.css';
import SectorQuery from './components/SectorQuery'
import {ApolloProvider} from "react-apollo"
import TabContainer from "./components/TabContainer"

const test_sector_spots = [
                    {
                        "spot":{
                            "full": false,
                            "active": true
                        },
                        "image_coordinates":{
                            "right": 1,
                            "top": 0,
                            "bottom": 1
                        }
                    },
                    {
                        "spot":{
                            "full": true,
                            "active": true
                        },
                        "image_coordinates":{
                            "left": 1,
                            "right": 2,
                            "top": 0,
                            "bottom": 1
                        }
                    },
                    {
                        "spot":{
                            "full": false,
                            "active": false
                        },
                        "image_coordinates":{
                            "left": 2,
                            "right": 3,
                            "top": 0,
                            "bottom": 1
                        }
                    },
                    {
                        "spot":{
                            "full": true,
                            "active": true
                        },
                        "image_coordinates":{
                            "left": 0,
                            "right": 1,
                            "top": 1,
                            "bottom": 2
                        }
                    },
                    {
                        "spot":{
                            "full": true,
                            "active": false
                        },
                        "image_coordinates":{
                            "left": 1,
                            "right": 2,
                            "top": 1,
                            "bottom": 2
                        }
                    },
                    {
                        "spot":{
                            "full": false,
                            "active": true
                        },
                        "image_coordinates":{
                            "left": 2,
                            "right": 3,
                            "top": 1,
                            "bottom": 2
                        }
                    },
                ]

const data = {
        "sectors": [
            {
                "pk": 1,
                "x": 0,
                "y": 0,
                "sector_spots": test_sector_spots
            },
            {
                "pk": 2,
                "x": 2,
                "y": 1,
                "sector_spots": test_sector_spots
            },
            {
                "pk": 3,
                "x": 8,
                "y": 1,
                "sector_spots": test_sector_spots
            },
            {
                "pk": 4,
                "x": 5,
                "y": 1,
                "sector_spots": test_sector_spots
            },
            {
                "pk": 5,
                "x": 4,
                "y": 6,
                "sector_spots": test_sector_spots
            }
        ]
    }


class App extends Component {
  render() {
    return (
        <ApolloProvider client={this.props.client}>
            <div className="App">
                <div>
                    <TabContainer></TabContainer>
                    <SectorQuery></SectorQuery>
                </div>
            </div>
        </ApolloProvider>
    );
  }
}

export default App;