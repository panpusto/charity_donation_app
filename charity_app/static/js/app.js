document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();

          if (this.currentStep === 1) {
            if (categoriesValidation() === false) {
              this.currentStep++;
              this.updateForm();
            } else {
                alert("Musisz wybrać kategorię.")
            }
          }
          else if (parseInt(this.currentStep) === 2) {
            let bags_quantity = document.getElementById('bags');
            if (parseInt(bags_quantity.value) > 0) {
              this.currentStep++;
              this.updateForm();
            } else {
                alert("Musisz zadeklarować co najmniej jeden worek!")
            }
          }
          else if (parseInt(this.currentStep) === 3) {
            if (institutionValidation() === false) {
              this.currentStep++;
              this.updateForm();
            } else {
              alert("Musisz wybrać instytucję, której chcesz przekazać dary.")
            }
          }
          else if (parseInt(this.currentStep) === 4) {
            let address = document.forms["donation-form"]["address"].value;
            let city = document.forms["donation-form"]["city"].value;
            let zip_code = document.forms["donation-form"]["zip_code"].value;
            let phone_number = document.forms["donation-form"]["phone_number"].value;
            let pick_up_date = document.forms["donation-form"]['pick_up_date'].value;
            let pickup_formatted = new Date(pick_up_date.replace(/-/g, '/'));
            let today_date = new Date(Date.now());
            let pick_up_time = document.forms["donation-form"]["pick_up_time"].value;
            console.log(pick_up_time < '10:00')
            if ((address !== '') &&
                (city !== '') &&
                (zip_code !== '') &&
                (phone_number !== '') &&
                (pick_up_date !== '') &&
                (pick_up_time !== '')) {
              this.currentStep++;
              this.updateForm();
            } else if (address === '') {
                alert("Uzupełnij pole 'Ulica'.")
            } else if ((city === '') || (isNaN(city) === false)) {
                alert("Uzupełnij pole 'Miasto'. Nie używaj cyfr.")
            } else if ((zip_code === '') || (zip_code.length !== 5) || (isNaN((zip_code)) === true))  {
                alert("Wpisz kod pocztowy w formacie XXXXX, np. 50304")
            } else if ((phone_number === '') || (isNaN(phone_number) === true)) {
                alert("Wpisz numer telefonu w formacie XXXXXXXXX, np. 123456789")
            } else if (phone_number.length > 12) {
                alert("Wpisany numer telefonu jest za długi.")
            } else if (pick_up_date === '') {
                alert("Wybierz preferowaną datę odbioru.")
            } else if (pickup_formatted.getTime() < today_date.getTime()) {
                alert("Wybierz datę jutrzejszą lub późniejszą.")
            } else if ((pick_up_time === ''))  {
                alert("Wybierz preferowaną godzinę odbioru.")
            } else if ((pick_up_time > '20:00') || (pick_up_time < '10:00'))  {
                alert("Wybierz godzinę pomiędzy 10:00 a 20:00.")
            }
          }
          else {
            this.currentStep++;
            this.updateForm();
          }
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (parseInt(slide.dataset.step) === this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      /**
       * Summary for the form inputs before submit
       *
       */
    const btn = document.getElementById('donation-confirmation');
    btn.addEventListener('click', e => {
      document.getElementById("summary-quantity").textContent = document.getElementById('bags').value;
      document.querySelectorAll(".form-section--column ul li")[0].textContent = document.getElementById('address').value;
      document.querySelectorAll(".form-section--column ul li")[1].textContent = document.getElementById('city').value;
      document.querySelectorAll(".form-section--column ul li")[2].textContent = document.getElementById('zip_code').value;
      document.querySelectorAll(".form-section--column ul li")[3].textContent = document.getElementById('phone_number').value;
      document.querySelectorAll(".form-section--column ul li")[4].textContent = document.getElementById('pick_up_date').value;
      document.querySelectorAll(".form-section--column ul li")[5].textContent = document.getElementById('pick_up_time').value;
      document.querySelectorAll(".form-section--column ul li")[6].textContent = document.getElementById('pick_up_comment').value;
      const institutionInputs = document.getElementsByName('institution')
      institutionInputs.forEach(function (i) {
        if (i.checked) {
          const institution = i.parentElement.children[2].firstElementChild.innerHTML;
          document.getElementById("summary-institution").textContent = "Dla fundacji " + '"' + institution + '"';
    }
  })
})
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit() {
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});


const categoriesInputs = document.getElementsByName('categories');
const institutions = document.querySelectorAll('#institution');
const btnChosenCat = document.getElementById('chosen-categories');
const divInstitutions = document.querySelectorAll('#institution-label');
btnChosenCat.addEventListener("click", e => {
  divInstitutions.forEach(function (div) {
    div.removeAttribute('style');
  });
  let category_checked = [];
  categoriesInputs.forEach(function (category) {
    if (category.checked) {
      category_checked.push(category.value);
    }
  });
  institutions.forEach(function(i) {
    const institutionCategories = i.querySelectorAll('#cat');
    const instCatArr = [];
    institutionCategories.forEach(function (j) {
      instCatArr.push(j.value)
    })
    if (category_checked.every(elem => instCatArr.includes(elem)) === false) {
      i.style.display = 'none';
    }
  });
})


// form validation step_1
function categoriesValidation() {
  let noCategoriesChecked = true;
  let categories = document.querySelectorAll('#category');
  for (let category of categories) {
    if (category.checked) {
      noCategoriesChecked = false;
    }
  }
  return noCategoriesChecked
}

// form validation step_3
function institutionValidation() {
  let noInstitutionChecked = true;
  let institutions = document.querySelectorAll('#institution-label');
  for (let institution of institutions) {
    if (institution.checked) {
      noInstitutionChecked = false;
    }
  }
  return noInstitutionChecked
}