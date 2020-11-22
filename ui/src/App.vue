<template>
  <div id="app">
    <main-message introTitle="Bienvenidos a" appTitle="CONGA SIMULATOR"/>
    <b-button class="access-button">Ingresar</b-button>
  </div>
</template>
<script>
import MainMessage from './components/MainMessage.vue'

export default {
  name: 'App',
  components: {
    MainMessage
  }
}
</script>

<style>
#app {
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
