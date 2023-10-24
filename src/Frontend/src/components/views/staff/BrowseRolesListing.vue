<template>
    <div>
        <Nav />
    </div>

    <div>

        <!-- Search & Filter -->

        <div class="container container-style">
            <div class="row">
                <div class="col-md-4 text-left">
                    <input type="text" class="form-control search-box" v-model="searchBar"
                        placeholder="Search for Roles, Description, Skills" v-on:keyup.enter="filterSkills">

                </div>
                <div class="col-md-4 text-left">
                    <button class="btn btn-apply apply-button custom-button" @click="filterSkills"
                        style="border-radius: 10px">Search</button>
                </div>

                <div class="col-md-4 text-end">

                    <select v-model="skillSelected" @change="addFilter" class="form-select search-box">
                        <option value="" disabled selected>Find Skill by Name</option>
                        <option v-for="(skill, index) in allskills" :key="index" :value="skill">{{ skill }}</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Listings Display -->

        <div class="container">

            <!-- Filtered Skills Display (if there are filtered skills) -->

            <div class="row ms-1" v-if="filter_skills.length">
                <div class="col-md-3 skills-filter" v-for="(skill, index) in filter_skills" :key="index" :value="skill">
                    <span>{{ skill }}</span>
                    <button type="button" @click="removeFilter(index)" class="btn-close btn-sm btn-danger"></button>
                </div>
            </div>

            <!-- Roles Display -->

            <ul class="role-list" v-if="roles.length">

                <li v-for="role in sortedRoles" :key="role.role_id">

                    <div class="container-fluid listing">
                        <div class="row justify-content-between" style="margin: 20px 0px">

                            <!-- Display Role listing details (left) -->

                            <div class="col-8 col-md-6">
                                <h3 v-if="access_rights == 2"><router-link class="viewApplicant-btn"
                                        :to="{ name: 'Individual Role Listing', query: { role_id: role.role_id } }">{{
                                            role.role_name }} </router-link></h3>
                                <h3 v-else><router-link class="viewApplicant-btn"
                                        :to="{ name: 'Role Editing', query: { role_id: role.role_id } }">{{ role.role_name
                                        }} </router-link></h3>

                                <p>{{ role.no_of_pax }} staff needed</p>

                            </div>


                            <!-- Role Listing buttons -->

                            <!-- check whats the purpose of justify content center here  -->
                            <div v-if="access_rights == 2" class="col-4 text-end justify-content-center">

                                <button @click="populateModal(role.role_id, role.role_name)"
                                    class="btn btn-apply custom-button apply-button" data-bs-toggle="modal"
                                    data-bs-target="#applyModal" v-if="!role.applied">APPLY</button>
                                <button disabled class="btn btn-secondary btn-apply custom-button" v-else>APPLIED</button>

                                <p v-if="role.days_left == 0" :class="{ redTextCSS: role.days_left < 5 }">Closing today</p>

                                <p v-else :class="{ redTextCSS: role.days_left < 5 }">Closing in {{ role.days_left }} days
                                </p>
                            </div>

                            <div v-else class="col-4 col-md-4 text-end justify-content-center">

                                <router-link class="viewApplicant-btn"
                                    :to="{ name: 'View All Applicants', query: { role_id: role.role_id } }">
                                    <button type="button" class="btn viewbutton buttonspacing"> View Applicants </button>
                                </router-link>

                                <router-link style="text-decoration: none; color:black"
                                    :to="{ name: 'Role Editing', query: { role_id: role.role_id } }">
                                    <button type="button" class="btn btn-apply custom-button apply-button buttonspacing">
                                        Edit Role </button>
                                </router-link>

                                <p v-if="role.days_left < 0" class="redTextCSS">Entry Closed</p>
                                <p v-else-if="role.days_left == 0" :class="{ redTextCSS: role.days_left < 5 }">Closing today
                                </p>
                                <p v-else :class="{ redTextCSS: role.days_left < 5 }">Closing in {{ role.days_left }} days
                                </p>
                            </div>
                        </div>

                    </div>

                </li>
            </ul>

            <!-- If there are no roles -->
            <p v-else class="noroles">No roles available</p>


            <!-- START OF MODAL -->
            <div class="modal fade" id="applyModal" tabindex="-1" aria-labelledby="applyModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">

                    <div class="modal-content">

                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="applyModalLabel">Apply for {{
                                selected_role_name }}</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>

                        <div class="modal-body">
                            <form>
                                <div class="mb-3">
                                    <label for="message-text" class="col-form-label">Any Additional Remarks?
                                        (Optional)</label>
                                    <textarea class="form-control" id="message-text"></textarea>
                                </div>
                            </form>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" @click='applyRole(selected_role_id)' class="btn btn-primary">Send
                                application</button>
                        </div>

                    </div>
                </div>
            </div>
            <!-- END OF MODAL -->

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
            filter_skills: [],
            allskills: [],
            newskills: [],
            skillSelected: '',
            access_rights: '',
            roleId: '',
            applied: [],
            notApplied: [],
            staffId: sessionStorage.getItem('staff_id'),
            accessId: sessionStorage.getItem('access_id'),
            searchBar: '',
            search_query_values: [],

            // for the modal selection
            selected_role_id: null,
            selected_role_name: null,
        };
    },
    // think of this as calling the function right when u load the page
    mounted() {
        this.fetchRoles();
        this.allskills = [];
        this.newskills = [];
        this.filter_skills = [];
        this.getSkills();
        this.skillSelected = '';
        this.roleId = '';
        this.access_rights = sessionStorage.getItem('access_id');
        this.searchBar = '';
        this.search_query_values = [];
    },

    methods: {

        // function to help with modal rendering 
        populateModal(role_id, role_name) {

            this.selected_role_id = role_id;
            this.selected_role_name = role_name;

        },

        // the function that helps us call the endpoint and retrieve the data
        fetchRoles() {
            const apiUrl = 'http://127.0.0.1:5000/roles/get_all_by_staff/' + this.staffId;
            axios.get(apiUrl)
                .then(response => {

                    // Check if the response is empty array
                    if (response.data.data.roles.length == 0) {
                        this.roles = [];
                    }

                    // response is not empty
                    else {
                        this.roles = response.data.data.roles;
                    }

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

        removeFilter(index) {

            // push the removed filtered skill into the allskills array
            this.allskills.push(this.filter_skills[index]);
            this.allskills.sort();

            // remove the removed filtered skill from the filter_skills array
            this.filter_skills.splice(index, 1);

            // perform filtering of the results
            this.filterSkills();

        },

        filterSkills() {
            this.search_query_values = Array.from(this.filter_skills)
            if (this.searchBar != '') {
                this.search_query_values.push(this.searchBar);
            }
            console.log(this.search_query_values);

            const params = {
                "search_query": this.search_query_values
            };

            if (this.search_query_values.length) {

                axios
                    .post('http://127.0.0.1:5000/search/', {
                        "params": params
                    })
                    .then(response => {
                        const roles = response.data.data;
                        this.roles = roles;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    })

            }

            else {
                this.fetchRoles();
            }
        },

        getSkills() {
            axios
                .get('http://127.0.0.1:5000/skills/get_all')

                .then(response => {
                    this.responseData = response.data.data;
                    this.newskills = this.responseData.skills;
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

            const commentsTextBox = document.getElementById('message-text').value;


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

        },
        // END TO APPLY ROLE FOR MODAL

    },

    created() {
        if (!this.staffId && !this.accessId) {
            this.$router.push('/Login');
        }
    },
    computed: {
        // this is to sort the roles by applied and not applied
        sortedRoles() {
            let filteredRoles = this.roles
                .slice()
                .sort((a, b) => {
                    if (a.applied === false && b.applied === true) return -1;
                    if (a.applied === true && b.applied === false) return 1;
                    return 0;
                });

            // this is to filter out the roles that have closed based on ACCESS RIGHTS
            if (this.access_rights == 2) {
                filteredRoles = this.roles.filter(role => role.days_left >= 0)
            }
            return filteredRoles
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

.listing {
    width: 100%;
    margin: 30px 0px;
    border: 1px solid #EBEBEB;
    border-radius: 20px;
    background-color: white;
    box-shadow: 0 2px 22px 0 rgba(0, 0, 0, 0.2);
}

.noroles {
    margin: 10px;
    text-align: center;
    font-weight: bold;
    font-size: 20px
}

.buttonspacing {
    margin: 10px 0px 5px 5px
}

.viewbutton {
    background-color: #946383;
    color: #000000;
    font-weight: bold;
}

.search-box {
    background-color: #E9C4DC;
}

.skills-filter {
    background-color: #FDDEF2;
    padding: 5px;
    border-radius: 10px;
    margin-right: 10px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;

}

.redTextCSS {
    color: red;
}

.viewApplicant-btn {
    text-decoration: none;
    color: black
}</style>
