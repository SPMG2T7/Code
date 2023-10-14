<template>
    <div>
        <Nav />
    </div>
    
    <div>

        <!-- Search & Filter -->

        <table class="center" style="margin-top:20px;margin-bottom:20px;margin-left:auto;margin-right:auto;">
            <tr>
                <td style="border-left:5px solid #EBEBEB;border-right:0px solid #EBEBEB;">
                    <input type="text" v-model="searchBar" placeholder="Search" style="background-color:#E9C4DC;border-radius:10px;padding:2px 10px" v-on:keyup.enter="filterSkills()">
                </td>
                <td style="border-left:0px solid #EBEBEB;border-right:20px solid #EBEBEB;">
                    <button @click="filterSkills()" style="border-radius: 10px">Search</button>
                </td>
                <td style="border-left:0px solid #EBEBEB;border-right:5px solid #EBEBEB;">
                    <select v-model="skillSelected" @change="addFilter()" style="background-color:#E9C4DC;padding:5px 10px;border-radius:10px">
                        <option value="" disabled selected>Find Skill by Name</option>
                        <option v-for="(skill,index) in allskills" :key="index" :value="skill">
                            {{ skill }}
                        </option>
                    </select>
                </td>
            </tr>
        </table>

        <!-- Filtered Skills Display (if there are filtered skills) -->

        <table v-if="filter_skills.length" style="margin:5px auto">
            <tr>
                <td v-for="(skill,index) in filter_skills" :key="index" :value="skill" style="padding:5px;background-color:#FDDEF2;border-left:5px solid #EBEBEB;border-right:5px solid #EBEBEB; border-radius:10px">
                {{skill}} <button @click="removeFilter(index)">x</button>
            </td>
            </tr>
        </table>

        <!-- Listings Display -->

        <div class="container">

        <!-- Roles Display -->

            <!-- If there are roles, and no search or filter applied -->

            <ul class="role-list" v-if="roles.length">

                <li v-for="role in sortedRoles" :key="role.role_id">

                    <!-- PLS IGNORE THIS AND DONT DELETE!!! trying to fix an issue w the button display...
                        <div>

                        <table style="width:100%;border:1px solid black">
                            <tr style="width:100%">
                                <td class="ms-0 me-2"> 
                                    <h3>{{ role.role_name }}</h3>
                                    <p>{{ role.no_of_pax }} staff needed</p>
                                </td>
                                <td class="ms-2 me-0 my-2" style="float:right">
                                    <div v-if="access_rights == 2">
                                        <a href=""><button>View Applicants</button></a>
                                        <a href="/RoleEditing"><button @click="setRoleId(role.role_id)">Edit Role</button></a>
                                    </div>
                                </td>
                            </tr>
                        </table>
                        
                    </div> -->

                    <div class="container-fluid listing">
                        <div class="row justify-content-between" style="margin: 20px 0px">

                            <!-- Display Role listing details (left) -->

                            <div class="col-9">
                                <h3 v-if="access_rights == 2" @click="redirectToIndivRoleListing(role.role_id)">{{ role.role_name }}</h3>
                                <h3 v-else @click="redirecttoEdit(role.role_id)">{{ role.role_name }}</h3>
                                <p>{{ role.no_of_pax }} staff needed</p>
                                
                            </div>


                            <!-- Role Listing buttons -->

                            <!-- check whats the purpose of justify content center here  -->
                            <div v-if="access_rights == 2" class="col-3 text-end justify-content-center">
                                <button type="button" class="btn btn-apply custom-button apply-button" v-if="!role.applied" data-bs-toggle="modal"
                                    :data-bs-target="'#exampleModal-' + role.role_id">APPLY</button>

                                <button type="button" class="btn btn-secondary btn-apply custom-button" v-else
                                    data-bs-toggle="modal" :data-bs-target="'#exampleModal-' + role.role_id"
                                    disabled>APPLIED</button>

                                <p>Closing in {{ role.days_left }} days</p>
                            </div>

                            <!-- check what is vstack class  -->
                            <div v-else class="col-3 float-right vstack">
                                <button @click='redirectToViewAllApplicants(role.role_id)' type="button" class="btn viewbutton custom-button buttonspacing">View Applicants</button>
                                <button @click='redirectToRoleEdit(role.role_id)' type="button" class="btn btn-apply custom-button apply-button buttonspacing">Edit Role</button>
                            </div>


                        </div>

                        <!-- look to change modal implementation subsequently   -->
                        <!-- START OF MODAL -->
                        <div class="modal fade" :id="'exampleModal-' + role.role_id" tabindex="-1"
                            aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered">

                                <div class="modal-content">

                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="exampleModalLabel">New Application for {{
                                            role.role_name }}</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>

                                    <div class="modal-body">
                                        <form>
                                            <div class="mb-3">
                                                <label for="message-text" class="col-form-label">Any Comments?</label>
                                                <textarea class="form-control" :id="'message-text-' + role.role_id"></textarea>
                                            </div>
                                        </form>
                                    </div>

                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button type="button" @click='applyRole(role.role_id)' class="btn btn-primary">Send
                                            application</button>
                                    </div>

                                </div>
                            </div>
                        </div>
                        <!-- END OF MODAL -->
                        
                    </div>
                
                </li>
            </ul>

            <!-- If there are no roles -->
            <p v-else class="noroles">No roles available</p>

    </div>

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
            access_rights:'',
            roleId:'',
            applied: [],
            notApplied: [],
            staffId: sessionStorage.getItem('staff_id'),
            accessId: sessionStorage.getItem('access_id'),
            searchBar: '',
            search_query_values:[]
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
        this.access_rights=sessionStorage.getItem('access_id');
        this.searchBar='';
        this.search_query_values=[];
    },

    methods: {
        // the function that helps us call the endpoint and retrieve the data
        fetchRoles() {
            const apiUrl = 'http://127.0.0.1:5000/roles/get_all_by_staff/' + this.staffId;
            axios.get(apiUrl)
                .then(response => {
                    this.roles = response.data.data.roles;

                })
                .catch(error => {
                    console.error('Error fetching roles:', error);
                });
        },

        addFilter() {

            // push the new filtered skill into the filter_skills array
            const selectedSkill = this.skillSelected;
            this.filter_skills.push(selectedSkill);

            // remove the filtered skill from the allskills array
            const index = this.allskills.indexOf(selectedSkill);
            this.allskills.splice(index, 1);

            // perform filtering of the results
            this.filterSkills();
            
        },

        removeFilter(index){

            // push the removed filtered skill into the allskills array
            this.allskills.push(this.filter_skills[index]);

            // remove the removed filtered skill from the filter_skills array
            this.filter_skills.splice(index,1);

            // perform filtering of the results
            this.filterSkills();

        },

        filterSkills() {

            this.search_query_values = Array.from(this.filter_skills)
            this.search_query_values.push(this.searchBar);
            console.log(this.search_query_values);

            const params = {
                "search_query": this.search_query_values
            };

            axios
                .post('http://127.0.0.1:5000/search/',{
                    "params": params
                })

                .then(response => {

                    const roles=response.data.data;
                    console.log(roles)
                    this.roles=roles;
                })

                .catch(error => {
                    console.error('Error:', error);
                })
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


        // START TO APPLY ROLE FOR MODAL

        applyRole(roleID) {
            const commentsTextBox = document.getElementById('message-text-' + roleID).value;

            if (commentsTextBox.length == 0) {
                alert("Please enter a comment")
            }
            else {
                axios
                    .post('http://127.0.0.1:5000/roles/apply', {
                        params: {
                            role_id: roleID,
                            staff_id: this.staffId,
                            comments: commentsTextBox,
                        },
                    })
                    .then(() => {
                        alert('You have successfully applied for the role!');
                        window.location.reload();
                    })
                    .catch((error) => {
                        if (error.response.status == 500) {
                            alert(error.message);
                        } else {
                            alert('An error occured');
                        }
                    });
            }
        },
        // END TO APPLY ROLE FOR MODAL

        redirectToIndivRoleListing(roleId) {
            sessionStorage.setItem('role_id', roleId)
            this.$router.push('IndivRoleListing')
        },

        redirecttoEdit(roleId) {
            sessionStorage.setItem('role_id', roleId)
            this.$router.push('RoleEditing')
        },

        redirectToViewAllApplicants(roleId) {
            sessionStorage.setItem('role_id', roleId)
            this.$router.push('ViewAllApplicants')
        },

        redirectToRoleEdit(roleId) {
            sessionStorage.setItem('role_id', roleId)
            this.$router.push('RoleEditing')
        }

    },

    created() {
        // console.log(this.staffId, this.accessId)

        if (!this.staffId && !this.accessId) {
            this.$router.push('/Login');
        }
    },
    computed: {

        // this is to sort the roles by applied and not applied
        sortedRoles() {
            return this.roles.slice().sort((a, b) => {
                if (a.applied === false && b.applied === true) return -1;
                if (a.applied === true && b.applied === false) return 1;
                return 0;
            });
        },
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
    padding: 0;
    /* Remove default padding */
    margin: 0;
    /* Remove default margin */
}

h3 {
    font-size: 20px;
    font-weight: bold;
}

.role-list {
    list-style: none;
    /* Remove bullet points */
    padding: 0;
    /* Remove default padding */
    margin: 0;
    /* Remove default margin */
}

.custom-button {
    color: #000000;
    font-weight: bold;
}

.apply-button {
    background-color: #8BC100;
    width:130px;
}

.listing {
    width: 100%;
    margin: 30px 0px;
    border: 1px solid #EBEBEB;
    border-radius: 20px;
    background-color: white;
    box-shadow: 0 2px 22px 0 rgba(0, 0, 0, 0.2);
}

.noroles {
    margin:10px;
    text-align:center;
    font-weight:bold;
    font-size: 20px
}

.buttonspacing {
    margin: 5px 5px
}

.viewbutton {
    background-color: #946383;
}
</style>
