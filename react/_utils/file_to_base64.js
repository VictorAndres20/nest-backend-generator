export const toBase64 = (file) => (
    new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            return resolve(buildResultReaderParts(reader.result));
        }
        reader.onerror = error => reject(error);
    })
);

export const getFile = (id_input) => {
    let files = document.getElementById(id_input).files;
    if(files.length === 0){
        throw new Error('No file selected');
    }
    return files[0];
};

export const buildResultReaderParts = (result) => {
    let parts = result.split(';');
    let info = parts[0].split('/');
    let bytes = parts[1].split(',');
    return {
        type: info[0],
        extension: info[1],
        bytes64: bytes[1],
    };
}