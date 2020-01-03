let labs = document.getElementsByClassName('label')
let labs_arr = Array.from(labs)


let eventHideShow = function(event) {
    id = event.target.htmlFor
    form = document.getElementById(id)
    if (form.style.display == 'none') {
        form.style.display == 'block'
    }
    else {
       form.style.display == 'none'
    }
}

labs_arr.forEach(el => el.onclick = eventHideShow)

