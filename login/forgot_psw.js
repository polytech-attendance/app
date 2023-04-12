const url = "http://127.0.0.1:5500/testDB.json";
const form = document.getElementById('requestForm');
const email = document.getElementById('mail');
const reset_psw = './reset_psw.html'
//submission event for form 
form.addEventListener("submit",(e)=>{
    //implicitly 
    e.preventDefault();
    Validate();
    //send a request to check login info to server
    if (SuccessMsg()){
        fetch('url', {
            method: "post",
            body: JSON.stringify({
                email: email.value
            }),
            headers: {
                'Content-Type':'application/json'
            }
        })
        .then(response => {
            if (response.status === 200){
                window.location.href = reset_psw;
            }
            else{
                console.log(response);
                setErrorMsg(email, "Адрес почта не найден");
            }
        })
        .catch(error => {
            alert(error);
        })
    }
} );

//check if text is valid email 
const isEmail = (emailVal) =>{
    const filter =/^[\w-\.]+@+[\w-]{2,4}$/g;
    return emailVal.match(filter);
}

function Validate(){
    const emailVal = email.value.trim();
    //validate
    //email
    if (emailVal === ""){
        setErrorMsg(email, 'Пустое поле нельзя!');
    }
    else 
    setSuccessMsg(email);

}


// input :: edit box where to put errormsgs
function setErrorMsg(input, errormsgs){
    //get the field (parent element)
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    formControl.className = "form-outline error";
    small.innerText = errormsgs;
}

//set success msg for valid field
function setSuccessMsg(input){
    const formControl = input.parentElement;
    formControl.className = "form-outline success";
}

//If SuccessMsg = true -> send request
const SuccessMsg = () =>{
    //get all 'form-outline' elements - all fields
    let formContr = document.getElementsByClassName('form-outline');
    let Count = formContr.length - 1;
    for (var i = 0; i < formContr.length; i++){
        if (formContr[i].className === "form-outline success"){
            let sRate = 0 + i;
            //show which field is valid
            console.log(sRate);
        }
        else return false;
    }
    return true;
}

