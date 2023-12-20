export default (styles: Record<string, string>): void => {
  const root = document.documentElement;

  const toKebabCase = (str: string) =>
    str.replace(/([a-z])([A-Z0-9])/g, '$1-$2').toLowerCase();

  Object.entries(styles).forEach(([key, value]) => {
    const cssVarName = `--${toKebabCase(key)}`;
    root.style.setProperty(cssVarName, value);
  });
}
