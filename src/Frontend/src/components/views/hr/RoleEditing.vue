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
            skills: [],
            allskills: [],
            skillSelected: '',
            responseData: '',
            newskills: [],
            roleName: '',
            roleDescription: '',
            staffNeededNumber: '',
            closingDate: '',
            roleLocation: '',
            roleDepartment: '',
            role_id: null,
            truthy: ''
        };
    },
    computed: {

    },
    methods: {
        convertDateFormat() {
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            const parts = this.closingDate.split('-');
            const year = parseInt(parts[0], 10);
            const month = months[parseInt(parts[1], 10) - 1];
            const day = parseInt(parts[2], 10);

            const dateObj = new Date(this.closingDate);
            const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            const dayOfWeek = daysOfWeek[dateObj.getDay()];

            const formattedDate = `${dayOfWeek} ${month} ${day.toString().padStart(2, '0')} ${year} 00:00:00 GMT+0000 (UTC)`;

            return formattedDate;
        },
        updateRole() {

            if (!this.roleName.length || !this.roleDescription.length || !this.skills.length || typeof this.staffNeededNumber != 'number' || !this.roleLocation.length || !this.closingDate.length) {

                alert("Please fill in all fields, otherwise role listing cannot be updated!");
            }
            else {

                const params = {
                    "role_id": this.role_id,
                    "role_name": this.roleName,
                    "role_description": this.roleDescription,
                    "no_of_pax": this.staffNeededNumber,
                    "department": this.roleDepartment,
                    "location": this.roleLocation,
                    "skills_name": this.skills,
                    "expiry_timestamp": this.convertDateFormat()
                }

                console.log(params);
                axios
                    .put('http://127.0.0.1:5000/roles/update', {

                        "params": params

                    })

                    .then(response => {
                        console.log(response);
                        alert("Role was updated successfully!");
                        window.location.reload();
                    })

                    .catch(error => {
                        console.error('Error:', error);
                        alert("Role was not created due to an error on our server's part. Please try again!");
                    });
            }
        },

        addSkill() {
            const selectedSkill = this.skillSelected;
            this.skills.push(selectedSkill);
            console.log(selectedSkill);

            const index = this.allskills.indexOf(selectedSkill);
            this.allskills.splice(index, 1);

        },

        removeSkill(index) {
            const y = this.skills.splice(index, 1);
            const mynewallskills = JSON.parse(JSON.stringify(this.allskills));

            this.truthy = false;
            for (let i in mynewallskills) {
                const thisskill = mynewallskills[i];
                if (thisskill == y[0]) {
                    this.truthy = true;
                }
            }

            if (this.truthy) {
                console.log('pass')
            }
            else {
                this.allskills.push(y[0]);
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

        getThisRole() {
            console.log(this.role_id);
            axios
                .get('http://127.0.0.1:5000/roles/' + this.role_id)

                .then(response => {
                    const responseData = response.data.data;

                    this.roleName = responseData.role_name;
                    this.roleDescription = responseData.role_description;
                    this.skills = responseData.skills_required;
                    this.staffNeededNumber = responseData.no_of_pax;
                    this.roleDepartment = responseData.department;
                    this.roleLocation = responseData.location;
                    this.closingDate = responseData.expiry_date;
                    this.closingDate = this.reverseDateFormat(this.closingDate)

                })

                .catch(error => {
                    console.error('Error:', error);
                });
        },

        reverseDateFormat(closingDate) {

            const date = new Date(closingDate)
            var dd = date.getDate();
            var mm = date.getMonth() + 1;
            var yyyy = date.getFullYear();
            if (dd < 10) { dd = '0' + dd; }
            if (mm < 10) { mm = '0' + mm; }
            return closingDate = yyyy + '-' + mm + '-' + dd;

        },
        redirectBrowse() {
            if (confirm("Are you sure you want to discard changes?")) {
                this.$router.push('/');
            }
        },

    },
    mounted: function () {
        this.skills = [];
        this.allskills = [];
        this.newskills = [];
        this.getSkills();
        this.role_id = this.$route.query.role_id;
        this.getThisRole();
        this.truthy = '';
    }
}
</script>

<template>
    <div>
        <Nav />

        <div class="container">

            <div class="title section">
                <div class="row">
                    <div class="col-md-12">
                        <h1>Role Editing</h1>
                        <br />
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-8">
                        <input type="text" class="role-name form-control" placeholder="Role Name" v-model="roleName">
                    </div>
                    <div class="col-md-4 text-end">
                        <button type="button" class="btn btn-danger btn-apply custom-button me-3"
                            @click="redirectBrowse()">CANCEL</button>
                        <button type="button" class="btn btn-success btn-apply custom-button apply-button"
                            @click="updateRole">UPDATE</button>
                    </div>
                </div>
            </div>

            <div class="desc section">
                <div class="row">
                    <div class="col-md-12">
                        <h4>Role Description</h4>
                        <textarea class="role-desc" placeholder="Role Description" v-model="roleDescription"></textarea>
                    </div>
                </div>
            </div>

            <div class="info section">
                <div class="row">

                    <div class="col-md-8" style="padding:0px">
                        <table class="table">
                            <div class="row">
                                <div class="col-md-4">
                                    <h4>Role Location</h4>
                                </div>
                                <div class="col-md-6">
                                    <input type="text" class="form-control custom-input" placeholder="Location"
                                        v-model="roleLocation"><br />
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-4">
                                    <h4>Role Department</h4>
                                </div>
                                <div class="col-md-6">
                                    <input type="text" class="form-control custom-input" placeholder="Department"
                                        v-model="roleDepartment"><br />
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-4">
                                    <h4>Number of Staff Needed</h4>
                                </div>
                                <div class="col-md-6">
                                    <input type="number" class="form-control custom-input" placeholder="Number of Staff"
                                        v-model="staffNeededNumber"><br />
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-4">
                                    <h4>Application Closing Date</h4>
                                </div>
                                <div class="col-md-6">
                                    <input type="date" class="form-control custom-input" placeholder="Closing Date"
                                        v-model="closingDate"><br />
                                </div>
                            </div>

                        </table>
                    </div>

                    <div class="col-md-4">
                        <h4>Skills Required</h4>
                        <table class="table mt-4">
                            <tr>
                                <th scope="col" colspan="4" style="text-decoration:underline;">Skill(s)</th>
                            </tr>
                            <tr v-if="!skills.length">
                                <td><em>No skills selected yet.</em></td>
                            </tr>
                            <tr v-else v-for="(skill, index) in skills" :key="index">
                                <td>{{ index + 1 }}</td>
                                <td>{{ skill }}</td>
                                <td><button class="btn btn-secondary" @click="removeSkill(index)">Remove</button></td>
                            </tr>
                        </table>
                        <p style="font-weight: bold;">Add Skill</p>
                        <select class="form-select form-select-md mb-3" v-model="skillSelected" @change="addSkill()">
                            <option value="" disabled selected>Find Skill by Name</option>
                            <option v-for="(skill, index) in allskills" :key="index" :value="skill">
                                {{ skill }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
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

.role-name {
    border-radius: 12px;
    font-size: 20px;
    font-weight: bold;
}

.role-desc {
    border: none;
    border-radius: 12px;
    padding: 10px;
    font-size: 14px;
    height: 200px;
    width: 100%;
}

.custom-button {
    width: 130px;
    color: #000000;
    font-weight: bold;
}

.custom-input {
    border: none;
}

.custom-dropdown {
    background-color: white;
    border: none;
    border-radius: 8px;
    padding: 5px;
}
</style>