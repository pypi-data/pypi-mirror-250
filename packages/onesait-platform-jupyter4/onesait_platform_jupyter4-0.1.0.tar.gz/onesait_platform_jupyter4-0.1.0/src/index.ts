import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/** Import to use the Onesait Platform settings */
import { ISettingRegistry } from '@jupyterlab/settingregistry';

/** Import to add commands to the Command Palette */
import { ICommandPalette } from '@jupyterlab/apputils';

/** Import to open the file management */
import { FileDialog, IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { IDocumentManager } from '@jupyterlab/docmanager';

/** Import to add notification popups */
import { Notification } from '@jupyterlab/apputils';

/** Import the icon for the command palette. If changed, remember
 * to update the plugin.json jupyter.lab.setting-icon */
import { extensionIcon } from '@jupyterlab/ui-components';

import { showDialog, Dialog } from '@jupyterlab/apputils';

/**
 * Initialization data for the onesait_platform_jupyter4 extension.
 */

const PLUGIN_ID = 'onesait_platform_jupyter4:plugin';

const plugin: JupyterFrontEndPlugin<void> = {
  /** Set the ID of the schema/ config JSON --> extension:name */
  id: PLUGIN_ID,
  description: 'A JupyterLab 4 extension to use with Onesait Platform',
  autoStart: true,
  optional: [
    ISettingRegistry,
    IDocumentManager,
    ICommandPalette,
    IFileBrowserFactory
  ],
  activate: (
    app: JupyterFrontEnd,
    settings: ISettingRegistry,
    manager: IDocumentManager,
    palette: ICommandPalette,
    factory: IFileBrowserFactory
  ) => {
    console.log(
      'Onesait Platform JupyterLab 4 extension is activated.\nv1.0.0'
    );

    const { commands } = app;
    const command = 'onesait-platform-command-export-notebooks';

    /** Set the Onesait Platform settings values */
    let url = '';
    let token = '';
    let overwrite = false;
    let importAuthorizations = false;

    /** This function will update the setting values when updated */
    function updateSetting(setting: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type
      url = setting.get('op_url').composite as string;
      token = setting.get('op_token').composite as string;
      overwrite = setting.get('op_overwrite').composite as boolean;
      importAuthorizations = setting.get('op_importAuthorizations')
        .composite as boolean;
    }

    const getNotebook = async (file: any) => {
      const protocol = window.location.protocol + '//';
      const host = window.location.host;
      const pathname = '/api/contents/';
      const filename = file.name;

      const notebookUrl = protocol + host + pathname + filename;

      /** GET the Notebook from the Jupyter Lab*/
      const notebook = await fetch(notebookUrl);
      const parsed = await notebook.json();
      const json = parsed.content;

      return json;
    };

    const exportNotebook = async (url: string, json: object, token: string) => {
      return await fetch(url, {
        method: 'POST',
        headers: {
          'X-OP-APIKey': token,
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
      });
    };

    Promise.all([app.restored, settings.load(PLUGIN_ID)])
      .then(([, setting]) => {
        /** Get the settings */
        updateSetting(setting);

        /** Listen for the plugin setting changes */
        setting.changed.connect(updateSetting);

        // Add the command to the palette
        commands.addCommand(command, {
          label: 'Onesait Platform: Export Notebooks...',
          icon: extensionIcon,
          caption:
            'Export the selected Notebooks to Onesait Platform Zeppelin Notebooks',
          execute: async (args: any) => {
            /** Check if the user has entered the Platform URL and token */
            if (url === '' || token === '') {
              const warn =
                'Please configure Onesait Platform URL and token data before begin to work.';
              console.warn(warn);
              Notification.warning(warn);
            } else {
              /** Open the file manager to let the user to select the notebooks */
              // TODO: filter just Notebooks
              const dialog = FileDialog.getOpenFiles({
                manager // IDocumentManager
                //filter: model => model.type === 'notebook' // optional (model: Contents.IModel) => boolean
                //filter: (model: Contents.IModel) => model.type === 'notebook'
                //filter: value => filteredItems.indexOf(value.name !== -1)
              });

              const result = await dialog;

              if (result.button.accept) {
                const files = result.value;
                const platformApiRest =
                  '/controlpanel/api/notebooks/import/jupyter';

                files?.forEach(async (file: any) => {
                  /** Check if the file is a Notebook. This is checked
                   * here'cause the getOpenFiles filters I'm not able
                   * to construct the filter. */
                  // TODO: make the filter allows only Notebooks
                  if (file.type === 'notebook') {
                    /** Get the Notebook as a JSON */
                    const json = await getNotebook(file);

                    /** Set the URL to fetch the Notebook */
                    const fetchUrl =
                      'https://' +
                      url +
                      platformApiRest +
                      '/' +
                      file.name.replace('.ipynb', '') +
                      '?overwrite=' +
                      overwrite +
                      '&importAuthorizations' +
                      importAuthorizations;

                    // WORKING ON IT
                    const postNotebook = await exportNotebook(
                      fetchUrl,
                      json,
                      token
                    );

                    if (!postNotebook.ok) {
                      Notification.error(
                        'Something went wrong while exporting the Notebook.'
                      );
                      console.error(
                        'Something went wrong sending the Notebook to Onesait Platform.\nVerify that the URL and token are valid, or the Notebook name does not previously exist and the overwrite option is disabled.'
                      );
                    } else {
                      const postResponse = await postNotebook.json();
                      const msg =
                        'The Notebook has been exported successfully. ID: ' +
                        postResponse.id;

                      //console.log('REPORT:', postResponse);

                      Notification.success(msg);
                    }
                  } else {
                    const error =
                      'The file "' + file.name + '" is not a Notebook.';
                    Notification.error(error);
                  }
                });
              }
            }
          }
        });

        const category = 'Onesait Platform Extension';
        palette.addItem({
          command,
          category,
          args: { origin: 'from palette' }
        });

        app.commands.addCommand('onesait-platform:export-single-notebook', {
          label: 'Export to Onesait Platform',
          caption:
            'Export this Jupyter Notebook to Onesait Platform Notebooks.',
          icon: extensionIcon,
          execute: () => {
            /** Check if the user has entered the Platform URL and token */
            if (url === '' || token === '') {
              const warn =
                'Please configure Onesait Platform URL and token data before begin to work.';
              console.warn(warn);
              Notification.warning(warn);
            } else {
              const file = factory.tracker.currentWidget?.selectedItems().next()
                .value;

              if (file) {
                showDialog({
                  title: 'Export Notebook to Onesait Platform',
                  body: 'The following Notebook will be exported: ' + file.path,
                  buttons: [Dialog.okButton(), Dialog.cancelButton()]
                })
                  .then(async res => {
                    if (res.button.label !== 'Ok') {
                      return;
                    }
                    if (file.type === 'notebook') {
                      const platformApiRest =
                        '/controlpanel/api/notebooks/import/jupyter';

                      /** Get the Notebook as a JSON */
                      const json = await getNotebook(file);

                      /** Set the URL to fetch the Notebook */
                      const postUrl =
                        'https://' +
                        url +
                        platformApiRest +
                        '/' +
                        file.name.replace('.ipynb', '') +
                        '?overwrite=' +
                        overwrite +
                        '&importAuthorizations=' +
                        importAuthorizations;

                      // WORKING ON IT
                      const postNotebook = await exportNotebook(
                        postUrl,
                        json,
                        token
                      );

                      if (!postNotebook.ok) {
                        Notification.error(
                          'Something went wrong while exporting the Notebook.'
                        );
                        console.error(
                          'Something went wrong sending the Notebook to Onesait Platform.\nVerify that the URL and token are valid, or the Notebook name does not previously exist and the overwrite option is disabled.'
                        );
                      } else {
                        const postResponse = await postNotebook.json();
                        const msg =
                          'The Notebook has been exported successfully. ID: ' +
                          postResponse.id;

                        //console.log('REPORT:', postResponse);

                        Notification.success(msg);
                      }
                    } else {
                      const error =
                        'The file "' + file.name + '" is not a Notebook.';
                      Notification.error(error);
                    }
                  })
                  .catch(e => {
                    console.error(e);
                    const error =
                      'Something went wrong while exporting the Notebook.';
                    Notification.error(error);
                  });
              }
            }
          }
        });
      })
      .catch(reason => {
        const error = 'Something went wrong when reading the settings.';
        console.error(error + `\n${reason}`);
        Notification.error(error);
      });
  }
};

export default plugin;
