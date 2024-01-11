import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { PageConfig } from '@jupyterlab/coreutils'
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Dialog, MainAreaWidget, showDialog } from '@jupyterlab/apputils';
import { ILauncher } from "@jupyterlab/launcher";
import { Menu, Widget } from '@lumino/widgets';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ChatlasWidget } from './widgets/ChatlasWidget';
import { GetSupportFormWidget } from './widgets/GetSupportFormWidget';
import { aboutVoiceAtlasDialog } from './widgets/AboutWidget';
import { loadSetting, saveSetting } from './utils';
import { getHelpIcon } from './style/IconsStyle'

const PLUGIN_ID = 'jupyterlab_asksmce_voat:plugin'
const plugin: JupyterFrontEndPlugin<void> = {
    id: PLUGIN_ID,
    requires: [IMainMenu, ISettingRegistry, ILauncher],
    autoStart: true,
    activate
};

let atlasId = '';

async function activate(app: JupyterFrontEnd, mainMenu: IMainMenu, settings: ISettingRegistry, launcher: ILauncher): Promise<void> {
    console.log('JupyterLab extension jupyterlab_asksmce_voat is activated!');
    const openChatlas = 'jupyterlab_asksmce_voat:openChatlas';
    const getSupport = 'jupyterlab_asksmce_voat:getSupport';
    const aboutVoiceAtlas = 'jupyterlab_asksmce_voat:aboutVoiceAtlas';

    Promise.all([app.restored, settings.load(PLUGIN_ID)])
        .then(async ([, setting]) => {
            // await saveSetting(setting, '59e9d968-9c6a-45b3-aa07-cbdc5207e406')
            //await saveSetting(setting, 'ec30b07b-6f09-4529-ba28-9cb7ed23b8e0')
            await saveSetting(setting, '59e9d968-9c6a-45b3-aa07-cbdc5207e406')
            atlasId = loadSetting(setting);
        }).catch((reason) => {
            console.error(
                `Something went wrong when changing the settings.\n${reason}`
            );
        });

    const menu = new Menu({ commands: app.commands });
    menu.title.label = 'OSS Support'

    app.commands.addCommand(openChatlas, {
        label: 'Support Chat',
        caption: 'Support Chat',
        icon: (args) => (args["isPalette"] ? undefined : getHelpIcon),
        execute: async () => {
            const content = new ChatlasWidget(atlasId)
            content.title.label = 'Chatlas for JupyterLab';
            const widget = new MainAreaWidget<ChatlasWidget>({ content })
            app.shell.add(widget, 'main');
        }
    });

    app.commands.addCommand(getSupport, {
        label: 'Support Form',
        caption: 'Support Form',
        execute: async () => {
            const currentUser = PageConfig.getOption('serverRoot').split('/')[2] || ""
            const content = new GetSupportFormWidget({ username: currentUser })
            content.title.label = 'Contact Support';
            Widget.attach(content, document.body)
        }
    });

    app.commands.addCommand(aboutVoiceAtlas, {
        label: 'About OSS Support',
        caption: 'About OSS Support',
        execute: async () => {
            const { aboutBody, aboutTitle } = aboutVoiceAtlasDialog();
            const result = await showDialog({
                title: aboutTitle,
                body: aboutBody,
                buttons: [
                    Dialog.createButton({
                        label: 'Dismiss',
                        className: 'jp-About-button jp-mod-reject jp-mod-styled'
                    })
                ]
            });

            if (result.button.accept) {
                return;
            }
        }
    })

    menu.addItem({ command: openChatlas });
    menu.addItem({ command: getSupport });
    menu.addItem({ type: 'separator' });
    menu.addItem({ command: aboutVoiceAtlas });

    mainMenu.addMenu(menu, { rank: 2000 });

    if (launcher) {
        console.log('There is launcher')
        launcher.add({
            command: openChatlas,
            category: "SMCE Services",
            args: { isLauncher: true }
        });
    } else {
        console.log('There is launcher')
    }
}

export default plugin;
