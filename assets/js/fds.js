/* =====================================================================
   First Digital Surveillance — site JS  (v2)
   nav · CRM lead routing · UTM capture · speed-to-lead · live feeds
   · scroll reveal · counters · AI chat + live agent
   ---------------------------------------------------------------------
   >>> GO-LIVE: everything you change lives in FDS_CONFIG below.
   ===================================================================== */

const FDS_CONFIG = {

  /* ---- 1. CRM inbound webhook ----------------------------------------
     Any CRM / automation platform that accepts an inbound webhook works.
     Paste the endpoint URL here. Every form, the callback bar and the
     chatbot POST a JSON lead to it.
     Leave "" to run in DEMO mode (no network call, payload logged instead). */
  crmWebhookUrl: "",

  /* ---- 2. Optional hosted form / calendar embeds ----------------------
     Drop in an embed URL and the matching block on the page is replaced
     by the live iframe. Leave blank to keep the built-in versions.       */
  crmEmbeds: {
    contactForm: "",
    quoteForm:   "",
    calendar:    ""
  },

  /* ---- 3. Optional hosted chat widget ---------------------------------
     Set useHostedChat:true plus a loader URL + widget id to swap the
     built-in Ava widget for a hosted live-chat product.                  */
  useHostedChat: false,
  hostedChatLoaderUrl: "",
  hostedChatResourcesUrl: "",
  hostedChatWidgetId: "",

  /* ---- 4. Speed to Lead ----------------------------------------------
     callbackSeconds  = the promise made on the site (countdown length)
     avgResponse      = the number shown in the live "avg first response" pill */
  callbackSeconds: 60,
  avgResponseSeconds: 47,

  /* ---- 5. Tracking ---------------------------------------------------- */
  gtmId: "",              // GTM-XXXXXXX
  ga4Id: "",              // G-XXXXXXXXXX
  callTrackingNumber: "", // dynamic number insertion for paid traffic

  /* ---- 6. Business constants ------------------------------------------ */
  phone: "(310) 901-4954",
  phoneRaw: "+13109014954",
  email: "info@cctvinstallation-losangeles.com",

  /* ---- 7. Live agent hours (local time) -------------------------------- */
  liveHours: { weekday: [7, 19], weekend: [9, 17] }
};

/* ===================================================================== */
const $  = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];

function getUtms() {
  const p = new URLSearchParams(location.search);
  const keep = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','msclkid'];
  const out = {};
  keep.forEach(k => { if (p.get(k)) out[k] = p.get(k); });
  try {
    const stored = JSON.parse(sessionStorage.getItem('fds_utm') || '{}');
    Object.assign(stored, out);
    sessionStorage.setItem('fds_utm', JSON.stringify(stored));
    return stored;
  } catch (e) { return out; }
}

function agentIsOnline() {
  const n = new Date(), d = n.getDay(), h = n.getHours();
  const w = (d === 0 || d === 6) ? FDS_CONFIG.liveHours.weekend : FDS_CONFIG.liveHours.weekday;
  return h >= w[0] && h < w[1];
}

/* ---------------------------------------------------------------------
   Every lead on the site goes through here.
   Demo mode logs the exact JSON the CRM will receive.
   --------------------------------------------------------------------- */
async function pushLead(payload) {
  const lead = {
    ...payload,
    source: 'Website — First Digital Surveillance',
    page: location.pathname.split('/').pop() || 'index.html',
    pageTitle: document.title,
    referrer: document.referrer || 'direct',
    submittedAt: new Date().toISOString(),
    speedToLeadTarget: FDS_CONFIG.callbackSeconds + 's',
    ...getUtms()
  };

  console.log('%c[LEAD CAPTURED]', 'background:#BF1220;color:#fff;padding:2px 7px;border-radius:4px', lead);
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: 'generate_lead', lead_type: lead.formName, value: 1 });

  if (!FDS_CONFIG.crmWebhookUrl) return { demo: true, lead };
  try {
    await fetch(FDS_CONFIG.crmWebhookUrl, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(lead)
    });
    return { ok: true, lead };
  } catch (e) { console.warn('Lead webhook failed', e); return { ok: false, lead }; }
}

/* =====================================================================
   Chrome: header, nav, reveal, counters
   ===================================================================== */
