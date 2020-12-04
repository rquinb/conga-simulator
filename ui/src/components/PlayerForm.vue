<template>
    <b-form-group :label="FormTitle" >
        <b-input-group :prepend="`Jugador ${playerNum}`">
            <b-form-input  
                :class="playerNum == 1 ? 'simulator-form-element input-player input-player-1' : 'simulator-form-element input-player input-player-2'" 
                v-model="player.name" 
                trim
                @change="handleChange">
            </b-form-input>
        </b-input-group>
        <b-input-group prepend="Tipo de Agente">
            <b-form-select 
                v-model="player.agentType.selected" 
                :options="player.agentType.options"
                @change="handleChange">
            </b-form-select>
        </b-input-group>
        <b-input-group class="md-2" prepend="Rango de cartas aceptados" :append="`Min: ${player.acceptedCardsRange.minCard} | Max: ${player.acceptedCardsRange.maxCard}`">
            <b-form-input 
                v-model="player.acceptedCardsRange.minCard" 
                type="range" 
                min="1" 
                max="12" 
                step="1"
                @change="handleChange">
            </b-form-input>
            <b-form-input 
                v-model="player.acceptedCardsRange.maxCard" 
                type="range" 
                min="1" 
                max="12" 
                step="1"
                @change="handleChange">
            </b-form-input>
        </b-input-group>
        <b-input-group prepend="Maximo valor antes de cortar" :append="player.maxRestBeforeCutting">
            <b-form-input 
                v-model="player.maxRestBeforeCutting" 
                type="range" 
                min="0" 
                max="10" 
                step="1"
                @change="handleChange">
            </b-form-input>
        </b-input-group>
    </b-form-group>
</template>
<script>
export default {
    name: "player-form",
    props: {
        FormTitle: String,
        playerNum: Number
    },
    data(){
        return {
            player:{
                    number: parseInt(this.playerNum),
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
            }

        },
    methods: {
        handleChange(){
            this.$emit('updatePlayer', this.player);
        }
    }
}
</script>>
<style>
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
</style>