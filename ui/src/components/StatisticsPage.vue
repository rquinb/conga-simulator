<template>
    <div>
        <template v-if="displayStatistics">
            <statistics :statistics="statistics"></statistics>
        </template>
    </div>
</template>
<script>
import axios from 'axios';
import Statistics from './Statistics/Statistics.vue'
export default {
    title: 'Conga Simulator',
    data(){
        return {
            displayStatistics: false,
            simulationId: this.$route.params.simulationId,
            statistics: {},
        }
    },
    components:{
        Statistics
    },
    methods:{
        getSimulation(){
            this.displayStatistics = false;
            axios.get(`${process.env.VUE_APP_API_URL}/games-simulations/${this.simulationId}`).then((response) => {
                this.statistics = response.data.details;
                this.displayStatistics = true;

            }).catch((response) => {
                console.log(response);
                this.displayStatistics = false;
            });
        }
    },
    created() {
        this.getSimulation()
    },
}
</script>