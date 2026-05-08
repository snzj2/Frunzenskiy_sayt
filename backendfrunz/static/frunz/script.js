// Глобальные UI-элементы
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav');
const accessibilityBtn = document.querySelector('[data-accessibility-toggle]');

if (burger && nav) {
  burger.addEventListener('click', () => {
    const opened = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', String(opened));
  });
}

// Переключатель версии для слабовидящих
function applyAccessibilityMode(enabled) {
  document.body.classList.toggle('accessible', enabled);
  if (accessibilityBtn) {
    const nextLabel = enabled ? 'Обычная версия' : 'Версия для слабовидящих';
    if (!accessibilityBtn.classList.contains('access-icon-btn')) {
      accessibilityBtn.textContent = nextLabel;
    }
    accessibilityBtn.setAttribute('aria-label', nextLabel);
    accessibilityBtn.setAttribute('title', nextLabel);
    accessibilityBtn.setAttribute('aria-pressed', String(enabled));
  }
}

const storedAccessibility = localStorage.getItem('accessibilityMode') === '1';
applyAccessibilityMode(storedAccessibility);

if (accessibilityBtn) {
  accessibilityBtn.addEventListener('click', () => {
    const next = !document.body.classList.contains('accessible');
    localStorage.setItem('accessibilityMode', next ? '1' : '0');
    applyAccessibilityMode(next);
  });
}

// Фильтры для страниц мероприятий/клубов/новостей/документов
function initFilterableList() {
  const listRoot = document.querySelector('[data-list-root]');
  if (!listRoot) return;

  const items = [...listRoot.querySelectorAll('[data-item]')];
  const controls = [...document.querySelectorAll('[data-filter-control]')];
  const search = document.querySelector('[data-search-control]');

  function normalize(value) {
    return String(value || '').toLowerCase().trim();
  }

  function applyFilters() {
    const controlValues = {};
    controls.forEach((control) => {
      controlValues[control.dataset.filterControl] = normalize(control.value);
    });
    const query = normalize(search?.value);

    let visible = 0;
    items.forEach((item) => {
      const matchesControls = Object.entries(controlValues).every(([key, value]) => {
        if (!value || value === 'all') return true;
        return normalize(item.dataset[key]).includes(value);
      });
      const haystack = normalize(item.dataset.search || item.textContent);
      const matchesSearch = !query || haystack.includes(query);
      const show = matchesControls && matchesSearch;
      item.classList.toggle('hidden', !show);
      if (show) visible += 1;
    });

    const empty = document.querySelector('[data-empty-state]');
    if (empty) empty.classList.toggle('hidden', visible > 0);
  }

  controls.forEach((control) => control.addEventListener('change', applyFilters));
  if (search) search.addEventListener('input', applyFilters);
  applyFilters();
}

initFilterableList();

