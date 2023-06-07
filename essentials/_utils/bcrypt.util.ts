//npm install bcrypt
import * as bcrypt from 'bcrypt';

const saltOrRounds = 10;

export const generateSalt = () => {
    return bcrypt.genSaltSync(saltOrRounds);
}

export const cryptText = (text: string): string => {
    return bcrypt.hashSync(text, saltOrRounds);
}

export const isSameCrypted = (text: string, crypt: string): boolean => {
    return bcrypt.compareSync(text, crypt);
}