import { useCallback, useEffect, useState } from "react";
// import { message } from "antd";

export const useByValue = ({ fetchFunc, value = null, isMountFetch = false, keyData = 'data', transformFunc }) => {

    const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState(keyData === 'data' ? null : []);

    const loadData = useCallback((paramValue, callback) => {
        if(! fetchFunc) throw new Error('No "fetchFunc" specified in "useById" hook');

        setIsLoading(true);
        fetchFunc(paramValue)
        .then(json => {
            setIsLoading(false);
            setData(transformFunc?.(json[keyData]) ?? json[keyData]);
            callback?.(json);
        })
        .catch(error => {
            setIsLoading(false);
            // message.error(error.message);
        });
    }, [fetchFunc]);

    useEffect(() => {
        if(isMountFetch && value) loadData(value);
    }, [isMountFetch, value, loadData]);

    return {
        isLoading,
        data,
        loadData,
    }
}