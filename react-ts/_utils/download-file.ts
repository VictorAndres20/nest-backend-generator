export const downloadFile = (
  mimeType: string,
  base64bytes: string,
  fileName: string,
  extension: string
) => {
  const a = document.createElement('A') as HTMLAnchorElement;
  a.href = `data:${mimeType};base64,${base64bytes}`;
  a.target = '_blank';
  a.download = `${fileName}.${extension}`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};

export const downloadPdfFile = (base64bytes: string, fileName: string) => {
  downloadFile('application/pdf', base64bytes, fileName, 'pdf');
};

export const downloadExcelFile = (base64bytes: string, fileName: string) => {
  downloadFile(
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    base64bytes,
    fileName,
    'xlsx'
  );
};
