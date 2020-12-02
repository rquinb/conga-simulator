<template>
    <b-container>
        <b-col class="menu" md="2"></b-col>
        <b-col class="main" md="10">
            <b-card class="text-center">
                <b-card-title>CONGA SIMULATOR</b-card-title>
                <b-form-group id="player-1" label="Jugador 1" label-for="player-1">
                    <b-form-input class="text-center" id="player-1" v-model="gameConfig.players.playerOne" trim></b-form-input>
                </b-form-group>
                <b-form-group id="player-2" label="Jugador 2" label-for="player-2">
                    <b-form-input class="text-center" id="player-2" v-model="gameConfig.players.playerTwo" trim></b-form-input>
                </b-form-group>
                <b-form-group id="games-number" label="Numero de juegos a simular" label-for="games-number">
                    <b-form-input id="games-number" v-model="gameConfig.gamesNumber" type="range" min="0" max="1000"></b-form-input>
                    <span>Juegos: <span style="font-weight:bold">{{gameConfig.gamesNumber}}</span></span>
                </b-form-group>
                <div class="simulate-button-container">
                    <b-button @click="getGames"><b-spinner small type="grow" v-if="displayLoadingSpinner"></b-spinner>{{simulateButtonText}}</b-button>
                </div>
                <template v-if="displayLoadingSpinner">
                    <div class="loading-element">
                        <ping-pong class="spinner" size="150px"></ping-pong>
                    </div>
                </template>
            </b-card>
            <template v-if="displayStatistics">
                <statistics :statistics="statistics"></statistics>
            </template>
        </b-col>
    </b-container>
</template>
<script>
import axios from 'axios';
import PingPong from 'vue-loading-spinner/src/components/PingPong.vue'
import Statistics from './Statistics/Statistics.vue'
export default {
    data(){
        return {
            displayStatistics: false,
            displayLoadingSpinner : false,
            statistics: {},
            gameConfig: {
                players: {
                    playerOne: "",
                    playerTwo: "" 
                },
                gamesNumber: 0
            }
        }
    },
    components:{
        Statistics,
        PingPong
    },
    methods:{
        getGames(){
            this.displayStatistics = false;
            this.displayLoadingSpinner = true;
            axios.get('http://localhost:5000/games-simulation',{
                params: {
                    "number-of-games": this.gameConfig.gamesNumber,
                    "player-1": this.gameConfig.players.playerOne,
                    "player-2": this.gameConfig.players.playerTwo
                }
            }).then((response) => {
                this.statistics = response.data.games;
                this.displayLoadingSpinner = false;
                this.displayStatistics = true;
            }).catch(() => {
                this.displayLoadingSpinner = false;
            });
        }
    },
computed:{
    simulateButtonText(){
        return this.displayLoadingSpinner ? "Simulando juegos...": "SIMULAR JUEGOS";
    }
  }
}
</script>
<style scoped>
    .menu{
        background-color: rgb(133, 132, 132);
    }
    .loading-element{
        width: 100%;
    }
    .simulate-button-container{
        width: 100%;
    }
    .spinner{
        margin-left: 40%;
    }
</style>>
