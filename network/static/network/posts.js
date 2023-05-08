function saveHandler(id) {
    const newDescription = document.getElementById(`textarea-${id}`).value;
    const description = document.getElementById(`post-description-${id}`)
    const modal = document.getElementById(`edit-modal-${id}`) 
    const body = document.body
    fetch(`/edit/${id}`, {
        method: 'POST',
        body:JSON.stringify({
            newEdit: newDescription
        })
    }).then(response => response.json())
    .then(result => {
        description.innerHTML = result.data;
        modal.classList.remove("fade");
        modal.setAttribute("aria-hidden","true");
        modal.style.display = "none";
        const modalBackdrop = document.getElementsByClassName("modal-backdrop");
        for (let i = 0; i < modalBackdrop.length; i++){
            document.body.removeChild(modalBackdrop[i]);
        }
        body.classList.remove("modal-open"); 
     });
}

function likeHandler(id, status){
    const button = document.getElementById(`like-btn-${id}`)
    if(status === false){
        button.innerHTML = "Unlike"
        button.classList.remove("btn-outline-primary")
        button.classList.add("btn-outline-danger")
		fetch(`posts/${id}`, {
			method: 'PUT',
			body: JSON.stringify({
				liked: true
			})
		}).then(response => response.json())
        .then(result => {
            const countVal = document.querySelector(`#like-${id}`);
            countVal.textContent = `Likes: ${result.likes_count}`;
        }) .catch(error => console.error(error));
} else {
        button.innerHTML = "Like"
        button.classList.add("btn-outline-primary")
        button.classList.remove("btn-outline-danger")

		fetch(`posts/${id}`, {
			method: 'PUT',
			body: JSON.stringify({
				liked: false
			})
		}).then(response => response.json())
        .then(result => {
            const countVal = document.querySelector(`#like-${id}`);
            countVal.textContent = `Likes: ${result.likes_count}`;
        }) .catch(error => console.error(error));

	}
}
