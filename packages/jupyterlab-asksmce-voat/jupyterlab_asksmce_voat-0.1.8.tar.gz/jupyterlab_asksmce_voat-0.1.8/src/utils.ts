import { Dialog, showDialog } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotification } from "jupyterlab_toastify";
import isEmpty from 'lodash.isempty';

import { EditSettingsWidget } from "./widgets/EditSettingsWidget"

export function loadSetting(setting: ISettingRegistry.ISettings): string {
    // Read the settings and convert to the correct type
    let atlasId = setting.get('atlasId-asksmce').composite as string;
    return atlasId;
}

export async function saveSetting(setting: ISettingRegistry.ISettings, atlasId: string): Promise<string> {
    // Read the settings and convert to the correct type
    await setting.set('atlasId-asksmce', atlasId);
    return atlasId;
}

export async function configureNewAtlas(settings: ISettingRegistry, pluginId: string): Promise<any> {
    // Load the current Atlas ID from settings
    let currentAtlasID = await Promise.all([settings.load(pluginId)])
        .then(([setting]) => {
            return loadSetting(setting);
        }).catch((reason) => {
            INotification.error(`Could not get the configuration. Please contact the administrator.`, { autoClose: 3000 });
            console.error(
                `Something went wrong when getting the current atlas id.\n${reason}`
            );
        });
    // Pass it to the AtlasIdPrompt to show it in the input
    const newAtlasID = await showDialog({
        body: new EditSettingsWidget(currentAtlasID || ""),
        buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Save" })],
        focusNodeSelector: "input",
        title: "Settings"
    })

    if (newAtlasID.button.label === "Cancel") {
        return;
    }

    if (isEmpty(newAtlasID.value)) {
        INotification.error(`Please, insert a valid Atlas Id. Visit help.voiceatlas.com for more information.`, { autoClose: 3000 });
        return;
    }

    // Show notification perhaps using jupyterlab_toastify
    // Save new atlas id in settings
    await Promise.all([settings.load(pluginId)])
        .then(([setting]) => {
            setting.set('atlasId-asksmce', newAtlasID.value)
            INotification.success('Success', {
                autoClose: 3000
            });
            return newAtlasID.value
        }).catch((reason) => {
            INotification.error(`Could not save the configuration. Please contact the administrator.`, {
                autoClose: 3000
            });
            console.error(
                `Something went wrong when setting a new atlas id.\n${reason}`
            );
        });
}