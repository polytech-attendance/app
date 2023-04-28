<script>
    import ScheduleGrid from "$lib/ScheduleGrid.svelte";

    /** @type {import('./$types').PageData} */
    export let data;
</script>

<div class="topnav">
    <p class="greeting"> Здравствуйте, {data.teacher.full_name}!</p>
</div>
<div class="main-board">
    <ScheduleGrid days={data.days}/>
</div>

<style>
.main-board {
    align-self: center;
    margin: 10px;
    max-width:100%;
    display: flex;
    flex-direction:row;
    align-items: flex-end;
}
</style>