import { JSX } from 'react';
import MyPage from './my-page';
import { my_page_path } from './path-pages';

export interface RouterPage {
  path: string;
  component: () => JSX.Element;
}

export interface RouterPageWithChildren extends RouterPage {
  children?: RouterPage[];
}

export type RouterPages = Array<RouterPage | RouterPageWithChildren>;

/**
 * {
 *      path: `${my_page_path.path}`,
 *      component: MyPage,
 * },
 * //Nested
 * {
 *      path: `${parent_path.path}`,
 *      component: ParentTemplate, // This has <Outlet /> Component
 *      children: [
 *          {
 *              path: `${child_path.path}`,
 *              component: ChildPage,
 *          },
 *      ],
 * },
 *
 */

export const router_pages: RouterPages = [
  // My Page
  {
    path: `${my_page_path.path}`,
    component: MyPage,
  },
  // More pages
];
