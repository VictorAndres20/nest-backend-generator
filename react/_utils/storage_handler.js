import {crypt, decrypt} from './crypt';

const TOKEN_KEY = 'qwer';
const COMPANY_KEY = 'asdf';
const FINANCIAL_TYPE = 'poiu';
const FINANCIAL_TYPE_NAME = 'alskd';
const USER_ID_KEY = 'zxcv';
const ROL_ID_KEY = 'uiop';

export const putValue = (key, value) => {
    window.localStorage.setItem(key, crypt(value.toString()));
}

export const getValue = (key) => {
    let data = window.localStorage.getItem(key);
    if(data != null) return decrypt(data);
    else return data;
}

export const cleanValue = (key) => {
    window.localStorage.removeItem(key);
}

export const cleanValues = () => {
    window.localStorage.clear();
}

export const putToken = (token) => {
    putValue(TOKEN_KEY, token);
}

export const getToken = () => {
    return getValue(TOKEN_KEY);
}

export const putCompany = (id) => {
    putValue(COMPANY_KEY, id);
}

export const getCompany = () => {
    return Number(getValue(COMPANY_KEY));
}

export const putFinancialType = (id) => {
    putValue(FINANCIAL_TYPE, id);
}

export const getFinancialType = () => {
    return getValue(FINANCIAL_TYPE);
}

export const putFinancialTypeName = (name) => {
    putValue(FINANCIAL_TYPE_NAME, name);
}

export const getFinancialTypeName = () => {
    return getValue(FINANCIAL_TYPE_NAME);
}

export const putUserId = (id) => {
    putValue(USER_ID_KEY, id);
}

export const getUserId = () => {
    return getValue(USER_ID_KEY);
}

export const putRol = (id) => {
    putValue(ROL_ID_KEY, id);
}

export const getRol = () => {
    return getValue(ROL_ID_KEY);
}