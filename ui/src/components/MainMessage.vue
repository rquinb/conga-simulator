<template>
  <div >
      <b-row class="message-row">
          {{introTitle}}
      </b-row>
      <b-row class="message-row">
        <b-card >
          <h1 class="app-title">
           {{appTitle}}
          </h1>
        </b-card>
      </b-row>
  </div>
</template>
<script>
export default {
  name: 'main-message',
  props: {
    introTitle: String,
    appTitle: String
  }
}
</script>
<style scoped>
  .message-row{
    text-align: center;
    display: block ruby;
  }
  .app-title{
    font-weight: bold;
    font-style: italic;
  }
</style>