function initChrome() {
  const header = $('.header');
  if (header) {
    const onScroll = () => header.classList.toggle('is-stuck', window.scrollY > 8);
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
  const burger = $('.burger'), nav = $('.nav');
  if (burger && nav) burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open);
  });

  const here = location.pathname.split('/').pop() || 'index.html';
  $$('.nav a').forEach(a => { if (a.getAttribute('href') === here) a.classList.add('is-active'); });

  if (FDS_CONFIG.callTrackingNumber) $$('[data-phone]').forEach(el => el.textContent = FDS_CONFIG.callTrackingNumber);
  $$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
  $$('[data-avg]').forEach(el => el.textContent = FDS_CONFIG.avgResponseSeconds + 's');
  $$('[data-cbsec]').forEach(el => el.textContent = FDS_CONFIG.callbackSeconds);

  // scroll reveal (fail-open if IO is unsupported)
  if (!('IntersectionObserver' in window)) { $$('[data-reveal]').forEach(el => el.classList.add('in')); return; }
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  $$('[data-reveal]').forEach((el, i) => { el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });

  // count-up numbers
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target, to = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
    const pre = el.dataset.pre || '', suf = el.dataset.suf || '';
    let t0 = null;
    const tick = ts => {
      if (!t0) t0 = ts;
      const p = Math.min((ts - t0) / 1400, 1), e2 = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + (to * e2).toFixed(dec).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suf;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick); cio.unobserve(el);
  }), { threshold: .5 });
  $$('[data-count]').forEach(el => cio.observe(el));
}


/* =====================================================================
   Hero service carousel
   ===================================================================== */
function initHeroSlider() {
  const wrap = $('.heroslides'); if (!wrap) return;
  const slides = $$('.hslide', wrap);
  const dots = $$('.hdot');
  const count = $('.hcount b');
  if (slides.length < 2) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const DWELL = 6500;
  let i = 0, timer = null, paused = false;

  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('is-on', k === i));
    dots.forEach((d, k) => d.classList.toggle('is-on', k === i));
    if (count) count.textContent = String(i + 1).padStart(2, '0');
  }
  function next(step) { show(i + step); restart(); }
  function restart() {
    clearInterval(timer);
    if (reduced || paused) return;
    timer = setInterval(() => show(i + 1), DWELL);
  }

  dots.forEach(d => d.addEventListener('click', () => next(+d.dataset.go - i)));
  $$('.harrow').forEach(a => a.addEventListener('click', () => next(+a.dataset.dir)));

  // pause while the visitor is reading or interacting
  const hero = wrap.closest('.hero') || wrap;
  const hold = v => { paused = v; wrap.classList.toggle('is-paused', v); restart(); };
  hero.addEventListener('mouseenter', () => hold(true));
  hero.addEventListener('mouseleave', () => hold(false));
  hero.addEventListener('focusin', () => hold(true));
  hero.addEventListener('focusout', () => hold(false));
  document.addEventListener('visibilitychange', () => hold(document.hidden));

  // keyboard
  hero.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { e.preventDefault(); next(1); }
    if (e.key === 'ArrowLeft')  { e.preventDefault(); next(-1); }
  });

  // swipe
  let x0 = null;
  wrap.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  wrap.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 45) next(dx < 0 ? 1 : -1);
    x0 = null;
  }, { passive: true });

  show(0); restart();
}

/* =====================================================================
   Live camera feeds — real clock in the HUD
   ===================================================================== */
