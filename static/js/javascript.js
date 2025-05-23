document.addEventListener("DOMContentLoaded", () => {
  const countdownElement = document.querySelector(".countdown");

  // Таймер обратного отсчёта
  const weddingDate = new Date("September 19, 2025 00:00:00").getTime();
  const interval = setInterval(function () {
    const now = new Date().getTime();
    const distance = weddingDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("days").innerHTML = days;
    document.getElementById("hours").innerHTML = hours;
    document.getElementById("minutes").innerHTML = minutes;
    document.getElementById("seconds").innerHTML = seconds;

    // Показываем блок countdown после загрузки данных
    // Показываем блок countdown после загрузки данных
    if (!countdownElement.classList.contains("visible")) {
      countdownElement.classList.add("visible");
    }

    if (distance < 0) {
      clearInterval(interval);
      countdownElement.innerHTML = "Свадьба уже состоялась!";
    }
  }, 1000);

  // Плавный скролл к секции "Программа дня"
  document.getElementById("to-program").addEventListener("click", function () {
    const programSection = document.getElementById("program");
    programSection.scrollIntoView({ behavior: "smooth" });
  });

  // Управление музыкой
  const musicControl = document.getElementById("music-control");
  const musicIcon = document.getElementById("music-icon");
  const backgroundMusic = document.getElementById("background-music");

  let isPlaying = false;

  musicControl.addEventListener("click", () => {
    if (isPlaying) {
      backgroundMusic.pause();
      musicIcon.classList.remove("fa-pause");
      musicIcon.classList.add("fa-play");
    } else {
      backgroundMusic.play();
      musicIcon.classList.remove("fa-play");
      musicIcon.classList.add("fa-pause");
    }
    isPlaying = !isPlaying;
  });

  // Добавление новых полей для имени
  const addNameButton = document.getElementById("add-name");
  const nameFields = document.getElementById("name-fields");

  addNameButton.addEventListener("click", () => {
    const newField = document.createElement("div");
    newField.classList.add("name-field"); // Контейнер для нового поля

    // Добавляем поле ввода и кнопку удаления
    newField.innerHTML = `
      <input type="text" name="name[]" class="survey__input" placeholder="Имя и Фамилия" required>
      <button type="button" class="remove-name btn btn--remove">
        <i class="fas fa-trash"></i>
      </button>
    `;

    // Добавляем новое поле в контейнер
    nameFields.appendChild(newField);

    // Привязываем обработчик события для кнопки удаления
    const removeButton = newField.querySelector(".remove-name");
    removeButton.addEventListener("click", () => {
      nameFields.removeChild(newField); // Удаляем поле
    });
  });

  const attendanceYes = document.getElementById('attendance-yes');
  const attendanceNo = document.getElementById('attendance-no');
  const nameSection = document.getElementById('name-section');
  const drinksSection = document.getElementById('drinks-section');
  const submitSection = document.getElementById('submit-section');
  const nonAlcoholicCheckbox = document.getElementById('non-alcoholic');
  const nonAlcoholicInput = document.getElementById('non-alcoholic-input');
  window.history.scrollRestoration = "manual"; // Отключаем сохранение позиции прокрутки
  window.scrollTo(0, 0);
  // Показываем/скрываем секции в зависимости от выбора
  attendanceYes.addEventListener('change', () => {
    if (attendanceYes.checked) {
      nameSection.style.display = 'block';
      drinksSection.style.display = 'block';
      submitSection.style.display = 'block';
    }
  });

  attendanceNo.addEventListener('change', () => {
    if (attendanceNo.checked) {
      nameSection.style.display = 'block';
      drinksSection.style.display = 'none';
      submitSection.style.display = 'block';
    }
  });

  const form = document.getElementById("survey-form");
  const modal = document.getElementById("success-modal");
  const closeModalButton = document.getElementById("close-modal");

  form.addEventListener("submit", (event) => {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(form);

    fetch("/submit", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          // Показываем модальное окно
          modal.style.display = "flex";

          // Закрытие модального окна через 10 секунд
          setTimeout(() => {
            window.location.href = "/"; // Возврат на главную страницу
          }, 10000);
        } else {
          alert("Произошла ошибка при отправке данных.");
        }
      })
      .catch((error) => {
        console.error("Ошибка:", error);
        alert("Произошла ошибка при отправке данных.");
      });
  });

  // Обработчик для кнопки закрытия модального окна
  closeModalButton.addEventListener("click", () => {
    modal.style.display = "none";
    window.location.href = "/"; // Возврат на главную страницу
  });



  // Установка высоты вьюпорта для мобильных устройств
  const setViewportHeight = () => {
    const vh = document.documentElement.clientHeight * 0.01; // 1% от высоты видимой области
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  };
  
  // Устанавливаем высоту при загрузке страницы
  setViewportHeight();
  
  // Обновляем высоту при изменении размера окна
  window.addEventListener('resize', setViewportHeight);




const elementsToAnimate = document.querySelectorAll(
  ".timeline__event, .section__title, .section__text, .venue__img, .directions__text h3, .directions__text p, .line"
);

const handleScroll = () => {
  const scrollPosition = window.scrollY + window.innerHeight; // Текущая позиция прокрутки + высота окна

  elementsToAnimate.forEach((element) => {
      const rect = element.getBoundingClientRect(); // Положение элемента относительно окна
      const elementPosition = element.offsetTop; // Позиция элемента относительно документа

      // Если элемент находится в зоне видимости или выше текущей позиции
      if (scrollPosition >= elementPosition && rect.top <= window.innerHeight) {
          element.classList.add("visible");
      }
  });
};

// Проверяем элементы сразу при загрузке страницы
handleScroll();

// Запускаем проверку при прокрутке
window.addEventListener("scroll", handleScroll);
});
