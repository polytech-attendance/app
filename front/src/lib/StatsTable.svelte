<script>
    export let studentList;
</script>
<table>
    <thead>
        <tr>
            <th>ФИО</th>
            <th>Доля посещенных занятий</th>
        </tr>
    </thead>
    <tbody>
    {#each studentList as student (student.id)}
        <tr>
            <th class:foreign={student.is_foreign}>{student.abbrev_name}</th>
            <td>{student.stat+'%'}</td>
        </tr>
    {/each}
    </tbody>
</table>

<style>
    table thead, table tbody {
        display: contents;
    }
    .foreign::after {
        content: '*'
    }
    table {
        display: block;
        overflow-x: scroll;
    }
</style>