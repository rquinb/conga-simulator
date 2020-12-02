<script>

import { Doughnut } from 'vue-chartjs'

export default {
  name: "cuts-report",
  extends: Doughnut,
  props:{
      playerCuts: Object
  },
data(){
    return{
        chartdata: {
            labels: this.labels(),
            datasets: [
            {
                backgroundColor: this.backgroundColors(),
                label: "Tipos de cortes",
                data: this.values()
            }
            ]
        },
            options: {
                responsive: true,
                maintainAspectRatio: false
        }
            
    }
},
methods:{
    values(){
        let values = [];
        for(let key of Object.keys(this.playerCuts)){
            values.push(this.playerCuts[key])
        }
        return values
    },
    labels(){
        return Object.keys(this.playerCuts).map((value)=> value == "no_cut" ? "Sin corte" : value == "normal_cut" ? "Corte normal" : value == "zero_cut" ? "Corte en Cero" : "Conga")
    },
    backgroundColors(){
        console.log(Object.keys(this.playerCuts).map((value)=> value == "no_cut" ? "black" : value == "normal_cut" ? "lightgreen" : value == "zero_cut" ? "green" : "darkgreen"))
        return Object.keys(this.playerCuts).map((value)=> value == "no_cut" ? "black" : value == "normal_cut" ? "lightgreen" : value == "zero_cut" ? "green" : "darkgreen")
    }
},
mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}

</script>