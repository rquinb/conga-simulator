<template>
    <b-container class="game-container">
        <b-card class="game-card text-center shadow-lg">
            <div class="game-information">
                <b-table class="game-table" :items="game.score_evolution" :fields="scoreEvolutionTable.fields" thead-class="bg-dark text-white"></b-table>
                <b-list-group flush>
                    <b-list-group-item>
                        <span>Ganador: </span>
                        <span class="data winner">{{game.winner}}</span>
                    </b-list-group-item>
                </b-list-group>
            </div>
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