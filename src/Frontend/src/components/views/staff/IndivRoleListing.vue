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
            responseData_staff: [],
            responseData: [],
            staffSkills: [],
            roleSkills: [],
            unmatchedSkills: [],
        };
    },
    computed: {
        getRoleID() {
            return this.$route.query.roleID
        },
        percentageMatchingSkills() {
            const matchingSkills = this.roleSkills.filter(skill => this.staffSkills.includes(skill));
            const percentage = (matchingSkills.length / this.roleSkills.length) * 100;
            return Math.round(percentage);
        }
    },
    methods: {
        fetchData() {
            const roleID = this.getRoleID
            this.roleID = roleID
            axios
                .get('http://127.0.0.1:5000/roles/' + roleID)
                .then(response => {
                    this.responseData = response.data.data;
                    this.roleSkills = this.responseData.skills_required
                    console.log(this.responseData)
                    console.log(this.roleID)

                })
                .catch(error => {
                    console.error('Error:', error);
                });

            axios
                .get("http://127.0.0.1:5000/staff/123458")
                .then(response => {
                    this.responseData_staff = response.data[0].data;
                    this.staffSkills = this.responseData_staff.staff_skills
                    console.log(this.responseData_staff)
                    console.log(this.staffSkills)
                    console.log(this.roleSkills)
                    // Calculate unmatchedSkills here after fetching data
                    this.unmatchedSkills = this.staffSkills.filter(
                        (skill) => !this.roleSkills.includes(skill)
                    );


                })
                .catch(error => {
                    console.error('Error:', error);
                });




            console.log(this.unmatchedSkills)

        },
        // START TO APPLY ROLE FOR MODAL

        applyRole() {
            const commentsTextBox = document.getElementById('message-text').value;

            axios
                .post('http://127.0.0.1:5000/roles/apply', {
                    params: {
                        role_id: this.roleID,
                        staff_id: 123457,
                        comments: commentsTextBox,
                    },
                })
                .then((response) => {
                    alert(response.data['data']);
                    window.location.reload();
                })
                .catch((error) => {
                    if (error.response.status == 500) {
                        alert('An error occured redeeming the reward');
                    } else {
                        alert(error.message);
                    }
                    window.location.reload();
                });
        },
        // END TO APPLY ROLE FOR MODAL
    },
    mounted: function () {
        this.fetchData();
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
                    <img class="img-responsive rounded" src="../../../assets/profile.jpeg" />
                </div>
                <div class="col-md-6 d-flex align-items-center text-center">
                    <h1>{{ responseData.role_name }}</h1>
                </div>
                <div class="col-3 align-items-center text-center">
                    <p class="h6">{{ responseData.no_of_pax }} staff needed</p>
                    <p style="margin: 0px;">Closing in {{ responseData.days_left }} days</p>
                </div>

                <div class="col-2 d-flex align-items-center justify-content-end">
                    <button type="button" class="btn btn-primary custom-button apply-button" data-bs-toggle="modal"
                        data-bs-target="#exampleModal">Apply</button>
                </div>
            </div>
        </div>

        <h5>Role Description</h5>

        <p>{{ responseData.role_description }}</p>

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



        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">

                <div class="modal-content">

                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">New Application</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div class="modal-body">
                        <form>
                            <div class="mb-3">
                                <label for="message-text" class="col-form-label">Any Comments?</label>
                                <textarea class="form-control" id="message-text"></textarea>
                            </div>
                        </form>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" @click='applyRole()' class="btn btn-primary">Send message</button>
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
    /* height: 70px; */
    object-fit: cover;
    /* border-radius: 90%; */
}

.container {
    background-color: white;

}
</style>