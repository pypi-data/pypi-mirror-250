"use strict";
(self["webpackChunkjupyterlab_jupyterbook_navigation"] = self["webpackChunkjupyterlab_jupyterbook_navigation"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param browser_dir Current broswer directory as a string
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = "", browser_dir = "", init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    let requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, "jupyterlab-jupyterbook-navigation", // API Namespace
    endPoint);
    // Include browser_dir in the request
    if (browser_dir) {
        requestUrl += `?browser_dir=${encodeURIComponent(browser_dir)}`;
    }
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log("Not a JSON response body.", response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__);





const plugin = {
    id: "jupyterlab-jupyterbook-navigation:plugin",
    description: "A JupyterLab extension that mimics jupyter-book chapter navigation on an un-built, cloned jupyter book in JupyterLab.",
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__.IDocumentManager],
    activate: async (app, shell, fileBrowserFactory, docManager) => {
        console.log("JupyterLab extension jupyterlab-jupyterbook-navigation is activated!");
        // Create the widget only once
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget();
        widget.id = "@jupyterlab-sidepanel/jupyterbook-toc";
        // widget.title.iconClass = 'jp-NotebookIcon jp-SideBar-tabIcon';
        widget.title.iconClass = "jbook-icon jp-SideBar-tabIcon";
        widget.title.className = "jbook-tab";
        widget.title.caption = "Jupyter-Book Table of Contents";
        const summary = document.createElement("p");
        widget.node.appendChild(summary);
        // Attach the `activate` event handler to the widget
        widget.activate = async () => {
            console.debug("Widget shown");
            // Get the primary file browser used in JupyterLab
            const fileBrowser = fileBrowserFactory.tracker.currentWidget;
            // Check if the file browser is available and log if it's not
            if (!fileBrowser) {
                console.debug("File browser widget is null.");
            }
            else {
                console.debug("Active file browser widget found.");
            }
            // Make the API request and update the widget's content
            try {
                const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("get-toc", fileBrowser === null || fileBrowser === void 0 ? void 0 : fileBrowser.model.path);
                console.log(data);
                summary.innerHTML = data["data"];
                // Add the button event listener after the widget's content is updated
                addClickListenerToButtons(fileBrowser, docManager);
                addClickListenerToChevron();
            }
            catch (reason) {
                console.error(`The jupyterlab_jupyterbook_navigation server extension appears to be missing.\n${reason}`);
            }
        };
        // Add the widget to the sidebar
        shell.add(widget, "left", { rank: 400 });
        widget.activate();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
function addClickListenerToChevron() {
    const buttons = document.querySelectorAll(".toc-chevron");
    buttons.forEach(buttonElement => {
        // Perform a type assertion here
        const button = buttonElement;
        button.addEventListener("click", (event) => {
            console.log(`Button clicked`);
            toggleList(button);
        });
    });
}
function toggleList(button) {
    var _a;
    const list = (_a = button.parentElement) === null || _a === void 0 ? void 0 : _a.nextElementSibling; // Type assertion for HTMLElement
    if (list.style.display === "none") {
        list.style.display = "block";
        button.innerHTML = '<i class="fa fa-chevron-up toc-chevron"></i>';
    }
    else {
        list.style.display = "none";
        button.innerHTML = '<i class="fa fa-chevron-down toc-chevron"></i>';
    }
}
function addClickListenerToButtons(fileBrowser, docManager) {
    const buttons = document.querySelectorAll(".toc-button");
    buttons.forEach(button => {
        button.addEventListener("click", (event) => {
            console.log(`Button clicked`);
            // Check if the file browser is available
            if (!fileBrowser) {
                console.error("File browser is not available.");
                return;
            }
            // Check if the file browser's path is a valid string
            if (typeof fileBrowser.model.path !== "string") {
                console.error(`Invalid path: The current path is either not set or not a string. Path: ${fileBrowser.model.path}`);
                return;
            }
            // If all checks pass, log the current directory
            console.log(`Current directory: ${fileBrowser.model.path}`);
            const browser_path = fileBrowser.model.path;
            const filePath = button.getAttribute("data-file-path");
            if (typeof filePath === "string") {
                if (filePath.includes(".md")) {
                    docManager.openOrReveal(browser_path + "/" + filePath, "Markdown Preview");
                }
                else {
                    docManager.openOrReveal(browser_path + "/" + filePath);
                }
            }
        });
    });
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.cd5cb15f950bb595dcfd.js.map