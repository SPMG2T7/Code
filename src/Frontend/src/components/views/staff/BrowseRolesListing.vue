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
            staffId: sessionStorage.getItem('staff_id'),
            accessId: sessionStorage.getItem('access_id'),
        };
    },
    // think of this as calling the function right when u load the page
    mounted() {
        this.fetchRoles();
    },
    methods: {
        // the function that helps us call the endpoint and retrieve the data
        fetchRoles() {
            const apiUrl = 'http://127.0.0.1:5000/roles/get_all_by_staff/' + this.staffId;
            axios.get(apiUrl)
                .then(response => {
                    this.roles = response.data.data.roles;

                    console.log(response.data.data);
                    console.log(this.roles)
                })
                .catch(error => {
                    console.error('Error fetching roles:', error);
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
    },
    created() {
        console.log(this.staffId, this.accessId)

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

<template>
    <div>
        <Nav />
    </div>

    <div class="container">
        <!-- v-if here means the v-for below will only run if the length of roles.length is not 0 -->
        <ul class="role-list" v-if="roles.length">

            <!-- What this does is to create a <li> for each entry of role that it finds in the db
                e.g. if there are five entries in the DB, it will create this same <li> five times
                    think of it as template -->
            <li v-for="role in sortedRoles" :key="role.role_id">

                <div class="container-fluid listing">
                    <div class="row justify-content-between" style="margin: 20px 0px">

                        <!-- column 1 -->
                        <div class="col-md-9">
                            <!-- <img src="https://via.placeholder.com/150" alt="role image" style="width: 100%; height: 100%"> -->
                            <h3>{{ role.role_name }}</h3>
                            <p>{{ role.no_of_pax }} staff needed</p>
                        </div>

                        <!-- column 2 -->
                        <div class="col-md-3 text-end">
                            <button type="button" class="btn btn-success btn-apply custom-button apply-button"
                                v-if="!role.applied" data-bs-toggle="modal"
                                :data-bs-target="'#exampleModal-' + role.role_id">APPLY</button>

                            <button type="button" class="btn btn-secondary btn-apply custom-button" v-if="role.applied"
                                data-bs-toggle="modal" :data-bs-target="'#exampleModal-' + role.role_id"
                                disabled>APPLIED</button>

                            <p>Closing in {{ role.days_left }} days</p>
                        </div>

                    </div>

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
        <!-- if the number of entries is 0, v-else will run -->
        <p v-else>No roles available</p>



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
    width: 130px;
    color: #000000;
    font-weight: bold;
}

.apply-button {
    background-color: #8BC100;
}

.listing {
    width: 100%;
    margin: 30px 0px;
    border: 1px solid #EBEBEB;
    border-radius: 20px;
    background-color: white;
    box-shadow: 0 2px 22px 0 rgba(0, 0, 0, 0.2);
}
</style>