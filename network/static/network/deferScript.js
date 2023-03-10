// Event handler for toggling (Edit) textareas in corresponding Chirps
const handleEditBttn = (event) => {

    // Loads Textarea
    const buttonId = event.currentTarget.id;
    const textareaContainer = document.querySelector(`.${buttonId}`);
    textareaContainer.style.display = 'block';

    // Resize textarea height in accordance to content
    const tx = document.getElementsByTagName("textarea");
    for (let i = 0; i < tx.length; i++) {
    tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;" + "width: 100%;");
    tx[i].addEventListener("input", OnInput, false);
    }
    function OnInput() {
    this.style.height = 0;
    this.style.height = (this.scrollHeight) + "px";
    }

    // Remove original chirp being edited
    const parent = event.currentTarget.parentNode;
    parent.style.display = 'none'; 
};

// Event listener for edit buttons
const editBttn = document.querySelectorAll('.editButton');
editBttn.forEach((button) => button.addEventListener("click", handleEditBttn));

// Event handler for edits form submission
const handleFormSubmit = async (event) => {
    event.preventDefault();

    // Assign variables to key content values
    const formElements = event.currentTarget.childNodes;
    const chirpContent = formElements[1].value;
    const currentChirpId = formElements[1].id;
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    // Post using async...await fetch
    try {
        const response = await fetch('/edit', {
            method: 'POST',
            body: JSON.stringify({
                chirpId: currentChirpId,
                content: chirpContent }),
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": csrfToken
            }
        });
        const jsonResponse = await response.json();
        console.log(jsonResponse);
    } catch (error) {
        console.log(error);
    }

    // Instantly updates edited chirps on user's DOM
    const editedChirp = document.getElementById(`bttn${currentChirpId}`).parentNode;
    editedChirp.style.display = 'block';
    editedChirp.childNodes[5].innerHTML = chirpContent
    const textareaContainer = document.getElementById(`texta${currentChirpId}`);
    textareaContainer.style.display = 'none';
}

// Event listener for form submission
const editForm = document.querySelectorAll('.editForm');
editForm.forEach((form) => form.addEventListener("submit", handleFormSubmit));