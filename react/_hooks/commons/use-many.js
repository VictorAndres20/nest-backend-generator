import { useCallback, useEffect, useState } from "react";
//import { message } from "antd";

export const useMany = ({ fetchFunc, isMountFetch = false }) => {

    const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState([]);

    const loadData = useCallback(() => {
        if(! fetchFunc) throw new Error('No "fetchFunc" specified in "useMany" hook');

        setIsLoading(true);
        fetchFunc()
        .then(json => {
            setIsLoading(false);
            setData(json.list);
        })
        .catch(error => {
            setIsLoading(false);
            //message.error(error.message);
        });
    }, [fetchFunc]);

    useEffect(() => {
        if(isMountFetch) loadData();
    }, [isMountFetch, loadData]);

    return {
        isLoading,
        data,
        loadData,
    }
}