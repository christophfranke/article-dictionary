import darken from './helper/darken';

const baseColors = {
    viewColor: "#0945a4",
    actionColor: "#107303",
    errorColor: "#f8d7da",
    successColor: "#109e06",
};

const foreground = {
    foreground100: "#fff",
    foreground95: "#eee",
    foreground90: "#ddd",
    foreground80: "#ccc",
};

const background = {
    background100: "#222",
    background98: "#2a2a2a",
    background95: "#333",
    background80: "#666",    
}

const wordColors = {
    new: "rgba(0, 64, 255, 0.25)",
    seen: "rgba(255, 203, 0, 0.125)",
    mark: "rgba(204, 22, 22, 0.5)",
};

export default {
    fontFamily: "'Helvetica', 'Arial', sans-serif",
    fontWeight: "lighter",

    background100: background.background100,
    background98: background.background98,
    background95: background.background95,
    background80: background.background80,

    foreground100: foreground.foreground100,
    foreground95: foreground.foreground95,
    foreground90: foreground.foreground90,
    foreground80: foreground.foreground80,

    viewColor: baseColors.viewColor,
    viewColorHover: darken(baseColors.viewColor, 7),

    actionColor: baseColors.actionColor,
    actionColorHover: darken(baseColors.actionColor, 7),

    errorColor: baseColors.errorColor,
    errorColorDark: darken(baseColors.errorColor, 10),
    errorColorDarker: darken(baseColors.errorColor, 30),

    successColor: baseColors.successColor,
    successColorDark: darken(baseColors.successColor, 10),
    successColorDarker: darken(baseColors.successColor, 30),

    contentNewWordColor: wordColors.new,
    contentSeenWordColor: wordColors.seen,
    contentMarkWordColor: wordColors.mark,
    tableHighlightColor: wordColors.seen,

    headerBackgroundColor: background.background95,
    headerFontColor: foreground.foreground100,
    headerHoverColor: baseColors.viewColor,

    internalLinkColor: foreground.foreground100,
};
