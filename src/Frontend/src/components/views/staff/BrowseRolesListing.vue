<template>
    <div>
        <Nav/>
    </div>
    
    <div>
        <!-- v-if here means the v-for below will only run if the length of roles.length is not 0 -->
        <ul class="role-list" v-if="roles.length">
            
            <!-- What this does is to create a <li> for each entry of role that it finds in the db
                e.g. if there are five entries in the DB, it will create this same <li> five times
                    think of it as template -->
            <li v-for="role in roles" :key="role.role_id">

                <div class="container-fluid rounded" style="width: 100%; margin: 30px 0px; border: 1px solid black">
                    <div class="row" style="margin: 20px 0px">
                    
                        <!-- column 1 -->
                        <div class="col-md-10">
                            <!-- <img src="https://via.placeholder.com/150" alt="role image" style="width: 100%; height: 100%"> -->
                            <h3>{{ role.role_name }}</h3>
                            <p>{{ role.no_of_pax }} staff needed</p>
                        </div>

                        <!-- column 2 -->
                        <div class="col-md-2 justify-content-center">
                            <button type="button" class="btn btn-secondary custom-button" onclick="apply()">Apply</button>
                            <p>Closing in {{ role.days_left }} days</p>
                        </div>

                    </div>
                </div>

            </li>
        </ul>
        <!-- if the number of entries is 0, v-else will run -->
        <p v-else>No roles available</p>
    </div>

</template>
  
<script>
import Nav from "../../views/NavBar.vue"
import axios from 'axios'

export default {
    name: "App",
    components: {
        Nav
    },
    // we will initialise an empty list here first so we can append the axios return later
    data() {
        return {
            roles: [],
            isLoggedIn: false
        };
    },  
    // think of this as calling the function right when u load the page
    mounted() {
        this.fetchRoles();
    },
    methods: {
        // the function that helps us call the endpoint and retrieve the data
        fetchRoles() {
            const apiUrl = 'http://127.0.0.1:5000/roles/get_all';
            axios.get(apiUrl)
                .then(response => {
                    this.roles = response.data.data.roles;
                })
                .catch(error => {
                    console.error('Error fetching roles:', error);
                });
        }
    },
    created() {
        const staffId = sessionStorage.getItem('staff_id');
        const accessId = sessionStorage.getItem('access_id');

        console.log(staffId, accessId)
        
        if (!staffId && !accessId) {
            // Staff is not logged in, redirect to login page
            this.$router.push('/Login');
        }
    }
};
</script>
  
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

p {
    padding: 0; /* Remove default padding */
    margin: 0; /* Remove default margin */
}

h3 {
    font-size: 20px;
    font-weight: bold;
}

.role-list {
    list-style: none; /* Remove bullet points */
    padding: 0; /* Remove default padding */
    margin: 0; /* Remove default margin */
}

.custom-button {
    width: 140px;
    background-color: #8BC100;
    color: #000000;
  }

</style>