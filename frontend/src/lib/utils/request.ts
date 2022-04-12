import Cookies from 'js-cookie';
import { env } from '$lib/env';

export default function request(method, path, data = null) {
    const headers = {
        Accept: 'application/json',
        ...(data && { 'Content-Type': 'application/json' }),
        ...(['POST', 'PUT', 'PATCH', 'DELETE'].includes(method.toUpperCase()) && {
            'X-CSRFToken': Cookies.get('csrftoken')
        })
    };
    return fetch(`http://${env.BACKEND_HOST}:${env.BACKEND_PORT}${path}`, {
        method: method.toUpperCase(),
        credentials: 'include',
        headers,
        ...(data && { body: JSON.stringify(data) })
    });
}
