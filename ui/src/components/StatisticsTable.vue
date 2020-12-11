<template>
    <div>
        <template v-if="displayStatistics">
            <b-row>
                <b-col>
                    <b-card>
                        <b-card-title>Historial de Simulaciones</b-card-title>
                        <b-table class="gradient-background game-table text-center" 
                            selectable
                            select-mode="single"
                            :items="items"
                            :fields="fields"
                            @row-selected="onRowSelected"
                            thead-class="bg-dark text-white"
                        ></b-table>
                    </b-card>
                </b-col>
            </b-row>
        </template>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    title: 'Conga Simulator',
    data(){
        return {
            displayStatistics: false,
            fields: [
                  {key:'simulation_id', label:'Id'}, 
                  {key:'created', label:'Fecha'},
                  {key:'mean_rounds_per_game', label:'Promedio de rounds por juego'},
                  {key:'total_games', label:'Total de juegos'}
            ],
            items: []
        }
    },
    methods:{
        getSimulations(){
            this.displayStatistics = false;
            axios.get(`${process.env.VUE_APP_API_URL}/games-simulations`).then((response) => {
                this.items = response.data.result;
                this.displayStatistics = true;

            }).catch((response) => {
                console.log(response);
                this.displayStatistics = false;
            });
        },
        onRowSelected(item){
            this.$router.push(`games-statistics/${item[0].simulation_id}`)
        }
    },
    created() {
        this.getSimulations()
    },
}
</script>