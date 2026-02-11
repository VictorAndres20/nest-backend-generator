// npm install bcrypt
// npm i --save-dev @types/bcrypt
import bcrypt from 'bcrypt';

const saltOrRounds = 10;

export const generateSalt = (): string => {
  return bcrypt.genSaltSync(saltOrRounds);
};

export const encryptText = (text: string): string => {
  return bcrypt.hashSync(text, saltOrRounds);
};

export const isSameEncrypted = (text: string, crypt: string): boolean => {
  return bcrypt.compareSync(text, crypt);
};
