document.addEventListener('DOMContentLoaded', function() {
  // ========== Навбар при скролле ==========
  const navbar = document.querySelector('.navbar');
  
  function updateNavbar() {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
  
  // Инициализация при загрузке
  updateNavbar();
  
  // Обновление при скролле
  window.addEventListener('scroll', function() {
    updateNavbar();
  });

  // ========== Плавная прокрутка ==========
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        // Закрываем мобильное меню если открыто
        const navbarCollapse = document.querySelector('.navbar-collapse.show');
        if (navbarCollapse) {
          new bootstrap.Collapse(navbarCollapse).hide();
        }
        
        // Плавная прокрутка
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: 'smooth'
        });
        
        // Добавляем хеш в URL без перезагрузки
        if (history.pushState) {
          history.pushState(null, null, targetId);
        } else {
          location.hash = targetId;
        }
      }
    });
  });

  // ========== Анимации при прокрутке ==========
  function animateOnScroll() {
    const elements = document.querySelectorAll('.service-card, .value-item');
    const windowHeight = window.innerHeight;
    
    elements.forEach(element => {
      const elementPosition = element.getBoundingClientRect().top;
      const animationPoint = windowHeight - 100;
      
      if (elementPosition < animationPoint) {
        element.classList.add('fade-in');
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
      }
    });
  }
  
  // Инициализация анимаций
  document.querySelectorAll('.service-card, .value-item').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  });
  
  // Запуск при загрузке и скролле
  animateOnScroll();
  window.addEventListener('scroll', animateOnScroll);

  // ========== Обработка форм ==========
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Создаем уведомление
      const alertDiv = document.createElement('div');
      alertDiv.className = 'alert alert-success alert-dismissible fade show';
      alertDiv.style.position = 'fixed';
      alertDiv.style.bottom = '20px';
      alertDiv.style.right = '20px';
      alertDiv.style.zIndex = '1000';
      alertDiv.style.maxWidth = '300px';
      alertDiv.innerHTML = `
        <strong>Спасибо!</strong> Ваша заявка принята. Мы свяжемся с вами в ближайшее время.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      
      document.body.appendChild(alertDiv);
      
      // Закрытие через 5 секунд
      setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
      }, 5000);
      
      // Сбрасываем форму
      this.reset();
      
      // Закрываем модальное окно если есть
      const modal = bootstrap.Modal.getInstance(document.getElementById('call'));
      if (modal) {
        modal.hide();
      }
    });
  });

  // ========== Инициализация модального окна ==========
  const callModal = document.getElementById('call');
  if (callModal) {
    callModal.addEventListener('shown.bs.modal', function() {
      document.getElementById('nameInput').focus();
    });
  }

  // ========== Плавное появление страницы ==========
  document.body.style.opacity = '0';
  setTimeout(() => {
    document.body.style.transition = 'opacity 0.5s ease';
    document.body.style.opacity = '1';
  }, 100);
});