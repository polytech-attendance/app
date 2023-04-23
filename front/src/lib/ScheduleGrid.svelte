<script>
    import { onMount } from "svelte";
    import Checklist from "./Checklist.svelte";

    //import fs from 'fs';
    const baseURL = 'http://localhost:5173';


    var gridRow = (time) => (
        2 + Math.floor((+time.split(':')[0]-10)/2)
    )
    function displayDate(date) {
        switch(date){
            case 1: return "Пн";
            case 2: return "Вт";
            case 3: return "Ср";
            case 4: return "Чт";
            case 5: return "Пт";
            case 6: return "Сб";
            case 7: return "Вс";
        }
    }

    //later should be user's token 
    const tokenTeacher = '3549';

    let schedule = fetch(baseURL +'/main?teacherId='+(tokenTeacher))
    .then(response =>{
        return response.json();
    })
    .then(data =>{
        return data;
    })
    .catch(err=>{
        console.log("Fetch failed: "+err);
    })

</script>

<!-- need to wait schedule to load -->
{#await schedule}
<p>loading...</p>
{:then schedule} 
<div class="grid">
    {#each schedule.days as {weekday, date}}
        <div class="grid-day-header" style:grid-column={weekday}>{displayDate(weekday)} {date}</div>
    {/each}
    {#each schedule.days as day}
        {#each day.lessons as {subject, typeObj, time_start, teachers,groups}}
                <div class="grid-item"
                     style:grid-column={displayDate(day.weekday)}
                     style:grid-row={gridRow(time_start)}
                >
                    <div class="subject">{subject}</div>
                    <span class="time">{time_start}</span>
                    <div class="teachers">
                        {#each teachers as teacher}
                            <div class="teacher">
                                {(teacher == null) ? "" : teacher.full_name}
                            </div>
                        {/each}
                        </div>

                    <!-- For the checklist -->
                    {#each groups as {id,name}}
                            <Checklist props={{groupId:id, groupName: name, classId:typeObj.id, date:day.date, time:time_start}}/>
                    {/each}
                </div>
            {/each}
    {/each}
</div>
{/await}



<style>
.grid-item .subject {
    font-weight: bold;
    font-size: 16px;
    color: black;
}
.grid-item .time {
    padding: 5px;
    margin: 0 10px;
    color: #fff;
}
.grid-item .teacher {
    color: black;
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