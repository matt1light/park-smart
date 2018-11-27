import React, { Component } from 'react';
import './LotChart2.css'
import createHistorySlider from './HistorySpotChart'
import createSector from './SectorChart2.js'
// import {scaleLinear, scaleOrdinal} from 'd3-scale'
// import {select, event} from 'd3-selection'
// import {drag} from 'd3-drag'

import * as d3 from 'd3'
const resolution = 50

class LotChart extends Component {
    constructor(props){
        super(props)
        this.createLotChart = this.createLotChart.bind(this)
        this.state = this.props
    }

    componentDidMount(){
        this.createLotChart()
    }
    // componentDidUpdate(){
    //     this.createLotChart()
    // }

    createLotChart() {
        // createLot(this.node, this.state.height, this.state.width, this.state.data)
        createHistorySlider(this.node, this.state.width, this.state.height, Date.now(), changeDate)
    }

    render() {
        return <svg ref={node=> this.node = node} 
                    width={this.props.width} 
                    height={this.props.height}>
        </svg>
    }

}

function changeDate(date){
    console.log(date)
}

function createLot(node, height, width, state){
    // these constants need to be replaced
    const xMax = 10
    const yMax = 10

    const xScale = d3.scaleLinear().domain([0, xMax]).range([0, width])
    const yScale = d3.scaleLinear().domain([0, yMax]).range([0, height])

    // add grid
    d3.select(node).selectAll('.vertical')
                   .data(d3.range(1, width/resolution))
                   .enter()
                   .append('line')
                   .attr('class', 'vertical')
                   .attr('x1', (d)=>d*resolution)
                   .attr('y1', 0)
                   .attr('x2', (d)=>d*resolution)
                   .attr('y2', height)

    d3.select(node).selectAll('.horizontal')
                   .data(d3.range(1, height/resolution))
                   .enter()
                   .append('line')
                   .attr('class', 'horizontal')
                   .attr('x1', 0)
                   .attr('y1', (d)=>d*resolution)
                   .attr('x2', width)
                   .attr('y2', (d)=>d*resolution)

    // enter sectors
    d3.select(node).selectAll('svg')
                .data(state.sectors)
                .enter()
                .append('svg')
    
    // exit sectors
    d3.select(node).selectAll('svg')
                .data(state.sectors)
                .exit()
                .remove()

    // update sectors
    var sectorsSvgs = d3.select(node).selectAll('svg')
                .data(state.sectors)
                .call(createSector, xScale(1), yScale(1), (d) => d.sector_spots, (d) => d.pk)
                .attr("x", (d)=> xScale(d.x))
                .attr("y", (d) => yScale(d.y))
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
}

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
    d3.select(this).classed("active", false)
}




export default LotChart;