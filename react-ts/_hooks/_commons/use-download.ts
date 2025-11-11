import { useCallback, useState } from 'react';
//import { message } from "antd";
import { downloadPdfFile } from '../../_utils/download-file';
import { HttpResponse } from '../../_services/_commons/base.types';

interface HttpResponseData {
  bytes: string;
}

interface UseDownloadByIdProps<P extends string> {
  fetchFunc: (value?: P) => Promise<HttpResponse<HttpResponseData>>;
  fileName?: string;
}

interface UseDownloadData<P extends string> {
  fileNameParam: string;
  paramValue?: P;
  callback?: (json: HttpResponse<HttpResponseData>) => void;
}

export const useDownload = <P extends string>({
  fetchFunc,
  fileName,
}: UseDownloadByIdProps<P>) => {
  const [isLoadingPdf, setIsLoadingPdf] = useState(false);

  const downloadPdf = useCallback(
    ({ fileNameParam, paramValue, callback }: UseDownloadData<P>) => {
      if (!fetchFunc)
        throw new Error('No "fetchFunc" specified in "useDownload" hook');

      setIsLoadingPdf(true);
      fetchFunc(paramValue)
        .then((json) => {
          setIsLoadingPdf(false);
          if (!json.data?.bytes) throw new Error('No bytes');
          downloadPdfFile(json.data.bytes, fileNameParam ?? fileName);
          callback?.(json);
        })
        .catch((error) => {
          setIsLoadingPdf(false);
          console.error(error.message);
          //message.error(error.message);
        });
    },
    [fetchFunc]
  );

  return {
    isLoadingPdf,
    downloadPdf,
  };
};
