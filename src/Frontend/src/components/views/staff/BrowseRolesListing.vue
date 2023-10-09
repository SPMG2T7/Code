<template>
    <div>
        <Nav/>
    </div>
    
    <div>

        <select v-model="skillSelected" @change="addFilter()" style="background-color:#E9C4DC">
            <option value="" disabled selected>Find Skill by Name</option>
            <option v-for="(skill,index) in allskills" :key="index" :value="skill">
                {{ skill }}
            </option>
        </select>

        <table v-if="filter_skills.length">
        <tr>
        <td v-for="(skill,index) in filter_skills" :key="index" :value="skill" style="padding:5px;background-color:#FDDEF2;border-left:5px solid white;border-right:5px solid white">
        {{skill}} <button @click="removeFilter(index)">x</button>
        </td>
        </tr></table>


        <!-- v-if here means the v-for below will only run if the length of roles.length is not 0 -->
        <ul class="role-list" v-if="roles.length && !filter_skills.length">
            
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
                        <div v-if="access_rights == 1 | access_rights == 3 | access_rights == 4" class="col-md-2 justify-content-center">
                            <a href=""><button type="button" class="btn btn-secondary custom-button">View Applicants</button></a>
                            <a href="/RoleEditing"><button type="button" class="btn btn-secondary custom-button" @click="setRoleId(role.role_id)">Edit Role</button></a>
                        </div>

                        <div v-else class="col-md-2 justify-content-center">
                            <button type="button" class="btn btn-secondary custom-button" onclick="apply()">Apply</button>
                            <p>Closing in {{ role.days_left }} days</p>
                        </div>

                    </div>
                </div>

            </li>
        </ul>

        <!-- If there are roles, there are filtered skills, and there are NO roles within the filtered skills -->
        <ul class="role-list" v-else-if="roles.length && filter_skills.length && !filtered_roles.length">

            <p>No roles available</p>

        </ul>

        <!-- If there are roles, there are filtered skills, and there are roles within the filtered skills -->
        <ul class="role-list" v-else-if="roles.length && filter_skills.length && filtered_roles.length">

            <li v-for="role in filtered_roles" :key="role.role_id">

                <div class="container-fluid rounded" style="width: 100%; margin: 30px 0px; border: 1px solid black">
                    <div class="row" style="margin: 20px 0px">
                    
                        <!-- column 1 -->
                        <div class="col-md-10">
                            <!-- <img src="https://via.placeholder.com/150" alt="role image" style="width: 100%; height: 100%"> -->
                            <h3>{{ role.role_name }}</h3>
                            <p>{{ role.no_of_pax }} staff needed</p>
                        </div>

                        <!-- column 2 -->
                        <div v-if="access_rights == 1 | access_rights == 3 | access_rights == 4" class="col-md-2 justify-content-center">
                            <a href=""><button type="button" class="btn btn-secondary custom-button">View Applicants</button></a>
                            <a href="/RoleEditing"><button type="button" class="btn btn-secondary custom-button" @click="setRoleId(role.role_id)">Edit Role</button></a>
                        </div>

                        <div v-else class="col-md-2 justify-content-center">
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
            isLoggedIn: false,
            filter_skills:[],
            allskills:[],
            newskills:[],
            skillSelected:'',
            filtered_roles: [],
            access_rights:'',
            roleId:''
        };
    },  
    // think of this as calling the function right when u load the page
    mounted() {
        this.fetchRoles();
        this.allskills=[];
        this.newskills=[];
        this.filter_skills=[];
        this.getSkills();
        this.skillSelected='';
        this.roleId='';
        this.filtered_roles=[];
        this.access_rights=sessionStorage.getItem('access_id');
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
        },

        addFilter() {

            const selectedSkill = this.skillSelected;
            this.filter_skills.push(selectedSkill);

            const index = this.allskills.indexOf(selectedSkill);
            this.allskills.splice(index, 1);

            this.filterSkills();
            

        },

        removeFilter(index){

            this.allskills.push(this.filter_skills[index]);
            this.filter_skills.splice(index,1);

            if (this.filter_skills.length) {
                this.filterSkills();

            }
            else {
                this.filtered_roles=[];
            }

        },
    
        getSkills() {
                axios
                    .get('http://127.0.0.1:5000/skills/get_all')

                    .then(response => {
                        this.responseData = response.data.data;
                        this.newskills=this.responseData.skills;
                        for (let i = 0; i < this.newskills.length; i++) {
                            this.allskills.push(this.newskills[i].skill_name);
                        }
                    })

                    .catch(error => {
                        console.error('Error:', error);
                    });
            },

        filterSkills() {
            const params = {
                "search_query": this.filter_skills
            };

            axios
                .post('http://127.0.0.1:5000/search/',{
                    "params": params
                })

                .then(response => {

                    const roles=response.data.data;
                    this.filtered_roles=roles;
                })

                .catch(error => {
                    console.error('Error:', error);
                })
        },

        setRoleId(role_id) {
            sessionStorage.setItem('role_id', role_id);
            console.log(sessionStorage.getItem('role_id'));
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