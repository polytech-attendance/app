<script>
    export let subjectId;
    export let groupId;
    export let subjectName;
    export let groupName;
    export let lessons;
</script>

<table>
    <thead>
        <tr>
            {#each lessons[0].attendance_list as {abbrev_name, id, is_foreign, group_id} (id)}
                <td class:foreign={is_foreign}>{abbrev_name}</td>
            {/each}
        </tr>
    </thead>
    <tbody>
    {#each lessons as {lesson_id, lesson_start_date, attendance_list} (lesson_id)}
        <tr>
            <th>{lesson_start_date}</th>
            {#each attendance_list as {id, status} (id)}
                <td>{status}</td>
            {/each}
        </tr>
    {/each}
    </tbody>
</table>

<style>
    table {
        display: table;
    }
    table tr {
        display: table-cell;
    }
    table tr td {
        display: block;
    }

    .foreign::after {
        content: '*'
    }
</style>