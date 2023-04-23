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

	//only get group lists to load table. Interaction later based on each element of student. 
	// dataRaw = {[group_id, [att:]]}
	//use date, lesson etc here
	// export const dataRaw = fetch('')
	// 	.then(response => {
	// 		if (response !== 200){
	// 			console.log ("Error: Request error");
	// 		}
	// 		else{
	// 			return response.JSON();
	// 		}
	// 	})
	// 	.catch(error=>{
	// 		console.log("Connection error: " + error);
	// 	})


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
	let studentList = [{student_id: 1234,student_name:'a', student_status: true, student_is_foreign: true}, {student_name:'b', student_status: false,student_is_foreign: false}];

	export function toggleElement(element){
		let parent = getParent(element,options.studentSelector);

		if (parent.classList.contains("absent")){
			parent.classList.remove("absent");
			return 1;
		}
		else parent.classList.add("absent");
		return 0;
	}
	export function sendStatus(status,studentId){

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
</script>

<!-- Test button --> <!-- Replace by button on schedule -->

  <a class="text-muted" href="#!" data-bs-toggle="modal" data-bs-target="#check-table">
	{props.groupName}
  </a>

  <div class="modal fade" id="check-table" tabindex="-1">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<!-- Группа -->
				Группа: {props.groupName}
			</div>
			<div class="modal-body">
				<div class="container">
					{#each studentList as student}
						<button class={"row w-100"+" "+
						(student.student_is_foreign ? "":"foreign")+" "+
						(student.student_status ? "":"absent")} on:click={(event)=>{
							sendStatus(toggleElement(event.target),student.student_id)
						}}
						id={student.student_id}>
						{student.student_name + (student.student_is_foreign ? "*" :"")}
						</button>
					{/each}
				</div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-primary" data-bs-dismiss="modal">Закрыт</button>
			</div>
		</div>		
	</div>
</div>

<style>

	.row.absent {
		background-color: #ec6d79;
	}
	.row.foreign{
		
	}
	.row{
		margin-top: 10px;
		background-color: #66e9ac;
		border-radius: 1px;
	}
	@media (min-width: 640px) {

	}
</style>