<script>
    var lesson1 = {
        subject: "Теория графов",
        time_start: "18:00",
        teacher: {
            id: 3549,
            full_name: "Востров Алексей Владимирович",
            first_name: "Востров",
            middle_name: "Алексей",
            last_name: "Владимирович",
          },
    };
    var lesson2 = {
        subject: "Теория графов",
        time_start: "12:00",
        teacher: {
            id: 3549,
            full_name: "Востров Алексей Владимирович",
            first_name: "Востров",
            middle_name: "Алексей",
            last_name: "Владимирович",
          },
    };
    var lesson3 = {
        subject: "Теория графов",
        time_start: "14:00",
        teacher: {
            id: 3549,
            full_name: "Востров Алексей Владимирович",
            first_name: "Востров",
            middle_name: "Алексей",
            last_name: "Владимирович",
          },
    };
    var days = [
        {
            weekday: 1,
            date: '2023-04-10',
            lessons: [
                lesson1, lesson2, lesson3
            ]
        },
        {
            weekday: 2,
            date: '2023-04-11',
            lessons: [
                lesson1, lesson2
            ]
        }
    ];
    var weekdays = [
        {
            weekday: 1,
            name: 'Пн',
            date: '2023-04-10',
        },
        {
            weekday: 2,
            name: 'Вт',
            date: '2023-04-11',
        },
        {
            weekday: 3,
            name: 'Ср',
            date: '2023-04-12',
        },
        {
            weekday: 4,
            name: 'Чт',
            date: '2023-04-13',
        },
        {
            weekday: 5,
            name: 'Пт',
            date: '2023-04-14',
        },
        {
            weekday: 6,
            name: 'Сб',
            date: '2023-04-15',
        },
    ];
    var gridRow = (time) => (
        2 + Math.floor((+time.split(':')[0]-10)/2)
    )
    var displayName = (teach) => (
        teach.first_name
        + ` ${teach.middle_name[0]}.`
        + ('last_name' in teach ? ` ${teach.last_name[0]}.` : '')
    );
</script>

<div class="grid">
    {#each weekdays as {weekday, name, date}}
        <div class="grid-day-header" style:grid-column={weekday}>{name} {date}</div>
    {/each}
    {#each days as {weekday, date, lessons}}
        {#each lessons as {subject, time_start, teacher}}
                <div class="grid-item"
                     style:grid-column={weekday}
                     style:grid-row={gridRow(time_start)}
                >
                    <div class="subject">{subject}</div>
                    <span class="time">{time_start}</span>
                    <div class="teacher">{displayName(teacher)}</div>
                </div>
            {/each}
    {/each}
</div>

<style>
.grid-item .subject {
    font-weight: bold;
    font-size: 16px;
    color: #fff;
}
.grid-item .time {
    padding: 5px;
    margin: 0 10px;
    color: #fff;
}
.grid-item .teacher {
    color: #eee;
    font-size: 11pt;
}
.grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
    margin:10px;
}
.grid-day-header {
     grid-row: 1;
    text-align: center;
    font-weight: bold;
}
.grid-item {
    /*border: black 1pt solid;*/
    border-radius: 4px;
    padding: 5px;
    background-color: var(--purple);
    gap: 10px;
    display: flex;
    flex-direction: column;
}
</style>