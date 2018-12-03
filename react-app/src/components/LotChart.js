import React, { Component, ReactFragment } from 'react';
import './LotChart.css'
import createSector from './SectorChart.js'
import {Mutation} from 'react-apollo'
import gql from 'graphql-tag'
import {GET_SECTORS_QUERY, UPDATE_SECTOR_LOCATION} from './GraphQL'
// import {scaleLinear, scaleOrdinal} from 'd3-scale'
// import {select, event} from 'd3-selection'
// import {drag} from 'd3-drag'

import * as d3 from 'd3'


const resolution = 50

class LotChart extends Component {
    constructor(props){
        super(props)
        this.createLotChart = this.createLotChart.bind(this)
        this.state = {change: {}}
    }

    componentDidMount(){
        this.createLotChart()
    }
    componentDidUpdate(){
        this.createLotChart()
        this.props.onRefetch()
    }

    createLotChart() {
        createLot(this.node, this.props, this.state)
        // createHistorySlider(this.node, this.state.width, this.state.height, Date.now(), changeDate)
    }

    render() {
        return (
            <Mutation mutation={UPDATE_SECTOR_LOCATION} >
                {(updateSector) => (
                    <div className = "card">
                        <form id="update_form"
                        onSubmit={e => {
                        e.preventDefault();
                        updateSector({ variables: this.state.change });
                        this.setState({change: {}});
                        }}
                    >
                        <div className="card">
                            <div className = "card">
                            <svg ref={node=> this.node = node} 
                                    width={this.props.width} 
                                    height={this.props.height}>
                            </svg>
                            </div>
                            <button className="btn btn-primary" type="submit">Save Position</button>
                            <button type="button" className="btn btn-danger" onClick={()=>
                            this.props.onRefetch()
                            }>Reset</button>
                         </div>
                     </form>
                     </div>
                 )}
             </Mutation>
        )

    }
}

var createLot = (node, props, state) =>{
    // these constants need to be replaced
    console.log(props.data)
    const xMax = 10
    const yMax = 10

    const xScale = d3.scaleLinear().domain([0, xMax]).range([0, props.width])
    const yScale = d3.scaleLinear().domain([0, yMax]).range([0, props.height])


    // add grid
    d3.select(node).selectAll('.vertical')
                   .data(d3.range(1, props.width/resolution))
                   .enter()
                   .append('line')
                   .attr('class', 'vertical')
                   .attr('x1', (d)=>d*resolution)
                   .attr('y1', 0)
                   .attr('x2', (d)=>d*resolution)
                   .attr('y2', props.height)

    d3.select(node).selectAll('.horizontal')
                   .data(d3.range(1, props.height/resolution))
                   .enter()
                   .append('line')
                   .attr('class', 'horizontal')
                   .attr('x1', 0)
                   .attr('y1', (d)=>d*resolution)
                   .attr('x2', props.width)
                   .attr('y2', (d)=>d*resolution)

    // enter sectors
    d3.select(node).selectAll('svg')
                .data(props.data)
                .enter()
                .append('svg')
    
    // exit sectors
    d3.select(node).selectAll('svg')
                .data(props.data)
                .exit()
                .remove()

    // update sectors
    var sectorsSvgs = d3.select(node).selectAll('svg')
                .data(props.data)
                .call(createSector, xScale(1), yScale(1), (d) => d.sectorSpots, (d) => d.pk)
                .attr("x", (d)=> xScale(d.xIndex))
                .attr("y", (d) => yScale(d.yIndex))
                .attr("width", () => xScale(1))
                .attr("height", () => yScale(1))
                // this is allowing the sectors to be dragged
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended))
    //appending IDs
    sectorsSvgs.append("text")
               .attr("x", xScale(0.5))
               .attr("y", yScale(0.5))
               .attr("text-anchor", "start")
               .style("fill", "steelblue")
               .text((d)=>d.pk)


    function dragstarted(d){
        d3.select(this).raise().classed("active", true)
    }

    function dragged(d){
        let x = d3.event.x
        let y = d3.event.y
        let gridX = Math.round(x/resolution)*resolution
        let gridY = Math.round(y/resolution)*resolution

        d3.select(this).attr("x", d.x = gridX).attr("y", d.y = gridY)
    }

    function dragended(d){
        d3.select(this).raise().classed("active", false)
        state.change = {id: d.id, xIndex: xScale.invert(d.x), yIndex: yScale.invert(d.y)}
        // d3.select( '#update_form').node
    }
}


export default LotChart;