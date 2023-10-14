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
            staffId: sessionStorage.getItem('staff_id'),
            accessId: sessionStorage.getItem('access_id'),
            roleId: null,
            responseData_staff: null,
            responseData_role: null, 
            roleName: "",
            staff_list: [],
        }
    },
    methods: {
        fetchData() {
            // const id = this.getID
            const url = 'http://127.0.0.1:5000/role_application/get_all/' + this.roleId
            axios
                .get(url)
                .then(response => {
                    this.responseData_appData = response.data.data.application_data;
                    this.responseData_role = response.data.data.role_data;
                    this.responseData_staff = response.data.data.staff_data;
                    this.roleSkills = this.responseData_role.skills_required
                    
                    for (let i=0; i < this.responseData_staff.length; i++){
                        this.staffName = this.responseData_staff[i].first_name + " " + this.responseData_staff[i].last_name;
                        this.staffSkills = this.responseData_staff[i].staff_skills
                        this.department = this.responseData_staff[i].department
                        const row = [this.staffName, this.staffSkills, this.department, this.responseData_staff[i].staff_id]
                        this.staff_list.push(row)
                    }

                    this.roleName = this.responseData_role.role_name

                    // console.log(this.responseData_role)
                    // console.log(this.staff_list)
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
        
        redirectToIndivApplicant(roleId, staffId) {
            sessionStorage.setItem('role_id', roleId)
            sessionStorage.setItem('staff_id', staffId)
            this.$router.push('IndivApplicant')

        },

        redirectToEdit() {
            this.$router.push('RoleEditing')
        },
    },
    computed: {
        percentageMatchingSkills() {
            const matchingSkills = this.roleSkills.filter(skill => this.staffSkills.includes(skill));
            const percentage = (matchingSkills.length / this.roleSkills.length) * 100;
            return percentage;
        },

    },
    mounted: function () {
        this.roleId = this.$route.params.role_id;
        this.fetchData();

    },
    created() {
        // console.log(this.staffId, this.accessId)

        if (!this.staffId && !this.accessId) {
            // Staff is not logged in, redirect to login page
            this.$router.push('/Login');
        }
    }
}

</script>

<template>
    <div>
        <Nav />

        <div class="container">
            
            <div class="title section">
                <div class="row">
                    <div class="col-md-9">
                        <h1>{{ roleName }}</h1>
                    </div>
                    <div class="col-md-3 text-end">
                        <button @click="redirectToEdit()" type="button" class="btn btn-success btn-apply custom-button">EDIT ROLE</button>
                    </div>
                </div>
            </div>
                    
            <div class="applicants section">
                <div class="row">
                    <h4>Applicant Overview</h4>
                    <table class="table-responsive">
                        <thead>
                            <tr>
                                <th>Applicant</th>
                                <th>Applicant Name</th>
                                <th>Skill Match</th>
                                <th>Current Department</th>
                                <th>See More</th>
                            </tr>
                        </thead>

                        <tr v-for="(staff, indx) in this.staff_list" :value=staff[1] :key=staff[0]>
                            <td>{{ indx+1 }}</td>
                            <td>{{ staff[0] }}</td>
                            <td>{{ percentageMatchingSkills }}% </td>
                            <td>{{ staff[2] }}</td>
                            <td><a class="btn" @click="redirectToIndivApplicant(this.roleId,staff[3])" role="button">
                                <i class="fa-solid fa-caret-right"></i>
                            </a></td>
                        </tr>
                    </table>
                </div>
            </div>

            <router-link to="/">Browse All Roles</router-link>
            
        </div>
    </div>
</template>


<style scoped>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #000000;
    background-color: #EBEBEB;
    margin-top: 60px;
}

h4 {
    font-weight: bold;
    font-size: 18px;
    background-color: transparent;
}

.section {
    margin: 20px 0px;
}

.custom-button {
    width: 130px;
    color: #000000;
    font-weight: bold;
}

tr {
    border: 1px lightgray solid;
}

thead, th {
    background-color: lightgray;
    padding: 10px;
}

td {
    padding: 10px;
}

@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css');

</style>