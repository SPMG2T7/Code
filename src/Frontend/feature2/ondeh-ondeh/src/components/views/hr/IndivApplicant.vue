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
            roleSkills: [],
            unmatchedSkills: [],
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
                    this.roleSkills = this.responseData_roleData.skills_required
                    this.currentRole = this.responseData_staffData.current_role
                    this.appliedRole = this.responseData_roleData.role_name


                    // Calculate unmatchedSkills here after fetching data
                    this.unmatchedSkills = this.staffSkills.filter(
                        (skill) => !this.roleSkills.includes(skill)
                    );

                    console.log(this.responseData_roleData)
                    console.log(this.responseData_staffData)
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
    },
    computed: {
        percentageMatchingSkills() {
            const matchingSkills = this.roleSkills.filter(skill => this.staffSkills.includes(skill));
            const percentage = (matchingSkills.length / this.roleSkills.length) * 100;
            return percentage; // Limit the percentage to two decimal places
        }
    },
    mounted: function () {
        this.fetchData();

        console.log(this.unmatchedSkills)
    }

}
</script>

<template>
    <Nav />

    <h2>{{ staffName }}</h2>
    <p><span class="fw-bold">Current Job Role:&emsp;</span>{{ currentRole }}</p>
    <p><span class='fw-bold'>Applied for Job Role:&emsp;</span>{{ appliedRole }}</p>
    <p><span class="fw-bold">Skill Match - </span>{{ percentageMatchingSkills }}%</p>
    <table class="table w-auto">
        <thead>
            <tr>
                <th scope="col" class="fw-bold">Skill Name</th>
                <th scope="col" class="fw-bold">Role Requirement</th>
                <th scope="col" class="fw-bold">My Skill</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="rSkills in roleSkills" :key="rSkills"
                :class="{ 'table-success': staffSkills.includes(rSkills), 'table-danger': !staffSkills.includes(rSkills) }">
                <td>{{ rSkills }}</td>
                <td>✓</td>
                <td v-if="staffSkills.includes(rSkills)">✓</td>
                <td v-else>✗</td>
                <!-- <td>Otto</td>
                <td>{{ skill }}</td> -->
            </tr>
        </tbody>
    </table>

    <p><span class="fw-bold">Other Skills: </span> {{ unmatchedSkills.join(', ') }}</p>



    <!-- <p>Staff Skills: </p>
    <ul>
        <li v-for="skill in staffSkills" :key="skill">{{ skill }}</li>
    </ul>

    <p>Role Skills: </p>
    <ul>
        <li v-for="rSkills in roleSkills" :key="rSkills">{{ rSkills }}</li>
    </ul> -->
</template>

<style scoped>
/* * {
    padding-left: 40px;
} */
</style>