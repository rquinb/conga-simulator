<template>
    <b-container class="statistics-container">
        <b-card class="statistics-card text-center shadow-lg">
            <div class="game-title">
                <b-card-title>Estadisticas</b-card-title>
            </div>
            <div class="game-information">
                <div class="section-title">
                    <b-card-title>General</b-card-title>
                </div>
                <b-list-group flush>
                    <b-list-group-item>
                        <span>Jugador 1: </span>
                        <span class="data">{{statistics.name_player_1}}</span><span class="symbol-player-1">✪</span>
                    </b-list-group-item>
                    <b-list-group-item>
                        <span>Jugador 2: </span>
                        <span class="data">{{statistics.name_player_2}}</span><span class="symbol-player-2">✪</span>
                    </b-list-group-item>
                    <b-list-group-item>
                        <span>Cantidad de juegos: </span>
                        <span class="data">{{statistics.number_of_games}}</span>
                    </b-list-group-item>
                </b-list-group>
            </div>
            <div class="game-information">
                <div class="section-title">
                    <b-card-title>Rounds</b-card-title>
                    <rounds :statistics="statistics"></rounds>
                </div>
            </div>
            <b-button :class="displayGames ? 'btn-danger': 'btn-success'" @click="toggleDisplayGames"> {{showGamesButtonText}}</b-button>
            <template v-if="displayGames">
                <game v-for="(game, index) in statistics.games_report" :game="game" :key="index"></game>
            </template>
        </b-card>
    </b-container>
</template>
<script>

import Rounds from './Rounds.vue'
import Game from './Game.vue'

export default {
  name: 'statistics',
  props: {
      statistics: Object, 
  },
  components: {
      Rounds,
      Game
  },
  data(){
      return {
        displayGames : false
      }
  },
  methods:{
    toggleDisplayGames(){
        this.displayGames = !this.displayGames;
    }
  },
  computed:{
    showGamesButtonText(){
        return this.displayGames ? "Ocultar detalle de Juegos": "Mostrar detalle de Juegos"
    }
  }
}
</script>

<style>
    .statistics-container{
        margin-top: 4%;
        margin-bottom: 4%;
    }
    .statistics-card{
        font-size: large;
    }
    .game-information{
        text-align: center;
    }
    .game-title{
        font-weight: bolder;
        font-style: italic;
    }
    .section-title{
        text-decoration: underline;
    }
    .data{
        font-weight: bold;
    }
    .symbol-player-1{
        color: blue;
        font-size: xx-large;
    }
    .symbol-player-2{
        color: red;
        font-size: xx-large;
    }

</style>