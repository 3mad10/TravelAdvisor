import axios from 'axios';
import { API_URL } from './config';

const BASE_URL = API_URL;
const api = axios.create({
    baseURL: BASE_URL
})

export default api;