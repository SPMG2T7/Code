<script>
import axios from 'axios'

export default {
    name: "App",
    components: {

    },
    data() {
        return {
            roleID: null,
            staffDetails: [],
            staffId: sessionStorage.getItem('staff_id'),
            accessId: sessionStorage.getItem('access_id'),
        };
    },
    methods: {
        // the function that helps us call the endpoint and retrieve the data
        fetchData() {
            axios
                .get("http://127.0.0.1:5000/staff/" + this.staffId)
                .then(response => {
                    this.staffDetails = response.data[0].data;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },

        resetSession() {
            sessionStorage.clear();
            this.$router.push('/Login')
        },

        redirectBrowse() {
            this.$router.push('/');
        },

        redirectCreate() {
            this.$router.push('/RoleCreation')
        },

        redirectProfile() {
            this.$router.push('/')
        },

        redirectSettings() {
            this.$router.push('/')
        }

    },
    mounted: function () {
        this.fetchData();
    },
    created() {
        // console.log(this.staffId, this.accessId)
        if (!this.staffId && !this.accessId) {
            this.$router.push('/Login');
        }
    },
}
</script>

<template>

    <nav class="navbar navbar-expand-lg bg-body-tertiary rounded-3">
        <div class="container-fluid">
            <img class="mx-2" src="../../assets/gojobs_logo.png" />
            <span class="navbar-brand fw-bold">GoJobs Portal</span>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">

            <div class="navbar-nav ms-left mb-2 mb-lg-0">
            
                <p class="hover-underline-animation" style="margin:0px 10px;" @click="redirectBrowse">Browse Role Listings</p>
                <p v-if="this.accessId == 1 || this.accessId == 3 || this.accessId == 4" class="hover-underline-animation" @click="redirectCreate">Create New Role</p>

            </div>

                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item profile-name">
                        <!-- Welcome, {{ name }} ({{ balance_points }} Points) -->
                        Welcome, {{ staffDetails.first_name}}!
                    </li>

                    <div class="nav-link p-0" data-bs-toggle="dropdown">
                        <li class="nav-item">
                            <button id="imgButton" class="btn btn-default">
                                <img src="../../assets/profile.png" />
                            </button>


                        <div class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                            <span class="dropdown-item" @click="redirectProfile()">Profile</span>
                            <span class="dropdown-item" @click="redirectSettings()">Settings</span>
                            <span class="dropdown-item" @click="resetSession()" style="cursor:pointer;">Log Out</span>
                        </div>

                    </li>
            </div>
            </ul>
        </div>
        </div>
    </nav>
</template>

<style scoped>
nav {
    background: linear-gradient(263deg, #946282 0%, #8BC100 100%);
}

.navbar-nav {
    display: flex;
    align-items: center;
    justify-content: center;
}

#imgButton {
    font-size: 24px;
    border: none;
    cursor: pointer;
    outline: none;
    margin: auto;
    display: block;
    background-color: transparent !important;
}

#imgButton:hover {
    background-color: transparent !important;
}

*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    position: relative;
    font-weight: normal;
}

img {
    width: 35px;
    height: 35px;
    object-fit: cover;
    border-radius: 50%;
}

.profile-name {
    color: black;
    font-weight: bold;
}

.listing {
    background: rgba(233, 196, 220, 0.3);
}

.hover-underline-animation:hover {
    cursor:pointer;
}

.hover-underline-animation {
  display: inline-block;
  position: relative;
}

.hover-underline-animation::after {
  content: '';
  position: absolute;
  width: 100%;
  transform: scaleX(0);
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: #000000;
  transform-origin: bottom right;
  transition: transform 0.25s ease-out;
}

.hover-underline-animation:hover::after {
  transform: scaleX(1);
  transform-origin: bottom left;
}

</style>