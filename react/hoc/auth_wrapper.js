import React from 'react';
import { getToken } from '../_utils/storage_handler';
import { Link } from 'react-router-dom';

/*
Change validateSession function as your needs
And more validations if you need 

To use it
called like

import AuthWrapper from './hoc/auth_wrapper';
const AuthComponent = AuthWrapper(MainRouter);

Like this create a new Component that is wrapped by AuthWarpper

*/

const AuthWrapper = (AuthComponent) => (
    class extends React.Component{
        render(){
            if(validateSession()){
                /*
                let route = document.location.pathname.replace("/content/", "");
                if(! validate_route_rol(route, getRol())){
                    return(
                        <Result
                            status="error"
                            title="No estas autorizado"
                            subTitle="¡Tus permisos de usuario no te permiten realizar esta acción!"
                            extra={[
                            <Button onClick={() => window.location.href = '/'} type="primary" key="console">
                                Ir a login
                            </Button>
                            ]}
                        />
                    );
                }
                */
                return(<AuthComponent {...this.props} />);
            } else {
                return(
                    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: '20px 20px' }}>
                        <span>¡Ingreso no autorizado!</span>
                        <span>Debes iniciar sesión para ingresar</span>
                        <Link to={'/'}>
                            Ir a login
                        </Link>
                    </div>
                );
            }
        }
    }
);

const validateSession = () => {
    /*
    let token = getToken();
    if(token == null){
        return false;
    }
    */
    return false;
}

export default AuthWrapper;