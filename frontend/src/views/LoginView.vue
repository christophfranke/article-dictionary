<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLogin, useUser } from '@/use/user';

import Form from '@/elements/Form.vue';
import FormGroup from '@/elements/FormGroup.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Button from '@/elements/Button.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';
import InternalLink from '@/elements/InternalLink.vue';


const router = useRouter();

const { login, email, password, errorMessage, isLoading } = useLogin();

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
  <Form @submit.prevent="loginAndRedirect" class="login-form">
    <FormGroup>
      <Label for="email">Email:</Label>
      <Input type="email" id="email" v-model="email" required />
    </FormGroup>
    <FormGroup>
      <Label for="password">Password:</Label>
      <Input type="password" id="password" v-model="password" required />
    </FormGroup>
    <FormGroup>
      <Button type="submit" :disabled="isLoading">Login</Button>
      <InternalLink to="/register" class="register-link">Don't have an account? Register here</InternalLink>
    </FormGroup>
    <ErrorMessage :message="errorMessage" />
  </Form>
</template>

<style scoped lang="scss">
.login-form {
  max-width: 400px;
  margin: 100px auto 0;
}

.form-group {
  margin-bottom: 20px;
}

.register-link {
  margin-top: 10px; /* Adjust the spacing */
}

.error-message {
  margin-top: 10px;
}
</style>
