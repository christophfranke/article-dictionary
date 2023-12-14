<script setup lang="ts">
import { ref, onMounted, watchEffect } from 'vue';
import { useProfile, useUpdateProfile } from '@/use/user';
import { useSupportedLanguages } from '@/use/language';


const form = ref({
  email: '',
  name: '',
  newPassword: '',
  confirmPassword: '',
  sourceLanguage: '',
  targetLanguage: '',
});

const languages = useSupportedLanguages()
const profile = useProfile();
const updateProfile = useUpdateProfile();

watchEffect(() => {
  form.value.email = profile.email.value;
  form.value.name = profile.name.value;
  form.value.sourceLanguage = profile.sourceLanguage.value;
  form.value.targetLanguage = profile.targetLanguage.value;
})

const submitForm = async () => {
  const formData = Object.fromEntries(
    Object.entries(form.value).filter(([key, value]) => value !== '')
  );

  if (formData.newPassword !== formData.confirmPassword) {
    delete formData.newPassword;
    console.error('Passwords do not match');
  }
  delete formData.confirmPassword;

  if (formData.newPassword) {
    formData.password = formData.newPassword;
    delete formData.newPassword;
  }

  if (await updateProfile(formData)) {
    form.value.newPassword = '';
    form.value.confirmPassword = '';
  }
};
</script>

<template>
  <div class="profile-settings">
    <h2>Profile Settings</h2>

    <form @submit.prevent="submitForm" class="settings-form">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="form.email" required />
      </div>

      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="form.name" />
      </div>

      <div class="form-group">
        <label for="newPassword">New Password:</label>
        <input type="password" id="newPassword" v-model="form.newPassword" />
      </div>

      <div class="form-group">
        <label for="confirmPassword">Confirm New Password:</label>
        <input type="password" id="confirmPassword" v-model="form.confirmPassword" />
      </div>

      <div class="form-group">
        <label for="sourceLanguage">I want to learn:</label>
        <select id="sourceLanguage" v-model="form.sourceLanguage" disabled>
          <option v-for="(label, value) in languages" :key="value" :value="value">{{ label }}</option>
        </select>
      </div>

      <div class="form-group">
        <label for="targetLanguage">My language is:</label>
        <select id="targetLanguage" v-model="form.targetLanguage" disabled>
          <option v-for="(label, value) in languages" :key="value" :value="value">{{ label }}</option>
        </select>
      </div>

      <button type="submit" class="save-button">Save Changes</button>
    </form>
  </div>
</template>

<style scoped>
.profile-settings {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.settings-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

input,
select {
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

.save-button {
  background-color: #28a745;
}
</style>
