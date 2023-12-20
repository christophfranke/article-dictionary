import dark from './dark';
import bright from './bright';
import classic from './classic';
import setCssVariables from './helper/setVariables';

const themes: { [key: string]: { [key: string]: string } } = {
  dark,
  bright,
  classic,
}

let currentTheme = 'bright'
export const setTheme = (theme: string): void => {
  if (theme in themes) {
    currentTheme = theme;
    setCssVariables(themes[theme]);
    const profile = JSON.parse(localStorage.getItem('profile') ?? '{}') ?? {};
    profile.theme = theme
    localStorage.setItem('profile', JSON.stringify(profile));
  } else {
    console.log(`Theme ${theme} not found`);
  }
}

export const getTheme = () => themes[currentTheme];
export const getThemeName = () => currentTheme;

export const setInitialTheme = () => {
  const profile = JSON.parse(localStorage.getItem('profile') ?? '{}');
  if (profile?.theme) {
    setTheme(profile.theme);
  } else {
    setTheme('bright');
  }
}
