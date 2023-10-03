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
            roleID: 0,
            count_applicant: 0,
            days_left: 0,
            department: "",
            expiry_date: "",
            listed_by: "",
            location: "",
            no_of_pax: 0,
            role_description: "",
            role_name: "",
            skills_required: [],
        };
    },
    computed: {
        getRoleID() {
            return this.$route.query.roleID
        }
    },
    methods: {
        fetchData() {
            const roleID = this.getRoleID
            this.roleID = roleID
            axios
                // .get('http://127.0.0.1:5000/roles/00004')
                .get('http://127.0.0.1:5000/roles/' + roleID)
                .then(response => {
                    this.responseData = response.data.data;
                    this.count_applicant = this.responseData.count_applicant;
                    this.days_left = this.responseData.days_left;
                    this.department = this.responseData.department;
                    this.expiry_date = this.responseData.expiry_date;
                    this.listed_by = this.responseData.listed_by;
                    this.location = this.responseData.location;
                    this.no_of_pax = this.responseData.no_of_pax;
                    this.role_description = this.responseData.role_description;
                    this.role_name = this.responseData.role_name;
                    this.skills_required = this.responseData.skills_required;
                    console.log(this.responseData)
                    console.log(this.roleID)

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
        const staffId = sessionStorage.getItem('staff_id');
        const accessId = sessionStorage.getItem('access_id');

        console.log(staffId, accessId)
        
        if (!staffId && !accessId) {
            // Staff is not logged in, redirect to login page
            this.$router.push('/Login');
        }
    }

}
</script>

<template>
    <Nav />
    <div class="container m-2 mt-4">
        <div class="container mb-3">
            <div class="row">
                <div class="col-1">
                    <!-- <img src="your-image.jpg" alt="Image" class="img-fluid"> -->
                    <img class="img-responsive rounded" src="../../../assets/profile.jpeg" />
                </div>
                <div class="col-11 d-flex align-items-center text-center">
                    <h1>{{ role_name }}</h1>
                </div>
            </div>
        </div>

        <h3>Role Description</h3>

        {{ role_description }}


        <!-- START OF MODAL -->

        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Apply</button>

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
</style>