"use strict";
(self["webpackChunkonesait_platform_jupyter4"] = self["webpackChunkonesait_platform_jupyter4"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/** Import to use the Onesait Platform settings */

/** Import to add commands to the Command Palette */

/** Import to open the file management */


/** Import to add notification popups */

/** Import the icon for the command palette. If changed, remember
 * to update the plugin.json jupyter.lab.setting-icon */


/**
 * Initialization data for the onesait_platform_jupyter4 extension.
 */
const PLUGIN_ID = 'onesait_platform_jupyter4:plugin';
const plugin = {
    /** Set the ID of the schema/ config JSON --> extension:name */
    id: PLUGIN_ID,
    description: 'A JupyterLab 4 extension to use with Onesait Platform',
    autoStart: true,
    optional: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry,
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory
    ],
    activate: (app, settings, manager, palette, factory) => {
        console.log('Onesait Platform JupyterLab 4 extension is activated.\nv1.0.0');
        const { commands } = app;
        const command = 'onesait-platform-command-export-notebooks';
        /** Set the Onesait Platform settings values */
        let url = '';
        let token = '';
        let overwrite = false;
        let importAuthorizations = false;
        /** This function will update the setting values when updated */
        function updateSetting(setting) {
            // Read the settings and convert to the correct type
            url = setting.get('op_url').composite;
            token = setting.get('op_token').composite;
            overwrite = setting.get('op_overwrite').composite;
            importAuthorizations = setting.get('op_importAuthorizations')
                .composite;
        }
        const getNotebook = async (file) => {
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
        const exportNotebook = async (url, json, token) => {
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
                icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.extensionIcon,
                caption: 'Export the selected Notebooks to Onesait Platform Zeppelin Notebooks',
                execute: async (args) => {
                    /** Check if the user has entered the Platform URL and token */
                    if (url === '' || token === '') {
                        const warn = 'Please configure Onesait Platform URL and token data before begin to work.';
                        console.warn(warn);
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.warning(warn);
                    }
                    else {
                        /** Open the file manager to let the user to select the notebooks */
                        // TODO: filter just Notebooks
                        const dialog = _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.FileDialog.getOpenFiles({
                            manager // IDocumentManager
                            //filter: model => model.type === 'notebook' // optional (model: Contents.IModel) => boolean
                            //filter: (model: Contents.IModel) => model.type === 'notebook'
                            //filter: value => filteredItems.indexOf(value.name !== -1)
                        });
                        const result = await dialog;
                        if (result.button.accept) {
                            const files = result.value;
                            const platformApiRest = '/controlpanel/api/notebooks/import/jupyter';
                            files === null || files === void 0 ? void 0 : files.forEach(async (file) => {
                                /** Check if the file is a Notebook. This is checked
                                 * here'cause the getOpenFiles filters I'm not able
                                 * to construct the filter. */
                                // TODO: make the filter allows only Notebooks
                                if (file.type === 'notebook') {
                                    /** Get the Notebook as a JSON */
                                    const json = await getNotebook(file);
                                    /** Set the URL to fetch the Notebook */
                                    const fetchUrl = 'https://' +
                                        url +
                                        platformApiRest +
                                        '/' +
                                        file.name.replace('.ipynb', '') +
                                        '?overwrite=' +
                                        overwrite +
                                        '&importAuthorizations' +
                                        importAuthorizations;
                                    // WORKING ON IT
                                    const postNotebook = await exportNotebook(fetchUrl, json, token);
                                    if (!postNotebook.ok) {
                                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('Something went wrong while exporting the Notebook.');
                                        console.error('Something went wrong sending the Notebook to Onesait Platform.\nVerify that the URL and token are valid, or the Notebook name does not previously exist and the overwrite option is disabled.');
                                    }
                                    else {
                                        const postResponse = await postNotebook.json();
                                        const msg = 'The Notebook has been exported successfully. ID: ' +
                                            postResponse.id;
                                        //console.log('REPORT:', postResponse);
                                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.success(msg);
                                    }
                                }
                                else {
                                    const error = 'The file "' + file.name + '" is not a Notebook.';
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error(error);
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
                caption: 'Export this Jupyter Notebook to Onesait Platform Notebooks.',
                icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.extensionIcon,
                execute: () => {
                    var _a;
                    /** Check if the user has entered the Platform URL and token */
                    if (url === '' || token === '') {
                        const warn = 'Please configure Onesait Platform URL and token data before begin to work.';
                        console.warn(warn);
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.warning(warn);
                    }
                    else {
                        const file = (_a = factory.tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.selectedItems().next().value;
                        if (file) {
                            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                                title: 'Export Notebook to Onesait Platform',
                                body: 'The following Notebook will be exported: ' + file.path,
                                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton()]
                            })
                                .then(async (res) => {
                                if (res.button.label !== 'Ok') {
                                    return;
                                }
                                if (file.type === 'notebook') {
                                    const platformApiRest = '/controlpanel/api/notebooks/import/jupyter';
                                    /** Get the Notebook as a JSON */
                                    const json = await getNotebook(file);
                                    /** Set the URL to fetch the Notebook */
                                    const postUrl = 'https://' +
                                        url +
                                        platformApiRest +
                                        '/' +
                                        file.name.replace('.ipynb', '') +
                                        '?overwrite=' +
                                        overwrite +
                                        '&importAuthorizations=' +
                                        importAuthorizations;
                                    // WORKING ON IT
                                    const postNotebook = await exportNotebook(postUrl, json, token);
                                    if (!postNotebook.ok) {
                                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('Something went wrong while exporting the Notebook.');
                                        console.error('Something went wrong sending the Notebook to Onesait Platform.\nVerify that the URL and token are valid, or the Notebook name does not previously exist and the overwrite option is disabled.');
                                    }
                                    else {
                                        const postResponse = await postNotebook.json();
                                        const msg = 'The Notebook has been exported successfully. ID: ' +
                                            postResponse.id;
                                        //console.log('REPORT:', postResponse);
                                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.success(msg);
                                    }
                                }
                                else {
                                    const error = 'The file "' + file.name + '" is not a Notebook.';
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error(error);
                                }
                            })
                                .catch(e => {
                                console.error(e);
                                const error = 'Something went wrong while exporting the Notebook.';
                                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error(error);
                            });
                        }
                    }
                }
            });
        })
            .catch(reason => {
            const error = 'Something went wrong when reading the settings.';
            console.error(error + `\n${reason}`);
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error(error);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.515242cd68a93a318e25.js.map