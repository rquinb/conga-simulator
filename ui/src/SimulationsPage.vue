<template>
    <b-row>
        <b-col md="2">
            <b-button v-b-toggle.menu>
                <b-icon icon="menu-up" aria-hidden="true"></b-icon> Menu
            </b-button>
            <b-sidebar id="menu" title="Menu de simulaciones" bg-variant="dark" text-variant="light" shadow>
                <b-button-group vertical>
                    <b-button @click="displayFunctionality('simulationMaker')">Crear simulacion</b-button>
                    <b-button @click="displayFunctionality('simulationsTable')">Historial de Simulaciones</b-button>
                </b-button-group>
            </b-sidebar>
        </b-col>
        <b-col md="10">
            <template v-if='display.simulationMaker'>
                <simulator></simulator>
            </template>
            <template v-else-if="display.simulationsTable">
                <statistics-table @displayStatistics="handleDisplayStatistics"></statistics-table>
            </template>
            <template v-else-if="display.simulationsDetails">
                <row>
                    <b-col>
                        <b-button @click="displayFunctionality('simulationsTable')">Atras</b-button>
                    </b-col>
                </row>
                <statistics :statistics="statistics"></statistics>
            </template>
        </b-col>
    </b-row>
</template>
<script>
import Simulator from './components/Simulator.vue'
import StatisticsTable from './components/StatisticsTable.vue'
import Statistics from './components/Statistics/Statistics.vue'

export default {
    data(){
        return {
            statistics: {},
            display: {
                simulationMaker: true,
                simulationsTable: false,
                simulationsDetails: false
            }
        }
    },
    components: {
        Simulator,
        StatisticsTable,
        Statistics
    },
    methods:{
        displayFunctionality(functionalityName){
            let functionalities = Object.keys(this.display);
            for(let functionality of functionalities){
                this.display[functionality] = functionality == functionalityName ? true : false
            }
        },
        handleDisplayStatistics(item){
            this.statistics = item;
            this.displayFunctionality('simulationsDetails');
        }
    }
}
</script>>