import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { PLUGIN_ID } from './utils/constants';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { LabIcon } from '@jupyterlab/ui-components';
import { ISignal, Signal } from '@lumino/signaling';
import { CompatibilityManager } from './utils/compatibility';
import { compareVersions } from './utils/utils';
import { dataCollectionPlugin } from './dataCollectionPlugin';

// to register the svg icon to reuse it in the settings (through schema/settings.json > jupyter.lab.setting-icon)
import schemaStr from '../style/icons/dataCollection_cropped.svg';
export const schemaIcon = new LabIcon({
  name: `${PLUGIN_ID}:schema-icon`,
  svgstr: schemaStr
});

// class that holds the value of the disabledNotebooks list and emits a signal when the value changes
class DisabledNotebooksSignaler {
  set value(newValue: string[] | null) {
    if (newValue === this._value) {
      return;
    }
    this._value = newValue;
    this._valueChanged.emit(newValue);
  }

  get value() {
    return this._value;
  }

  get valueChanged(): ISignal<this, string[] | null> {
    return this._valueChanged;
  }
  // null before the message from the other extension has been received, an array of string after
  private _value: string[] | null = null;
  private _valueChanged = new Signal<this, string[] | null>(this);
}

export const disabledNotebooksSignaler = new DisabledNotebooksSignaler();
export let isDashboardExtensionInstalled = false;

const activate = (
  app: JupyterFrontEnd,
  settingRegistry: ISettingRegistry
): void => {
  console.log(`JupyterLab extension ${PLUGIN_ID} is activated!`);

  isDashboardExtensionInstalled = app
    .listPlugins()
    .some(item => item.includes('jupyterlab_unianalytics_dashboard'));

  console.log(
    'Is dashboard extension also installed ?',
    isDashboardExtensionInstalled
  );

  if (isDashboardExtensionInstalled) {
    // do something
    window.addEventListener('message', (event: any) => {
      // check that the message was emitted from the same origin
      if (
        event.origin === window.origin &&
        event.data &&
        event.data.identifier === 'unianalytics'
      ) {
        disabledNotebooksSignaler.value = event.data.authNotebooks;
      }
    });
  }

  const targetVersion = '3.1.0';
  const appNumbers = app.version.match(/[0-9]+/g);

  if (appNumbers && compareVersions(app.version, targetVersion) >= 0) {
    const jupyterVersion = parseInt(appNumbers[0]);

    CompatibilityManager.setJupyterVersion(jupyterVersion);

    dataCollectionPlugin(app, settingRegistry);
  } else {
    console.log(`Use a more recent version of JupyterLab (>=${targetVersion})`);
  }
};

const plugin: JupyterFrontEndPlugin<void> = {
  id: `${PLUGIN_ID}:plugin`,
  autoStart: true,
  requires: [ISettingRegistry],
  activate: activate
};

export default plugin;
