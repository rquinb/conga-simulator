<template>
    <b-container>
        <b-card class="gradient-background game-card text-center shadow-lg">
            <b-table 
                class="gradient-background game-table" 
                :items="game.score_evolution" 
                :fields="scoreEvolutionTable.fields" 
                thead-class="bg-dark text-white"
                @row-clicked="item=>$set(item, '_showDetails', !item._showDetails)"
                >
                <template #cell()="data">
                    <template v-if="data.value.cut == null">
                        <span>{{ data.value.points}}</span>
                    </template>
                    <template v-else-if="data.value.cut == 'zero_cut'">
                        <span v-b-tooltip.hover title="Corte en Cero">{{data.value.points}} ✂✫</span>
                    </template>
                    <template v-else-if="data.value.cut == 'normal_cut'">
                        <span v-b-tooltip.hover title="Corte Normal">{{data.value.points}} ✂</span>
                    </template>
                    <template v-else >
                        <span v-b-tooltip.hover title="Conga">{{data.value.points}} ♛</span>
                    </template>
                </template>
                <template #row-details="row">
                    <b-list-group>
                        <b-list-group-item v-for="(move, index) in row.item.moves" :key="index">
                            <move :move="move" :position="parseInt(index)"></move>
                        </b-list-group-item>
                    </b-list-group>
                </template>
            </b-table>
            <b-list-group flush>
                <b-list-group-item class="gradient-background">
                    <span>Ganador: </span>
                    <span class="data winner">{{game.winner}}</span>
                </b-list-group-item>
            </b-list-group>
        </b-card>
    </b-container>
</template>
<script>
import Move from './Move'

export default {
  name: 'game',
  props: {
      game: Object, 
      key: Number,
      namePlayer1: String,
      namePlayer2: String
  },
  components: {
      Move
  },
  data(){
      return {
          scoreEvolutionTable: {
              fields: [
                  {key:'player_1', label:`Puntos ${this.namePlayer1}`}, 
                  {key:'player_2', label:`Puntos ${this.namePlayer2}`}
                ]
          }
      }
  }
}
</script>

<style>
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
    .game-table{
        font-size: x-large;
    }

</style>