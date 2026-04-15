export type SignupData = {
    name:string;
    birthdate:Date;
    phonenumber?:string;
    address:string;
    email:string;
    password:string;
}

export type LoginData = {
    email:string;
    password:string;
}