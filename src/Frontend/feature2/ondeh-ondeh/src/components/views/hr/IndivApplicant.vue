<script>
import Nav from "../../views/NavBar.vue"
import axios from 'axios'

export default {
    name: "App",
    components: {
        Nav
    },
    data() {
        return {
            responseData: null,
            staffName: "",
            currentRole: "",
            staffSkills: []
        };
    },
    computed: {
        getID() {
            return this.$route.query.id
        }
    },
    methods: {
        fetchData() {
            const id = this.getID

            axios
                .get('http://127.0.0.1:5000/staff/' + id)
                .then(response => {
                    this.responseData = response.data.data;
                    this.staffName = this.responseData.first_name + " " + response.data.data.last_name;
                    this.staffSkills = this.responseData.staff_skills
                    console.log(this.staffName)
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
    },
    mounted: function () {
        this.fetchData();
    }

}
</script>

<template>
    <Nav />
    <h1>Individual Applicant</h1>
    <button @click="fetchData">Fetch Data</button>

    <h2>{{ staffName }}</h2>
    <p>Current Job Role: </p>
    <p>Applied for Job Role: </p>
    <p>Skills: </p>
    <ul>
        <li v-for="skill in staffSkills" :key="skill">{{ skill }}</li>
    </ul>
</template>

<style scoped>
* {
    padding-left: 40px;
}
</style>