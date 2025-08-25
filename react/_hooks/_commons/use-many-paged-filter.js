import { useCallback, useEffect, useState } from "react";
//import { message } from "antd";

const limit = 7;

export const useManyPagedFiltered = ({ fetchFunc }) => {

    const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState([]);
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(0);
    const [filter, setFilter] = useState('');

    const loadData = useCallback((pageParam, filter) => {
        if(! fetchFunc) throw new Error('No "fetchFunc" specified in "useManyPaged" hook');

        setIsLoading(true);
        fetchFunc(pageParam, limit, filter)
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
        if(page !== undefined) {
            if (filter){
                const getData = setTimeout(() => {
                    loadData(page, filter);
                }, 2000)
              
                return () => clearTimeout(getData);
            } else {
                loadData(page, filter);
            }
        }
    }, [page, filter, loadData]);

    return {
        isLoading,
        data,
        total,
        page,
        limit,
        filter,
        setPage,
        loadData,
        setFilter
    }
}