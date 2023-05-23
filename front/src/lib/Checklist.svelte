<script>
    import {onMount} from 'svelte';

    export let groupId;
    export let groupName;
    export let date;
    export let lessonId;
    export let time;

    //studentList should get from the main page. Click each group leading to each

    async function sendStatus(status, studentId) {
        //send data to update attendance api
        let response = await fetch('http://127.0.0.1:8000/api/v1/attendance', {
            method: 'post',
            body: JSON.stringify({
                student_id: studentId,
                status: (status) ? 1 : 0,
                // date: date,
                // time: time,
                lesson_id: lessonId,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.status === 200) {
            console.log("OK");
        }
    }

    let group = [];

    onMount(async () => {
       let response = await fetch(`http://127.0.0.1:8000/api/v1/groups/${groupId}/attendance/?lesson_id=${lessonId}&format=json`);
        if (response.ok) {
            group = await response.json();
        } else {
            group = []
        }
    });
    const displayDate = (date) => (
        new Date(Date.parse(date))
            .toLocaleDateString("ru-RU",
                { weekday: 'short',
                    month: '2-digit',
                    day: 'numeric', })
    );
    const handleClick = (student) => async () => {
        student.status = !student.status;
        await sendStatus(student.status, student.id)
            .catch(err=> alert("Cannot save choice: "+err));
        group = group; // needed to update
    }
</script>

<!-- Test button -->
<button class="btn btn-light" data-bs-toggle="modal" data-bs-target={"#check-table" + groupId}>
    {groupName}
</button>
<!-- Bug appeared here: must pay attention to the data-bs-target (to avoid pointing to the same modal for all text-muted) -->
<div class="modal fade" id={"check-table" + groupId}>
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <!-- Группа -->
                <p>Группа: {groupName}</p>
                <p>{displayDate(date)}</p>
                <p>{time}</p>
            </div>
            <div class="modal-body">
                <div class="container">
                    {#each group as student}
                        <button class="btn row w-100" class:foreign={student.is_foreign}
                                class:absent={!student.status}
                                on:click={handleClick(student)}
                                id={student.id}>
                            {student.abbrev_name}
                        </button>
                    {/each}
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Закрыть</button>
            </div>
        </div>
    </div>
</div>

<style>
    .row.absent {
        background-color: #ec6d79;
    }
    .row.foreign::after {
        content: '*'
    }
    .row {
        margin-top: 10px;
        background-color: #66e9ac;
        border-radius: 5px;
        padding-top: 5px;
        padding-bottom: 5px;
        align-content: flex-start;
    }
</style>