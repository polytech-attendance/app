import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/subjects/${params.subject_id}/attendance/?format=json`);
    if (res.ok) {
        return await res.json();
    } else {
        throw error(404, 'Not found');
    }
}