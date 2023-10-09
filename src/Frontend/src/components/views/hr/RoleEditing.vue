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
            roleDepartment:'',
            role_id:'',
            truthy:''
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
            
            const params = {
                        "role_id":this.role_id,
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
                .put('http://127.0.0.1:5000/roles/update',{

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
            this.allskills.splice(index, 1);

        },

        removeSkill(index) {
            const y = this.skills.splice(index,1);
            const mynewallskills = JSON.parse(JSON.stringify(this.allskills));

            this.truthy = false;
            for (const i in mynewallskills) {
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
                    this.newskills=this.responseData.skills;
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

                    this.roleName=responseData.role_name;
                    this.roleDescription=responseData.role_description;
                    this.skills=responseData.skills_required;
                    this.staffNeededNumber=responseData.no_of_pax;
                    this.roleDepartment=responseData.department;
                    this.roleLocation=responseData.location;
                    this.closingDate=responseData.expiry_date;
                    this.closingDate=this.reverseDateFormat(this.closingDate)

                })

                .catch(error => {
                    console.error('Error:', error);
                });
        },

        reverseDateFormat(closingDate) {

            const date = new Date(closingDate)
            var dd = date.getDate(); 
            var mm = date.getMonth()+1;
            var yyyy = date.getFullYear(); 
            if(dd<10){dd='0'+dd;} 
            if(mm<10){mm='0'+mm;}
            return closingDate=yyyy+'-'+mm+'-'+dd;

        }

    },
    mounted: function () {
        this.skills=[];
        this.allskills=[];
        this.newskills=[];
        this.getSkills();
        this.role_id=sessionStorage.getItem('role_id');
        console.log(this.role_id);
        this.getThisRole();
        this.truthy='';
    }
}
</script>

<template>
    <div>
        <Nav />
        <h1>HR_Role Editing</h1>

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
        <button @click="updateRole">Update Role</button>

        <br><br>
        <router-link to="/">BrowseRoles</router-link>

        <RouterView></RouterView>
    </div>
</template>

<style scoped>
</style>