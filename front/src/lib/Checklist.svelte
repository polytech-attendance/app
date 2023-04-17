<script>
	const options = {
		tableSelector: "#check-table",
		studentSelector: ".row",
	}

	//only get group lists to load table. Interaction later based on each element of student. 
	// dataRaw = {[group_id, [att:]]}
	export const dataRaw = fetch('')
		.then(response => {
			if (response !== 200){
				console.log ("Error: Request error");
			}
			else{
				return response.JSON();
			}
		})
		.catch(error=>{
			console.log("Connection error: " + error);
		})
	
	let date = dataRaw.date, classId = dataRaw.class_id;
	function getParent(element, selector){
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

	export function toggleStatus(){
		let parent = getParent(this,options.studentSelector);
		let status = 0;
		//toggle status 

		if (parent.classList.contains("absent")){
			parent.classList.remove("absent");
			status = 1;
		}
		else parent.classList.add("absent");

		//send data to update attendance api
		fetch('testDB.json',{
			method: 'post',
			body: JSON.stringify({
				date : date,
				class_id: classId,
				student_id: parent.id,
				student_status: status,
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

<main>
<!-- Test button --> <!-- Replace by button on schedule -->
  <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#check-table">
	Launch demo modal
  </button>

  <div class="modal fade" id="check-table" tabindex="-1">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<!-- Группа -->
				Группа: {classId}
				<br>
				Посыщаемость:  
			</div>
			<div class="modal-body">
				<div class="container">
					{#each studentList as student}
						<button class={"row w-100"+" "+
						(student.student_is_foreign ? "":"foreign")+" "+
						(student.student_status ? "":"absent")} on:click={toggleStatus} 
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
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 50%;
		margin: 0 auto;
	}

	.row.absent {
		background-color: #ec6d79;
	}
	.row.foreign{
		
	}
	.row{
		margin-top: 10px;
		background-color: #66e9ac;
	}
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>