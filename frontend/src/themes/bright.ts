import darken from './helper/darken';

const baseColors = {
    viewColor: "#007bff",
    actionColor: "#4caf50",
    errorColor: "#f8d7da",
};

const wordColors = {
    new: "rgba(51, 153, 255, 0.15)",
    seen: "rgba(255, 191, 128, 0.25)",
    mark: "rgba(204, 22, 22, 0.5)",
}

export default {
    fontFamily: "'Helvetica Neue', 'Arial', sans-serif",

    background100: "#fff",
    background98: "#f8f8f8",
    background95: "#f2f2f2",
    background80: "#ddd",

    foreground100: "#333",
    foreground95: "#444",
    foreground90: "#555",
    foreground80: "#666",

    viewColor: baseColors.viewColor,
    viewColorHover: darken(baseColors.viewColor, 10),

    actionColor: baseColors.actionColor,
    actionColorHover: darken(baseColors.actionColor, 10),

    errorColor: baseColors.errorColor,
    errorColorDark: darken(baseColors.errorColor, 10),
    errorColorDarker: darken(baseColors.errorColor, 30),

    contentNewWordColor: wordColors.new,
    contentSeenWordColor: wordColors.seen,
    contentMarkWordColor: wordColors.mark,
    tableHighlightColor: wordColors.seen,

    internalLinkColor: baseColors.viewColor,
};
