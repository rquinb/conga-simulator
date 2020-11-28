<template>
  <div id="main">
    <main-message introTitle="Bienvenidos a" appTitle="CONGA SIMULATOR"/>
    <b-button class="access-button" @click="toSimulator">Ingresar</b-button>
  </div>
</template>
<script>
import MainMessage from './MainMessage.vue'

export default {
  name: 'Main',
  components: {
    MainMessage
  },
  methods:{
    toSimulator(){
      this.$router.push('/simulator');
    }
  }
}
</script>

<style>
#main {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.access-button{
  margin-top: 1%;
}
</style>