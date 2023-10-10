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
            roleId: 2,
            responseData_staff: null,
            responseData_role: null, 
            staff_list: [],
        }
    },
    methods: {
        fetchData() {
            // const id = this.getID
            console.log(this.staffId);
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
                        const row = [this.staffName, this.staffSkills, this.department]
                        this.staff_list.push(row)
                    }

                    this.roleName = this.responseData_role.role_name

                    console.log(this.responseData_role)
                    console.log(this.staff_list)
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
            return percentage;
        }
    },
    mounted: function () {
        this.fetchData();

    },
    created() {
        console.log(this.staffId, this.accessId)

        if (!this.staffId && !this.accessId) {
            // Staff is not logged in, redirect to login page
            this.$router.push('/Login');
        }
    }
}

</script>

<template>
    <div>
        <Nav/>
        <h1>View All Applicants</h1>
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
</style>