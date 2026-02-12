import { Link } from "react-router-dom";
// import { home_page_path } from "../../pages/path-pages";

export function NotFoundPage() {
  return (
    <div>
      <h1>Página no encontrada</h1>
      <Link to={/*home_page_path.full_path*/ ""}>Ir al inicio</Link>
    </div>
  );
}
