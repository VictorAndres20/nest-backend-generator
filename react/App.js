import React from 'react';
import {
  BrowserRouter as Router,
  Routes as Switch,
  Route
} from "react-router-dom";
import { router_pages } from './pages/router_pages';

function App() {

  const renderRoutes = (modules) => {
    return modules.map((module, key) =>{
      if(module.children){
        return(
          <Route exact path={`${module.path}`} element={<module.component />} key={`route_${module.path}_${key}`}>
            {
              renderRoutes(module.children)
            }
          </Route>
        );
      }
      return(
        <Route exact path={`${module.path}`} element={<module.component />} key={`route_${module.path}_${key}`} />
      );
    });
  }

  return (
    <Router>
        <Switch>
          {
            renderRoutes(router_pages)
          }
          <Route path='*' element={<NotFound />} />
        </Switch>
    </Router>
  );
}

function NotFound() {
  return(
    <>Not found</>
  );
}

export default App;