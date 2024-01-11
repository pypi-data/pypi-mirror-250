import React, { useState } from "react";
import {
    DialogContent,
    DialogTitle,
    CssBaseline,
    TextField,
    Grid,
    DialogContentText
} from '@mui/material';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';

// const FORM_ENDPOINT = ""; // TODO - fill on the later step

interface IUserInfo {
    username: string;
}

interface IUserProps {
    userInfo: IUserInfo;
}

const GetSupportFormComponent: React.FC<IUserProps> = (IUserProps): JSX.Element => {
    const [window, setWindowState] = useState(true)
    const [subject, setSubject] = useState("")
    const [description, setDescription] = useState("")

    const _handleSubmit = (event: any) => {
        event.stopPropagation();
        console.log(`Username => ${IUserProps.userInfo.username}`)
        console.log(`Subject => ${subject}`)
        console.log(`Description => ${description}`)
        setWindowState(false)
    };

    // const _onClick = (event: any): void => {
    //     event.stopPropagation();
    //     setWindowState(false)
    //     console.log(`Window State Click => ${window}`)
    // }

    const _onClose = (event: any): void => {
        event.stopPropagation();
        setWindowState(false)
        console.log(`Window State Close => ${window}`)
    }

    return (
        <React.Fragment>
            <CssBaseline />
            <Dialog
                open={window}
                //onClick={_onClick}
                onClose={_onClose}
                maxWidth='sm'
                fullWidth
                scroll='paper'
                onBackdropClick={_onClose}
            >
                <DialogTitle>
                    Contact Support
                </DialogTitle>
                <DialogContent>
                    <DialogContentText >
                        We would love to hear from you. Please, fill up the form. We will get in touch as soon as we can.
                    </DialogContentText>
                    <Grid
                        container
                        direction="column"
                        justifyContent="center"
                        alignItems="stretch"
                        spacing={2}
                        sx={{ mt: 2 }}
                    >
                        <form onSubmit={_handleSubmit}>
                            <Grid
                                item
                                container
                                direction="column"
                                justifyContent="center"
                                alignItems="stretch"
                                spacing={2}
                                sx={{ margin: 'auto', padding: 'auto' }}
                            >
                                <Grid item sx={{ pr: '16px' }}>
                                    <TextField
                                        id="name-input"
                                        name="name"
                                        label="Name"
                                        type="text"
                                        variant='outlined'
                                        value={IUserProps.userInfo.username}
                                        fullWidth
                                        disabled
                                    />
                                </Grid>
                                <Grid item sx={{ pr: '16px' }}>
                                    <TextField
                                        id="subject-input"
                                        name="subject"
                                        label="Subject"
                                        type="text"
                                        variant='outlined'
                                        value={subject}
                                        placeholder="Short description of the issue/suggestion/comment/recommendation."
                                        onChange={event => setSubject(event.target.value)}
                                        fullWidth
                                        required
                                    />
                                </Grid>
                                <Grid item sx={{ pr: '16px' }}>
                                    <TextField
                                        id="description-input"
                                        name="description"
                                        label="Description"
                                        type="text"
                                        variant='outlined'
                                        value={description}
                                        placeholder="Long description of the issue/suggestion/comment/recommendation."
                                        onChange={event => setDescription(event.target.value)}
                                        multiline
                                        maxRows={5}
                                        rows={5}
                                        fullWidth
                                        required
                                    />
                                </Grid>
                                <Grid
                                    container
                                    justifyContent="flex-end"
                                    alignItems="center"
                                    spacing={2}
                                    sx={{ mt: 2 }}
                                >
                                    <Grid item>
                                        <Button variant="contained" color="primary" onClick={_handleSubmit} autoFocus >Submit</Button>
                                    </Grid>
                                    <Grid item>
                                        <Button variant="contained" color="primary" onClick={_onClose}>Close</Button>
                                    </Grid>

                                </Grid>

                            </Grid>
                        </form>
                    </Grid>
                </DialogContent>
            </Dialog>
        </React.Fragment>
    )
};

export default GetSupportFormComponent;