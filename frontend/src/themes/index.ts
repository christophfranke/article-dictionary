import dark from './dark';
import bright from './bright';
import classic from './classic';
import setCssVariables from './helper/setVariables';

const themes: { [key: string]: { [key: string]: string } } = {
  dark,
  bright,
  classic,
}

let currentTheme = ''
export const setTheme = (theme: string = 'bright'): void => {
  if (theme in themes) {
    currentTheme = theme;
    setCssVariables(themes[theme]);
  } else {
    console.log(`Theme ${theme} not found`);
  }
}

export const getTheme = () => themes[currentTheme];
export const getThemeName = () => currentTheme;
export const setInitialTheme = () => {
  if (!currentTheme) {
    setTheme();
  }
}
