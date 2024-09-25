<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useRegister } from '@/use/user';
import { useSupportedLanguages } from '@/use/language'

import Form from '@/elements/Form.vue';
import FormGroup from '@/elements/FormGroup.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Select from '@/elements/Select.vue';
import Button from '@/elements/Button.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';

import __ from '@/i18n'


const { email,
    name,
    password,
    sourceLanguage,
    targetLanguage,
    register,
    errorMessage,
    isLoading,
} = useRegister();
const router = useRouter();

const registerAndRedirect = async () => {
    const result = await register()
    if (result) {
        router.push('/')
    }
};

const languages = useSupportedLanguages();
const otherLanguages = computed(() => {
    const result = { ...languages.value };
    delete result[sourceLanguage.value];

    return result;
});


</script>

<template>
    <Form @submit.prevent="registerAndRedirect" class="register-form">
        <FormGroup>
            <Label for="email">{{ __('Email:') }}</Label>
            <Input type="email" id="email" v-model="email" required />
        </FormGroup>
        <FormGroup>
            <Label for="name">{{ __('Name:') }}</Label>
            <Input type="text" id="name" v-model="name" />
        </FormGroup>
        <FormGroup>
            <Label for="password">{{ __('Password:') }}</Label>
            <Input type="password" id="password" v-model="password" required />
        </FormGroup>

        <FormGroup>
            <Label for="sourceLanguage">{{ __('I want to learn:') }}</Label>
            <Select id="sourceLanguage" v-model="sourceLanguage" :options="languages" required />
        </FormGroup>

        <FormGroup>
            <Label for="targetLanguage">{{ __('My language is:') }}</Label>
            <Select id="targetLanguage" v-model="targetLanguage" :options="otherLanguages" required />
        </FormGroup>

        <FormGroup>
            <Button type="submit" :disabled="isLoading">{{ __('Register') }}</Button>
        </FormGroup>

        <ErrorMessage :message="errorMessage" />
    </Form>
</template>


<style scoped lang="scss">
.register-form {
  max-width: 400px;
  margin: 100px auto 0;

  .form-group {
    margin-bottom: 20px;
  }

  .error-message {
    margin-top: 10px;    
  }
}
</style>
