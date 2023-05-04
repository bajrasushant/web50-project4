document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.edit-btn').forEach(function(button) {
        button.onclick = function () {
            const id = button.dataset.postid;
            const idToGet = "post-description-".concat(id);
            const buttonToGet = "edit-btn-".concat(id);
            const editButton = document.querySelector('#' + buttonToGet);
            const postToReplace = document.querySelector('#' + idToGet);
            const newText = document.createElement('textarea');
            newText.setAttribute('id', 'edit-text-'+id);
            newText.classList.add('form-control');
            const saveButton = document.createElement('button');
            saveButton.innerHTML = "Save";
            saveButton.setAttribute('id', "save-btn-"+id);
            saveButton.setAttribute('type', 'submit');
            saveButton.classList.add("btn", "btn-secondary", "save-btn");
            postToReplace.parentNode.replaceChild(newText, postToReplace);
            editButton.parentNode.replaceChild(saveButton, editButton);
        }
    });
});
