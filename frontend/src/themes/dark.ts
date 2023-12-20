import darken from './helper/darken';

const baseColors = {
    viewColor: "#0945a4",
    actionColor: "#107303",
    errorColor: "#f8d7da",
};

const foregroundColors = {
    foreground100: "#fff",
    foreground95: "#eee",
    foreground90: "#ddd",
    foreground80: "#ccc",
};

const wordColors = {
    new: "rgba(0, 64, 255, 0.25)",
    seen: "rgba(255, 203, 0, 0.125)",
    mark: "rgba(204, 22, 22, 0.5)",
};

export default {
    fontFamily: "'Helvetica', 'Arial', sans-serif",

    background100: "#222",
    background98: "#2a2a2a",
    background95: "#333",
    background80: "#666",

    foreground100: foregroundColors.foreground100,
    foreground95: foregroundColors.foreground95,
    foreground90: foregroundColors.foreground90,
    foreground80: foregroundColors.foreground80,

    viewColor: baseColors.viewColor,
    viewColorHover: darken(baseColors.viewColor, 7),

    actionColor: baseColors.actionColor,
    actionColorHover: darken(baseColors.actionColor, 7),

    errorColor: baseColors.errorColor,
    errorColorDark: darken(baseColors.errorColor, 10),
    errorColorDarker: darken(baseColors.errorColor, 30),

    contentNewWordColor: wordColors.new,
    contentSeenWordColor: wordColors.seen,
    contentMarkWordColor: wordColors.mark,
    tableHighlightColor: wordColors.seen,

    internalLinkColor: foregroundColors.foreground100,
};
