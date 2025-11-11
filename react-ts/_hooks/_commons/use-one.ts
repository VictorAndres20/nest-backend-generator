import { useEntityQuery, UseEntityQueryProps } from './use-entity-query';
//import { message } from "antd";

export const useOne = <E, P>({
  fetchFunc,
  filterData,
  isMountFetch = false,
}: UseEntityQueryProps<E, P>) => {
  const { isLoading, fetchedData, loadData } = useEntityQuery({
    fetchFunc,
    filterData,
    isMountFetch,
  });

  return {
    isLoading,
    data: fetchedData.data,
    loadData,
  };
};
