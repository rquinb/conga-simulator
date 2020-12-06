<template>
    <b-container class="statistics-container" fluid>
        <b-row class="games-details-button-row">
            <b-col class="text-center">
                <b-button :class="displayGames ? 'btn-danger': 'btn-success'" @click="toggleDisplayGames"> {{gamesButtonText}}</b-button>
            </b-col>
        </b-row>
        <b-row class="row-height justify-content-center">
            <b-col :md="displayGames ? 6: 8">
                <b-card class="gradient-background statistics-card text-center shadow-lg">
                    <div class="game-title">
                        <b-card-title>Estadisticas</b-card-title>
                    </div>
                    <div class="game-information">
                        <div class="section-title">
                            <b-card-title>General</b-card-title>
                        </div>
                        <b-list-group flush>
                            <b-list-group-item class="gradient-background">
                                <span>Jugador 1: </span>
                                <span class="data">{{statistics.name_player_1}}</span><span class="symbol-player-1">✪</span>
                            </b-list-group-item>
                            <b-list-group-item class="gradient-background">
                                <span>Jugador 2: </span>
                                <span class="data">{{statistics.name_player_2}}</span><span class="symbol-player-2">✪</span>
                            </b-list-group-item>
                            <b-list-group-item class="gradient-background">
                                <span>Cantidad de juegos: </span>
                                <span class="data">{{statistics.number_of_games}}</span>
                            </b-list-group-item>
                        </b-list-group>
                    </div>
                    <div class="game-information">
                        <div class="section-title">
                            <b-card-title>Proporcion de juegos ganados</b-card-title>
                            <winners-proportion :statistics="statistics"></winners-proportion>
                        </div>
                    </div>
                    <div class="game-information">
                        <div class="section-title">
                            <b-card-title>Distribucion de longitud de Rounds</b-card-title>
                            <rounds-histogram :statistics="statistics"></rounds-histogram>
                        </div>
                    </div>
                    <div class="game-information">
                        <div class="section-title">
                            <b-card-title>Detalle de longitud de Rounds</b-card-title>
                            <rounds :statistics="statistics"></rounds>
                        </div>
                    </div>
                    <div class="game-information">
                        <div class="section-title">
                            <b-card-title>Comparacion de cantidad de cortes por jugador</b-card-title>
                            <cut-types-comparison 
                                :namePlayer1="statistics.name_player_1" :cutsPlayer1="statistics.player_1_cuts" 
                                :namePlayer2="statistics.name_player_2" :cutsPlayer2="statistics.player_2_cuts">
                            </cut-types-comparison>
                        </div>
                    </div>
                    <div class="game-information">
                        <div class="section-title">
                            <b-card-title>Detalle de tipos de corte por jugador</b-card-title>
                        </div>
                        <b-card class="gradient-background statistics-card text-center">
                            <b-container fluid>
                                <b-row>
                                    <b-col md="6">
                                        <b-card-title>{{statistics.name_player_1}}<b-card-title>
                                        <cuts-report :playerCuts="statistics.player_1_cuts"></cuts-report>
                                    </b-col>
                                    <b-col md="6">
                                        <b-card-title>{{statistics.name_player_2}}<b-card-title>
                                        <cuts-report :playerCuts="statistics.player_2_cuts"></cuts-report>
                                    </b-col>
                                </b-row>
                            </b-container>
                        </b-card>
                    </div>
                </b-card>
            </b-col>
            <template v-if="displayGames">
                <b-col md="6">
                    <b-pagination v-model="games.currentPage" :total-rows="rows" :per-page="games.perPage"></b-pagination>
                    <game v-for="(game, index) in statistics.games_report.slice(games.perPage * (games.currentPage - 1), games.perPage * games.currentPage)" 
                        :game="game" :key="index" 
                        :namePlayer1="statistics.name_player_1"
                        :namePlayer2="statistics.name_player_2" >
                    </game>
                </b-col>
            </template>
        </b-row>
    </b-container>
</template>
<script>

import Rounds from './Rounds.vue'
import Game from './Game.vue'
import WinnersProportion from './WinnersProportion.vue'
import RoundsHistogram from './RoundsHistogram.vue'
import CutsReport from './CutsReport.vue'
import CutTypesComparison from './CutTypesComparison.vue'

export default {
  name: 'statistics',
  props: {
      statistics: Object, 
  },
  components: {
      Rounds,
      Game,
      WinnersProportion,
      RoundsHistogram,
      CutsReport,
      CutTypesComparison
  },
  data(){
      return {
        displayGames : false,
        games:{
            perPage: 6,
            currentPage: 1,
            gamesReport: this.statistics.games_report
        }
      }
  },
  methods:{
    toggleDisplayGames(){
        this.displayGames = !this.displayGames;
    }
  },
  computed:{
    gamesButtonText(){
        return this.displayGames ? "Ocultar detalle de Juegos": "Mostrar detalle de Juegos"
    },
    rows(){
        return this.games.gamesReport.length
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
        margin-top: 5%;
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
    .row-height{
        height: 100vh;
    }
    .games-details-button-row{
        margin-top: 3%;
        margin-bottom: 3%;
    }
    .scrollable-column{
        overflow-y: scroll;
    }

</style>