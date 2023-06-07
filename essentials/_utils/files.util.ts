import * as fs from 'fs';
import * as crypto from 'crypto';
import * as path from 'path';

export const getRandomFileName = () => {
    return crypto.randomUUID();
}

export const writeInternalFile = (pathFile: string, fileName: string, jsonContent: string) => {
  try {
    fs.writeFileSync(path.join(pathFile, fileName), jsonContent, 'utf8');
  } catch(err) {
    console.log(err.message);
    throw new Error(err.message);
  }
}

export const readBase64InternalFile = (pathFile: string, fileName: string) : string => {
  try {
    return fs.readFileSync(path.join(pathFile, fileName), {encoding: 'base64'});
  } catch(err) {
    console.log(err.message);
    throw new Error(err.message);
  }
}

export const deleteInternalFile = (pathFile: string, fileName: string) => {
  try {
    fs.unlinkSync(path.join(pathFile, fileName))
  } catch(err) {
    console.log(err.message);
    throw new Error(err.message);
  }
}

