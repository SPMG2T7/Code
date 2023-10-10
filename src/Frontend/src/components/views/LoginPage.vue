<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent=handleSubmit>
      <div class="form-group">
        <label for="staff_name">Staff Name:</label>
        <select v-model="staff_select" id="staff_name" class="form-control">
          <option value="" selected>Please select one</option>
          <option v-for="staff in this.staff_names" :value=staff[1] :key=staff[0]>
            {{ staff[0] }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
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
          if (staff.access_rights == '1') {
            this.access_right = 'Staff'
          } else {
            this.access_right = 'Human Resources'
          }
          this.staff_names.push([`${staff.first_name} (${this.access_right})`, [staff.staff_id, staff.access_rights]]);
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
  max-width: 400px;
  margin: 0 auto;
  margin-top: 10px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
