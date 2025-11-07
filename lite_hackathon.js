// ======================================================
// 🔧 기본 유틸
// ======================================================
const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

// Footer year
const year = $('#year');
if (year) year.textContent = new Date().getFullYear();

// ======================================================
// 📂 Sidebar
// ======================================================
const openSidebar = () => {
  document.body.classList.add('is-open');
  $('#sidebar').setAttribute('aria-hidden', 'false');
  $('#overlay').setAttribute('aria-hidden', 'false');
};
const closeSidebar = () => {
  document.body.classList.remove('is-open');
  $('#sidebar').setAttribute('aria-hidden', 'true');
  $('#overlay').setAttribute('aria-hidden', 'true');
};

$('#openSidebar').addEventListener('click', openSidebar);
$('#closeSidebar').addEventListener('click', closeSidebar);
$('#overlay').addEventListener('click', closeSidebar);
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeSidebar();
});

// ======================================================
// 🔐 Login
// ======================================================
$('#loginBtn').addEventListener('click', () => {
  window.location.href = 'login.html';
});

// ======================================================
// 🔍 Search
// ======================================================
$('#searchForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const q = ($('#q').value || '').trim();
  if (!q) return alert('검색어를 입력하세요.');
  alert(`검색 기능 준비 중입니다.\n입력한 검색어: ${q}`);
});

// ======================================================
// 🗓️ Timetable grid
// ======================================================
(function buildTimetable() {
  const area = $('.timetable .cells');
  if (!area) return;
  const rows = 5,
    cols = 6;
  for (let i = 0; i < rows * cols; i++) {
    area.appendChild(document.createElement('div'));
  }
})();

// ======================================================
// 🧩 Widget modal
// ======================================================
const modal = $('#widgetModal');
const openModal = () => document.body.classList.add('is-modal');
const closeModal = () => document.body.classList.remove('is-modal');

$('#fabAdd').addEventListener('click', openModal);
$('#closeModal').addEventListener('click', closeModal);
modal.addEventListener('click', (e) => {
  if (e.target === modal) closeModal();
});

// ======================================================
// 🧱 Widget factory
// ======================================================
function createWidget(type) {
  const card = document.createElement('article');
  card.className = 'widget';
  card.dataset.widget = type;

  const header = document.createElement('header');
  header.className = 'widget-header';

  const h3 = document.createElement('h3');
  const closeBtn = document.createElement('button');
  closeBtn.className = 'icon-btn sm remove-widget';
  closeBtn.title = '위젯 삭제';
  closeBtn.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>`;

  closeBtn.addEventListener('click', () => {
    setTimeout(() => {
      card.remove();
      updateWidgetHint();
    }, 0);
  });

  header.append(h3, closeBtn);

  const body = document.createElement('div');
  body.className = 'widget-body';

  switch (type) {
    case 'timetable': {
      h3.textContent = '시간표';
      const wrap = document.createElement('div');
      wrap.className = 'timetable';
      const cells = document.createElement('div');
      cells.className = 'cells';
      for (let i = 0; i < 30; i++)
        cells.appendChild(document.createElement('div'));
      wrap.appendChild(cells);
      body.appendChild(wrap);
      break;
    }
    case 'lunch': {
      h3.textContent = '오늘의 급식';
      const ul = document.createElement('ul');
      ul.className = 'lunch-list';
      [
        '밥 · 국 · 메인 반찬',
        '부반찬 A',
        '부반찬 B',
        '디저트(과일/요거트)',
      ].forEach((t) => {
        const li = document.createElement('li');
        li.textContent = t;
        ul.appendChild(li);
      });
      body.appendChild(ul);
      break;
    }
    case 'exam-schedule': {
      h3.textContent = '수행평가 일정';
      body.innerHTML =
        '<p>다가오는 수행평가 일정이 표시됩니다. (연동 예정)</p>';
      break;
    }
    case 'calendar': {
      h3.textContent = '캘린더';
      body.innerHTML = '<p>월간 학사일정 위젯입니다. (연동 예정)</p>';
      break;
    }
    case 'notice': {
      h3.textContent = '알림';
      body.innerHTML = '<p>공지/알림 모아보기. (연동 예정)</p>';
      break;
    }
    default: {
      h3.textContent = '커스텀 위젯';
      body.textContent = '내용을 구성하세요.';
    }
  }

  card.append(header, body);
  return card;
}

// ======================================================
// 💡 위젯 안내 문구
// ======================================================
function updateWidgetHint() {
  const widgetCount = document.querySelectorAll('.widget-grid .widget').length;
  const hint = document.getElementById('widgetHint');
  if (!hint) return;
  hint.style.display = widgetCount === 0 ? 'inline-block' : 'none';
}

// ======================================================
// ➕ 모달에서 위젯 추가
// ======================================================
$$('.picker-item', modal).forEach((btn) => {
  btn.addEventListener('click', () => {
    const w = createWidget(btn.dataset.widget);
    $('#widgetGrid').appendChild(w);
    updateWidgetHint();
    closeModal();
  });
});

// ======================================================
// 🗑️ 초기 위젯 삭제 버튼
// ======================================================
$$('.remove-widget').forEach((btn) => {
  btn.addEventListener('click', (e) => {
    const card = e.currentTarget.closest('.widget');
    setTimeout(() => {
      card.remove();
      updateWidgetHint();
    }, 0);
  });
});

// ✅ 페이지 로드 시 초기 상태 확인
updateWidgetHint();

// ======================================================
// 💬 채팅 + Gmail 전송 기능 추가
// ======================================================

if (typeof io !== 'undefined') {
  const socket = io();

  const chatInput = $('#chatInput');
  const chatMessages = $('#chatMessages');
  const sendBtn = $('#sendBtn');
  const toggleChat = $('#toggleChat');
  const chatBox = $('#chatbox');
  const teacherSelect = $('#teacher');

  let folded = false;
  let chatHistory = [];

  // 메시지 추가 함수
  function addMsg(text, who = 'you') {
    const div = document.createElement('div');
    div.className = 'msg' + (who === 'me' ? ' me' : '');
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    chatHistory.push((who === 'me' ? '나: ' : '선생님: ') + text);
  }

  // 전송 버튼 클릭 시
  if (sendBtn) {
    sendBtn.addEventListener('click', () => {
      const msg = chatInput.value.trim();
      if (!msg) return;
      addMsg(msg, 'me');
      socket.emit('message', msg);
      chatInput.value = '';

      const email = teacherSelect.value;
      if (email) {
        fetch('/send_gmail', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: email,
            content: chatHistory.join('\n'),
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.status === 'ok') {
              addMsg(`✅ 대화 내용이 ${email} 로 전송되었습니다.`);
            } else {
              addMsg(`⚠️ 메일 전송 실패: ${data.message}`);
            }
          })
          .catch((err) => addMsg('⚠️ 네트워크 오류: ' + err.message));
      }
    });
  }

  // Enter 키 전송
  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendBtn.click();
      }
    });
  }

  // 서버로부터 메시지 수신
  socket.on('message', (msg) => addMsg(msg, 'you'));

  // 접기 버튼
  if (toggleChat) {
    toggleChat.addEventListener('click', () => {
      folded = !folded;
      chatBox.classList.toggle('folded', folded);
      toggleChat.innerHTML = folded
        ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><path d="M6 9l6 6 6-6" /></svg>'
        : '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><path d="M18 15l-6-6-6 6" /></svg>';
    });
  }
}
