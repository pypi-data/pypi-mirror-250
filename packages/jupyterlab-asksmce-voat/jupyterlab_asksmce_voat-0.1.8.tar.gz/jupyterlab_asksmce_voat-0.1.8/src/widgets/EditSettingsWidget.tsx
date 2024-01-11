import { Widget } from '@lumino/widgets';
import isEqual from "lodash.isequal";

export class EditSettingsWidget extends Widget {
    constructor(atlasId: string) {
        const body = document.createElement("div");
        const existingLabel = document.createElement("label");
        existingLabel.textContent = "Atlas ID:";

        const input = document.createElement("input");
        input.value = isEqual(atlasId, "") ? "" : atlasId;
        input.placeholder = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";

        body.appendChild(existingLabel);
        body.appendChild(input);

        super({ node: body });
    }

    get inputNode() {
        return this.node.getElementsByTagName("input")[0];
    }

    getValue() {
        return this.inputNode.value;
    }
}
