<script>
    import Checklist from "./Checklist.svelte";

    export let days;

    const gridRow = (time) => (
        2 + Math.floor((+time.split(':')[0] - 10) / 2)
    );
    const displayDate = (date) => (
        new Date(Date.parse(date))
            .toLocaleDateString("ru-RU",
                { weekday: 'short',
                    month: '2-digit',
                    day: 'numeric', })
    );
</script>

<div class="grid">
    {#each days as {lessons, weekday, date}}
        <div class="grid-day-header" style:grid-column={weekday}>{displayDate(date)}</div>
        {#each lessons as {subject, typeObj, time_start, time_end, name, teachers, groups}}
            <div class="grid-item"
                 style:grid-column={weekday}
                 style:grid-row={gridRow(time_start)}
            >
                <div class="subject">{subject}</div>
                <div class="last-item-element">
                    <span class="time">{time_start}</span>
<!--                    <span class="lesson-type">{typeObj.name}</span>-->
                </div>
                {#if teachers}
                    <div class="teachers">
                    {#each teachers as teacher}
                        <div class="teacher">
                            {teacher == null ? "" : teacher.full_name}
                        </div>
                    {/each}
                    </div>
                {/if}
                {#each groups as g}
                    <Checklist groupId={g.id} groupName={g.name} {date} lessonId={g.lesson_id} time={time_start} class="group-btn"/>
                {/each}
            </div>
        {/each}
    {/each}
</div>

<style>
    .grid-item .subject {
        font-weight: bold;
        font-size: 16px;
        color: var(--bs-white);
    }

    .grid-item .time {
        padding: 5px;
        margin: 0 10px;
        color: var(--bs-white);
    }

    .grid-item .teacher {
        color: #eee;
        font-size: 11pt;
    }

    .grid-item .lesson-type {
        font-weight: normal;
        color: var(--bs-white);
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 10px;
        margin: 10px;
    }

    .grid-day-header {
        grid-row: 1;
        text-align: center;
        font-weight: bold;
    }
    .grid-day-header {
        border-right: darkgray 1px solid;
    }
    .grid-day-header:last-child {
        border-right: none;
    }

    .grid-item {
        border-radius: 4px;
        padding: 5px;
        background-color: var(--bs-purple);
    }


    .grid-item {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .last-item-element {
        margin-bottom: auto;
    }
</style>