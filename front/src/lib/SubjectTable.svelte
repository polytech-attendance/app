<script>
    import {error} from "@sveltejs/kit";

    export let subjectId;
    export let groupId;
    export let subjectName;
    export let groupName;
    export let lessons;
    export let studentList;

    var change_attendance = (studentId, lessonId) => (async e =>  {
        let response = await fetch('http://127.0.0.1:8000/api/v1/attendance', {
            method: 'post',
            body: JSON.stringify({
                student_id: studentId,
                status: (e.target.checked) ? 1 : 0,
                lesson_id: lessonId,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw error('Can\'t update attendance');
        }
    })

    const displayDateTime = start_iso_time => (
        new Date(Date.parse(start_iso_time))
            .toLocaleDateString("ru-RU",
                { weekday: 'short',
                    year: '2-digit',
                    month: '2-digit',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit' })
    );
</script>

<table>
    <thead>
        <tr>
            <th>ФИО</th>
            {#each studentList as {abbrev_name, id, is_foreign} (id)}
                <td class:foreign={is_foreign}>{abbrev_name}</td>
            {/each}
        </tr>
    </thead>
    <tbody>
    {#each lessons as lesson (lesson.id)}
        <tr>
            <th>{displayDateTime(lesson.start_iso_time)}</th>
            {#each lesson.attendance_list as {id, status} (id)}
                <td><input type="checkbox" checked={status} on:change={change_attendance(id, lesson.id)}></td>
            {/each}
        </tr>
    {/each}
    </tbody>
</table>

<style>
    table thead, table tbody {
        display: contents;
    }
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