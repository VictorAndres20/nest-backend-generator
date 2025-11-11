export const isEnterKeyPressed = (key: string) => {
  return key === 'Enter';
};

export const enterKeyHandler = (event: KeyboardEvent, callBack: () => void) => {
  if (isEnterKeyPressed(event.key)) {
    callBack();
  }
};
