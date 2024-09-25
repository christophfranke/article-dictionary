import { watchEffect, ref, computed } from 'vue';

export default (props: any) => {  
    const isInViewport = (element: HTMLElement) => {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    watchEffect(() => {
        if (props.display.behaviour.scroll && props.dictionary.isVisible(props.highlight)) {
            const word = props.dictionary.find(props.highlight)!;
            const elem = document.getElementById(`word-${word.id}`);
            if (elem && !isInViewport(elem)) {
                elem.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });
}
