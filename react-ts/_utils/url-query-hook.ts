/* IMPLEMENTATION in component
imports ...
...

function Component(){
	...

	const query = useQuery();
	...
	query.get("param");
}

*/

import React from 'react';
import { useLocation } from 'react-router-dom';

export const useQuery = () => {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
};
