<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, watchEffect, watch } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { useProfile, useUpdateProfile } from '@/use/user';
import { useSupportedLanguages, useSupportedInterfaces } from '@/use/language';
import { setTheme } from '@/themes';

import Headline from '@/elements/Headline.vue';
import Form from '@/elements/Form.vue';
import FormGroup from '@/elements/FormGroup.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Button from '@/elements/Button.vue';
import Select from '@/elements/Select.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';

import __ from '@/i18n'


const form = reactive({
  email: '',
  name: '',
  newPassword: '',
  confirmPassword: '',
  sourceLanguage: '',
  targetLanguage: '',
  interfaceLanguage: '',
  theme: '',
});

const languages = useSupportedLanguages()
const interfaces = useSupportedInterfaces()
const { profile } = useProfile();
const { updateProfile, errorMessage, isLoading } = useUpdateProfile();
const isDirty = ref<boolean>(false)

watchEffect(() => {
  if (!form.email) {
    form.email = profile.email;
  }
  if (!form.name) {
    form.name = profile.name;
  }
  if (!form.sourceLanguage) {
    form.sourceLanguage = profile.sourceLanguage;
  }
  if (!form.targetLanguage) {
    form.targetLanguage = profile.targetLanguage;
  }
  if (!form.interfaceLanguage) {
    form.interfaceLanguage = profile.interfaceLanguage;
  }
  if (!form.theme) {
    form.theme = profile.theme;
  }
});

const submitForm = async () => {
  const formData = Object.fromEntries(
    Object.entries(form).filter(([key, value]) => value !== '')
  );

  delete formData.sourceLanguage;
  delete formData.targetLanguage;

  if (await updateProfile(formData)) {
    form.newPassword = '';
    form.confirmPassword = '';
    isDirty.value = false;
  }
};

watchEffect(() => {
  setTheme(form.theme);
});

onBeforeUnmount(() => {
  setTheme(profile.theme);
});

const setDirty = () => {
  isDirty.value = true
}

onBeforeRouteLeave((to, from, next) => {
  if (isDirty.value) {
    const answer = window.confirm(__('You have unsaved changes. Do you really want to leave?'));
    if (answer) {
      next();
    } else {
      next(false);
    }
  } else {
    next();
  }
});


const themes = {
  'bright': 'Light',
  'dark': 'Dark',
  'classic': 'Classic',
};
</script>

<template>
  <div class="profile-settings">
    <Headline>{{ __('Profile Settings') }}</Headline>

    <Form @submit.prevent="submitForm" class="settings-form">
      <FormGroup>
        <Label for="email">{{ __('Email:') }}</Label>
        <Input type="email" id="email" v-model="form.email" @change="setDirty" required />
      </FormGroup>

      <FormGroup>
        <Label for="name">{{ __('Name:') }}</Label>
        <Input type="text" id="name" v-model="form.name" @change="setDirty" />
      </FormGroup>

      <FormGroup>
        <Label for="theme">{{ __('Theme:') }}</Label>
        <Select v-model="form.theme" :options="themes" @change="setDirty">
        </Select>
      </FormGroup>

      <FormGroup>
        <Label for="newPassword">{{ __('New Password:') }}</Label>
        <Input type="password" id="newPassword" v-model="form.newPassword" @change="setDirty" />
      </FormGroup>

      <FormGroup>
        <Label for="confirmPassword">{{ __('Confirm New Password:') }}</Label>
        <Input type="password" id="confirmPassword" v-model="form.confirmPassword" @change="setDirty" />
      </FormGroup>

      <FormGroup>
        <Label for="interfaceLanguage">{{ __('Interface language:') }}</Label>
        <Select id="interfaceLanguage" v-model="form.interfaceLanguage" @change="setDirty">
          <option v-for="(label, value) in interfaces" :key="value" :value="value">{{ label }}</option>
        </Select>
      </FormGroup>

      <FormGroup>
        <Label for="sourceLanguage">{{ __('I want to learn:') }}</Label>
        <Select id="sourceLanguage" v-model="form.sourceLanguage" disabled>
          <option v-for="(label, value) in languages" :key="value" :value="value">{{ label }}</option>
        </Select>
      </FormGroup>

      <FormGroup>
        <Label for="targetLanguage">{{ __('My language is:') }}</Label>
        <Select id="targetLanguage" v-model="form.targetLanguage" disabled>
          <option v-for="(label, value) in languages" :key="value" :value="value">{{ label }}</option>
        </Select>
      </FormGroup>

      <Button type="submit" class="save-button" :disabled="isLoading || !isDirty">{{ __('Save Changes') }}</Button>
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
