//DOM
const save_settings_button = document.getElementById('save_settings')
const activate_modals = document.getElementsByClassName('activate_modal')

state = 0

//MODALS - Event Listener 
for (const button of activate_modals) {
    button.addEventListener('click', function(e) {
        const type = e.target.id
        const modal = document.querySelector(`.${type}`)        
        modal.style.visibility = 'visible' 
        const close = modal.firstElementChild.children[0]
        close.addEventListener('click', function() {
            modal.style.visibility = 'hidden'
        })
    });
}

//SETTINGS
save_settings_button.addEventListener('click', function() {
    const partymode = document.getElementById('party_mode')
    if(partymode.checked) {
        const user = document.getElementById('top_bar_username')
        console.log(user)
        user.classList.add('partymode')
    }
})