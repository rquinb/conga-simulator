<template>
    <b-container class="game-container">
        <b-card class="game-card text-center shadow-lg">
            <b-row class="game-title text-center">
                <b-card-title>Juego {{key}}</b-card-title>
            </b-row>
            <b-row class="game-information text-center">
                <b-list-group flush>
                    <b-list-group-item>
                        <span>Jugador 1: </span>
                        <span class="data">{{game.player_1}}</span>
                    </b-list-group-item>
                    <b-list-group-item>
                        <span>Jugador 2: </span>
                        <span class="data">{{game.player_2}}</span>
                    </b-list-group-item>
                </b-list-group>
            </b-row>
            <b-row class="game-information text-center">
                <span>Resultados </span>
                <b-table class="game-table" :items="game.score_evolution" :fields="scoreEvolutionTable.fields" bordered></b-table>
                <b-list-group flush>
                    <b-list-group-item>
                        <span>Ganador: </span>
                        <span class="data winner">{{game.winner}}</span>
                    </b-list-group-item>
                </b-list-group>
            <b-row>
        </b-card>
    </b-container>
</template>
<script>

export default {
  name: 'game',
  props: {
      game: Object, 
      key: Number
  },
  data(){
      return {
          scoreEvolutionTable: {
              fields: [
                  {key:'player_1_points', label:'Puntos Jugador 1'}, 
                  {key:'player_2_points', label:'Puntos Jugador 2'}]
          }
      }
  }
}
</script>

<style>
    .game-container{
        margin-top: 4%;
    }
    .game-card{
        text-align: center;
        display: flex;
        font-size: large;
    }
    .game-information{
        text-align: center;
    }
    .data{
        font-weight: bolder;
    }
    .winner{
        color: rgb(11, 146, 29);
    }

</style>