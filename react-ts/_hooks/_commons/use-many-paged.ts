import { useCallback, useState } from "react";
import { useEntityQuery, type UseEntityQueryProps } from "./use-entity-query";
//import { message } from "antd";

export const useManyPaged = <E, P extends { page: number; limit: number }>({
  fetchFunc,
  filterData,
  isMountFetch = false,
}: UseEntityQueryProps<E, P>) => {
  const [pagedFilterData, setPagedFilterData] = useState<P | undefined>(
    filterData,
  );

  const { isLoading, fetchedData, loadData } = useEntityQuery<E, P>({
    fetchFunc,
    filterData: pagedFilterData,
    isMountFetch,
  });

  const setPage = useCallback((page: number) => {
    setPagedFilterData((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        page,
      };
    });
  }, []);

  const setLimit = useCallback((limit: number) => {
    setPagedFilterData((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        limit,
      };
    });
  }, []);

  return {
    isLoading,
    pagedFilterData,
    paged: fetchedData.paged,
    loadData,
    setPage,
    setLimit,
  };
};
