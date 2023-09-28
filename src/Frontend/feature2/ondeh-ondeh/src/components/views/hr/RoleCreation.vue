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
            skillSelected: ''
        };
    },
    computed: {
        
    },
    methods: {
        createRole() {
            console.log(this.skills)

            axios
                .post('http://127.0.0.1:5000/roles/create',{

                    "params": {
                        "role_name": this.roleName,
                        "role_description": this.roleDescription,
                        "skills_required": this.skills,
                        "listed_by": 123459,
                        "no_of_pax": this.staffNeededNumber,
                        "department": "Engineering",
                        "location": "San Francisco",
                        "expiry_timestamp": this.closingDate
                    }

                })

                .then(response => {
                console.log('sent')
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

            console.log('when editing is allowed there has to be a deletion handler also, and it will add back the skill to the allskills array once deleted. but i mean deletion is for a diff function not this one!');
            
        },

        getSkills() {
            axios
                .get('http://127.0.0.1:5000/skills/get_all')

                .then(response => {
                    this.responseData = response.data.data;
                    this.skills=this.responseData.skills;
                    for (let i = 0; i < this.skills.length; i++) {
                        this.skill_name = this.responseData.skill_name;
                        console.log(this.skill_name);
                        this.allskills.push(this.skill_name);
                        
                        }

                    console.log(this.allskills);
                })

                .catch(error => {
                    console.error('Error:', error);
                });
        },

    },
    mounted: function () {
        this.skills=[];
        this.allskills=[];
        this.getSkills();
    }
}
</script>

<template>
    <div>
        <Nav />
        <h1>HR_Role Creation</h1>

        <input type="text" placeholder="Role Name" id="roleName">

        <br>
        <br>
        Role Description <input type="text" id="roleDescription" placeholder="Role Description">
        
        <br>
        <br>
        Skills Required
        <table border="1">
        <tr>
            <th colspan="2">Skill</th>
        </tr>
        <tr v-for="(skill, index) in skills" :key="index">
            <td>{{ index+1 }}</td>
            <td>{{ skill }}</td>
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

        <!--
            <input type="text" id="skillName" :skillName="skillName" @keypress.enter="searchSkill(skillName)" placeholder="Search Skills by Name">
            <input type="text" id="searchSkillName" placeholder="Search Skills by Name">
        -->

        <br>
        <br>
        Number of Staff Needed <input type="number" id="staffNeededNumber">

        <br>
        <br>
        Application Closing Date <input type="date" id="closingDate">

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