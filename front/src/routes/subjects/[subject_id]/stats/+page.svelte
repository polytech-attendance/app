<script>
    import StatsTable from "$lib/StatsTable.svelte";

    /** @type {import('./$types').PageData} */
    export let data;
</script>
<h1>
    Статистика посещений группой {data.group.name} дисциплины {data.subject.name}
</h1>

<StatsTable studentList={data.group.student_list}/>