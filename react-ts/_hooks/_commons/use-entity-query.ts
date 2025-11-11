import { useCallback, useEffect, useState } from 'react';
import { HttpResponse } from '../../_services/_commons/base.types';
// import { message } from "antd";

export interface UseEntityQueryProps<E, P> {
  fetchFunc: (filterData: P | undefined) => Promise<HttpResponse<E>>;
  filterData?: P;
  isMountFetch?: boolean;
}

export interface UseEntityData<E> {
  data?: E | null;
  list?: E[] | null;
  paged?: {
    list?: E[];
    total?: number;
  } | null;
}

export const useEntityQuery = <E, P>({
  fetchFunc,
  filterData,
  isMountFetch = false,
}: UseEntityQueryProps<E, P>) => {
  const [isLoading, setIsLoading] = useState(false);
  const [fetchedData, setFetchedData] = useState<UseEntityData<E>>({
    data: null,
    list: [],
    paged: null,
  });

  const loadData = useCallback(
    (
      paramFilterData: P | undefined,
      callback?: (json: HttpResponse<E>) => void
    ) => {
      if (!fetchFunc)
        throw new Error('No "fetchFunc" specified in "useEntityQuery" hook');

      setIsLoading(true);
      fetchFunc(paramFilterData)
        .then((json) => {
          setIsLoading(false);
          setFetchedData({
            data: json.data ?? null,
            list: json.list ?? [],
            paged: json.paged
              ? { list: json.paged[0], total: json.paged[1] }
              : null,
          });
          callback?.(json);
        })
        .catch((error) => {
          setIsLoading(false);
          console.error(error.message);
          // message.error(error.message);
        });
    },
    [fetchFunc]
  );

  useEffect(() => {
    if (isMountFetch && filterData) loadData(filterData);
  }, [isMountFetch, filterData, loadData]);

  return {
    isLoading,
    fetchedData,
    loadData,
  };
};
