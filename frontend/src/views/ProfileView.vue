<script setup lang="ts">
import { ref, onMounted, watchEffect, watch } from 'vue';
import { useProfile, useUpdateProfile } from '@/use/user';
import { useSupportedLanguages } from '@/use/language';
import { getThemeName, setTheme } from '@/themes';

import Headline from '@/elements/Headline.vue';
import Form from '@/elements/Form.vue';
import FormGroup from '@/elements/FormGroup.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Button from '@/elements/Button.vue';
import Select from '@/elements/Select.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';


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
const { updateProfile, errorMessage, isLoading } = useUpdateProfile();

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

  delete formData.sourceLanguage;
  delete formData.targetLanguage;

  if (await updateProfile(formData)) {
    form.value.newPassword = '';
    form.value.confirmPassword = '';
  }
};

const theme = ref(getThemeName());
watch(theme, newValue => {
  setTheme(newValue);
})
</script>

<template>
  <div class="profile-settings">
    <Headline>Profile Settings</Headline>

    <Form @submit.prevent="submitForm" class="settings-form">
      <FormGroup>
        <Label for="email">Email:</Label>
        <Input type="email" id="email" v-model="form.email" required />
      </FormGroup>

      <FormGroup>
        <Label for="name">Name:</Label>
        <Input type="text" id="name" v-model="form.name" />
      </FormGroup>

      <FormGroup>
        <Label for="theme">Theme:</Label>
        <Select v-model="theme">
          <option value="bright">Light</option>
          <option value="dark">Dark</option>
        </Select>
      </FormGroup>

      <FormGroup>
        <Label for="newPassword">New Password:</Label>
        <Input type="password" id="newPassword" v-model="form.newPassword" />
      </FormGroup>

      <FormGroup>
        <Label for="confirmPassword">Confirm New Password:</Label>
        <Input type="password" id="confirmPassword" v-model="form.confirmPassword" />
      </FormGroup>

      <FormGroup>
        <Label for="sourceLanguage">I want to learn:</Label>
        <Select id="sourceLanguage" v-model="form.sourceLanguage" disabled>
          <option v-for="(label, value) in languages" :key="value" :value="value">{{ label }}</option>
        </Select>
      </FormGroup>

      <FormGroup>
        <Label for="targetLanguage">My language is:</Label>
        <Select id="targetLanguage" v-model="form.targetLanguage" disabled>
          <option v-for="(label, value) in languages" :key="value" :value="value">{{ label }}</option>
        </Select>
      </FormGroup>

      <Button type="submit" class="save-button" :disabled="isLoading">Save Changes</Button>
    </Form>
    <ErrorMessage :message="errorMessage" />
  </div>
</template>

<style scoped>
.profile-settings {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.settings-form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

label {
  margin-bottom: 5px;
}
</style>
