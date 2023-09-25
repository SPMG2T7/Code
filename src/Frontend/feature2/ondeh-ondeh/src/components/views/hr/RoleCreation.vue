<script>
import Nav from "../../views/NavBar.vue"

export default {
    name: "App",
    components: {
        Nav
    }
}
</script>

<template>
    <div>
        <Nav />
        <h1>Hello this is role creation</h1>
        <router-link to="/browseroles">BrowseRoles</router-link>
        <RouterView></RouterView>
    </div>
</template>

<style scoped>
</style>