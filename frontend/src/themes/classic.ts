import darken from './helper/darken';

const baseColors = {
    viewColor: "#51779f",
    actionColor: "#387b3b",
    errorColor: "#f8d7da",
};

const wordColors = {
    new: "rgba(51, 153, 255, 0.15)",
    seen: "rgba(255, 191, 128, 0.25)",
    mark: "rgba(204, 22, 22, 0.5)",
}

const background = {    
    background100: "#fff",
    background98: "#f8f8f8",
    background95: "#f2f2f2",
    background80: "#ddd",
}

const foreground = {
    foreground100: "#333",
    foreground95: "#444",
    foreground90: "#555",
    foreground80: "#666",
}


export default {
    fontFamily: "'Times New Roman', serif",
    fontWeight: "normal",

    background100: background.background100,
    background98: background.background98,
    background95: background.background95,
    background80: background.background80,

    foreground100: foreground.foreground100,
    foreground95: foreground.foreground95,
    foreground90: foreground.foreground90,
    foreground80: foreground.foreground80,

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

    headerBackgroundColor: foreground.foreground95,
    headerHoverColor: foreground.foreground90,
    headerFontColor: background.background95,

    internalLinkColor: baseColors.viewColor,
};
