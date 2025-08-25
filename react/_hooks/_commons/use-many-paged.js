import { useCallback, useEffect, useState } from "react";
//import { message } from "antd";

const limit = 7;

export const useManyPaged = ({ fetchFunc }) => {

    const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState([]);
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(0);

    const loadData = useCallback((pageParam) => {
        if(! fetchFunc) throw new Error('No "fetchFunc" specified in "useManyPaged" hook');

        setIsLoading(true);
        fetchFunc(pageParam, limit)
        .then(json => {
            setIsLoading(false);
            setData(json.paged[0]);
            setTotal(json.paged[1]);
        })
        .catch(error => {
            setIsLoading(false);
            //message.error(error.message);
        });
    }, [fetchFunc, limit]);

    useEffect(() => {
        if(page !== undefined) loadData(page);
    }, [page, loadData]);

    return {
        isLoading,
        data,
        total,
        page,
        limit,
        setPage,
        loadData,
    }
}