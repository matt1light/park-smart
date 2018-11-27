import {range, min, max} from 'd3-array'
import {timeFormat} from 'd3-time-format'
import {select} from 'd3-selection'


import * as simple_slider from 'd3-simple-slider'

let dateValue = 0

function createHistorySlider(node, width, height, date, callBackFunction){
    var margin = {
        left: 10,
        right:10,
        top: 10,
        bottom: 10
    }


    var temp_date = new Date(date)
    console.log('type', typeof(temp_date))
    console.log('date', temp_date)

    var data = range(0, 47).map((d) => new Date(temp_date.getFullYear(), 
                                                temp_date.getMonth(), 
                                                temp_date.getDay(), 
                                                d/2, 
                                                (d%2)*30))

    var slider = simple_slider.sliderHorizontal()
                   .min(min(data))
                   .max(max(data))
                   .step(1000*60*30)
                   .width(width)
                   .tickFormat(timeFormat('%H:%M'))
                   .tickValues(data)
                   .on('onchange', (val) => changeDateValue(val))

    var group = select(node).append("svg")
                   .attr("width", width)
                   .attr("height", height)
                   .append("g")
                   .attr("transform", "translate(30, 30)")

    group.call(slider)

    function changeDateValue(date){
        callBackFunction(date)
    }

}

export default createHistorySlider