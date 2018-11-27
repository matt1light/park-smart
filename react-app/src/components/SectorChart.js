import React, { Component } from 'react';
import {scaleLinear, scaleOrdinal} from 'd3-scale'
import {max} from 'd3-array'
import {select} from 'd3-selection'



class SectorChart extends Component {
    constructor(props){
        super(props)
        this.createSectorChart = this.createSectorChart.bind(this)
        this.state = this.props
    }

    componentDidMount(){
        this.createSectorChart()
    }
    componentDidUpdate(){
        this.createSectorChart()
    }

    createSectorChart(){
        // get the base node (svg)
        createSector(this.node, this.state.height, this.state.width, this.state.data)
    }

    render() {
        return <svg ref={node=> this.node = node} 
                    width={this.props.width} 
                    height={this.props.height}>
        </svg>
    }
}

function createSector(node, height, width, sector){
    const svg_height = height
    const svg_width = width

    // get the maximum x in the data
    const xMax = 3
    // get the maximum y in the data
    const yMax = 2

    const xScale = scaleLinear().domain([0, xMax]).range([0, svg_width])
    const yScale = scaleLinear().domain([0, yMax]).range([0, svg_height])
    const colourScale = scaleOrdinal().domain(['avalable','full','inactive']).range(['green', 'red', 'grey'])

    // enter
    select(node).selectAll('rect')
                .data(sector)
                .enter()
                .append('rect')

    // exit
    select(node).selectAll('rect')
                .data(sector)
                .exit()
                .remove()

    // update
    select(node).selectAll('rect')
                .data(sector)
                .style('fill', (d) => colourScale(getSpotState(d.spot)))
                .attr('x', (d) => xScale(getX(d.image_coordinates)))
                .attr('y', (d) => yScale(getY(d.image_coordinates)))
                .attr('width', svg_width/xMax)
                .attr('height', svg_height/yMax)

}
function getSpotState(spot){
        if(!spot.active){
            return 'inactive'
        }
        else if (spot.full){
            return 'full'
        }
        else {
            return 'avaliable'
        }
    }

function getX(image_coordinates){
    return image_coordinates.left
}

function getY(image_coordinates){
    return image_coordinates.top
}
export default SectorChart;