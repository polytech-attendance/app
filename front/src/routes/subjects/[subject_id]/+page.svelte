<script>
    import SubjectTable from "$lib/SubjectTable.svelte";
    /** @type {import('./$types').PageData} */
    export let data;
</script>

<SubjectTable groupId={data.group.group_id},
              groupName={data.group.groupname},
              subjectId={data.subject.subject_id},
              subjectName={data.subject.subject_name},
              lessons={data.lessons}/>