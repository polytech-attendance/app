<script>
    import {onMount} from 'svelte';

    export let groupId;
    export let groupName;
    export let date;
    export let classId;
    export let time;

    //studentList should get from the main page. Click each group leading to each

    async function sendStatus(status, studentId) {
        //send data to update attendance api
        let response = await fetch('http::/api/api/data', {
            method: 'post',
            body: JSON.stringify({
                student_id: studentId,
                student_status: status,
                date: date,
                time: time,
                class_id: classId,
                group_id: groupId,
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
        // TODO pass other parameters too, because need initial values for student.status
        let response = await fetch(`/students?groupId=${groupId}`);
        group = await response.json();
    });

    const handleClick = (student) => async () => {
        student.status = !student.status;
        await sendStatus(student.status, student.id);
        group = group; // needed to update rows
    }
</script>

<!-- Test button -->
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target={"#check-table" + groupId}>
    {groupName}
</button>
<!-- Bug appeared here: must pay attention to the data-bs-target (to avoid pointing to the same modal for all text-muted) -->
<div class="modal fade" id={"check-table" + groupId}>
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <!-- Группа -->
                <p>Группа: {groupName}</p>
                <p>{date}</p>
                <p>{time}</p>
            </div>
            {#if (group.length === 0)}
                <p>Список загружается...</p>
            {:else}
                <div class="modal-body">
                    <div class="container">
                        {#each group.students as student}
                            <button class="btn row w-100" class:foreign={student.is_foreign}
                                    class:absent={!student.status}
                                    on:click={handleClick(student)}
                                    id={student.id}>
                                {student.student_name}
                            </button>
                        {/each}
                    </div>
                </div>
            {/if}
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