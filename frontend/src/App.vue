<template>
  <div id="app">
    <Menu />
    <router-view/>
  </div>
</template>

<script>
import Menu from './components/menubar.vue'
export default {
    components: {
      Menu
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Archivo&display=swap');
#app {
  font-family: 'Archivo', sans-serif;
  text-align: center;
  color: #6998a3;
  margin: -7px;
}

</style>
