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
            roleID: null,
            accessId: sessionStorage.getItem('access_id'),
            responseData_staff: [],
            roles: [],
            staffSkills: [],
            roleSkills: [],
            unmatchedSkills: [],
        };
    },
    computed: {
        percentageMatchingSkills() {
            const matchingSkills = this.roleSkills.filter(skill => this.staffSkills.includes(skill));
            const percentage = (matchingSkills.length / this.roleSkills.length) * 100;
            return Math.round(percentage);
        }
    },
    methods: {
        // the function that helps us call the endpoint and retrieve the data
        fetchRoles() {
            const apiUrl = 'http://127.0.0.1:5000/roles/get_all_by_staff/' + this.staffId;
            axios.get(apiUrl)
                .then(response => {
                    this.roles = response.data.data.roles;
                    const index = this.roles.findIndex(role => role.role_id == this.roleID);
                    this.roles = this.roles[index]
                    this.roleSkills = this.roles.skills_required
                    // console.log(this.roles.applied)
                    // console.log(this.roles[3])
                    // console.log(this.roles[index])

                })
                .catch(error => {
                    console.error('Error fetching roles:', error);
                });
            axios
                .get("http://127.0.0.1:5000/staff/" + this.staffId)
                .then(response => {
                    this.responseData_staff = response.data[0].data;
                    this.staffSkills = this.responseData_staff.staff_skills

                    // Calculate unmatchedSkills here after fetching data
                    this.unmatchedSkills = this.staffSkills.filter(
                        (skill) => !this.roleSkills.includes(skill)
                    );
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },

        // START TO APPLY ROLE FOR MODAL
        applyRole() {
            const commentsTextBox = document.getElementById('message-text').value;

            axios
                .post('http://127.0.0.1:5000/roles/apply', {
                    params: {
                        role_id: this.roleID,
                        staff_id: this.staffId,
                        comments: commentsTextBox,
                    },
                })
                .then(() => {
                    alert('You have successfully applied for the role!');
                    window.location.reload();
                    // this.$router.push({ path: this.$route.path })
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
    mounted() {
        this.roleID = this.$route.query.role_id;
        console.log(this.roleID);
        this.fetchRoles();
    },
    created() {
        console.log(this.staffId, this.accessId)
        if (!this.staffId && !this.accessId) {
            this.$router.push('/Login');
        }
    },
}
</script>

<template>
    <Nav />
    <div class="container container-style">
        <div class="container mb-3">
            <div class="row">
                <div class="col-1">
                    <!-- <img src="your-image.jpg" alt="Image" class="img-fluid"> -->
                    <img class="img-responsive rounded" src="../../../assets/profile.png" />
                </div>
                <div class="col-md-7 d-flex align-items-center text-center">
                    <h1>{{ roles.role_name }}</h1>
                </div>
                <div class="col-2 d-flex align-items-center text-center justify-content-center">

                    <div class="align-items-center ">
                        <p class="h6">{{ roles.no_of_pax }} staff needed</p>
                        <p v-if="roles.days_left == 0" :class="{ redTextCSS: roles.days_left < 5 }">Closing today</p>

                        <p v-else-if="roles.days_left == 1" :class="{ redTextCSS: roles.days_left < 5 }">Closing in {{ roles.days_left }} day</p>
                        <p v-else :class="{ redTextCSS: roles.days_left < 5 }">Closing in {{ roles.days_left }} days</p>
                    </div>
                </div>
                <div class="col-2 d-flex align-items-center justify-content-end">
                    <button v-if="!roles.applied" type="button" class="btn custom-button apply-button"
                        data-bs-toggle="modal" data-bs-target="#applyModal">Apply</button>

                    <button v-if="roles.applied" type="button" class="btn btn-secondary btn-apply custom-button"
                        data-bs-toggle="modal" data-bs-target="#applyModal" disabled>APPLIED</button>
                </div>
            </div>
        </div>

        <h5>Role Description</h5>

        <p>{{ roles.role_description }}</p>

        <p class="fw-bold"><span>Skill Match - </span>{{ percentageMatchingSkills }}%</p>
        <table class="table w-auto">
            <thead>
                <tr class="table-secondary">
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
                </tr>
            </tbody>
        </table>

        <!-- START OF MODAL -->
        <div class="modal fade" id="applyModal" tabindex="-1" aria-labelledby="applyModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">

                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="applyModalLabel">New Application for {{
                            roles.role_name }}</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <div class="mb-3">
                                <label for="message-text" class="col-form-label">Any Additional Remarks? (Optional)</label>
                                <textarea class="form-control" id="message-text"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" @click='applyRole()' class="btn btn-primary">Send
                            application</button>
                    </div>

                </div>
            </div>
        </div>
        <!-- END OF MODAL -->

    </div>
</template>

<style scoped>
img {
    width: 100%;
    object-fit: cover;
}

.container {
    background-color: white;
}
</style>