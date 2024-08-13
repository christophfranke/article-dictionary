<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { useRoute } from 'vue-router'; // Import Vue Router's useRoute
import { useReset } from '@/use/user';

import Form from '@/elements/Form.vue';
import FormGroup from '@/elements/FormGroup.vue';
import Label from '@/elements/Label.vue';
import Input from '@/elements/Input.vue';
import Button from '@/elements/Button.vue';
import ErrorMessage from '@/elements/ErrorMessage.vue';
import SuccessMessage from '@/elements/SuccessMessage.vue';
import InternalLink from '@/elements/InternalLink.vue';

import __ from '@/i18n'

const route = useRoute(); // Use Vue Router to access URL parameters
const { requestReset, completeReset, errorMessage, isLoading } = useReset();

const email = ref('');
const passwordResetSuccess = ref(false);
const newPassword = ref('');
const token = ref<string | null>(null); // State to hold the reset token

// Extract the token from URL parameters
watchEffect(() => {
    token.value = route.query.token ? String(route.query.token) : null;
});

// Handle password reset request
const resetPassword = async () => {
    passwordResetSuccess.value = await requestReset(email.value);
};

// Handle password change completion
const changePassword = async () => {
    if (token.value) {
        passwordResetSuccess.value = await completeReset(token.value, newPassword.value);
    }
};
</script>

<template>
    <Form @submit.prevent="changePassword" class="reset-form" v-if="token">
        <div>
            <FormGroup>
                <Label for="new-password">{{ __('New Password:') }}</Label>
                <Input type="password" id="new-password" v-model="newPassword" :disabled="passwordResetSuccess" required />
            </FormGroup>
            <FormGroup v-if="!passwordResetSuccess">
                <Button type="submit" :disabled="isLoading" role="view">{{ __('Change Password') }}</Button>
            </FormGroup>
            <ErrorMessage :message="errorMessage" />
            <div v-if="passwordResetSuccess">
                <SuccessMessage :message="__('Your password has been changed successfully!')" />
                <InternalLink to="/login" class="back-to-login">Back to login</InternalLink>
            </div>
        </div>
    </Form>
    <Form @submit.prevent="resetPassword" class="reset-form" v-else>
        <div>
            <FormGroup>
                <Label for="email">{{ __('Email:') }}</Label>
                <Input type="email" id="email" v-model="email" :disabled="passwordResetSuccess" required />
            </FormGroup>
            <FormGroup v-if="!passwordResetSuccess">
                <Button type="submit" :disabled="isLoading" role="view">{{ __('Reset password') }}</Button>
            </FormGroup>
            <ErrorMessage :message="errorMessage" />
            <SuccessMessage v-if="passwordResetSuccess" :message="__('A password reset link has been sent to $1', email)" />
        </div>
        <div v-if="!passwordResetSuccess">
            <InternalLink to="/login">Back to login</InternalLink>
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

.back-to-login {
    margin-top: 25px;
    font-size: 18px;
    text-align: center;
}
</style>
