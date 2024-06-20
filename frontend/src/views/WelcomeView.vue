<script setup lang="ts">
import InternalLink from '@/elements/InternalLink.vue';
import __ from '@/i18n';
</script>
<template>
    <div class="container">
        <header>
            <h1>{{ __('Welcome to International Reading') }}</h1>
            <p>{{ __('Immerse yourself in a new language through your own content.') }}</p>
        </header>

        <section>
            <h2>{{ __('Supported Languages') }}</h2>
            <p>{{ __('We currently support the following languages:') }}</p>
            <ul>
                <li>{{ __('English') }}</li>
                <li>{{ __('Deutsch (German)') }}</li>
                <li>{{ __('Français (French)') }}</li>
                <li>{{ __('Español (Spanish)') }}</li>
                <li>{{ __('Português (Portuguese)') }}</li>
                <li>{{ __('Ελληνικά (Greek)') }}</li>
                <li>{{ __('Polski (Polish)') }}</li>
                <li>{{ __('Русский (Russian)') }}</li>
            </ul>
        </section>

        <section>
            <h2>{{ __('How It Works') }}</h2>
            <p>{{ __("Our platform allows you to learn a new language by immersing yourself in content of your choice. Here's how it works:") }}</p>
            <ol>
                <li>{{ __('Create an article or choose a public one.') }}</li>
                <li>{{ __('We translate the article word by word.') }}</li>
                <li>{{ __("Hover over words you don't know to see the translation.") }}</li>
                <li>{{ __('Read in your target language and learn new words quickly in topics that interest you.') }}</li>
            </ol>
            <p>{{ __("It's less like learning and more like diving into a new culture!") }}</p>
        </section>

        <section>
            <h2>{{ __('Your Learning Journey') }}</h2>
            <p>{{ __('Track your progress with our built-in statistics and review system. Our system uses spaced repetition (SRS) and word frequency analysis to help you retain new vocabulary effectively.') }}</p>
        </section>

        <section>
            <h2>{{ __('Get Started') }}</h2>
            <ol>
                <li><InternalLink to="/register">{{ __('Create an account.') }}</InternalLink></li>
                <li>{{ __('Find content you want to read in your target language.') }}</li>
                <li>{{ __('Create an article and fill it with your content. The content can be at any difficulty level.') }}</li>
                <li>{{ __('Start reading and learn new words as you go.') }}</li>
            </ol>
        </section>

        <section>
            <h2>{{ __('Advanced Features') }}</h2>
            <ol>
                <li>{{ __('You can tackle content that is more advanced than your usual reading level. The hover feature makes understanding complex texts more manageable.') }}</li>
                <li>{{ __('Each article includes a vocabulary list with translations of all words that are currently unknown to you.') }}</li>
                <li>{{ __('Hover over a word to see its translation. Click on a word to mark it as known, and it will no longer display its translation. This helps you visually track your progress.') }}</li>
                <li>{{ __('We calculate a difficulty score for each article based on your known and unknown words. Our system then recommends articles that match your current learning level, ensuring they are not too difficult.') }}</li>
                <li>{{ __('The SRS (Spaced Repetition System) and article reader are integrated. The SRS considers the words you read in the reader, allowing for effective learning. You can read a bit and then review words immediately to reinforce your memory. You can also focus on learning words from a specific article to prepare for reading it.') }}</li>
                <li>{{ __('You have full control over your learning process: you can modify suggested translations, skip words, or ignore them as needed.') }}</li>
                <li>{{ __('Our system automatically detects and ignores words that do not belong to your target language, keeping your learning focused.') }}</li>
                <li>{{ __('Similar words are clustered together, ensuring that your learning statistics are accurate.') }}</li>
            </ol>
        </section>
    </div>
</template>

<style scoped lang="scss">
@import "@/style/global.scss";

.container {
    width: 80vw;
    max-width: 1400px;
    margin: 0 auto;
}

header {
    text-align: center;
    margin: 20px 0;
    h1 {
        color: $headline-font-color;
        margin-bottom: 10px;
    }
}

section {
    background-color: $card-outer-background-color;
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
    border: 1px solid $border-color;

    h2 {
        color: $headline-font-color;
        margin-bottom: 10px;
    }

    p, li {
        color: $main-color;
    }

    ul, ol {
        margin-left: 20px;
    }

    ol {
        li {
            margin-bottom: 10px;
        }
    }
}
</style>