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
            roleName:'',
            roleDescription:'',
            staffNeededNumber:'',
            closingDate:'',
            roleLocation:'',
            roleDepartment:''
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
        createRole() {    
            // Construct the desired format
            //Mon Dec 12 2023 00:00:00 GMT+0000 (UTC)
            console.log(this.closingDate)
            console.log(this.convertDateFormat())
            const params = {
                        "role_name": this.roleName,
                        "role_description": this.roleDescription,
                        "skills_required": this.skills,
                        "listed_by": 123459,
                        "no_of_pax": this.staffNeededNumber,
                        "department": this.roleDepartment,
                        "location": this.roleLocation,
                        "expiry_timestamp": this.convertDateFormat()
                    }
            axios
                .post('http://127.0.0.1:5000/roles/create',{

                    "params": params

                })

                .then(response => {
                    console.log(response);
                })

                .catch(error => {
                    console.error('Error:', error);
                });

        },

        addSkill() {
            const selectedSkill = this.skillSelected;
            this.skills.push(selectedSkill);
            console.log(selectedSkill);

            const index = this.allskills.indexOf(selectedSkill);
            const x = this.allskills.splice(index, 1);

            console.log(x)
        },

        removeSkill(index) {
            this.allskills.push(this.skills[index])
            const y = this.skills.splice(index,1)

            console.log(y)
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

    },
    mounted: function () {
        this.skills=[];
        this.allskills=[];
        this.newskills=[];
        this.getSkills();

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
    <div>
        <Nav />
        <h1>HR_Role Creation</h1>

        <input type="text" placeholder="Role Name" v-model="roleName">

        <br>
        <br>
        Role Description <input type="text" v-model="roleDescription" placeholder="Role Description">

        <br>
        <br>
        Role Location <input type="text" v-model="roleLocation" placeholder="Location" >

        <br>
        <br>
        Role Department <input type="text" v-model="roleDepartment" placeholder="Department" >
        
        <br>
        <br>
        Number of Staff Needed <input type="number" placeholder="Number of Staff" v-model="staffNeededNumber">

        <br>
        <br>
        Application Closing Date <input type="date" placeholder="Closing Date" v-model="closingDate">

        <br>
        <br>
        Skills Required
        <table border="1">
        <tr>
            <th colspan="2">Skill</th>
        </tr>
        <tr v-if="!skills.length"><td><i>No skills selected yet.</i></td></tr>
        <tr v-else v-for="(skill, index) in skills" :key="index">
            <td>{{ index+1 }}</td>
            <td>{{ skill }}</td>
            <td><button @click="removeSkill(index)">Remove</button></td>
        </tr>
        </table>


        <br>
        <br>
        Add Skill
        <select v-model="skillSelected" @change="addSkill()">
            <option value="" disabled selected>Find Skill by Name</option>
            <option v-for="(skill,index) in allskills" :key="index" :value="skill">
                {{ skill }}
            </option>
        </select>


        <br>
        <br>
        <button @click="createRole">Create Role</button>

        <br><br>
        <router-link to="/browseroles">BrowseRoles</router-link>

        <RouterView></RouterView>
    </div>
</template>

<style scoped>
</style>