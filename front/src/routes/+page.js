/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
    //TODO later should be user's token
    var tokenTeacher = '3549';
    const res = await fetch(`/scheduler?teacherId=${tokenTeacher}`);
    return await res.json();
}
