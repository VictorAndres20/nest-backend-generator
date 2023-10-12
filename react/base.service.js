import { MAIN_API_HOST } from '../_config/api';
import { getToken } from '../_utils/storage_handler';

export const HEADERS_OPTIONS = {
    'Content-Type': 'application/json',
    "Authorization":`Bearer ${getToken()}`
};

export const GET_OPTIONS = {
    method: "GET",
    headers: HEADERS_OPTIONS
};

export const POST_OPTIONS = {
    method: "POST",
    headers: HEADERS_OPTIONS
};

export const PUT_OPTIONS = {
    method: "PUT",
    headers: HEADERS_OPTIONS
};

export const DELETE_OPTIONS = {
    method: "DELETE",
    headers: HEADERS_OPTIONS
};

export const sendFetch = (path, options, body=null) => {
    if(body !== null) options.body = JSON.stringify(body);
    return new Promise((resolve, reject) => {
        fetch(`${MAIN_API_HOST}${path}`,options)
        .then(res => {
            // console.log("Response: " + res);
            return res.json();
        })
        .then(json => resolve(json))
        .catch(err => reject(err));
    });
}

export const handleFetch = async (path, options, body) => {
    let json = await sendFetch(path, options, body);
    if(! json.ok) throw new Error(json.error);
    return json;
}