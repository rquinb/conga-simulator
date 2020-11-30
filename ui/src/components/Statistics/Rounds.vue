<script>

import { Bar } from 'vue-chartjs'

export default {
  name: "rounds",
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
                backgroundColor: this.barsColor(),
                label: false,
                data: this.statistics.rounds_per_game,
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
    barsColor(){
        return this.statistics.games_report.map((gameReport)=> gameReport.winner == this.statistics.name_player_1 ? "blue" : "red")
    },
    labels(){
        return this.statistics.rounds_per_game.map((value, index) => index + 1)
    }
},
mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>