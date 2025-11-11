export const toBase64 = (file: Blob) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      return resolve(buildResultReaderParts(reader.result as string));
    };
    reader.onerror = (error) => reject(error);
  });

export const getFile = (id_input: string) => {
  const files = (document.getElementById(id_input) as HTMLInputElement)?.files;
  if (!files || files.length === 0) {
    throw new Error('No file selected');
  }
  return files[0];
};

export const buildResultReaderParts = (result: string) => {
  const parts = result.split(';');
  const info = parts[0].split('/');
  const bytes = parts[1].split(',');
  return {
    type: info[0],
    extension: info[1],
    bytes64: bytes[1],
  };
};
