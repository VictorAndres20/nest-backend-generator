export const genUuid = () => {
  return (String(1e7) + -1e3 + -4e3 + -8e3 + -1e11).replace(
    /[018]/g,
    (c: unknown | number) =>
      (
        (c as number) ^
        (crypto.getRandomValues(new Uint8Array(1))[0] &
          (15 >> ((c as number) / 4)))
      ).toString(16)
  );
};
