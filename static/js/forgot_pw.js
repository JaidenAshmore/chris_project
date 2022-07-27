// NOT IN USE!

//DOM
const forgot_link = document.getElementById('forgot_link')


//Event Listeners
forgot_link.addEventListener('click', function() {
    const modal = document.getElementById('modal-forgot');
    const close_buttons = document.getElementsByClassName('button_close');
    modal.style.visibility = 'visible';

    for (const button of close_buttons) {
        button.addEventListener('click', function() {
        modal.style.visibility = 'hidden';
        });
    }     
})