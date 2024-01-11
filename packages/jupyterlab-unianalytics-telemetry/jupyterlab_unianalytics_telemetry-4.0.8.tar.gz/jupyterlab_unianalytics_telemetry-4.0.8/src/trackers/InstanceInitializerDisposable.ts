import { Signal } from '@lumino/signaling';
import { IDisposable } from '@lumino/disposable';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Selectors } from '../utils/constants';
import { CompatibilityManager } from '../utils/compatibility';
import { getUnianalyticsCookie, setUnianalyticsCookie } from '../utils/utils';

export class InstanceInitializerDisposable implements IDisposable {
  constructor(panel: NotebookPanel) {
    const notebookModel = panel.context.model;

    const notebookId = CompatibilityManager.getMetadataComp(
      notebookModel,
      Selectors.notebookId
    );

    if (notebookId) {
      // if no instance_id yet,

      const notebookIdCookieMap = getUnianalyticsCookie();

      // parse the JSON string into a JavaScript object
      const notebookIdCookieDictionary = notebookIdCookieMap
        ? JSON.parse(notebookIdCookieMap)
        : {};

      // check if the notebook ID is already present in the dictionary
      if (!notebookIdCookieDictionary[notebookId]) {
        // if not, generate a new UUID and update the dictionary
        const newUUID = crypto.randomUUID();
        notebookIdCookieDictionary[notebookId] = newUUID;

        // save the updated dictionary back to the cookie
        setUnianalyticsCookie(JSON.stringify(notebookIdCookieDictionary));
      }
    }
  }

  get isDisposed(): boolean {
    return this._isDisposed;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    this._isDisposed = true;
    Signal.clearData(this);
  }

  private _isDisposed = false;
}
