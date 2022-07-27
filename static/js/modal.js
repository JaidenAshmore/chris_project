// NOT IN USE!

//DOM
const modal_buttons = document.getElementsByClassName('modal-button')
const close_buttons = document.getElementsByClassName('close-button');


//Event Listeners
for (const modal_button of modal_buttons) {
    modal_button.addEventListener('click', function(e) {
        const name = e.target.id;
        const modal = document.getElementById(`modal-${name}`);
        modal.style.visibility = 'visible'
    })
}

for (const close_button of close_buttons) {
    close_button.addEventListener('click', function() {
        const modal = close_button.parentElement.parentElement;
        modal.style.visibility = 'hidden';
    })
}

