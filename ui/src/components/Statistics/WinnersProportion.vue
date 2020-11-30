<script>

import { Doughnut } from 'vue-chartjs'

export default {
  name: "winners-proportion",
  extends: Doughnut,
  props:{
      statistics: Object
  },
data(){
    return{
        chartdata: {
            labels: [this.statistics.name_player_1, this.statistics.name_player_2],
            datasets: [
            {
                backgroundColor: ['blue', 'red'],
                label: "Proporcion de victorias por jugador",
                data: [this.statistics.proportion_of_wins_player_1, this.statistics.proportion_of_wins_player_2]
            }
            ]
        },
            options: {
                responsive: true,
                maintainAspectRatio: false
        }
            
    }
},
mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>