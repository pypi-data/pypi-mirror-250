import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the @dfnotebook/ipycollections-extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@dfnotebook/ipycollections-extension:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension @dfnotebook/ipycollections-extension is activated!');
  }
};

export default plugin;