function initFeeds() {
  const stamps = $$('.feed__clock');
  if (!stamps.length) return;
  const tick = () => {
    const d = new Date();
    const p = n => String(n).padStart(2, '0');
    const s = `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
    stamps.forEach(el => el.textContent = s);
  };
  tick(); setInterval(tick, 1000);
}

/* =====================================================================
   SPEED TO LEAD — header callback widget
   ===================================================================== */
function initCallback() {
  $$('.callback').forEach(box => {
    const form = $('.callback__form', box);
    const live = $('.callback__live', box);
    if (!form || !live) return;
    const ringFg = $('.ring .fg', live), ringNum = $('.ring b', live), label = $('.cb-label', live);

    form.addEventListener('submit', async e => {
      e.preventDefault();
      const input = $('input', form), val = input.value.trim();
      if (!val) { input.focus(); return; }

      await pushLead({ formName: 'Speed to Lead — header callback', phone: val, requestType: 'Instant callback' });
      input.value = '';
      box.classList.add('is-live');

      const total = FDS_CONFIG.callbackSeconds;
      let left = total;
      const C = 94.2;
      const steps = [
        [total, 'Request received'],
        [Math.round(total * .85), 'Confirmation text sent'],
        [Math.round(total * .55), 'Routing to an available tech'],
        [Math.round(total * .25), 'Tech is dialing you now']
      ];
      const paint = () => {
        ringNum.textContent = left;
        ringFg.style.strokeDashoffset = C - (left / total) * C;
        const s = steps.find(s => left <= s[0]);
        if (s) label.textContent = s[1];
      };
      paint();
      const iv = setInterval(() => {
        left--;
        if (left <= 0) {
          clearInterval(iv);
          ringNum.textContent = '✓';
          ringFg.style.strokeDashoffset = 0;
          label.textContent = 'Calling you now';
          setTimeout(() => box.classList.remove('is-live'), 6000);
          return;
        }
        paint();
      }, 1000);
    });
  });
}

/* =====================================================================
   SPEED TO LEAD — phone demo sequence
   ===================================================================== */
function initPhoneDemo() {
  const phone = $('.phone'); if (!phone) return;
  const items = $$('[data-seq]', phone).sort((a, b) => a.dataset.seq - b.dataset.seq);
  const timers = [];
  const run = () => {
    timers.forEach(clearTimeout); timers.length = 0;
    items.forEach(i => i.classList.remove('show'));
    items.forEach(i => timers.push(setTimeout(() => i.classList.add('show'), +i.dataset.delay)));
  };
  $('.phone__replay', phone)?.addEventListener('click', run);
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { run(); io.unobserve(e.target); } }), { threshold: .35 });
  io.observe(phone);
}


/* =====================================================================
   Site-visit booker (built-in; swap for a hosted calendar via crmEmbeds)
   ===================================================================== */
function initBooker() {
  const box = $('.booker'); if (!box) return;
  const daysEl = $('.booker__days', box), slotsEl = $('.booker__slots', box);
  const selEl = $('.booker__sel', box), goEl = $('.booker__go', box);
  const SLOTS = ['8:00 – 10:00 AM', '10:00 AM – 12:00 PM', '12:00 – 2:00 PM', '2:00 – 4:00 PM', '4:00 – 6:00 PM'];
  const state = { day: null, dayLabel: '', slot: null };

  const D = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  const M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  for (let i = 1; i <= 7; i++) {
    const d = new Date(); d.setDate(d.getDate() + i);
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'daychip';
    b.innerHTML = `<small>${D[d.getDay()]}</small><b>${d.getDate()}</b><span>${M[d.getMonth()]}</span>`;
    b.addEventListener('click', () => {
      $$('.daychip', daysEl).forEach(x => x.classList.remove('is-on'));
      b.classList.add('is-on');
      state.day = d; state.dayLabel = `${D[d.getDay()]} ${M[d.getMonth()]} ${d.getDate()}`;
      state.slot = null; renderSlots(i); update();
    });
    daysEl.appendChild(b);
  }

  function renderSlots(seed) {
    slotsEl.innerHTML = '';
    SLOTS.forEach((t, j) => {
      const taken = ((seed * 3 + j * 5) % 7) === 0;
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'slot' + (taken ? ' is-taken' : '');
      b.textContent = t; b.disabled = taken;
      if (taken) b.title = 'Already booked';
      b.addEventListener('click', () => {
        $$('.slot', slotsEl).forEach(x => x.classList.remove('is-on'));
        b.classList.add('is-on'); state.slot = t; update();
      });
      slotsEl.appendChild(b);
    });
  }

  function update() {
    const ready = state.day && state.slot;
    goEl.disabled = !ready;
    selEl.textContent = ready ? `${state.dayLabel} · ${state.slot}`
      : state.day ? `${state.dayLabel} — now pick a window` : 'Select a day, then a time window';
  }

  goEl.addEventListener('click', async () => {
    goEl.disabled = true; goEl.textContent = 'Booking…';
    await pushLead({ formName: 'Site visit booked (on-site calendar)',
      requestType: 'Site visit', bookedDay: state.dayLabel, bookedSlot: state.slot });
    $('.bk-when', box).textContent = `${state.dayLabel}, ${state.slot}`;
    box.classList.add('is-booked');
  });

  renderSlots(1);
  daysEl.firstChild.click();
}

/* =====================================================================
   Forms → CRM
   ===================================================================== */
function initForms() {
  $$('form[data-lead-form]').forEach(form => {
    if (form.classList.contains('callback__form')) return;
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const btn = form.querySelector('[type=submit]'), label = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.innerHTML = 'Sending…'; }

      const data = Object.fromEntries(new FormData(form).entries());
      data.formName = form.dataset.leadForm;
      await pushLead(data);

      if (btn) { btn.disabled = false; btn.innerHTML = label; }
      form.reset();
      const note = form.querySelector('.form-note') || form.parentElement.querySelector('.form-note');
      if (note) {
        note.classList.add('is-visible');
        note.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        setTimeout(() => note.classList.remove('is-visible'), 10000);
      }
    });
  });
}

/* =====================================================================
   Optional hosted embeds
   ===================================================================== */
function initEmbeds() {
  $$('[data-embed]').forEach(slot => {
    const url = FDS_CONFIG.crmEmbeds[slot.dataset.embed];
    if (!url) return;
    const h = slot.dataset.embedHeight || '640';
    slot.outerHTML = `<iframe src="${url}" style="width:100%;height:${h}px;border:none;border-radius:26px"
      scrolling="no" title="First Digital Surveillance booking"></iframe>`;
  });
}

/* =====================================================================
   AI CHATBOT + LIVE AGENT
   ===================================================================== */
const FDSChat = {
  lead: {}, step: 0, mode: 'ai', transcript: [], booted: false, el: {},

  flow: [
    { key: 'intent',   q: 'Hi 👋 I’m <b>Ava</b>, First Digital Surveillance’s AI assistant. What can I help you with?',
      chips: ['Get a free quote', 'Book an installation', 'Service my existing system', 'Pricing question'] },
    { key: 'property', q: 'Got it. What type of property is this for?',
      chips: ['Home', 'Business / Retail', 'Warehouse', 'Apartment / HOA', 'New construction'] },
    { key: 'cameras',  q: 'Roughly how many cameras are you looking at?',
      chips: ['1–4', '5–8', '9–16', '16+', 'Not sure yet'] },
    { key: 'city',     q: 'Which city are you in? (We cover LA, Orange, San Bernardino &amp; Riverside counties.)',
      chips: ['Los Angeles', 'Long Beach', 'Glendale', 'Torrance', 'Orange County', 'Other'] },
    { key: 'timeline', q: 'When are you hoping to get this installed?',
      chips: ['ASAP / this week', 'Within 30 days', '1–3 months', 'Just researching'] },
    { key: 'name',     q: 'Perfect. What’s your name?', input: true, placeholder: 'First and last name' },
    { key: 'phone',    q: 'Thanks {name}! Best number to reach you? We call back in under 60 seconds.', input: true, placeholder: '(310) 555-0100' },
    { key: 'email',    q: 'And your email, so we can send the written quote?', input: true, placeholder: 'you@email.com' }
  ],

  init() {
    if (FDS_CONFIG.useHostedChat && FDS_CONFIG.hostedChatWidgetId) return this.loadHostedChat();
    this.el.root = $('#fds-chat'); if (!this.el.root) return;
    const r = this.el.root;
    this.el.panel = $('.chat-panel', r);
    this.el.body = $('.chat-body', r);
    this.el.chips = $('.chat-chips', r);
    this.el.input = $('.chat-input input', r);
    this.el.status = $('.chat-status', r);
    this.el.name = $('.chat-name', r);

    $('.chat-launch', r).addEventListener('click', () => this.toggle(true));
    $('.chat-close', r).addEventListener('click', () => this.toggle(false));
    const teaser = $('.chat-teaser', r);
    $('.chat-teaser button', r)?.addEventListener('click', e => { e.stopPropagation(); teaser.remove(); });
    teaser?.addEventListener('click', () => this.toggle(true));
    $$('.chat-tab', r).forEach(t => t.addEventListener('click', () => this.setMode(t.dataset.mode)));
    $('.chat-input', r).addEventListener('submit', e => {
      e.preventDefault();
      const v = this.el.input.value.trim(); if (!v) return;
      this.el.input.value = ''; this.say(v, 'user'); this.handleInput(v);
    });
    setTimeout(() => teaser?.classList.add('show'), 4500);
  },

  loadHostedChat() {
    $('#fds-chat')?.remove();
    const s = document.createElement('script');
    s.src = FDS_CONFIG.hostedChatLoaderUrl;
    if (FDS_CONFIG.hostedChatResourcesUrl) s.setAttribute('data-resources-url', FDS_CONFIG.hostedChatResourcesUrl);
    s.setAttribute('data-widget-id', FDS_CONFIG.hostedChatWidgetId);
    document.body.appendChild(s);
  },

  toggle(open) {
    this.el.panel.classList.toggle('is-open', open);
    $('.chat-launch', this.el.root).style.display = open ? 'none' : '';
    $('.chat-teaser', this.el.root)?.remove();
    if (open && !this.booted) { this.booted = true; this.ask(0); }
    if (open) setTimeout(() => this.el.input.focus(), 300);
  },

  setMode(mode) {
    $$('.chat-tab', this.el.root).forEach(t => t.classList.toggle('is-active', t.dataset.mode === mode));
    if (mode === this.mode) return;
    this.mode = mode;
    if (mode === 'agent') this.connectAgent();
    else {
      this.el.name.textContent = 'Ava · AI Assistant';
      this.el.status.innerHTML = '<i></i> Replies instantly, 24/7';
      this.sys('Switched back to the AI assistant');
      this.say('I’m back 👋 Want me to pick up where we left off?', 'bot',
        ['Continue my quote', 'Start over', 'Text me the price list']);
    }
  },

  scroll() { this.el.body.scrollTop = this.el.body.scrollHeight; },

  say(text, who = 'bot', chips = null, meta = null) {
    if (meta) { const m = document.createElement('div'); m.className = 'msg-meta'; m.textContent = meta; this.el.body.appendChild(m); }
    const d = document.createElement('div'); d.className = 'msg ' + who; d.innerHTML = text;
    this.el.body.appendChild(d);
    this.transcript.push(`${who === 'user' ? 'Visitor' : who === 'agent' ? 'Agent' : 'Ava'}: ${text.replace(/<[^>]+>/g, '')}`);
    this.setChips(chips); this.scroll();
  },

  sys(text) { const d = document.createElement('div'); d.className = 'msg-sys'; d.textContent = text; this.el.body.appendChild(d); this.scroll(); },

  setChips(chips) {
    this.el.chips.innerHTML = '';
    if (!chips) return;
    chips.forEach(c => {
      const b = document.createElement('button');
      b.className = 'chip'; b.type = 'button'; b.textContent = c;
      b.addEventListener('click', () => { this.say(c, 'user'); this.handleInput(c); });
      this.el.chips.appendChild(b);
    });
    this.scroll();
  },

  typing(ms, cb) {
    this.setChips(null);
    const t = document.createElement('div'); t.className = 'typing'; t.innerHTML = '<i></i><i></i><i></i>';
    this.el.body.appendChild(t); this.scroll();
    setTimeout(() => { t.remove(); cb(); }, ms);
  },

  ask(i) {
    this.step = i;
    const s = this.flow[i];
    if (!s) return this.finish();
    this.typing(i === 0 ? 500 : 720, () => {
      this.say(s.q.replace('{name}', (this.lead.name || '').split(' ')[0] || 'there'), 'bot', s.chips || null);
      this.el.input.placeholder = s.placeholder || 'Type your message…';
    });
  },

  handleInput(v) {
    if (this.mode === 'agent') return this.agentReply(v);
    const low = v.toLowerCase();
    if (/live agent|human|real person|speak to someone|representative/.test(low)) return this.setMode('agent');
    if (low === 'start over') { this.lead = {}; return this.ask(0); }
    if (low === 'continue my quote') return this.ask(this.step);
    if (/price|cost|how much|pricing/.test(low) && this.step === 0) {
      return this.typing(800, () => {
        this.say('Straight answer: most <b>residential 4-camera 4K systems</b> run <b>$1,200–$2,400 installed</b>, and ' +
          '<b>8–16 camera commercial systems</b> typically land <b>$3,500–$9,000</b> depending on cable runs, NVR storage ' +
          'and whether you add license-plate or AI analytics. Every quote is free and fixed — no surprises.', 'bot');
        setTimeout(() => this.ask(1), 900);
      });
    }
    const s = this.flow[this.step];
    if (!s) return this.typing(700, () => this.say(
      'Thanks — added to your file. A specialist will follow up shortly. Want a live agent right now instead?', 'bot',
      ['Talk to a live agent', 'Call (310) 901-4954', 'No thanks']));
    this.lead[s.key] = v;
    this.ask(this.step + 1);
  },

  async finish() {
    this.typing(900, async () => {
      const l = this.lead;
      this.say(`Perfect — you’re all set, <b>${(l.name || '').split(' ')[0]}</b>. Here’s what went over to our team:` +
        `<br><br>📍 <b>${l.city || '—'}</b> · ${l.property || '—'}<br>🎥 ${l.cameras || '—'} cameras · ${l.timeline || '—'}` +
        `<br>📞 ${l.phone || '—'}<br>✉️ ${l.email || '—'}`, 'bot');

      await pushLead({
        formName: 'AI Chatbot — Ava (qualified lead)',
        name: l.name, phone: l.phone, email: l.email, city: l.city,
        propertyType: l.property, cameraCount: l.cameras, timeline: l.timeline, intent: l.intent,
        transcript: this.transcript.join('\n'),
        tags: ['website-chat', 'ai-qualified', (l.timeline || '').includes('ASAP') ? 'hot-lead' : 'nurture']
      });

      setTimeout(() => {
        this.sys('Sent to the FDS dispatch team · marked New Inquiry');
        this.say(`Speed-to-lead is running — a tech will call you in under <b>${FDS_CONFIG.callbackSeconds} seconds</b> ` +
          'during our hours (Mon–Fri 7am–7pm, Sat–Sun 9am–5pm). Anything else?', 'bot',
          ['Book a time instead', 'Talk to a live agent', 'Text me the price list']);
      }, 1000);
    });
  },

  connectAgent() {
    this.mode = 'agent';
    $$('.chat-tab', this.el.root).forEach(t => t.classList.toggle('is-active', t.dataset.mode === 'agent'));
    const online = agentIsOnline();
    this.sys(online ? 'Connecting you to a live agent…' : 'Our team is offline right now');
    this.el.name.textContent = 'Connecting…';
    this.el.status.innerHTML = '<i></i> Finding an available agent';

    if (!online) return this.typing(1100, () => {
      this.el.name.textContent = 'FDS Support';
      this.el.status.innerHTML = '<i style="background:#F59E0B"></i> Offline — leave a message';
      this.say('Our live team is offline (Mon–Fri 7am–7pm, Sat–Sun 9am–5pm PT). Leave your number and the first ' +
        'available tech calls you back — or call <b>(310) 901-4954</b>.', 'agent',
        ['Leave my number', 'Back to AI assistant']);
    });

    this.typing(1500, () => {
      this.el.name.textContent = 'Marcus R. · FDS Support';
      this.el.status.innerHTML = '<i></i> Live agent · replies in ~30s';
      this.sys('Marcus R. joined the chat');
      this.typing(1200, () => {
        const l = this.lead;
        const ctx = l.city ? ` I can see Ava noted a ${l.cameras || ''} camera job in ${l.city} — I’ve got the details in front of me.` : '';
        this.say(`Hey, this is Marcus with First Digital Surveillance.${ctx} How can I help?`, 'agent', null,
          'Live agent · ' + new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }));
        this.setChips(['Schedule a site walk', 'Is my building wired already?', 'Do you service my system?']);
      });
    });
  },

  agentReply(v) {
    const low = v.toLowerCase();
    if (/back to ai|ai assistant/.test(low)) return this.setMode('ai');
    this.typing(1400, () => {
      let r;
      if (/site walk|schedule|appointment|book/.test(low))
        r = 'Happy to. Free on-site walkthroughs across LA, Orange, San Bernardino and Riverside — usually within 48 hours. ' +
            'I can hold a window right now; morning or afternoon better?';
      else if (/wired|cable|wiring|conduit/.test(low))
        r = 'Nine times out of ten we reuse existing coax or Cat5 — we test it on the walkthrough. If it needs new runs we do ' +
            'our own structured cabling in-house, so it stays one crew and one invoice.';
      else if (/service|repair|broken|not working|fix/.test(low))
        r = 'We service most major brands even if we didn’t install them — Hikvision, Dahua, Uniview, Lorex, Avigilon, Axis. ' +
            'What’s the system doing (or not doing) right now?';
      else if (/price|cost|quote|how much/.test(low))
        r = 'I can get you a firm number today. Quotes are free and fixed — the price on the estimate is the price on the invoice. ' +
            'What’s the address so I can check line-of-sight and cable runs?';
      else
        r = 'Got it — let me pull that up. Quickest way is a 10-minute call so I can size this properly. Want a tech to ring you now?';
      this.say(r, 'agent', ['Have a tech call me now', 'Book a time', 'Email me a quote']);
    });
  }
};

/* ===================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  initChrome(); initHeroSlider(); initFeeds(); initCallback(); initPhoneDemo(); initBooker();
  initForms(); initEmbeds(); FDSChat.init();
});
