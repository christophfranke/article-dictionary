<script setup lang="ts">
import { ref } from 'vue';
import { useReset } from '@/use/user';

import Form from '@/elements/Form.vue';
import FormGroup from '@/elements/FormGroup.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Button from '@/elements/Button.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';
import SuccessMessage from '@/elements/SuccessMessage.vue';

import __ from '@/i18n'

const { requestReset, errorMessage, isLoading } = useReset();

const email = ref('')
const passwordResetSuccess = ref(false)
const resetPassword = async () => {
    passwordResetSuccess.value = await requestReset(email.value)
}
</script>

<template>
    <Form @submit.prevent="resetPassword" class="reset-form">
        <div v-if="passwordResetSuccess">
            <FormGroup>
                <Label for="email">{{ __('Email:') }}</Label>
                <Input type="email" id="email" v-model="email" disabled="true" />
            </FormGroup>
            <SuccessMessage :message="__('A password reset link has been sent to $1', email)" />
        </div>
        <div v-else>
            <FormGroup>
                <Label for="email">{{ __('Email:') }}</Label>
                <Input type="email" id="email" v-model="email" required />
            </FormGroup>
            <FormGroup>
                <Button type="submit" :disabled="isLoading" role="view">{{ __('Reset password') }}</Button>
            </FormGroup>
            <ErrorMessage :message="errorMessage" />
        </div>
    </Form>
</template>


<style scoped lang="scss">
.reset-form {
  max-width: 600px;
  margin: 100px auto 0;
}

.form-group {
  margin-bottom: 20px;
}

.error-message {
  margin-top: 10px;
}
</style>