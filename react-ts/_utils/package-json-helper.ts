import packageJson from '../../package.json';

export const appVersion = () => {
  return packageJson.version;
};
