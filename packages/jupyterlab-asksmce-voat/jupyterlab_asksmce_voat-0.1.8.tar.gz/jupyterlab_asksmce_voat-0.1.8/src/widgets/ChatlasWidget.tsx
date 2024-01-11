import { Widget } from '@lumino/widgets';

export class ChatlasWidget extends Widget {
    constructor(atlasId: string) {
        const script = document.createElement('script')
        // script.setAttribute("src", "https://bot.voiceatlas.mysmce.com/v1/chatlas.js")
        const cssVA = ".container-va { position: absolute; bottom: 0; left: 0; right: 0; top: 0; }"
        let head = document.head || document.getElementsByTagName('head')[0]
        const style = document.createElement('style');
        head.appendChild(style);
        style.appendChild(document.createTextNode(cssVA));

        script.setAttribute("src", "https://bot.voiceatlas.com/v1/chatlas.js")
        script.setAttribute("async", "")
        document.body.appendChild(script)

        const container = document.createElement("div")
        container.setAttribute("class", "container-va")
        container.setAttribute("style", "width:100%;")
        const chatlas = document.createElement('app-chatlas')
        chatlas.setAttribute("atlas-id", atlasId)
        chatlas.setAttribute("full-screen", "true")
        chatlas.setAttribute("voice-enabled", "true")
        container.appendChild(chatlas)
        super({ node: container })
    }
}
