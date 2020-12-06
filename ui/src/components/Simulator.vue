<template>
    <b-container class="simulator-container" fluid>
        <b-row class="main text-center justify-content-md-center">
            <b-col>
                <b-card class="text-center simulator-form-element gradient-background">
                    <b-card-title>CONGA SIMULATOR</b-card-title>
                        <player-form 
                            FormTitle="Jugador 1" 
                            :playerNum="1"
                            @updatePlayer="handleUpdatePlayer">
                        </player-form>
                        <player-form 
                            FormTitle="Jugador 2" 
                            :playerNum="2"
                            @updatePlayer="handleUpdatePlayer">
                        </player-form>
                    <b-form-group id="games-number" label="Numero de juegos a simular" label-for="games-number">
                        <b-form-input id="games-number" v-model="gameConfig.numberOfGames" type="range" min="0" max="1000"></b-form-input>
                        <span>Juegos: <span style="font-weight:bold">{{gameConfig.numberOfGames}}</span></span>
                    </b-form-group>
                    <div class="simulate-button-container">
                        <b-button @click="getGames"><b-spinner small type="grow" v-if="displayLoadingSpinner"></b-spinner>{{simulateButtonText}}</b-button>
                    </div>
                    <template v-if="displayLoadingSpinner">
                        <div class="simulation">
                            <b-progress :max="simulationStatus.simulationProgress.total" animated>
                                <b-progress-bar :value="simulationStatus.simulationProgress.current_simulation">
                                    <span>Simulando <strong>{{ simulationStatus.simulationProgress.current_simulation }} de {{ simulationStatus.simulationProgress.total }} juegos</strong></span>
                                </b-progress-bar>
                            </b-progress>
                        </div>
                        <div class="loading-element">
                            <ping-pong class="spinner" size="150px"></ping-pong>
                        </div>
                    </template>
                </b-card>
            <b-col>
        </b-row>
        <b-row>
            <template v-if="displayStatistics">
                <statistics :statistics="statistics"></statistics>
            </template>
        </b-row>
    </b-container>
</template>
<script>
import axios from 'axios';
import PingPong from 'vue-loading-spinner/src/components/PingPong.vue'
import PlayerForm from './PlayerForm.vue'
import Statistics from './Statistics/Statistics.vue'
export default {
    title: 'Conga Simulator',
    data(){
        return {
            displayStatistics: false,
            displayLoadingSpinner : false,
            statistics: {},
            gameConfig: {
                players: {
                    playerOne: {},
                    playerTwo: {} 
                },
                numberOfGames: 0
            },
            simulationStatus: {
                simulationRunning : false,
                pollingInterval: null,
                taskStatusUrl: "",
                simulationProgress: {
                    current_simulation: 0,
                    total: 0 
                }
            }
        }
    },
    components:{
        Statistics,
        PingPong,
        PlayerForm
    },
    methods:{
        handleUpdatePlayer(event){
            if(event.number == 1){
                this.gameConfig.players.playerOne = event;
            }else{
                this.gameConfig.players.playerTwo = event;
            }
        },
        getGames(){
            this.displayStatistics = false;
            this.displayLoadingSpinner = true;
            axios.post('http://localhost:5000/games-simulation',{
                    "numberOfGames": parseInt(this.gameConfig.numberOfGames),
                    "player1": {
                        "name": this.gameConfig.players.playerOne.name,
                        "agentType": this.gameConfig.players.playerOne.agentType.selected,
                        "acceptedCardsRange":
                        [
                            parseInt(this.gameConfig.players.playerOne.acceptedCardsRange.minCard),
                            parseInt(this.gameConfig.players.playerOne.acceptedCardsRange.maxCard) 
                        ],
                        "maxRestBeforeCutting": parseInt(this.gameConfig.players.playerOne.maxRestBeforeCutting)
                    },
                    "player2": {
                        "name": this.gameConfig.players.playerTwo.name,
                        "agentType": this.gameConfig.players.playerTwo.agentType.selected,
                        "acceptedCardsRange":
                        [
                            parseInt(this.gameConfig.players.playerTwo.acceptedCardsRange.minCard),
                            parseInt(this.gameConfig.players.playerTwo.acceptedCardsRange.maxCard) 
                        ],
                        "maxRestBeforeCutting": parseInt(this.gameConfig.players.playerTwo.maxRestBeforeCutting)
                    }
            }).then((response) => {
                console.log(response.headers)
                this.simulationStatus.taskStatusUrl = response.headers['location'];
                this.simulationStatus.simulationRunning = true;
                console.log(this.simulationStatus.taskStatusUrl)

            }).catch(() => {
                this.displayLoadingSpinner = false;
            });
        }
    },
computed:{
    simulateButtonText(){
        return this.displayLoadingSpinner ? "Simulando juegos...": "SIMULAR JUEGOS";
    }
  },
  watch: {
    "simulationStatus.simulationRunning": function(val) {
        console.log(val)
        if (val) {
            this.simulationStatus.pollingInterval = setInterval(() => {
                axios.get(this.simulationStatus.taskStatusUrl).then((response)=>{
                    this.simulationStatus.simulationProgress.current_simulation = response.data.current_simulation;
                    this.simulationStatus.simulationProgress.total = response.data.total;
                    if(response.data.state == "FAILURE"){
                        this.displayLoadingSpinner = false;
                        this.simulationStatus.simulationRunning = false;
                        clearInterval(this.simulationStatus.pollingInterval)
                    }
                    if(response.data.result){
                        this.statistics = response.data.result;
                        this.displayLoadingSpinner = false;
                        this.simulationStatus.simulationRunning = false;
                        this.displayStatistics = true;
                        clearInterval(this.simulationStatus.pollingInterval)
                    }
                })
            }, 500);
        } else {
            clearInterval(this.simulationStatus.pollingInterval);
            }
        }
    }
}
</script>
<style>

    .gradient-background {
        background-image: linear-gradient(to bottom, rgba(250, 212, 212, 0.651), rgba(250, 212, 212, 0.986));
    }
    .simulation{
        margin-top: 3%;
    }
    .loading-element{
        width: 100%;
    }
    .simulate-button-container{
        width: 100%;
    }
    .spinner{
        margin-left: 42%;
    }
    .simulator-form-element{
        display: inline-block;
        width: 50%;
    }
    .input-player{
        font-weight: bold;
        font-size: x-large;
    }
    .input-player-1{
        color: blue;
    }
    .input-player-2{
        color: red;
    }
</style>>
