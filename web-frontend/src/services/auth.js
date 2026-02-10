import API from "./api";

export const loginUser = (data) =>
  API.post("api/login/", data);

export const registerUser = (data) =>
  API.post("api/register/", data);
