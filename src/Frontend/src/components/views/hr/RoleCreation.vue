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
            staffId: sessionStorage.getItem('staff_id'),
            accessId: sessionStorage.getItem('access_id')
        };
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

        createRole() {
            if (!this.roleName.length || !this.roleDescription.length || !this.skills.length || !this.staffId.length || typeof this.staffNeededNumber != 'number' || !this.roleLocation.length || !this.closingDate.length) {

                alert("Please fill in all fields, otherwise role listing cannot be created!");
            }
            else {

                const params = {
                    "role_name": this.roleName,
                    "role_description": this.roleDescription,
                    "skills_required": this.skills,
                    "listed_by": this.staffId,
                    "no_of_pax": this.staffNeededNumber,
                    "department": this.roleDepartment,
                    "location": this.roleLocation,
                    "expiry_timestamp": this.convertDateFormat()
                }

                axios
                    .post('http://127.0.0.1:5000/roles/create', {

                        "params": params

                    })

                    .then(response => {
                        console.log(response)
                        alert("Role was created successfully!");
                        this.$router.push('/')
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

            const index = this.allskills.indexOf(selectedSkill);
            this.allskills.splice(index, 1);

        },

        removeSkill(index) {
            this.allskills.push(this.skills[index])
            this.skills.splice(index, 1)
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

    },
    mounted: function () {
        this.skills = [];
        this.allskills = [];
        this.newskills = [];
        this.getSkills();

    },
    created() {
        if (!this.staffId && !this.accessId) {
            this.$router.push('/Login');
        }
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
                        <h1>Role Creation</h1>
                        <br />
                    </div>
                </div>

                <div class="row">

                    <div class="mb-3 col-md-9">
                        <input type="text" class="form-control role-name " placeholder="Role Name" v-model="roleName">
                    </div>
                    <div class="col-md-3 text-end">
                        <button type="button" class="btn btn-success btn-apply custom-button apply-button"
                            @click="createRole">CREATE</button>
                    </div>
                </div>
            </div>

            <div class="desc section">
                <div class="row">
                    <div class="col-md-12">
                        <h4>Role Description</h4>
                        <!-- <input type="text" placeholder="Role Description" v-model="roleDescription"> -->
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
                                <td><button type="button" class="btn btn-secondary"
                                        @click="removeSkill(index)">Remove</button></td>
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