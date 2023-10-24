<template>
  <div class="login-container">
    <div class="logo-container">
      <img src="../../assets/gojobs_logo.png" />
    </div>
    <h3>Welcome to GoJobs Portal!</h3><br/>
    <form @submit.prevent=handleSubmit>
      <div class="form-group">
        <label for="staff_name">Select User:</label>
        <select v-model="staff_select" id="staff_name" class="form-control">
          <option value="" selected disabled>Please select one:</option>
          <option v-for="staff in this.staff_names" :value=staff[1] :key=staff[0]>
            {{ staff[0] }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn apply-button">Log In</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      staff_names: [],
      staff_select: null,
      access_right: ''
    };
  },
  methods: {
    async getAllStaffName() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/staff/get_all');

        
        for (const staff of response.data.data.staffs) {

          // access right 1 is admin, 2 is user, 3 manager, 4 is HR
          if (staff.access_rights == '1') {
            staff.access_right = 'Admin'
          } else if (staff.access_rights == '2') {
            staff.access_right = 'Staff'
          } else if (staff.access_rights == '3') {
            staff.access_right = 'Manager'
          }
          else{
            staff.access_right = 'Human Resources'
          }
          
          // this.staff_names.push([`${staff.first_name} ${staff.last_name} (${staff.access_right})`, [staff.staff_id, staff.access_rights]]);
          this.staff_names.push([`[${staff.access_right}] ${staff.first_name} ${staff.last_name}`, [staff.staff_id, staff.access_rights]]);

        }
      } catch (error) {
        console.error('Error fetching staffs:', error);
      }
    },
    handleSubmit() {
      sessionStorage.setItem('staff_id', this.staff_select[0]);
      sessionStorage.setItem('access_id', this.staff_select[1])

      // Redirect to a specific route using this.$router.push
      this.$router.push('/');
    },
  },
  mounted() {
    this.getAllStaffName();
  },
};
</script>

<style scoped>
.login-container {
  background-color: white;
  min-width: 500px;
  padding: 40px;
  border: 1px solid #ccc;
  border-radius: 10px;
  text-align: center;
  position: absolute;
  top: 35%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.logo-container {
  display: inline-block;
  position: relative;
  transition: transform 0.8s; /* Add a smooth transition on hover */
}

.logo-container:hover {
  animation: shake 0.8s infinite; /* Start the shake animation on hover */
}

@keyframes shake {
  0% {
    transform: translateX(0); /* Initial position */
  }
  25% {
    transform: translateX(-5px); /* Move left */
  }
  50% {
    transform: translateX(5px); /* Move right */
  }
  75% {
    transform: translateX(-5px); /* Move left again */
  }
  100% {
    transform: translateX(0); /* Back to the initial position */
  }
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
}

.btn {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
}
</style>
