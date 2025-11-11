import { MAIN_API_HOST } from '../../_config/api';
import { getToken } from '../../_utils/storage-handler';

export const buildHeadersOptions = () => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${getToken()}`,
});

export const GET_OPTIONS = {
  method: 'GET',
};

export const POST_OPTIONS = {
  method: 'POST',
};

export const PUT_OPTIONS = {
  method: 'PUT',
};

export const DELETE_OPTIONS = {
  method: 'DELETE',
};

export const sendFetch = (
  path: string,
  optionsParam: any,
  body: any = null
): any => {
  const options = { ...optionsParam, headers: buildHeadersOptions() };
  if (body !== null) options.body = JSON.stringify(body);
  return new Promise((resolve, reject) => {
    fetch(`${MAIN_API_HOST}${path}`, options)
      .then((res) => {
        // console.log("Response: " + res);
        return res.json();
      })
      .then((json) => resolve(json))
      .catch((err) => reject(err));
  });
};

export const handleFetch = async (path: string, options: any, body: any) => {
  const json = await sendFetch(path, options, body);
  if (!json.ok) throw new Error(json.error);
  return json;
};
