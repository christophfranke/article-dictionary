import { ref } from 'vue';

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
    return 'just now';
  } else if (minutes < 60) {
    if (refresh) {
      setTimeout(() => refresh, 1000 * 60);
    }
    return `${minutes} min`;
  } else if (hours < 24) {
    if (refresh) {
      setTimeout(refresh, 1000 * 60 * 60);
    }
    return `${hours}h`;
  } else if (days < 7) {
    return `${days} day${days > 1 ? 's' : ''}`;
  }

  return `${weeks} week${weeks > 1 ? 's' : ''}`;
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
    return 'second';
  } else if (minutes < 60) {
    if (refresh) {
      setTimeout(() => refresh, 1000 * 60);
    }
    if (minutes === 1) {
      return 'minute';
    }
    return `${minutes} minutes`;
  } else if (hours < 24) {
    if (refresh) {
      setTimeout(refresh, 1000 * 60 * 60);
    }
    if (hours === 1) {
      return 'hour';
    }
    return `${hours}h`;
  } else if (days < 7) {
    if (days === 1) {
      return 'day';
    }
    return `${days} day${days > 1 ? 's' : ''}`;
  }

  if (weeks === 1) {
    return 'week';
  }
  return `${weeks} week${weeks > 1 ? 's' : ''}`;
}

export default () => {
  const now = ref(new Date());
  const timeAgo = (dateString: string): string => {
    if (!dateString) {
      return 'never';
    }
    const date = new Date(dateString);
    const relativeTime = (now.value as any) - (date as any)
    return describeTime(relativeTime)
  }

  return {
    describeTime,
    describeTimeInterval,
    timeAgo,
  }
}
