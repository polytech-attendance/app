<script>
    import SubjectTable from "$lib/SubjectTable.svelte";
    /** @type {import('./$types').PageData} */
    export let data;
</script>

<SubjectTable groupId={data.group.id},
              groupName={data.group.name},
              subjectId={data.subject.id},
              subjectName={data.subject.name},
              studentList={data.group.students_list}
              lessons={data.lessons}/>