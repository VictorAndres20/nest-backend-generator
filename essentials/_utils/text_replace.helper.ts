export const replace_accents = (text: string) => {
    return text
            .replace(/[Á]/g,"A")
            .replace(/[É]/g,"E")
            .replace(/[Í]/g,"I")
            .replace(/[Ó]/g,"O")
            .replace(/[Ú]/g,"U");
}