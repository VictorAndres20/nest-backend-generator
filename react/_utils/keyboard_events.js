export const isEnterKeyPressed = (key) => {
    return (key === 13)
}

export const enterKeyHandler = (event, callBack) => {
    if(isEnterKeyPressed(event.keyCode)){
        callBack();
    }
}