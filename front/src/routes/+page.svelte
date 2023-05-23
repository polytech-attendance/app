<script>
    import ScheduleGrid from "$lib/ScheduleGrid.svelte";
    // import Sidebar from "../lib/Sidebar.svelte";

    /** @type {import('./$types').PageData} */
    export let data;
</script>
<div id="main-layout">
<!--    <Sidebar mainId="main-area"/>-->
    <div id="main-area">
        <div class="topnav">
            <p class="greeting"> Здравствуйте, {data.teacher.full_name}!</p>
        </div>
        <div class="main-board">
                <ScheduleGrid days={data.days}/>
        </div>
    </div>
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

#main-layout{
    display: flex;
    flex-direction: row;
}
#main-area{
    display: flex;
    flex-direction: column;

}

</style>