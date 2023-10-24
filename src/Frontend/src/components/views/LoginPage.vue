<template>
  <div class="login-container">
    <img src="../../assets/gojobs_logo.png" />
    <h3>Welcome to GoJobs Portal!</h3><br/>
    <form @submit.prevent=handleSubmit>
      <div class="form-group">
        <label for="staff_name">Staff Name:</label>
        <select v-model="staff_select" id="staff_name" class="form-control" label="Staff Name">
          <option value="" selected>Please select one:</option>
          <option v-for="staff in this.staff_names" :value=staff[1] :key=staff[0]>
            {{ staff[0] }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn apply-button">Login</button>
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
          
          this.staff_names.push([`${staff.first_name} (${staff.access_right})`, [staff.staff_id, staff.access_rights]]);
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
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

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
