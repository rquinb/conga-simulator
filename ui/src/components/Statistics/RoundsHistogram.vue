<script>

import { Bar } from 'vue-chartjs'

export default {
  name: "rounds-histogram",
  extends: Bar,
  props:{
      statistics: Object
  },
data(){
    return{
        chartdata: {
            labels: this.labels(),
            datasets: [
                {
                    backgroundColor: "green",
                    label: "Distribucion de cada longitud de rounds",
                    data: this.values(),
                    yAxisID: 'y-axis'
                }
            ]
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
    values(){
        let values = [];
        for(let histogramBar of this.statistics.rounds_histogram){
            let key = Object.keys(histogramBar)[0]
            values.push(histogramBar[key])
        }
        return values
    },
    labels(){
        return this.statistics.rounds_histogram.map((histogramBar) => Object.keys(histogramBar)[0])
    }
},
mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>