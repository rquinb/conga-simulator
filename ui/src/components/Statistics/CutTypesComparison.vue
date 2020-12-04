<script>

import { Bar } from 'vue-chartjs'
import {getLabels} from './cutLabels.js'

export default {
  name: "cut-types-comparison",
  extends: Bar,
  props:{
      cutsPlayer1: Object,
      cutsPlayer2: Object,
      namePlayer1: String,
      namePlayer2: String
  },
data(){
    return{
        chartdata: {
            labels: this.labels(),
            datasets: this.buildDatasets()
        },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                yAxes: [
                    {
                        id: 'y-axis',
                        ticks:{
                            min: 0
                        }
                    }
                ]
            }
        }
            
    }
},
methods:{
    buildDatasets(){
        let datasets = []; 
        let cutTypes = Object.keys(this.cutsPlayer1)
        for(let playerNumber of [1, 2]){
            let data = [];
            let color = [];
            let label = playerNumber == 1 ? this.namePlayer1 : this.namePlayer2;
            for(let cut of cutTypes){
                color.push(playerNumber == 1 ? "blue": "red");
                data.push(playerNumber == 1 ? this.cutsPlayer1[cut] : this.cutsPlayer2[cut]);
            }
            datasets.push({
                backgroundColor: color,
                label: label,
                data: data,
                yAxisID: 'y-axis'
                })
        }
        return datasets
    },
    barsColor(data, playerNumber){
        return data.map(()=> playerNumber == 1 ? "blue" : "red")
    },
    labels(){
        return getLabels(Object.keys(this.cutsPlayer1))
    }
},
mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>