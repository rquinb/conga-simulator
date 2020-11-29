<template>
    <b-container>
        <b-col class="menu" cols="2"></b-col>
        <b-col class="main" cols="10">
            <b-card class="text-center">
                <b-card-title>CONGA SIMULATOR</b-card-title>
                <b-form-group id="player-1" label="Jugador 1" label-for="player-1">
                    <b-form-input id="player-1" v-model="gameConfig.players.playerOne" trim></b-form-input>
                </b-form-group>
                <b-form-group id="player-2" label="Jugador 2" label-for="player-2">
                    <b-form-input id="player-2" v-model="gameConfig.players.playerTwo" trim></b-form-input>
                </b-form-group>
                <b-form-group id="games-number" label="Numero de juegos a simular" label-for="games-number">
                    <b-form-input id="games-number" v-model="gameConfig.gamesNumber" type="range" min="0" max="1000"></b-form-input>
                    <span>Juegos: <span style="font-weight:bold">{{gameConfig.gamesNumber}}</span></span>
                </b-form-group>
                <b-button @click="getGames">SIMULAR JUEGOS</b-button>
            </b-card>
            <game v-for="(game, index) in games" :game="game" :key="index"></game>
        </b-col>
    </b-container>
</template>
<script>
import axios from 'axios';
import Game from './Game.vue'
export default {
    data(){
        return {
            games: [],
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
        Game
    },
    methods:{
        getGames(){
            axios.get('http://localhost:5000/games-simulation',{
                params: {
                    "number-of-games": this.gameConfig.gamesNumber,
                    "player-1": this.gameConfig.players.playerOne,
                    "player-2": this.gameConfig.players.playerTwo
                }
            }).then((response) => {
                console.log(response.data)
                this.games = response.data.games
            });
        }
    }
}
</script>
<style scoped>
    .menu{
        background-color: rgb(133, 132, 132);
    }
</style>>
