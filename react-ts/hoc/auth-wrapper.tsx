import React, { type JSX } from "react";
import { getToken } from "../_utils/storage-handler";
import { Link } from "react-router-dom";

/*
Change validateSession function as your needs
And more validations if you need

To use it
called like

import AuthWrapper from './hoc/auth_wrapper';
const AuthComponent = AuthWrapper(MainRouter) as unknown as () => JSX.Element;

Like this create a new Component that is wrapped by AuthWarpper

*/

const validateSession = (token: string | null) => {
  if (token == null) {
    return false;
  }

  return true;
};

const AuthWrapper = (AuthComponent: () => JSX.Element) =>
  class extends React.Component {
    override render() {
      if (validateSession(getToken())) {
        /* Uncomment to validate roles too
        let route = document.location.pathname.replace('/content/', '');
        if (!validate_route_rol(route, getRol())) {
          return (
            <Result
              status="error"
              title="No estas autorizado"
              subTitle="¡Tus permisos de usuario no te permiten realizar esta acción!"
              extra={[
                <Button
                  onClick={() => (window.location.href = '/')}
                  type="primary"
                  key="console"
                >
                  Ir a login
                </Button>,
              ]}
            />
          );
        }
        */
        return <AuthComponent {...this.props} />;
      }

      return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            padding: "20px 20px",
          }}
        >
          <span>¡Ingreso no autorizado!</span>
          <span>Debes iniciar sesión para ingresar</span>
          <Link to={"/"}>Ir a login</Link>
        </div>
      );
    }
  };

export default AuthWrapper;
