<script>
    import {error} from "@sveltejs/kit";

    export let subjectId;
    export let groupId;
    export let subjectName;
    export let groupName;
    export let lessons;
    export let studentList;

    $:attendance_data = studentList
        .map((s, i) => ({student: s, data: lessons
                .map(les => ({lessonId: les.id, ...les.attendance_list[i]}))}))

    const change_attendance = (studentId, lessonId) => (async e => {
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
                    // year: '2-digit',
                    month: '2-digit',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit' })
    );
</script>
<div class="table-container"><table>
    <thead>
        <tr>
            <th>ФИО</th>
        {#each lessons as lesson (lesson.id)}
            <th style="padding: 0 1em; text-align: center">{displayDateTime(lesson.start_iso_time)}</th>
        {/each}
        </tr>
    </thead>
    <tbody>
    {#each attendance_data as {student, data} (student.id)}
        <tr>
            <th class:foreign={student.is_foreign}>{student.abbrev_name}</th>
            {#each data as {id, status, lessonId} (lessonId)}
                <td style="text-align: center"><input type="checkbox" checked={status} on:change={change_attendance(id, lessonId)}></td>
            {/each}
        </tr>
    {/each}
    </tbody>
</table></div>

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
    th:first-child {
      position: absolute;
      width: 10em;
      left: 0;
      top: auto;
      /*only relevant for first row*/
      margin-top: -1px;
      /*compensate for top border*/
    }
    .table-container {
      /*width: 500px;*/
      overflow-x: scroll;
      margin-left: 10em;
      overflow-y: visible;
      padding: 0;
    }
</style>