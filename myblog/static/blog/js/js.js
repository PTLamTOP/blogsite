$(document).ready(function () {
    let buttons = $(".label-primary");
    buttons.on('click', function (event) {
        $(this.dataset.target).toggle();
    })
});








// let labs = document.getElementsByClassName('label-primary');
// let labs_arr = Array.from(labs);
//
//
// let eventHideShow = function(event) {
//     let id = event.target.value;
//     let form = document.getElementById(id);
//     if (form.style.display == 'none') {
//         form.style.display == 'block'
//     }
//     else {
//        form.style.display == 'none'
//     }
// }
//
// labs_arr.forEach(el => el.onclick = eventHideShow);
