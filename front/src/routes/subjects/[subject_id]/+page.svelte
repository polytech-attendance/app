<script>
    import SubjectTable from "$lib/SubjectTable.svelte";
    /** @type {import('./$types').PageData} */
    export let data;
</script>

<h1>
    Посещаемость группой {data.group.name} дисциплины {data.subject.name}
</h1>

<SubjectTable groupId={data.group.id},
              groupName={data.group.name},
              subjectId={data.subject.id},
              subjectName={data.subject.name},
              studentList={data.group.students_list}
              lessons={data.lessons}/>