// Фильтр для блока "Студии и направления" на странице клубов
function initStudiosFilter() {
  const root = document.querySelector('[data-studio-filter]');
  if (!root) return;

  const direction = root.querySelector('[data-studio-direction]');
  const cost = root.querySelector('[data-studio-cost]');
  const ageInput = root.querySelector('[data-studio-age]');
  const applyBtn = root.querySelector('[data-studio-apply]');
  const groupsRoot = document.querySelector('[data-studio-groups]');
  const countNode = document.querySelector('[data-studios-count]');
  const emptyState = document.querySelector('[data-studio-empty]');
  const modal = document.querySelector('[data-studio-modal]');

  if (!direction || !cost || !ageInput || !applyBtn || !groupsRoot || !modal) return;

  const data = [
    ['Музыкальное', 'Студия гитары «Аккорд»', '10-18'], ['Музыкальное', 'Студия фортепиано', '10-18'], ['Музыкальное', 'Скрипка', '12-25'],
    ['Вокальное', 'Студия эстрадного вокала', '10-18'], ['Вокальное', 'Вокальная студия', '10-18'], ['Вокальное', 'Вокально-инструментальные ансамбли', '10-18'], ['Вокальное', 'Студия вокала / ансамблевое пение', '10-18'],
    ['Танцевальное', 'Студия «Лаборатория танца»', '10-25'], ['Танцевальное', 'Ансамбль танца «Романтика»', '10-25'], ['Танцевальное', 'Пауэрлифтинг', '10-25'], ['Танцевальное', 'Спортивно-бальные танцы', '10-25'], ['Танцевальное', 'Студия акробатического рок-н-ролла «ЛИДЕР»', '10-25'], ['Танцевальное', 'Студия современного танца', '10-25'], ['Танцевальное', 'Студия современного танца «HEADWAY»', '10-25'], ['Танцевальное', 'Танцевально-акробатическая студия «FITBOLDANCE»', '10-25'], ['Танцевальное', 'Танцевальный класс «Геппи»', '10-25'], ['Танцевальное', 'Театр танца «Жемчужины Петербурга»', '10-25'], ['Танцевальное', 'Хореографический ансамбль «Каприз»', '10-25'], ['Танцевальное', 'Хореографический ансамбль «СМАЙЛ»', '10-25'],
    ['Театральное', 'Театр-студия «Мы»', '10-18'],
    ['Изобразительное', 'ИЗО-студия «Акварель»', '8-18'], ['Изобразительное', 'ИЗО-студия «Арт-город»', '8-18'], ['Изобразительное', 'Изостудия «Волшебная кисточка»', '8-18'], ['Изобразительное', 'Студия «Палитра»', '8-18'], ['Изобразительное', 'Студия живописи и мультипликации', '8-18'], ['Изобразительное', 'Студия росписи фарфора', '8-18'], ['Изобразительное', 'Художественная студия', '8-18'],
    ['Патриотическое', 'Студия исторический средневековый бой «Клуб Пересвет»', '12-18'],
    ['Спортивное', 'Армейский рукопашный бой (АРБ)', '10-25'], ['Спортивное', 'Ашихара каратэ', '10-25'], ['Спортивное', 'Бокс', '10-25'], ['Спортивное', 'Военно-тактические игры. Страйкбол', '10-25'], ['Спортивное', 'Волейбол', '10-25'], ['Спортивное', 'Каратэ', '10-25'], ['Спортивное', 'Настольный теннис', '10-25'], ['Спортивное', 'ОФП с элементами боевых искусств', '10-25'], ['Спортивное', 'Самбо', '10-25'], ['Спортивное', 'Секция «Своя игра»: шахматы, шашки, настольные игры', '10-25'], ['Спортивное', 'Страйкбол и Лазертаг', '10-25'], ['Спортивное', 'Стретчинг', '10-25'], ['Спортивное', 'Студия «Осознанный стретчинг»', '10-25'], ['Спортивное', 'Студия Саберфайтинг', '10-25'], ['Спортивное', 'Техника уличной самообороны', '10-25'], ['Спортивное', 'Тренажерный зал', '10-25'], ['Спортивное', 'Тхэквондо', '10-25'], ['Спортивное', 'Тяжелая атлетика', '10-25'], ['Спортивное', 'Шахматы', '10-25'],
    ['Другие направления', 'Волонтёрство', '12-25'], ['Другие направления', 'Место свободного общения', '12-25'], ['Другие направления', 'Место свободного общения («Гармония»)', '12-25'], ['Другие направления', 'Место свободного общения («Искра»)', '12-25'], ['Другие направления', 'Место свободного общения («Молоко»)', '12-25'], ['Другие направления', 'Место свободного общения («Прогресс»)', '12-25'], ['Другие направления', 'Место свободного общения («Романтика»)', '12-25'], ['Другие направления', 'Место свободного общения («Современник»)', '12-25'], ['Другие направления', 'Место свободного общения («Старт»)', '12-25'], ['Другие направления', 'Место свободного общения («Факел»)', '12-25'], ['Другие направления', 'Место свободного общения («Юность»)', '12-25'], ['Другие направления', 'Место свободного общения (3ФДНО / ВПК им. 3-й Фрунзенской дивизии)', '12-25'], ['Другие направления', 'Студия английского языка «Английский клуб»', '12-25'], ['Другие направления', 'Студия красоты и здоровья', '12-25']
  ].map(([category, title, age]) => ({ category, title, age, cost: 'бесплатно' }));

  const categoryDescriptions = {
    'Музыкальное': 'Инструменты, чувство ритма, музыкальный слух и сценическая практика.',
    'Вокальное': 'Постановка голоса, дыхание, ансамблевое пение и выступления.',
    'Танцевальное': 'Хореография, пластика, координация, сцена и динамика.',
    'Театральное': 'Актёрское мастерство, сценическая речь и работа в команде.',
    'Изобразительное': 'Рисунок, живопись, композиция и прикладное творчество.',
    'Патриотическое': 'Историческая реконструкция, командность и дисциплина.',
    'Спортивное': 'Сила, выносливость, дисциплина и соревновательные форматы.',
    'Другие направления': 'Коммуникация, мягкие навыки, полезные практики и сообщества.'
  };

  function inAgeRange(itemAge, ageValue) {
    if (!ageValue) return true;
    const [min, max] = String(itemAge || '').split('-').map(Number);
    if (!Number.isFinite(min) || !Number.isFinite(max)) return true;
    return ageValue >= min && ageValue <= max;
  }

  function openModal(studio) {
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
    modal.querySelector('[data-modal-direction]').textContent = `${studio.category.toUpperCase()} НАПРАВЛЕНИЕ`;
    modal.querySelector('[data-modal-title]').textContent = studio.title;
    modal.querySelector('[data-modal-description]').textContent = categoryDescriptions[studio.category];
    modal.querySelector('[data-modal-direction-tag]').textContent = studio.category;
    modal.querySelector('[data-modal-age]').textContent = `Возраст: ${studio.age} лет`;
    modal.querySelector('[data-modal-cost]').textContent = 'Стоимость: бесплатно';
    modal.querySelector('[data-modal-about]').textContent = `${studio.title} помогает развивать навыки в направлении «${studio.category.toLowerCase()}» в безопасной и поддерживающей среде.`;
    modal.querySelector('[data-modal-audience]').textContent = `Подойдёт участникам ${studio.age} лет, кто хочет регулярно заниматься, прокачивать навыки и участвовать в мероприятиях центра.`;
    modal.querySelector('[data-modal-important]').textContent = 'Расписание, площадку и наличие мест лучше уточнять у администратора центра перед записью.';
    modal.querySelector('[data-modal-program]').innerHTML = '<li>основы и практика по направлению</li><li>работа с педагогом и в группе</li><li>подготовка к выступлениям и проектам</li>';
  }

  function closeModal() {
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
  }

  modal.querySelectorAll('[data-studio-modal-close]').forEach((btn) => btn.addEventListener('click', closeModal));

  function applyStudiosFilter() {
    const selectedDirection = direction.value;
    const selectedCost = cost.value;
    const ageValue = Number(ageInput.value);
    const hasAge = Number.isFinite(ageValue) && ageInput.value !== '';

    const filtered = data.filter((item) => {
      const directionOk = selectedDirection === 'all' || item.category === selectedDirection;
      const costOk = selectedCost === 'all' || item.cost === selectedCost;
      const ageOk = !hasAge || inAgeRange(item.age, ageValue);
      return directionOk && costOk && ageOk;
    });

    groupsRoot.innerHTML = '';
    const grouped = filtered.reduce((acc, item) => {
      (acc[item.category] ||= []).push(item);
      return acc;
    }, {});

    Object.entries(grouped).forEach(([category, studios]) => {
      const section = document.createElement('article');
      section.className = 'studios-direction-block';
      section.innerHTML = `
        <div class="studios-direction-head">
          <h3>${category} направление</h3>
          <span>${studios.length} ${studios.length === 1 ? 'студия' : 'студии'}</span>
        </div>
        <p>${categoryDescriptions[category]}</p>
        <div class="studios-cards-grid">
          ${studios.map((studio) => `
            <article class="studio-card" tabindex="0">
              <div class="studio-card-top"><span class="studio-chip">${studio.category}</span><span class="studio-arrow">↗</span></div>
              <h4>${studio.title}</h4>
              <p>${categoryDescriptions[category]}</p>
              <div class="studio-card-tags"><span>Возраст: ${studio.age} лет</span><span>Стоимость: бесплатно</span></div>
              <button type="button" class="studio-link">Подробнее о студии</button>
            </article>
          `).join('')}
        </div>
      `;
      groupsRoot.append(section);

      const cards = section.querySelectorAll('.studio-card');
      cards.forEach((card, idx) => {
        const studio = studios[idx];
        const handler = () => openModal(studio);
        card.addEventListener('click', handler);
        card.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            handler();
          }
        });
      });
    });

    if (countNode) countNode.textContent = `Показано ${filtered.length} студий.`;
    if (emptyState) emptyState.classList.toggle('hidden', filtered.length > 0);
  }

  applyBtn.addEventListener('click', applyStudiosFilter);
  direction.addEventListener('change', applyStudiosFilter);
  cost.addEventListener('change', applyStudiosFilter);
  ageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') applyStudiosFilter();
  });

  applyStudiosFilter();
}

