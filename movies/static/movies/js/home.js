/* Refresh page on clicking the logo */
function refreshPage() {
    location.reload();
}


/************** Navigation Bar ************** */
const toggleMenu = () => {
  const navigation = document.querySelector('.navigation');

  const burgerMenu = document.querySelector(".menu-icon");
  const src = burgerMenu.getAttribute("src");

  const isBurger = src === "{% static 'movies/images/menu.png' %}";

  const iconName = isBurger ?
      "{% static 'movies/images/close.png' %}"
      :
      "{% static 'movies/images/menu.png' %}";

  burgerMenu.setAttribute(
      "src", iconName
  );

  if (!isBurger) {
      navigation.classList.add("navigation--mobile--fadeout");
      setTimeout (() => {
          navigation.classList.toggle (
              "navigation--mobile"
          );
      }, 300)
  } else {
      navigation.classList.remove("navigation--mobile--fadeout");
      navigation.classList.toggle (
          "navigation--mobile"
      );
  }
};



/* Function to show the search form and hide recommendation button */
function toggleForm() {
    let form = document.getElementById("search_form");
    let button = document.getElementById("toggle_button")
    
    if (form.style.display === "none") {
      form.style.display = "block"; 
      button.style.display = "none"; 
    } else {
      form.style.display = "none";  
      button.style.display = "block"  
    }
}


/********************** Movie List Section *************************/
const bankAccounts = document.getElementById('bank-accounts');

let isDown = false;
let startX;
let startY;
let scrollLeft;
let scrollTop;

bankAccounts.addEventListener('mousedown', (e) => {
  isDown = true;
  startX = e.pageX - bankAccounts.offsetLeft;
  startY = e.pageY - bankAccounts.offsetTop;
  scrollLeft = bankAccounts.scrollLeft;
  scrollTop = bankAccounts.scrollTop;
  bankAccounts.style.cursor = 'grabbing';
});

bankAccounts.addEventListener ('mouseleave', () => {
  isDown = false;
  bankAccounts.style.cursor = 'grab';
});

bankAccounts.addEventListener('mouseup', () => {
  isDown = false;
  bankAccounts.style.cursor = 'grab';
});

document.addEventListener('mousemove', (e) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - bankAccounts.offsetLeft;
  const y = e.pageY - bankAccounts.offsetTop;
  const walkX = (x - startX) * 1;
  const walkY = (y -startY) * 1;
  bankAccounts.scrollLeft = scrollLeft - walkX;
  bankAccounts.scrollTop = scrollTop - walkY;
});

const scrollLeftButton = document.getElementById(
  'action-button--previous');
const scrollRightButton = document.getElementById(
  'action-button--next'
);

scrollLeftButton.addEventListener('click', () => {
  bankAccounts.scrollBy({
    top: 0,
    left: -200,
    behavior:"smooth"
  });
});

scrollRightButton.addEventListener('click', () => {
  bankAccounts.scrollBy({
    top: 0,
    left: 200,
    behavior: "smooth"
  });
});

bankAccounts.addEventListener('scroll', (e) => {
  const position = bankAccounts.scrollLeft;
  if (position ===0 ) {
    scrollLeftButton.disabled = true;
  } else {
    scrollLeftButton.disabled = false;
  }

  if (
    Math.round(position) ===
    bankAccounts.scrollWidth -
    bankAccounts.clientWidth
  ) {
    scrollRightButton.disabled = true;
  } else {
    scrollRightButton.disabled = false;
  }
});


/********************Auto-complete on search bar***************** */
$(function () {
  $("#movie").autocomplete({
    source: function (request, response) {
      // AJAX request to get movie recommendations as the user types
      $.ajax({
        url: "/search/",  // Replace with your actual API endpoint
        dataType: "json",
        data: {
          query: request.term,
        },
        success: function (data) {
          response(data);
        },
      });
    },
    minLength: 2,  // Minimum characters before triggering autocomplete
    select: function (event, ui) {
      // Handle the selection of a movie
      console.log("Selected movie:", ui.item.label);
    },
  });
});


// JavaScript function to go back
function goBack() {
    window.history.back();
}
