# Pages folder in React

<p>
Change or delete my_page example page.
</p>

**Don't forget to configure path_pages and router_pages**

- path_pages.js
<p>
    File to register all paths (URLS) dor your pages application.
    Follow de structure of example object
</p>

```
export const my_page_path = {
    path: 'my-page',
    full_path: `/my-page`,
}

export const my_page2_path = {
    path: 'my-page2',
    full_path: `/my-page`,
}
```

- router_pages.js
<p>
    File for routing configuration.
    This will load App.js router using react-router-dom.
    Follow the structure.

````
export const router_pages = {
    {
         path: `${my_page_path.path}`, 
         component: MyPage, 
    },
    //Nested 
    { 
         path: `${parent_path.path}`, 
         component: ParentTemplate, // This has <Outlet /> Component
         children: [
             {
                 path: `${child_path.path}`, 
                 component: ChildPage,
             },
         ],
    },
},
````
</p>

- menu_pages.js
<p>If you need menu register</p>

```
import {
    facturabot_home_path, 
    facturabot_info_path 
} from "./path_pages";

export const facturabot_menu = {
    main: { 
        label: 'Home',
        path: `${facturabot_home_path.path}`,
        fullPath: `${facturabot_home_path.full_path}`,
    },
    info: { 
        label: 'Information',
        path: `${facturabot_info_path.path}`,
        fullPath: `${facturabot_info_path.full_path}`,
    }
}
```

<p>When you use this, you can create a menu widget loading the configuration</p>

````
import React from "react";
import { Link, Outlet } from "react-router-dom";
import { facturabot_menu } from "./menu_pages";

const FacturabotTemplate = () => {

    return(
        <>
            <ul>
            {
                Object.entries(facturabot_menu).map((module, key) => {
                    if(module[1].children){
                        return(
                            <div key={`nav_key_${module[1].path}_${key}`} >
                                {module[1].label}
                                <ul>
                                    {
                                        Object.entries(module[1].children).map((m, key) => (
                                            <li key={`nav_key_${m[1].path}_${key}`} >
                                                <Link to={`${m[1].fullPath}`}>
                                                    {m[1].label}
                                                </Link>
                                            </li>
                                        ))
                                    }
                                </ul>
                            </div>
                        );
                    }
                    return(
                        <li key={`nav_key_${module[1].path}_${key}`} >
                            <Link to={`${module[1].fullPath}`}>
                                {module[1].label}
                            </Link>
                        </li>
                    );
                })
            }
            </ul>
            <Outlet />
        </>
    );
};

export default FacturabotTemplate;
````