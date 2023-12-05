import { ref, onMounted, onBeforeUnmount, reactive } from 'vue';

interface TooltipPosition {
  x: number;
  y: number;
}

const useTooltip = (): { tooltipPosition: TooltipPosition } => {
  const tooltipPosition = reactive({ x: 0, y: 0 });

  const setTooltipPosition = (event: MouseEvent): void => {
    tooltipPosition.x = event.clientX + 10; // Add an offset to prevent the tooltip from overlapping with the cursor
    tooltipPosition.y = event.clientY + 20; // Adjust the offset based on your design preference
  };

  onMounted(() => {
    // Listen for mousemove events to update the tooltip position
    document.addEventListener('mousemove', setTooltipPosition);
  });

  onBeforeUnmount(() => {
    // Remove the event listener when the component is unmounted
    document.removeEventListener('mousemove', setTooltipPosition);
  });

  return { tooltipPosition };
};

export default useTooltip;
