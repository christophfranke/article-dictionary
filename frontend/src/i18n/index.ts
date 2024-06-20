export default (key: string, ...args: string[]): string => {
    const translation = key
    return args.reduce((text, arg, index) => text.replace(`$${index+1}`, arg), translation)
}
