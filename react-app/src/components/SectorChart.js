import * as d3 from 'd3'

function createSector(node, width, height, sector_spots, id){
    // get the maximum x in the data
    const xMax = 2000
    // get the maximum y in the data
    const yMax = 1250

    const xScale = d3.scaleLinear().domain([0, xMax]).range([0, width])
    const yScale = d3.scaleLinear().domain([0, yMax]).range([0, height])
    const colourScale = d3.scaleOrdinal().domain(['available','full','inactive']).range(['green', 'red', 'grey'])

    // enter
    node.selectAll('rect')
                .data(sector_spots)
                .enter()
                .append('rect')

    // exit
    node.selectAll('rect')
                .data(sector_spots)
                .exit()
                .remove()

    // update
    node.selectAll('rect')
                .data(sector_spots)
                .style('fill', (d) => colourScale(getSpotState(d.spot)))
                .attr('x', (d) => xScale(getX(d.imageCoordinates)))
                .attr('y', (d) => yScale(getY(d.imageCoordinates)))
                .attr('width', (d) => xScale(d.imageCoordinates.right - d.imageCoordinates.left))
                .attr('height', (d) => yScale(d.imageCoordinates.bottom - d.imageCoordinates.top))
}
function getSpotState(spot){
        if(!spot.active){
            return 'inactive'
        }
        else if (spot.full){
            return 'full'
        }
        else {
            return 'available'
        }
    }

function getX(image_coordinates){
    return image_coordinates.left
}

function getY(image_coordinates){
    return image_coordinates.top
}
export default createSector