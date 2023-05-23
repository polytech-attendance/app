/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    //TODO later should be user's token
    var tokenTeacher = '3512';
    const res = await fetch(`http://127.0.0.1:8000/api/v1/teachers/${tokenTeacher}/schedule/?format=json`);
    return await res.json();
}
