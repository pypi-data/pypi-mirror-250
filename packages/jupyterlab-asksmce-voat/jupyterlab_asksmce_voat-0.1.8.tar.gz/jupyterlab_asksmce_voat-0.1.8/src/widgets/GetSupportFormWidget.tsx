import { ReactWidget } from "@jupyterlab/apputils";
import React from 'react';
import GetSupportFormComponent from '../components/GetSupportFormComponent'

interface IUserInfo {
    username: string;
}

export class GetSupportFormWidget extends ReactWidget {
    userInfo: IUserInfo;

    constructor(userInfo: IUserInfo) {
        super()
        this.userInfo = userInfo
    }

    render(): JSX.Element {
        return <GetSupportFormComponent userInfo={this.userInfo} />
    }
}

