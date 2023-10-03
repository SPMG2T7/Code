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
            staffSkills: [],
            appliedRole: ""
        };
    },
    // computed: {
    //     getID() {
    //         return this.$route.query.id
    //     }
    // },
    methods: {
        fetchData() {
            // const id = this.getID

            axios
                .get('http://127.0.0.1:5000/application/2_123456')
                .then(response => {
                    this.responseData_roleData = response.data.data.role_data;
                    this.responseData_staffData = response.data.data.staff_data;
                    this.staffName = this.responseData_staffData.first_name + " " + this.responseData_staffData.last_name;
                    this.staffSkills = this.responseData_staffData.staff_skills
                    this.currentRole = this.responseData_staffData.current_role
                    this.appliedRole = this.responseData_roleData.role_name
                    console.log(this.responseData_roleData)
                    console.log(this.responseData_staffData)
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
    <h2>{{ staffName }}</h2>
    <p>Current Job Role: {{ currentRole }}</p>
    <p>Applied for Job Role: {{  appliedRole }}</p>
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