import { useCallback, useState } from "react";
import { downloadPdfFile } from "../../../_utils/download-file";
import { type HttpResponse } from "../../_services/_commons/base.types";

interface HttpResponseData {
  bytes: string;
}

interface UseDownloadByParamProps<P> {
  fetchFunc: (value?: P) => Promise<HttpResponse<HttpResponseData>>;
  fileName?: string;
}

interface UseDownloadData<P> {
  fileNameParam: string;
  paramData?: P;
  callback?: (json: HttpResponse<HttpResponseData>) => void;
}

export const useDownload = <P>({
  fetchFunc,
  fileName,
}: UseDownloadByParamProps<P>) => {
  const [isLoadingPdf, setIsLoadingPdf] = useState(false);

  const downloadPdf = useCallback(
    async ({ fileNameParam, paramData, callback }: UseDownloadData<P>) => {
      if (!fetchFunc)
        throw new Error('No "fetchFunc" specified in "useDownload" hook');

      setIsLoadingPdf(true);
      try {
        const json = await fetchFunc(paramData);
        if (!json.data?.bytes) throw new Error("No bytes");
        downloadPdfFile(json.data.bytes, fileNameParam ?? fileName);
        callback?.(json);
      } catch (error) {
        console.error((error as Error).message);
        throw error;
      } finally {
        setIsLoadingPdf(false);
      }
    },
    [fetchFunc, fileName],
  );

  return {
    isLoadingPdf,
    downloadPdf,
  };
};
