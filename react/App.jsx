import {
  BrowserRouter as Router,
  Routes as Switch,
  Route
} from "react-router-dom";
import { router_pages } from './pages/router_pages';
import NotFoundPage from "./widgets/not-found";

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
        <Route exact path={`${module.path}`} element={<module.component />} key={`main_route_${module.path}_${key}`} />
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
    <NotFoundPage />
  );
}

export default App;