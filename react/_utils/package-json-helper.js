import packageJson from '../../package.json';

export const app_version = () => {
    return packageJson.version;
}