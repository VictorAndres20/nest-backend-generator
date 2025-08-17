import { useCallback, useState } from "react";
//import { message } from "antd";
import { downloadPDFFile } from "../../_utils/download-file";

export const useDownloadById = ({ fetchFunc, fileName }) => {

    const [isLoading, setIsLoading] = useState(false);
    const [id, setId] = useState(null);

    const download = useCallback((paramValue, fileNameParam, callback) => {
        if(! fetchFunc) throw new Error('No "fetchFunc" specified in "useDownloadById" hook');

        setIsLoading(true);
        setId(paramValue)
        fetchFunc(paramValue)
        .then(json => {
            setIsLoading(false);
            if(! json.data.bytes) throw new Error("No bytes");
            downloadPDFFile(json.data.bytes, fileNameParam ?? fileName);
            callback?.(json);
        })
        .catch(error => {
            setIsLoading(false);
            //message.error(error.message);
        });
    }, [fetchFunc]);

    return {
        id,
        isLoading,
        download,
    }
}