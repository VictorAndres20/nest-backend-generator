/* IMPLEMENTATION in component
imports ...
...

function Component(){
	...

	const urlQuery = useUrlQuery();
	...
	urlQuery.get("param");
}

*/

import React from 'react';
import { useLocation } from 'react-router-dom';

export const useUrlQuery = () => {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
};
