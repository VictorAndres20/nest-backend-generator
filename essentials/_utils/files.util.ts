import * as fs from 'node:fs';
import * as crypto from 'node:crypto';
import * as path from 'node:path';

export const getRandomFileName = () => {
  return crypto.randomUUID();
};

export const writeInternalFile = (
  pathFile: string,
  fileName: string,
  jsonContent: string
) => {
  fs.writeFileSync(path.join(pathFile, fileName), jsonContent, 'utf8');
};

export const readBase64InternalFile = (
  pathFile: string,
  fileName: string
): string => {
  return fs.readFileSync(path.join(pathFile, fileName), {
    encoding: 'base64',
  });
};

export const deleteInternalFile = (pathFile: string, fileName: string) => {
  fs.unlinkSync(path.join(pathFile, fileName));
};
