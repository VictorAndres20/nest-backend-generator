// npm install crypto-js
// npm i --save-dev @types/crypto-js
import CryptoJS from 'crypto-js';

const PHRASE = 'AjksYut56uYhkbttj896KJ6GHrfTe4D';

export const crypt = (content: string) => {
  return CryptoJS.AES.encrypt(content, PHRASE).toString();
};

export const decrypt = (encrypted: string) => {
  const decryptedBytes = CryptoJS.AES.decrypt(encrypted, PHRASE);
  return decryptedBytes.toString(CryptoJS.enc.Utf8);
};
