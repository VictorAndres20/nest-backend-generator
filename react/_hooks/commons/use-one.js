import { useCallback, useEffect, useState } from "react";
//import { message } from "antd";

export const useOne = ({ fetchFunc, isMountFetch = false }) => {

    const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState(null);

    const loadData = useCallback(() => {
        if(! fetchFunc) throw new Error('No "fetchFunc" specified in "useOne" hook');

        setIsLoading(true);
        fetchFunc()
        .then(json => {
            setIsLoading(false);
            //console.log(json.data);
            setData(json.data);
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