initStudiosFilter();

// Кликабельные карточки клубов с переходом в Яндекс Карты
function initClubMapCards() {
  if (!(location.pathname.endsWith('clubs.html') || location.pathname === '/clubs/' || location.pathname.startsWith('/clubs/?'))) return;
  const clubsSectionCards = document.querySelector('.section .cards');
  if (!clubsSectionCards) return;
  const cards = [...clubsSectionCards.querySelectorAll('.card')];
  if (!cards.length) return;

  cards.forEach((card) => {
    const meta = card.querySelector('.meta');
    if (!meta) return;
    const address = meta.textContent.trim();
    const url = `https://yandex.ru/maps/?text=${encodeURIComponent(address)}`;

    card.classList.add('club-map-card');
    card.setAttribute('tabindex', '0');
    card.setAttribute('role', 'link');
    card.setAttribute('aria-label', `Открыть на карте: ${address}`);

    const openMap = () => window.open(url, '_blank', 'noopener');
    card.addEventListener('click', openMap);
    card.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openMap();
      }
    });
  });
}

initClubMapCards();

// Колесо интересов на главной
function initInterestsWheel() {
  const wheelRoot = document.querySelector('[data-interests-wheel]');
  if (!wheelRoot) return;

  const disc = wheelRoot.querySelector('[data-wheel-disc]');
  const spinBtn = wheelRoot.querySelector('[data-wheel-spin]');
  const resetBtn = wheelRoot.querySelector('[data-wheel-reset]');
  const resultCard = wheelRoot.querySelector('[data-wheel-result]');
  const resultTitle = wheelRoot.querySelector('[data-wheel-title]');
  const resultDescription = wheelRoot.querySelector('[data-wheel-description]');
  const resultList = wheelRoot.querySelector('[data-wheel-list]');

  const sectors = [
    {
      name: 'Спорт',
      description: 'Тебе подойдут активные и командные форматы, где можно проявить себя, зарядиться энергией и найти новых друзей.',
      picks: ['Танцевальная студия', 'Командные тренировки', 'Районные турниры']
    },
    {
      name: 'Медиа и digital',
      description: 'Тебе близки визуал, съёмка, контент и цифровые проекты. Здесь можно пробовать, создавать и развивать свои идеи.',
      picks: ['Фото- и видеостудия', 'Медиа-клуб', 'Digital-мастерская']
    },
    {
      name: 'Творчество',
      description: 'Тебе подойдут направления, где можно раскрыть себя через сцену, музыку, арт и креативные форматы.',
      picks: ['Театральная студия', 'Вокальное направление', 'Арт-мастерская']
    },
    {
      name: 'Волонтёрство',
      description: 'Тебе может быть интересно участвовать в полезных инициативах, помогать другим и становиться частью значимых проектов.',
      picks: ['Доброцентр', 'Волонтёрские акции', 'Социальные инициативы']
    },
    {
      name: 'Интеллект и развитие',
      description: 'Тебе подойдут форматы, где можно развивать мышление, навыки общения, лидерство и собственные проекты.',
      picks: ['Дискуссионный клуб', 'Проектная лаборатория', 'Образовательные интенсивы']
    },
    {
      name: 'Мероприятия',
      description: 'Тебе ближе динамика, встречи, фестивали и яркие события, где постоянно происходит что-то новое.',
      picks: ['Молодёжные фестивали', 'Районные события', 'Тематические программы']
    }
  ];

  let currentRotation = 0;

  function showResult(sector) {
    resultTitle.textContent = sector.name;
    resultDescription.textContent = sector.description;
    resultList.innerHTML = sector.picks.map((item) => `<li>${item}</li>`).join('');
    resultCard.classList.remove('hidden');
    resetBtn.classList.remove('hidden');
  }

  spinBtn.addEventListener('click', () => {
    const index = Math.floor(Math.random() * sectors.length);
    const segment = 360 / sectors.length;
    const centerOffset = index * segment + segment / 2;
    const spins = 5 + Math.floor(Math.random() * 3);
    currentRotation += spins * 360 + (360 - centerOffset);

    spinBtn.disabled = true;
    resetBtn.classList.add('hidden');
    resultCard.classList.add('hidden');
    disc.style.transform = `rotate(${currentRotation}deg)`;

    setTimeout(() => {
      showResult(sectors[index]);
      spinBtn.disabled = false;
    }, 4300);
  });

  resetBtn.addEventListener('click', () => {
    resultCard.classList.add('hidden');
    resetBtn.classList.add('hidden');
  });
}

initInterestsWheel();

// Обратная связь
const feedbackForms = document.querySelectorAll('[data-feedback-form]');
feedbackForms.forEach((form) => {
  const message = form.querySelector('[data-form-message]');
  form.addEventListener('submit', (event) => {
    if (form.dataset.serverForm === 'true') { return; }
    event.preventDefault();
    if (message) {
      message.textContent = 'Спасибо! Ваше обращение принято. Специалист свяжется с вами в рабочее время.';
    }
    form.reset();
  });
});
