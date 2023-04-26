<script>
	export let props;
		// props {
		// groupId: group_id,
		// groupName: group_name,
		// classId: class_id,
		// date: date,
		// time: time
		// }
	const options = {
		tableSelector: "#check-table",
		studentSelector: ".row",
	}
    const baseURL = 'http://localhost:5173';
		

	function getParent(element, selector){
		console.log(element)
		if (element.matches(selector)) return element;
		while (element.parentElement){
			if (element.parentElement.matches(selector)){
				return element.parentElement;
			}
			element = element.parentElement;
		}
	}

	//studentList should get from the main page. Click each group leading to each

	function toggleElement(element){
		let parent = getParent(element,options.studentSelector);

		if (parent.classList.contains("absent")){
			parent.classList.remove("absent");
			return 1;
		}
		else parent.classList.add("absent");
		return 0;
	}

	//til now not modified
	function sendStatus(status,studentId){
		//send data to update attendance api
		fetch('http::/api/api/data',{
			method: 'post',
			body: JSON.stringify({
				student_id: studentId,
				student_status: status,
				date : props.date,
				time: props.time,
				class_id: props.classId,
				group_id: props.groupId,
			}),
			headers:{
				'Content-Type':'application/json'
			}
		})
		.then(response => {
			if (response.status === 200){
				console.log("OK");
			}
		})
		.catch(error=>{
			console.log(error);
		})
	}
		 //reactivity while pros is updated
		let groupLoading =  fetch(baseURL+'/students?groupId='+(props.groupId).toString())
		.then(response =>{
			console.log(props.groupId);
			return response.json()
		})
		.then(data => {return data})
		.catch(err=>console.log('Cannot get data: '+err));
		//assure reactivity
</script>

<!-- Test button --> 
  <a class="text-muted" href="#!" data-bs-toggle="modal" data-bs-target={"#check-table" + props.groupId.toString()}>
	{props.groupName}
  </a>
  <!-- Bug appeared here: must pay attention to the data-bs-target (to avoid pointing to the same modal for all text-muted) -->
  <div class="modal fade" id={"check-table" + props.groupId.toString()}>
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<!-- Группа -->
			  <p>Группа: {props.groupName}</p>	
				<p>{props.date}</p>
				<p>{props.time}</p>
			</div>
			{#await groupLoading}
			<p>loading group...</p>
			{:then group} 
			<div class="modal-body">
				<div class="container">
					{#each group.students as student}
						<button class={"btn row w-100"+" "+
						(student.is_foreign ? "":"foreign")+" "+
						(student.status ? "":"absent")} on:click={(event)=>{
							sendStatus(toggleElement(event.target),student.id)
						}}
						id={student.id}>
						{student.student_name + (student.is_foreign ? "*" :"")}
						</button>
					{/each}
				</div>
			</div>
			{/await}
			<div class="modal-footer">
				<button type="button" class="btn btn-primary" data-bs-dismiss="modal">Закрыт</button>
			</div>

		</div>		
	</div>
</div>

<style>
	a{
		display:flex
	}
	.row.absent {
		background-color: #ec6d79;
	}
	.row.foreign{
		
	}
	.row{
		margin-top: 10px;
		background-color: #66e9ac;
		border-radius: 5px;
		padding-top: 5px;
		padding-bottom: 5px;
		align-content: left;
	}

</style>