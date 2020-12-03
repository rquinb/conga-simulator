<template>
    <b-container class="simulator-container" fluid>
        <b-row class="main text-center justify-content-md-center">
            <b-col>
                <b-card class="text-center simulator-form-element gradient-background">
                    <b-card-title>CONGA SIMULATOR</b-card-title>
                    <b-form-group label="Jugador 1" >
                        <b-input-group prepend="Jugador 1">
                            <b-form-input  class="simulator-form-element input-player input-player-1" v-model="gameConfig.players.playerOne.name" trim></b-form-input>
                        </b-input-group>
                        <b-input-group prepend="Tipo de Agente">
                            <b-form-select v-model="gameConfig.players.playerOne.agentType.selected" :options="gameConfig.players.playerOne.agentType.options"></b-form-select>
                        </b-input-group>
                        <b-input-group class="md-2" prepend="Rango de cartas aceptados" :append="`Min: ${gameConfig.players.playerOne.acceptedCardsRange.minCard} | Max: ${gameConfig.players.playerOne.acceptedCardsRange.maxCard}`">
                            <b-form-input id="min-1" v-model="gameConfig.players.playerOne.acceptedCardsRange.minCard" type="range" min="1" max="12" step="1"></b-form-input>
                            <b-form-input id="max-1" v-model="gameConfig.players.playerOne.acceptedCardsRange.maxCard" type="range" min="1" max="12" step="1"></b-form-input>
                        </b-input-group>
                        <b-input-group prepend="Maximo valor antes de cortar" :append="gameConfig.players.playerOne.maxRestBeforeCutting">
                            <b-form-input id="max-cut-rest-1" v-model="gameConfig.players.playerOne.maxRestBeforeCutting" type="range" min="0" max="10" step="1"></b-form-input>
                        </b-input-group>
                    </b-form-group>
                    <b-form-group label="Jugador 2" >
                        <b-input-group prepend="Jugador 2">
                            <b-form-input  class="simulator-form-element input-player input-player-2" v-model="gameConfig.players.playerTwo.name" trim></b-form-input>
                        </b-input-group>
                        <b-input-group prepend="Tipo de Agente">
                            <b-form-select v-model="gameConfig.players.playerTwo.agentType.selected" :options="gameConfig.players.playerTwo.agentType.options"></b-form-select>
                        </b-input-group>
                        <b-input-group class="md-2" prepend="Rango de cartas aceptados" :append="`Min: ${gameConfig.players.playerTwo.acceptedCardsRange.minCard} | Max: ${gameConfig.players.playerTwo.acceptedCardsRange.maxCard}`">
                            <b-form-input id="min-2" v-model="gameConfig.players.playerTwo.acceptedCardsRange.minCard" type="range" min="1" max="12" step="1"></b-form-input>
                            <b-form-input id="max-2" v-model="gameConfig.players.playerTwo.acceptedCardsRange.maxCard" type="range" min="1" max="12" step="1"></b-form-input>
                        </b-input-group>
                        <b-input-group prepend="Maximo valor antes de cortar" :append="gameConfig.players.playerTwo.maxRestBeforeCutting">
                            <b-form-input id="max-cut-rest-2" v-model="gameConfig.players.playerTwo.maxRestBeforeCutting" type="range" min="0" max="10" step="1"></b-form-input>
                        </b-input-group>
                    </b-form-group>
                    <b-form-group id="games-number" label="Numero de juegos a simular" label-for="games-number">
                        <b-form-input id="games-number" v-model="gameConfig.numberOfGames" type="range" min="0" max="1000"></b-form-input>
                        <span>Juegos: <span style="font-weight:bold">{{gameConfig.numberOfGames}}</span></span>
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
                    playerOne: {
                        name: "",
                        agentType: {
                            selected: null,
                            options: [
                            { value: null, text: 'Seleccione un tipo de agente' },
                            { value: 'conservative_chooser', text: 'Conservador' }
                            ]
                        },
                        acceptedCardsRange: {
                            minCard: 1,
                            maxCard: 12
                        },
                        maxRestBeforeCutting: 10
                    },
                    playerTwo: {
                        name: "",
                        agentType: {
                            selected: null,
                            options: [
                            { value: null, text: 'Seleccione un tipo de agente' },
                            { value: 'conservative_chooser', text: 'Conservador' }
                            ]
                        },
                        acceptedCardsRange: {
                            minCard: 1,
                            maxCard: 12
                        },
                        maxRestBeforeCutting: 10
                    } 
                },
                numberOfGames: 0
            },

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
<style>
    .gradient-background {
        background-image: linear-gradient(to bottom, rgba(250, 212, 212, 0.651), rgba(250, 212, 212, 0.986));
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
