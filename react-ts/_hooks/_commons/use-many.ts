import { useEntityQuery, UseEntityQueryProps } from './use-entity-query';
//import { message } from "antd";

export const useMany = <E, P>({
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
    list: fetchedData.list,
    loadData,
  };
};
