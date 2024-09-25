import { ref } from 'vue';
import __ from '@/i18n';

type RefreshFn = () => void;

const describeTime = (milliseconds: number, refresh?: RefreshFn): string => {
    const seconds = Math.round(milliseconds / 1000);
    const minutes = Math.round(seconds / 60);
    const hours = Math.round(minutes / 60);
    const days = Math.round(hours / 24);
    const weeks = Math.round(days / 7);

    if (seconds < 60) {
        if (refresh) {
            setTimeout(refresh, 1000);
        }
        return __('just now');
    } else if (minutes < 60) {
        if (refresh) {
            setTimeout(refresh, 1000 * 60);
        }
        return __('$1 min', minutes);
    } else if (hours < 24) {
        if (refresh) {
            setTimeout(refresh, 1000 * 60 * 60);
        }
        return __('$1h', hours);
    } else if (days < 7) {
        return days === 1
            ? __('1 day')
            : __('$1 days', days);
    }

    return weeks === 1
        ? __('1 week')
        : __('$1 weeks', weeks);
}

const describeTimeInterval = (milliseconds: number, refresh?: RefreshFn): string => {
    const seconds = Math.round(milliseconds / 1000);
    const minutes = Math.round(seconds / 60);
    const hours = Math.round(minutes / 60);
    const days = Math.round(hours / 24);
    const weeks = Math.round(days / 7);

    if (seconds < 60) {
        if (refresh) {
            setTimeout(refresh, 1000);
        }
        return __('second');
    } else if (minutes < 60) {
        if (refresh) {
            setTimeout(refresh, 1000 * 60);
        }
        if (minutes === 1) {
            return __('minute');
        }
        return __('$1 minutes', minutes);
    } else if (hours < 24) {
        if (refresh) {
            setTimeout(refresh, 1000 * 60 * 60);
        }
        if (hours === 1) {
            return __('hour');
        }
        return __('$1h', hours);
    } else if (days < 7) {
        if (days === 1) {
            return __('day');
        }
        return __('$1 days', days);
    }

    if (weeks === 1) {
        return __('week');
    }
    return __('$1 weeks', weeks);
}

export default () => {
    const now = ref(new Date());

    const timeAgo = (dateString: string): string => {
        if (!dateString) {
            return __('never');
        }
        const date = new Date(dateString);
        const relativeTime = now.value.getTime() - date.getTime();
        return describeTime(relativeTime);
    }

    return {
        describeTime,
        describeTimeInterval,
        timeAgo,
    }
}
