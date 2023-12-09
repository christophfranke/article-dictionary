<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLogin, useUser } from '@/use/user';

const router = useRouter();

const { login, email, password } = useLogin();

const loginAndRedirect = async () => {
  if (await login()) {    
    const nextPath = Array.isArray(router.currentRoute.value.query.next)
      ? '/'
      : router.currentRoute.value.query.next || '/';
    router.push(nextPath);
  }
}
</script>


<template>
  <form @submit.prevent="loginAndRedirect" class="login-form">
    <div class="form-group">
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="email" required />
    </div>
    <div class="form-group">
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required />
    </div>
    <div class="form-group">
      <button type="submit">Login</button>
      <router-link to="/register" class="register-link">Don't have an account? Register here</router-link>
    </div>
  </form>
</template>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
  margin-top: 100px;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.register-link {
  color: #007bff; /* Link color */
  text-decoration: none; /* Remove default underline */
  display: block;
  margin-top: 10px; /* Adjust the spacing */
  font-size: 14px;
}

.register-link:hover {
  text-decoration: underline; /* Underline on hover */
  background-color: transparent;
}
</style>
