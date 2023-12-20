import dark from './dark';
import bright from './bright';
import setCssVariables from './helper/setVariables';

const themes = {
  dark,
  bright
}

let currentTheme = 'bright'
export const setTheme = (theme: string): void => {
  if (theme in themes) {
    currentTheme = theme;
    setCssVariables(themes[theme]);
  } else {
    console.log(`Theme ${theme} not found`);
  }
}

export const getTheme = () => themes[currentTheme];
export const getThemeName = () => currentTheme;
