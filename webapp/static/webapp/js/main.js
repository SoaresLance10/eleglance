const imgs = document.querySelectorAll('.img-select a');
const imgBtns = [...imgs];
let imgId = 1;

imgBtns.forEach((imgItem) => {
    imgItem.addEventListener('click', (event) => {
        event.preventDefault();
        imgId = imgItem.dataset.id;
        slideImage();
    });
});

function slideImage(){
    const displayWidth = document.querySelector('.img-showcase img:first-child').clientWidth;

    document.querySelector('.img-showcase').style.transform = `translateX(${- (imgId - 1) * displayWidth}px)`;
}

window.addEventListener('resize', slideImage);

const filters = document.querySelector(".filter-wrapper")
const closeBtn = document.getElementById("close-btn")
const filterBtn = document.getElementById("filter-btn")
function closeFilters() {
    filters.classList.add("inactive-filter")
    console.log('inactive function')
}
closeBtn.addEventListener('click', closeFilters)

function showFilters() {
    filters.classList.remove("inactive-filter")
    console.log("show filters")
}

window.addEventListener('click', function(e){
    if (filters.classList.contains("inactive-filter")) {
        return;
    } else if (filterBtn.contains(e.target)) {
        return;
    } else if (filters.contains(e.target)){
        return;
    } else{
        closeFilters();
    }
});

