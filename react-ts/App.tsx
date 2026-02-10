import {
  BrowserRouter as Router,
  Routes as Switch,
  Route,
} from "react-router-dom";
import {
  router_pages,
  type RouterPages,
  type RouterPageWithChildren,
} from "./pages/router-pages";
import NotFoundPage from "./widgets/not-found";

function App() {
  const renderRoutes = (modules: RouterPages) => {
    return modules.map((module, key) => {
      if ((module as RouterPageWithChildren).children) {
        return (
          <Route
            path={`${module.path}`}
            element={<module.component />}
            key={`route_${module.path ?? "root"}_${key}`}
          >
            {renderRoutes((module as RouterPageWithChildren).children ?? [])}
          </Route>
        );
      }
      return (
        <Route
          path={`${module.path}`}
          element={<module.component />}
          key={`main_route_${module.path ?? "root"}_${key}`}
        />
      );
    });
  };

  return (
    <Router>
      <Switch>
        {renderRoutes(router_pages)}
        <Route path="*" element={<NotFound />} />
      </Switch>
    </Router>
  );
}

function NotFound() {
  return <NotFoundPage />;
}

export default App;
