// TO DO: FIX THE BACK BUTTON FUNCTIONALITY FOR THE LAST STEP

const stepMenuOne = document.querySelector('.formbold-step-menu1')
const stepMenuTwo = document.querySelector('.formbold-step-menu2')
const stepMenuThree = document.querySelector('.formbold-step-menu3')
const stepMenuFour = document.querySelector('.formbold-step-menu4')

const stepOne = document.querySelector('.formbold-form-step-1')
const stepTwo = document.querySelector('.formbold-form-step-2')
const stepThree = document.querySelector('.formbold-form-step-3')
const stepFour = document.querySelector('.formbold-form-step-4')

const formSubmitBtn = document.querySelector('.formbold-btn')
const formBackBtn = document.querySelector('.formbold-back-btn')

formSubmitBtn.addEventListener("click", function(event) {
  event.preventDefault()

  if (stepMenuOne.classList.contains('active')) {
    stepMenuOne.classList.remove('active')
    stepMenuTwo.classList.add('active')

    stepOne.classList.remove('active')
    stepTwo.classList.add('active')

    formBackBtn.classList.add('active')

  } else if (stepMenuTwo.classList.contains('active')) {
    stepMenuTwo.classList.remove('active')
    stepMenuThree.classList.add('active')

    stepTwo.classList.remove('active')
    stepThree.classList.add('active')

  } else if (stepMenuThree.classList.contains('active')) {
    stepMenuThree.classList.remove('active')
    stepMenuFour.classList.add('active')

    stepThree.classList.remove('active')
    stepFour.classList.add('active')

    formSubmitBtn.textContent = 'Submit'

  } else if (stepMenuFour.classList.contains('active')) {
    document.querySelector('form').submit()
  }
})

formBackBtn.addEventListener("click", function(event) {
    event.preventDefault()
  
    if (stepMenuTwo.classList.contains('active')) {
      stepMenuTwo.classList.remove('active')
      stepMenuOne.classList.add('active')
  
      stepTwo.classList.remove('active')
      stepOne.classList.add('active')
  
      formBackBtn.classList.remove('active')
    } else if (stepMenuThree.classList.contains('active')) {
      stepMenuThree.classList.remove('active')
      stepMenuTwo.classList.add('active')
  
      stepThree.classList.remove('active')
      stepTwo.classList.add('active')
  
      formSubmitBtn.textContent = 'Next'
    } else if (stepMenuFour.classList.contains('active')) {
      stepMenuFour.classList.remove('active')
      stepMenuThree.classList.add('active')
  
      stepFour.classList.remove('active')
      stepThree.classList.add('active')
  
      formSubmitBtn.textContent = 'Next'
    }
  })

function updateSliderValue(slider) {
    const valueDisplay = document.getElementById(slider.id + 'Value');
    valueDisplay.textContent = slider.value;
  }

  window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.formbold-slider').forEach(slider => {
      updateSliderValue(slider);
    });
  });

function updateSalaryPerProject() {
  const salary = parseFloat(document.getElementById('monthly_salary').value) || 0;
  const projects = parseFloat(document.getElementById('projects_handled').value) || 0;

  const spp = projects > 0 ? (salary / projects).toFixed(2) : 0;
  document.getElementById('salary_per_project').value = spp;
}

document.getElementById('monthly_salary').addEventListener('input', updateSalaryPerProject);
document.getElementById('projects_handled').addEventListener('input', updateSalaryPerProject);