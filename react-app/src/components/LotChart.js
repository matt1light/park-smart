import React, { Component } from 'react';
import SectorChart from './SectorChart'

class LotChart extends Component {
    constructor(props){
        super(props)
        this.createLotChart = this.createLotChart.bind(this)
        this.state = this.props
    }

    createLotChart(lotState) {
        let sectorChartList = []

        for(var i in lotState.sectors){
            sectorChartList.push(
                <SectorChart data = {lotState.sectors[i].sector_spots} height={500} width = {500}/>
            )
        }

        return(
            <div>
                {sectorChartList}
            </div>
        )
    }

    render() {
        return (
            <div>
                {this.createLotChart(this.state.data)}
            </div>
        );
    }
}

export default LotChart;