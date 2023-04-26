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

    let schedule = fetch(baseURL+'/scheduler?teacherId='+(tokenTeacher))
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


<!-- Top navigation bar -->
{#await schedule}
<p>loading...</p>
{:then schedule} 
<div class="topnav">
    <p class="greeting"> Здравствуйте, {schedule.teacher.full_name} !</p>
</div>
<div class="main-board">
        <div class="grid-container">
            {#each schedule.days as day}
                <div class="grid-day-header" style:grid-column={day.weekday+1}>{displayDate(day.weekday)} {day.date}</div>
                    <!-- <div class="grid-day-header" style:grid-column={day.weekday}>{displayDate(day.weekday)} {day.date}</div> -->
                    {#each day.lessons as {subject, typeObj, time_start, time_end, name, teachers,groups}}
                            <div class="grid-item lesson-row" style:grid-column=0 style:grid-row={gridRow(time_start)}>
                                {time_start} - {time_end}
                            </div>
                            <div class="grid-item"
                                style:grid-column={day.weekday+1}
                                style:grid-row={gridRow(time_start)}
                            >
                                <div class="subject">{subject}
                                    <span class="name" style:color=gray>{typeObj.name}</span>
                                </div>
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
    </div>
{/await}




<style>
  .main-board{
    max-width: 80%;
    display: flex;
    flex-direction:row;
    align-items: right;
  }
.grid-item .subject {
    font-weight: bold;
    font-size: 16px;
    color: black;
}
.grid-item .time {
    padding: 5px;
    margin: 0 10px;
    color: black;

}
.grid-item .teacher {
    color: black;
    font-size: 11pt;
}
.grid-container {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
    margin:10px;
    border-width: 5px gray;
    max-width: 90%;
    max-height: 90%;
}
.grid-day-header {
    grid-row: 1;
    text-align: center;
    font-weight: bold;
}
.grid-item {
    /*border: black 1pt solid;*/
    border: 5px black;
    padding: 5px;
    background-color: var(--purple);
    gap: 10px;
    display: flex;
    flex-direction: column;
    min-width: 50%;
}
</style>