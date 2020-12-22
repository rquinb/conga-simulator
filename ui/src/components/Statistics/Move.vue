<template>
    <b-card class="gradient-background">
        <b-card-title>{{`Jugada ${parseInt(position) + 1}`}}</b-card-title>
            <b-card-body>
                <b-row>
                    <b-col>
                        <b-title class="section-title">Nombre</b-title>
                    </b-col>
                    <b-col>
                        <span class="data">{{move.player_name}}</span>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-title class="section-title">Carta levantada</b-title>
                    </b-col>
                    <b-col>
                        <span class="data">{{move.retrieved_card}}</span>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-title class="section-title">Carta jugada</b-title>
                    </b-col>
                    <b-col>
                        <span class="data">{{move.played_card}}</span>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-title class="section-title">Cartas en mano</b-title>
                    </b-col>
                    <b-col>
                        <b-badge class="card-in-hand" v-for="(card, index_cards) in move.hand" :key="index_cards">{{card}}</b-badge>
                    </b-col>
                </b-row>
            </b-card-body>
    </b-card>   
</template>
<script>
export default {
    props: {
        move: Object,
        position: Number
    }
}
</script>
<style>
    .card-in-hand{
        margin-right: 1%;
    }
</style>