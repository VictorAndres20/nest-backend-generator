import { crypt, decrypt } from './crypt';

const TOKEN_KEY = 'qwer';
const USER_ID_KEY = 'zxcv';
const ROL_ID_KEY = 'uiop';

export const putValue = (key: string, value: string | number) => {
  window.localStorage.setItem(key, crypt(value.toString()));
};

export const getValue = (key: string) => {
  const data = window.localStorage.getItem(key);
  if (data != null) return decrypt(data);
  else return data;
};

export const cleanValue = (key: string) => {
  window.localStorage.removeItem(key);
};

export const cleanValues = () => {
  window.localStorage.clear();
};

export const putToken = (token: string) => {
  putValue(TOKEN_KEY, token);
};

export const getToken = () => {
  return getValue(TOKEN_KEY);
};

export const putUserId = (id: string) => {
  putValue(USER_ID_KEY, id);
};

export const getUserId = () => {
  return getValue(USER_ID_KEY);
};

export const putRol = (id: string) => {
  putValue(ROL_ID_KEY, id);
};

export const getRol = () => {
  return getValue(ROL_ID_KEY);
};
