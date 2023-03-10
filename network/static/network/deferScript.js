// Chirps (Posts) edit buttons
const editBttn = document.querySelectorAll('.editButton');

// Event handler for toggling (Edit) textareas in corresponding Chirps
const handleEditBttn = (event) => {

    // Loads Textarea
    const buttonId = event.currentTarget.id
    const textareaContainer = document.querySelector(`.${buttonId}`)
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

// Event listener for Edit buttons
editBttn.forEach((button) => button.addEventListener("click", handleEditBttn));