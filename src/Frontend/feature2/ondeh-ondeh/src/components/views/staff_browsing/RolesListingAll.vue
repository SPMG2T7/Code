<template>
    <h1>HELLO</h1>
    <router-link to="/">Home</router-link>
    <RouterView></RouterView>>
</template>
  
<script>
// import HelloWorld from "../../HelloWorld.vue"

export default {
    name: 'App',
    components: {
        // HelloWorld
    }
}
</script>
  
<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #af8ece;
    margin-top: 60px;
}
</style>
  