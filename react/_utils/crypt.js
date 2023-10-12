// npm install crypto-js
import CryptoJS from 'crypto-js';

const PRHASE = 'AjksYut56uYhkbttj896KJ6GHrfTe4D';


export const crypt = (content) => {
    return CryptoJS.AES.encrypt(content, PRHASE).toString();
}


export const decrypt = (encrypted) => {
    let decryptedBytes = CryptoJS.AES.decrypt(encrypted, PRHASE);
    return decryptedBytes.toString(CryptoJS.enc.Utf8);
}