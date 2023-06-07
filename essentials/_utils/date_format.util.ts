export const buildClassicDateFormat = (date: Date): string => {
    return `${date.getDate()} / ${date.getMonth() + 1} / ${date.getFullYear()}`;
} 