<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png">
  <h1>App.vue</h1> -->
  <div class="hello">
    <router-view />
  </div>
</template>

<style>
.container-style {
  padding: 20px;
  border-radius: 10px;
  margin-top: 24px;
}

.custom-button {
  width: 130px !important;
  color: #000000 !important;
  font-weight: bold !important;
}

.apply-button {
  background-color: #8BC100 !important;
}

.redTextCSS {
  color: red;
}


/* FOR CLASSES WITHIN EDITING ROLE AND CREATION ROLE */
.custom-input {
  border: none !important;
}

.role-desc {
  border: none;
  border-radius: 12px;
  padding: 10px;
  font-size: 14px;
  height: 200px;
  width: 100%;
}

.role-name {
    border-radius: 12px !important;
    font-size: 20px !important;
    font-weight: bold !important;
}
</style>