#!/usr/bin/env python3
"""Static site generator — First Digital Surveillance (v2, modernized)."""
import json, pathlib

OUT = pathlib.Path(__file__).parent
SITE = "https://cctvinstallation-losangeles.com"
PHONE = "(310) 901-4954"
PHONE_RAW = "+13109014954"
EMAIL = "info@cctvinstallation-losangeles.com"
ADDR = "3183 Wilshire Blvd Ste #196D10"
CITY, STATE, ZIP = "Los Angeles", "CA", "90010"

# ================================================================ icons
I = {
"phone":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
"mail":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="m2.6 6.8 9.4 5.6 9.4-5.6"/></svg>',
"pin":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10.5c0 6-8 11.5-8 11.5s-8-5.5-8-11.5a8 8 0 0 1 16 0z"/><circle cx="12" cy="10.3" r="2.9"/></svg>',
"clock":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/></svg>',
"bolt":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.6 2 4.2 13.4a.7.7 0 0 0 .54 1.15h5.02l-1.4 7.3a.7.7 0 0 0 1.23.57l9.4-11.4a.7.7 0 0 0-.54-1.15h-5.02l1.4-7.3A.7.7 0 0 0 13.6 2z"/></svg>',
"check":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m5 13 4.2 4.2L19 7"/></svg>',
"checkc":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="m8 12.2 2.7 2.7L16.2 9"/></svg>',
"arrow":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h13M13 6.2 18.8 12 13 17.8"/></svg>',
"star":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21l1.2-6.9-5-4.9 6.9-1z"/></svg>',
"cam":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="6.5" width="13.5" height="7.5" rx="2"/><path d="m16 9.2 4.6-2v8.8L16 13.4"/><path d="M9.2 14v3.2a2 2 0 0 0 2 2H13"/><path d="M6.6 19.2h5.2"/><path d="M9.2 6.5V3.4M6.4 3.4h5.6"/></svg>',
"dome":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 14a8.5 8.5 0 0 1 17 0z"/><path d="M2 14h20"/><circle cx="12" cy="10.2" r="2.3"/><path d="M12 17.2V21"/></svg>',
"intercom":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2.4" width="12" height="19.2" rx="2.4"/><circle cx="12" cy="8" r="2.1"/><path d="M9.2 13.6h5.6M9.2 17h5.6"/></svg>',
"lock":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2.4"/><path d="M7.8 10V7.2a4.2 4.2 0 0 1 8.4 0V10"/><circle cx="12" cy="15.4" r="1.4"/></svg>',
"cable":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7.4 2.6h9.2v5l3 3v10.8H4.4V10.6l3-3z"/><path d="M9.4 21.4v-4M12 21.4v-4M14.6 21.4v-4"/><path d="M10 2.6v3M14 2.6v3"/></svg>',
"monitor":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="13" rx="2.4"/><path d="M8.4 21h7.2M12 17v4"/><path d="m6.6 12.4 2.6-3.2 2.2 2.4 2.6-3.6 3.4 4.4"/></svg>',
"plate":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2.4"/><path d="M6 10.2v3.6M9.4 10.2v3.6M12.8 10.2v3.6M16.2 10.2v3.6"/></svg>',
"thermal":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.6V5.2a2 2 0 0 0-4 0v9.4a4 4 0 1 0 4 0z"/><path d="M12 9.2v5.8"/></svg>',
"ai":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="4.6" y="6.4" width="14.8" height="12" rx="3.4"/><circle cx="9.6" cy="12.4" r="1.25"/><circle cx="14.4" cy="12.4" r="1.25"/><path d="M12 2.8v3.6M2.6 11.4h2M19.4 11.4h2"/></svg>',
"build":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5.2 21V8.4L12 3.4l6.8 5V21"/><path d="M9.6 21v-5h4.8v5"/><path d="M9.6 11.2h.8M13.6 11.2h.8"/></svg>',
"shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.4 20 5.8v5.4c0 5.2-3.4 8.9-8 10.4-4.6-1.5-8-5.2-8-10.4V5.8z"/><path d="m8.8 11.8 2.2 2.2 4.2-4.4"/></svg>',
"nvr":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6.6" width="20" height="5.4" rx="1.6"/><rect x="2" y="13.4" width="20" height="5.4" rx="1.6"/><path d="M5.8 9.3h.02M5.8 16.1h.02"/><path d="M9.6 9.3h7.6M9.6 16.1h7.6"/></svg>',
"chat":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.8a8.2 8.2 0 0 1-11.9 7.4L3 21l1.9-6.2A8.2 8.2 0 1 1 21 11.8z"/></svg>',
"bot":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4.4" y="7.4" width="15.2" height="11.2" rx="3.2"/><circle cx="9.2" cy="13" r="1.1"/><circle cx="14.8" cy="13" r="1.1"/><path d="M12 3.4v4"/></svg>',
"agent":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="3.6"/><path d="M4.6 20a7.4 7.4 0 0 1 14.8 0"/></svg>',
"send":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 3 10.4 13.6M21 3l-6.7 18-3.9-7.4L3 9.7z"/></svg>',
"sms":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2.6" y="4.6" width="18.8" height="13.4" rx="3"/><path d="M7.5 20.8 11 18"/><path d="M8 10.6h.02M12 10.6h.02M16 10.6h.02"/></svg>',
"calendar":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m9.4 15.4 1.8 1.8 3.6-3.8"/></svg>',
"play":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.2 19 12 8 18.8z"/></svg>',
"fb":'<svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.1h-3.1V8.9c0-.9.25-1.5 1.55-1.5h1.65V4.6A22 22 0 0 0 14.3 4.5c-2.4 0-4 1.45-4 4.1v2.3H7.6V14h2.7v8z"/></svg>',
"tw":'<svg viewBox="0 0 24 24"><path d="M17.5 3h3l-6.6 7.5L21.8 21h-6l-4.7-6.1L5.7 21h-3l7-8L2.4 3h6.1l4.2 5.6zm-1 16h1.7L7.6 4.7H5.8z"/></svg>',
"ig":'<svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9s.68.82.9 1.38c.16.42.36 1.06.41 2.23.06 1.25.07 1.63.07 4.81s0 3.56-.07 4.81c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38s-.82.68-1.38.9c-.42.16-1.06.36-2.23.41-1.25.06-1.63.07-4.85.07s-3.6 0-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9s-.68-.82-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.2 15.56 2.2 15.18 2.2 12s0-3.56.07-4.81c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38s.82-.68 1.38-.9c.42-.16 1.06-.36 2.23-.41C8.44 2.2 8.82 2.2 12 2.2zm0 3.05A6.75 6.75 0 1 0 18.75 12 6.75 6.75 0 0 0 12 5.25zm0 11.13A4.38 4.38 0 1 1 16.38 12 4.38 4.38 0 0 1 12 16.38zm6.99-11.4a1.58 1.58 0 1 1-1.58-1.57 1.58 1.58 0 0 1 1.58 1.57z"/></svg>',
"yt":'<svg viewBox="0 0 24 24"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.76-1.77C18.25 5 12 5 12 5s-6.25 0-7.84.43A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.76 1.77C5.75 19 12 19 12 19s6.25 0 7.84-.43a2.5 2.5 0 0 0 1.76-1.77A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15.2V8.8l5.2 3.2z"/></svg>',
}

SOCIALS = [
 ("fb", "https://www.facebook.com/FirstDigitalSurveillance", "@FirstDigitalSurveillance", "Facebook"),
 ("tw", "https://twitter.com/cctv1st", "@cctv1st", "X (Twitter)"),
 ("ig", "https://www.instagram.com/1stdigitalsurveillance", "@1stdigitalsurveillance", "Instagram"),
 ("yt", "https://www.youtube.com/channel/UC6HvUgXntaIqfOZk8hjzoPg", "First Digital Surveillance", "YouTube"),
]

NAV = [("index.html","Home"),("services.html","Services"),("solutions.html","Solutions"),
       ("service-areas.html","Service Areas"),("contact.html","Contact")]

CITIES = ["Los Angeles","Long Beach","Santa Clarita","Glendale","Lancaster","Pomona","Torrance","Pasadena",
          "Burbank","Anaheim","Irvine","Santa Ana","Riverside","San Bernardino","Ontario","Corona",
          "Beverly Hills","Culver City","Downey","Inglewood","Van Nuys","Woodland Hills","Palm Springs","Alhambra"]

SERVICES = [
 ("cam","CCTV Camera Installation","cctv-camera-installation",
  "Design, supply and installation of 4K HD and IP surveillance systems for homes, offices, retail and industrial sites — with remote viewing on any phone.",
  ["4K / 8MP HD and IP camera systems","Indoor, outdoor, PTZ and dome cameras",
   "Mobile app viewing and motion alerts","Existing-system upgrades and camera repair"]),
 ("intercom","Phone Entry &amp; Intercom Systems","phone-entry-intercom",
  "Video and IP intercom installation, repair and replacement for apartment buildings, HOAs, gated communities and commercial lobbies.",
  ["DoorKing, Aiphone, Comelit, 2N and Linear","Video and telephone entry",
   "Cloud-managed tenant directories","Legacy system repair and retrofit"]),
 ("lock","Door Access Control &amp; Fob Systems","door-access-control",
  "Track every employee, visitor and contractor moving through your property with key-fob, keypad, mobile-credential and biometric access control.",
  ["Key fob, card and mobile credentials","Multi-door and multi-site management",
   "Time-based schedules and audit trails","Integration with your camera system"]),
 ("cable","Structured Cabling","structured-cabling",
  "Planning, design, installation and maintenance of structured network cable infrastructure — Cat5e, Cat6, Cat6a and fiber, done to code.",
  ["Cat5e / Cat6 / Cat6a and fiber runs","Server rack and patch panel build-outs",
   "Certified testing and labeling","Wi-Fi access point cabling"]),
 ("build","Pre-Wiring &amp; New Construction","prewire-new-construction",
  "Get the cabling right before the drywall goes up. We work from your plans and coordinate with your GC so the system drops in clean on day one.",
  ["Plan take-offs and device layout","Rough-in and trim-out phases",
   "GC and low-voltage coordination","Future-proof conduit and pathways"]),
 ("monitor","Remote CCTV Monitoring","remote-cctv-monitoring",
  "Live off-site monitoring that pairs virtual guard tours with real-time intervention — talk-downs, dispatch and verified alarm response.",
  ["24/7 live operator monitoring","Virtual guard tours and talk-downs",
   "Verified police dispatch","Far cheaper than on-site guards"]),
 ("plate","License Plate Recognition","license-plate-recognition",
  "Capture and read plates at gates, drives and parking structures — searchable logs, hot lists and automatic gate triggering.",
  ["Plate capture up to 60+ mph","Searchable vehicle logs",
   "Watchlist and hot-list alerts","Automatic gate / barrier control"]),
 ("thermal","Thermal Camera Solutions","thermal-cameras",
  "See in total darkness, smoke and fog. Thermal detection for perimeters, yards, solar farms, construction sites and fire-risk areas.",
  ["Zero-light perimeter detection","Long-range intrusion detection",
   "Early fire and heat detection","Fewer false alarms than optical"]),
 ("ai","AI Camera Systems","ai-camera-systems",
  "Deep-learning analytics that know the difference between a person, a vehicle and a raccoon — so you only get alerts that matter.",
  ["Person / vehicle / object classification","Line-crossing and loitering alerts",
   "Face and vehicle search","Up to 90% fewer false alerts"]),
]

PRODUCTS = [
 ("cam","HD Cameras","4MP–8MP turret, bullet and PTZ cameras with true WDR and 100ft+ IR night vision."),
 ("nvr","HD DVRs","4, 8, 16 and 32-channel recorders with RAID storage and remote playback."),
 ("dome","HD-IP Cameras","PoE IP cameras up to 4K with on-board analytics and edge recording."),
 ("nvr","HD-IP NVRs","Enterprise NVRs with failover, 30–120 day retention and mobile streaming."),
 ("intercom","Intercom &amp; Entry","Video intercom, telephone entry and cloud tenant directories."),
 ("thermal","Thermal Cameras","Radiometric and detection-grade thermal for perimeters and fire risk."),
 ("plate","LPR Cameras","Dedicated plate-capture cameras with IR filters for gates and drives."),
 ("ai","AI Analytics","Person/vehicle classification, heat maps, people counting and search."),
]

TESTIMONIALS = [
 ("Gene Kent","Arcadia, CA","Being able to check my cameras from my phone while I'm at work changed everything. Motion alerts come through in seconds and the picture is crystal clear at night."),
 ("Dana Lenox","Avalon, CA","I asked three companies for a quote. FDS was the only one that answered the same day and actually sent a technician who knew what he was talking about."),
 ("Betty Smith","Palm Springs, CA","The consultation was genuinely helpful — no pressure, no upsell. The install crew was courteous, clean, and finished ahead of schedule."),
 ("Louis Larose","Agoura Hills, CA","The newly installed video surveillance system is working great, have had no issues so far. Look forward to working with you guys."),
 ("Harvey Berry","Arcadia, CA","Our technician was patient with all my questions and their customer service is easy to reach. That alone is worth a lot these days."),
 ("Sondra Kang","Palm Springs, CA","Staff responded fast every time I called and the hardware has been rock solid. Exactly what I was hoping for."),
 ("Maurice Pannell","Alhambra, CA","We've had FDS do multiple installations across our properties. Professional and technically sharp every single time."),
 ("John Wright","Baldwin Park, CA","Easy and hassle-free experience from the first phone call to the walkthrough at the end."),
 ("Tristan Erica","Beverly Hills, CA","They replaced our old system quickly and the new one is far easier to use. Wish we'd called them sooner."),
]

FAQS = [
 ("How much does CCTV installation cost in Los Angeles?",
  "Most residential 4-camera 4K systems run $1,200–$2,400 fully installed. Commercial 8–16 camera systems typically land between $3,500 and $9,000 depending on cable runs, NVR storage and whether you add license plate recognition or AI analytics. Every First Digital Surveillance estimate is free, on-site and fixed — the number on your quote is the number on your invoice."),
 ("How fast will someone actually get back to me?",
  "Under 60 seconds during business hours. Every form, chat and callback request on this site fires an instant confirmation text and routes straight to the first available technician's phone. Our current average first response is 47 seconds — because the contractor who answers first almost always wins the job, and we would rather that be us."),
 ("How long does a security camera installation take?",
  "A typical 4–8 camera home installation is done in a single day. Commercial jobs with 16+ cameras, access control or new cabling usually run two to four days. We give you an exact schedule at the walkthrough, before any work starts."),
 ("Do you service systems you didn't install?",
  "Yes. We repair, upgrade and take over maintenance on most major brands — Hikvision, Dahua, Uniview, Lorex, Avigilon, Axis, Hanwha and more. In many cases we can reuse your existing cabling and simply upgrade the cameras and recorder."),
 ("Can I view my cameras on my phone?",
  "Every system we install includes free mobile and desktop viewing with live streaming, recorded playback, and push notifications for motion, person or vehicle detection. We set the app up on your phone and walk you through it before we leave."),
 ("Which areas of Southern California do you cover?",
  "All of Los Angeles County plus Orange County, San Bernardino County and Riverside County — including Long Beach, Santa Clarita, Glendale, Lancaster, Pomona, Torrance, Pasadena, Anaheim, Irvine, Riverside and Palm Springs."),
 ("Are you licensed and insured?",
  "Yes. First Digital Surveillance is a licensed, bonded and insured low-voltage contractor. We pull permits where required and every installation is performed by our own trained, background-checked technicians — never subcontracted out."),
 ("How long is footage stored?",
  "Standard systems store 14–30 days of continuous footage. We size storage to your needs, and 60, 90 or 120-day retention is available — as is cloud backup for critical cameras."),
]

# ================================================================ camera scenes
SCENES = {
"drive": """<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs>
<linearGradient id="nvA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#081410"/><stop offset="1" stop-color="#12271F"/></linearGradient>
<radialGradient id="irA" cx="50%" cy="86%" r="72%"><stop offset="0" stop-color="#7FE3B0" stop-opacity=".2"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<rect width="320" height="180" fill="url(#nvA)"/>
<path d="M0 76q22-15 44-5t42-7 40 9 44-11 46 9 44-5 60 7V0H0z" fill="#050E0B" opacity=".92"/>
<path d="M198 100V64l38-23 38 23v36z" fill="#0D1F19"/>
<rect x="222" y="76" width="28" height="24" fill="#17362B"/>
<rect x="256" y="72" width="12" height="10" fill="#1E4536"/>
<path d="M112 180l40-80h50l62 80z" fill="#173A30" opacity=".9"/>
<path d="M158 180l10-34M176 180l6-34" stroke="#2E6B57" stroke-width="3" stroke-linecap="round" opacity=".45"/>
<g fill="#0B1B15"><rect x="14" y="92" width="4" height="30"/><rect x="46" y="94" width="4" height="30"/><rect x="78" y="96" width="4" height="30"/><rect x="10" y="90" width="76" height="4"/></g>
<g><g transform="translate(120,86)">
<path d="M2 16 9 4h26l11 12z" fill="#22503F"/><rect x="0" y="16" width="48" height="9" rx="3" fill="#2E6B54"/>
<rect x="12" y="6" width="10" height="8" fill="#0C1F18"/><rect x="25" y="6" width="9" height="8" fill="#0C1F18"/>
<circle cx="11" cy="26" r="4.5" fill="#081512"/><circle cx="38" cy="26" r="4.5" fill="#081512"/>
<ellipse cx="52" cy="19" rx="7" ry="4" fill="#D9FFEF" opacity=".65"/>
</g></g>
<rect width="320" height="180" fill="url(#irA)"/></svg>""",

"dock": """<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs>
<linearGradient id="nvB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A1220"/><stop offset="1" stop-color="#16202E"/></linearGradient>
<radialGradient id="irB" cx="50%" cy="26%" r="76%"><stop offset="0" stop-color="#A8CBFF" stop-opacity=".16"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<rect width="320" height="180" fill="url(#nvB)"/>
<rect y="112" width="320" height="68" fill="#1A2634"/>
<g fill="#0E1926" stroke="#243851" stroke-width="1"><rect x="16" y="40" width="74" height="72" rx="2"/><rect x="123" y="40" width="74" height="72" rx="2"/><rect x="230" y="40" width="74" height="72" rx="2"/></g>
<g stroke="#1D2F45" stroke-width="1"><path d="M16 58h74M16 76h74M16 94h74M123 58h74M123 76h74M123 94h74M230 58h74M230 76h74M230 94h74"/></g>
<g fill="#FFE9A8" opacity=".45"><circle cx="53" cy="22" r="4"/><circle cx="160" cy="22" r="4"/><circle cx="267" cy="22" r="4"/></g>
<path d="M0 134h320" stroke="#33506E" stroke-width="2" stroke-dasharray="16 12" opacity=".55"/>
<g transform="translate(196,0)"><g>
<rect x="0" y="96" width="34" height="22" rx="4" fill="#2F4867"/><rect x="30" y="82" width="4" height="36" fill="#4C6C92"/>
<rect x="34" y="112" width="18" height="4" fill="#4C6C92"/><rect x="6" y="86" width="18" height="12" fill="#3B5878"/>
<circle cx="9" cy="120" r="6" fill="#111B27"/><circle cx="28" cy="120" r="6" fill="#111B27"/></g></g>
<g transform="translate(112,0)"><g>
<circle cx="0" cy="92" r="5.4" fill="#94AECD"/><path d="M-5 98h10l2 18h-14z" fill="#7E9BBE"/>
<rect x="-4.5" y="116" width="3.4" height="13" fill="#69869F"/><rect x="1.1" y="116" width="3.4" height="13" fill="#69869F"/></g></g>
<rect width="320" height="180" fill="url(#irB)"/></svg>""",

"lobby": """<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs>
<linearGradient id="nvC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C1119"/><stop offset="1" stop-color="#19212E"/></linearGradient>
<radialGradient id="irC" cx="50%" cy="20%" r="80%"><stop offset="0" stop-color="#C9DBF5" stop-opacity=".14"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<rect width="320" height="180" fill="url(#nvC)"/>
<rect y="122" width="320" height="58" fill="#1D2634"/>
<g stroke="#28374B" stroke-width="1" fill="none"><path d="M0 140h320M0 158h320M60 122v58M140 122v58M220 122v58"/></g>
<rect x="196" y="34" width="104" height="88" rx="2" fill="#101A28" stroke="#2A3D55"/>
<path d="M248 34v88M196 62h104M196 92h104" stroke="#2A3D55"/>
<rect x="18" y="78" width="112" height="44" rx="3" fill="#233246"/>
<rect x="18" y="72" width="112" height="8" rx="2" fill="#31465F"/>
<rect x="34" y="52" width="22" height="20" rx="2" fill="#1A2634"/>
<g fill="#2B3D54"><rect x="150" y="60" width="30" height="62" rx="3"/><rect x="154" y="72" width="22" height="3"/><rect x="154" y="86" width="22" height="3"/><rect x="154" y="100" width="22" height="3"/></g>
<g transform="translate(112,0)"><g>
<circle cx="0" cy="86" r="6" fill="#A8BFDC"/><path d="M-6 93h12l3 24h-18z" fill="#8FA9C8"/>
<rect x="-5" y="117" width="4" height="14" fill="#7590AE"/><rect x="1" y="117" width="4" height="14" fill="#7590AE"/></g></g>
<rect width="320" height="180" fill="url(#irC)"/></svg>""",

"thermal": """<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs>
<linearGradient id="thB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10032A"/><stop offset=".55" stop-color="#1D0640"/><stop offset="1" stop-color="#3A0F4B"/></linearGradient>
<radialGradient id="hot"><stop offset="0" stop-color="#FFF9CC"/><stop offset=".32" stop-color="#FFA43C"/><stop offset=".66" stop-color="#D21F5E" stop-opacity=".72"/><stop offset="1" stop-color="#5B1060" stop-opacity="0"/></radialGradient>
<filter id="bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.4"/></filter>
</defs>
<rect width="320" height="180" fill="url(#thB)"/>
<ellipse cx="160" cy="182" rx="230" ry="48" fill="#7A1B5C" opacity=".5" filter="url(#bl)"/>
<g stroke="#5E2C82" stroke-width="2" opacity=".8"><path d="M0 124h320"/><path d="M22 124V86M72 124V86M122 124V86M172 124V86M222 124V86M272 124V86"/><path d="M0 96h320" opacity=".5"/></g>
<g transform="translate(150,0)" filter="url(#bl)"><g>
<circle cx="0" cy="96" r="7.5" fill="url(#hot)"/><ellipse cx="0" cy="118" rx="9.5" ry="18" fill="url(#hot)"/>
<ellipse cx="-4" cy="140" rx="3.4" ry="9" fill="url(#hot)"/><ellipse cx="4" cy="140" rx="3.4" ry="9" fill="url(#hot)"/></g></g>
<ellipse cx="284" cy="146" rx="24" ry="10" fill="url(#hot)" opacity=".5" filter="url(#bl)"/>
</svg>""",
}

def feed(scene, cam, place, box=None, tag="", extra=""):
    """One live camera tile."""
    b = ""
    if box:
        cls, label = box
        b = f'<div class="feed__box {cls}" data-label="{label}"></div>'
    return f"""<figure class="feed">
{SCENES[scene]}
<div class="feed__scan"></div><div class="feed__vig"></div>
{b}
<div class="feed__hud">
  <span class="tl"><span class="rec"><i></i>REC</span> {cam}</span>
  <span class="tr">{tag}</span>
  <span class="bl">{place}</span>
  <span class="br feed__clock">--</span>
</div>{extra}</figure>"""

# ================================================================ partials
def socials_html(cls=""):
    out = [f'<div class="socials {cls}">']
    for key, url, handle, label in SOCIALS:
        out.append(f'<a class="social" href="{url}" target="_blank" rel="noopener" '
                   f'aria-label="{label}: {handle}" title="{label} — {handle}">'
                   f'<span class="social__ico">{I[key]}</span><span class="social__handle">{handle}</span></a>')
    out.append('</div>')
    return "".join(out)

def header(active):
    nav = "".join(f'<a href="{h}"{" class=is-active" if h==active else ""}>{t}</a>' for h, t in NAV)
    uid = active.replace('.html', '')
    return f"""
<div class="demoband">
  <div class="container">
    <span class="tag">DESIGN PREVIEW</span>
    <b>Proposed website for First Digital Surveillance</b>
    <span>Concept only &mdash; this is not the live site, and nothing submitted here is sent anywhere.</span>
  </div>
</div>

<!-- ===== SPEED TO LEAD callback bar (replaces the old "Request A Call" strip) ===== -->
<div class="speedbar">
  <div class="container">
    <div class="speedbar__pitch">
      <span class="bolt">{I['bolt']}</span>
      <span><b>Request A Call</b><small>We call you back in under <span data-cbsec>60</span> seconds</small></span>
    </div>

    <div class="callback">
      <form class="callback__form" data-lead-form="Speed to Lead — header callback" autocomplete="on">
        <label class="sr-only" for="cb-{uid}">Your phone number</label>
        <input id="cb-{uid}" type="tel" name="phone" placeholder="Your phone number…" required>
        <button type="submit">{I['bolt']} Call me now</button>
      </form>
      <div class="callback__live" role="status" aria-live="polite">
        <span class="ring">
          <svg viewBox="0 0 36 36"><circle class="bg" cx="18" cy="18" r="15"/><circle class="fg" cx="18" cy="18" r="15"/></svg>
          <b>60</b>
        </span>
        <span><b class="cb-label">Request received</b><small>Speed-to-lead sequence running…</small></span>
      </div>
    </div>

    <span class="livestat"><i></i>Avg first response <b data-avg>47s</b></span>
    {socials_html()}
  </div>
</div>

<header class="header">
  <div class="container">
    <a class="brand" href="index.html" aria-label="First Digital Surveillance home">
      <img src="assets/img/fds-logo.svg" width="206" height="56"
           alt="First Digital Surveillance — CCTV installation Los Angeles">
    </a>
    <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span></button>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <div class="header__cta">
      <a class="header__phone" href="tel:{PHONE_RAW}">{I['phone']}<span data-phone>{PHONE}</span></a>
      <a class="btn btn--red" href="contact.html">Free Estimate</a>
    </div>
  </div>
</header>"""

def cta_band():
    return f"""
<section class="ctaband">
  <div class="ctaband__mesh"></div>
  <div class="container">
    <div data-reveal>
      <h2>Get a free on-site security assessment</h2>
      <p>No pressure, no obligation. A licensed FDS technician walks your property and gives you a fixed written quote — and calls you back in under a minute.</p>
    </div>
    <div class="ctaband__btns" data-reveal>
      <a class="btn btn--white btn--lg" href="tel:{PHONE_RAW}">{I['phone']}<span data-phone>{PHONE}</span></a>
      <a class="btn btn--glass btn--lg" href="contact.html">Book Online</a>
    </div>
  </div>
</section>"""

def footer():
    svc = "".join(f'<li><a href="services.html#{s[2]}">{s[1]}</a></li>' for s in SERVICES[:6])
    cty = "".join(f'<li><a href="service-areas.html#{c.lower().replace(" ","-")}">CCTV Installation {c}</a></li>' for c in CITIES[:6])
    seo = " · ".join(f'<a href="service-areas.html">{c}</a>' for c in CITIES)
    return f"""
{cta_band()}
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <img class="footer__logo" src="assets/img/fds-logo-white.svg" width="222" height="60" alt="First Digital Surveillance">
        <p>Family owned and operated. For over 17 years First Digital Surveillance has designed, installed and
        serviced security camera systems across Los Angeles, Orange, San Bernardino and Riverside counties —
        with a relentless focus on quality of work and customer satisfaction.</p>
        {socials_html()}
      </div>
      <div><h4>Services</h4><ul>{svc}<li><a href="services.html">All services</a></li></ul></div>
      <div><h4>Popular Areas</h4><ul>{cty}<li><a href="service-areas.html">All service areas</a></li></ul></div>
      <div>
        <h4>Contact FDS</h4>
        <div class="footer__nap">
          <div>{I['pin']}<span><b>First Digital Surveillance</b><br>{ADDR}<br>{CITY}, {STATE} {ZIP}</span></div>
          <div>{I['phone']}<span><a href="tel:{PHONE_RAW}"><b data-phone>{PHONE}</b></a></span></div>
          <div>{I['mail']}<span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
          <div>{I['clock']}<span>Mon–Fri 7:00AM–7:00PM<br>Sat–Sun 9:00AM–5:00PM</span></div>
        </div>
        <a class="btn btn--red btn--block" href="contact.html">Get My Free Quote</a>
      </div>
    </div>
    <div class="footer__bar">
      <span>&copy; <span data-year>2026</span> First Digital Surveillance. All rights reserved. Licensed · Bonded · Insured.</span>
      <nav><a href="#">Terms &amp; Conditions</a><a href="#">Privacy Policy</a><a href="#">Remote Support</a><a href="sitemap.xml">Sitemap</a></nav>
    </div>
    <div class="footer__seo">
      <strong>Security camera installation near you:</strong> {seo}
      <br><br>First Digital Surveillance provides CCTV installation, security camera repair, door access control,
      video intercom and phone entry systems, structured cabling, license plate recognition, thermal imaging and
      remote video monitoring throughout Southern California.
    </div>
  </div>
</footer>

<div class="mobilebar">
  <a href="tel:{PHONE_RAW}">{I['phone']}Call Now</a>
  <a href="contact.html">{I['bolt']}60-Sec Callback</a>
</div>"""

CHAT = f"""
<div id="fds-chat">
  <div class="chat-teaser">
    <button aria-label="Dismiss">&times;</button>
    <b>Need a camera quote?</b>
    Ava, our AI assistant, prices your job in about 60 seconds — or hands you to a live tech.
  </div>
  <button class="chat-launch" aria-label="Open chat">{I['chat']}<span>Chat with us</span><span class="dot">1</span></button>
  <div class="chat-panel" role="dialog" aria-label="First Digital Surveillance chat">
    <div class="chat-head">
      <div class="chat-head__row">
        <span class="chat-avatar"><img src="assets/img/favicon.svg" alt=""></span>
        <span><b class="chat-name">Ava · AI Assistant</b><small class="chat-status"><i></i> Replies instantly, 24/7</small></span>
        <button class="chat-close" aria-label="Close chat">&times;</button>
      </div>
      <div class="chat-tabs">
        <button class="chat-tab is-active" data-mode="ai">{I['bot']} AI Assistant</button>
        <button class="chat-tab" data-mode="agent">{I['agent']} Live Agent</button>
      </div>
    </div>
    <div class="chat-body"></div>
    <div class="chat-chips"></div>
    <div class="chat-foot">
      <form class="chat-input">
        <label class="sr-only" for="chat-in">Message</label>
        <input id="chat-in" type="text" placeholder="Type your message…" autocomplete="off">
        <button class="chat-send" type="submit" aria-label="Send">{I['send']}</button>
      </form>
      <p class="chat-legal">Answers instantly · hands off to a live tech · <b>every chat saved</b></p>
    </div>
  </div>
</div>"""

# ================================================================ schema
def local_business():
    return {
      "@context":"https://schema.org","@type":["SecuritySystemInstaller","LocalBusiness"],
      "@id":SITE+"/#business","name":"First Digital Surveillance",
      "alternateName":"FDS Security Camera Installation Los Angeles",
      "description":"Family-owned security camera installation company serving Los Angeles, Orange, San Bernardino and Riverside counties for over 17 years. CCTV, access control, intercom, structured cabling and 24/7 remote monitoring, with a 60-second callback promise.",
      "url":SITE+"/","telephone":PHONE,"email":EMAIL,
      "logo":SITE+"/assets/img/fds-logo.svg","image":SITE+"/assets/img/fds-logo.svg",
      "priceRange":"$$","foundingDate":"2008",
      "address":{"@type":"PostalAddress","streetAddress":ADDR,"addressLocality":CITY,
                 "addressRegion":STATE,"postalCode":ZIP,"addressCountry":"US"},
      "geo":{"@type":"GeoCoordinates","latitude":34.0614,"longitude":-118.3089},
      "openingHoursSpecification":[
        {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"19:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday","Sunday"],"opens":"09:00","closes":"17:00"}],
      "areaServed":[{"@type":"City","name":c} for c in CITIES],
      "sameAs":[s[1] for s in SOCIALS],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"218","bestRating":"5"},
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Security Services",
        "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s[1].replace('&amp;','&')}} for s in SERVICES]}
    }

def faq_schema():
    return {"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQS]}

def breadcrumbs(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+"/"+u} for i,(n,u) in enumerate(items)]}

# ================================================================ shell
def page(fname, title, desc, body, schemas, keywords):
    ld = "\n".join('<script type="application/ld+json">'+json.dumps(s,separators=(",",":"))+'</script>' for s in schemas)
    canon = SITE + "/" + ("" if fname == "index.html" else fname)
    html = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="First Digital Surveillance">
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="Los Angeles">
<meta name="geo.position" content="34.0614;-118.3089">
<meta name="ICBM" content="34.0614, -118.3089">
<link rel="canonical" href="{canon}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/favicon.svg">

<meta property="og:type" content="website">
<meta property="og:site_name" content="First Digital Surveillance">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/fds-logo.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@cctv1st">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="theme-color" content="#BF1220">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">

{ld}
<!-- Analytics + CRM routing configured in assets/js/fds.js -->
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
{header(fname)}
<main id="main">
{body}
</main>
{footer()}
{CHAT}
<script src="assets/js/fds.js"></script>
</body>
</html>
"""
    (OUT / fname).write_text(html, encoding="utf-8")
    print("wrote", fname, len(html))

# ================================================================ blocks
AV_COLORS = ["#BF1220","#1D4F91","#0A0F1A","#A50E1C","#123A6B","#334155","#7E0A16","#3B82F6","#111A2C"]

def stars():
    return '<div class="stars">' + I['star']*5 + '</div>'

def lead_form(name, fid, compact=False):
    svc = "".join(f'<option>{s[1].replace("&amp;","&")}</option>' for s in SERVICES)
    cty = "".join(f'<option>{c}</option>' for c in CITIES)
    extra = "" if compact else f"""<div class="field-row">
    <div class="field"><label for="{fid}-t">Property type</label>
      <select id="{fid}-t" name="propertyType"><option value="">Select…</option><option>Home</option><option>Business / Retail</option><option>Warehouse / Industrial</option><option>Apartment / HOA</option><option>New construction</option></select></div>
    <div class="field"><label for="{fid}-q">How many cameras?</label>
      <select id="{fid}-q" name="cameraCount"><option value="">Select…</option><option>1–4</option><option>5–8</option><option>9–16</option><option>16+</option><option>Not sure yet</option></select></div>
  </div>
  <div class="field"><label for="{fid}-m">Tell us about the property</label>
    <textarea id="{fid}-m" name="message" placeholder="Single-story home, want coverage on the driveway and both side gates…"></textarea></div>"""
    return f"""
<form data-lead-form="{name}" id="{fid}" novalidate>
  <div class="field-row">
    <div class="field"><label for="{fid}-n">Full name</label>
      <input id="{fid}-n" name="name" type="text" placeholder="Jane Doe" required></div>
    <div class="field"><label for="{fid}-p">Phone</label>
      <input id="{fid}-p" name="phone" type="tel" placeholder="(310) 555-0100" required></div>
  </div>
  <div class="field"><label for="{fid}-e">Email</label>
    <input id="{fid}-e" name="email" type="email" placeholder="you@email.com" required></div>
  <div class="field-row">
    <div class="field"><label for="{fid}-c">City</label>
      <select id="{fid}-c" name="city"><option value="">Select…</option>{cty}<option>Other</option></select></div>
    <div class="field"><label for="{fid}-s">Service needed</label>
      <select id="{fid}-s" name="service"><option value="">Select…</option>{svc}</select></div>
  </div>
  {extra}
  <button class="btn btn--red btn--block btn--lg" type="submit">{I['bolt']} Get My Free Quote</button>
  <p class="fineprint">We call back in under 60 seconds during business hours. By submitting you agree to be contacted
  by First Digital Surveillance about your request. Message &amp; data rates may apply. We never sell your information.</p>
  <div class="form-note"><b>✓ Request received — watch your phone.</b>
  Confirmation text is on its way, your request is logged as a new inquiry, and the callback
  sequence has already started — a technician will be dialing shortly.</div>
</form>"""

def bento_services():
    spans = [3,3,2,2,2,3,3,3,3]   # each row sums to 6 columns
    out = ['<div class="bento">']
    for i,(key,name,slug,blurb,_b) in enumerate(SERVICES):
        wide = ' bcard--wide' if spans[i] == 3 else ''
        out.append(f"""<article class="bcard{wide}" data-reveal>
  <span class="bcard__n">{i+1:02d}</span>
  <div class="bcard__ico">{I[key]}</div>
  <h3>{name}</h3><p>{blurb}</p>
  <a class="bcard__link" href="services.html#{slug}">Learn more {I['arrow']}</a>
</article>""")
    out.append('</div>')
    return "".join(out)

def faq_block(n=None):
    items = FAQS[:n] if n else FAQS
    out = ['<div class="faq">']
    for i,(q,a) in enumerate(items):
        out.append(f'<details{" open" if i==0 else ""} data-reveal><summary>{q}</summary><div class="faq__a"><p>{a}</p></div></details>')
    out.append('</div>')
    return "".join(out)

def testimonial_grid(n=6):
    out = ['<div class="grid grid-3">']
    for i,(name,city,text) in enumerate(TESTIMONIALS[:n]):
        ini = "".join(p[0] for p in name.split()[:2])
        out.append(f"""<article class="quote" data-reveal>{stars()}
  <p>“{text}”</p>
  <div class="quote__who"><span class="avatar" style="background:{AV_COLORS[i%len(AV_COLORS)]}">{ini}</span>
  <span><b>{name}</b><small>{city}</small></span></div></article>""")
    out.append('</div>')
    return "".join(out)

def areas_marquee():
    chips = "".join(f'<a class="mchip" href="service-areas.html#{c.lower().replace(" ","-")}">{I["pin"]}{c}</a>' for c in CITIES)
    return f'<div class="marquee"><div class="marquee__track">{chips}{chips}</div></div>'

def areas_list():
    return '<div class="arealist">' + "".join(
        f'<a href="service-areas.html#{c.lower().replace(" ","-")}">{I["pin"]}{c}</a>' for c in CITIES) + '</div>'

def speed_to_lead():
    return f"""
<section class="section section--dark stl" id="speed">
  <div class="stl__glow"></div>
  <div class="container">
    <div class="stl__grid">
      <div data-reveal>
        <span class="eyebrow">Speed to Lead</span>
        <h2>The contractor who answers first wins the job. That's us.</h2>
        <p class="lead">Most security companies take hours to call a web lead back — some take days. Every enquiry on this
        site fires an instant text and rings the first available technician's phone. Current average first response:
        <b class="mono" style="color:#fff"><span data-avg>47s</span></b>.</p>

        <div class="stlstats">
          <div class="stlstat"><b><span data-count="391" data-suf="%">0%</span></b><span>more conversions when you respond inside 60 seconds</span></div>
          <div class="stlstat"><b><span data-count="78" data-suf="%">0%</span></b><span>of buyers hire the company that responds first</span></div>
          <div class="stlstat"><b><span data-count="21" data-suf="×">0×</span></b><span>more likely to qualify vs. a 30-minute callback</span></div>
        </div>

        <div class="timeline">
          <div class="tstep tstep--done"><span class="tstep__t">0:00</span>
            <div><h4>Your request is logged</h4><p>Form, chat or callback bar — it lands with the dispatch team instantly, tagged by city, job size and urgency.</p></div></div>
          <div class="tstep tstep--done"><span class="tstep__t">0:08</span>
            <div><h4>Confirmation text goes out</h4><p>An automated SMS from the local number confirms we've got it and tells them exactly what happens next.</p></div></div>
          <div class="tstep"><span class="tstep__t">0:45</span>
            <div><h4>A real technician calls</h4><p>The workflow rings available techs in order until one picks up, then connects the call — no queue, no voicemail.</p></div></div>
          <div class="tstep"><span class="tstep__t">2:30</span>
            <div><h4>Site visit on the calendar</h4><p>Booked live on the call, confirmed by text and email, with automatic reminders so nobody no-shows.</p></div></div>
        </div>

        <p style="margin-top:32px"><a class="btn btn--red btn--lg" href="#quote">{I['bolt']} Try it — get called back</a></p>
      </div>

      <div data-reveal>
        <div class="phone">
          <div class="phone__screen">
            <div class="phone__bar"><b>First Digital Surveillance</b><small>(310) 901-4954</small></div>
            <div class="phone__msgs">
              <span class="sms__t" data-seq="1" data-delay="200">Today · form submitted</span>
              <div class="sms sms--out" data-seq="2" data-delay="600">Requested a quote for 6 cameras — Torrance</div>
              <span class="sms__t" data-seq="3" data-delay="1400">8 seconds later</span>
              <div class="sms sms--in" data-seq="4" data-delay="1800">Hi Jane — Marcus at First Digital Surveillance. Got your request for 6 cameras in Torrance. Calling you in the next 60 seconds. Bad time? Just reply RESCHEDULE.</div>
              <span class="sms__t" data-seq="5" data-delay="3200">45 seconds later</span>
            </div>
            <div class="callcard" data-seq="6" data-delay="3600">
              <span class="callcard__ico">{I['phone']}</span>
              <span><b>Incoming — FDS Technician</b><small>mobile · 00:47 after submit</small></span>
            </div>
            <div class="phone__msgs" style="padding-top:0">
              <div class="sms sms--in" data-seq="7" data-delay="5000">Booked! Site walk Thursday 10:00am. Calendar invite + reminder sent. — FDS</div>
            </div>
          </div>
          <button class="phone__replay" type="button">↺ Replay the sequence</button>
        </div>
      </div>
    </div>
  </div>
</section>"""

# ================================================================ PAGES
def build_home():
    prod = "".join(f'<article class="tile" data-reveal><div class="tile__ico">{I[k]}</div><h3>{n}</h3><p>{d}</p></article>'
                   for k,n,d in PRODUCTS)
    body = f"""
<section class="hero">
  <div class="hero__mesh"></div><div class="hero__grid"></div>
  <div class="container">
    <div class="hero__inner">
      <div>
        <span class="pill"><em>17 YEARS</em> Los Angeles' #1 rated low-voltage contractor</span>
        <h1>Structured cabling installation, <span class="grad">certified, labeled</span> and done once.</h1>
        <p class="hero__sub">First Digital Surveillance designs and installs Cat5e, Cat6, Cat6a and fiber
        infrastructure — plus the cameras, access control and intercom that run on it — across LA, Orange,
        San Bernardino and Riverside counties. Backed by a
        <strong style="color:#fff">60-second callback</strong> and free on-site estimates.</p>
        <div class="hero__cta">
          <a class="btn btn--red btn--lg" href="tel:{PHONE_RAW}">{I['phone']}Call <span data-phone>{PHONE}</span></a>
          <a class="btn btn--glass btn--lg" href="#speed">{I['bolt']}See how fast we respond</a>
        </div>
        <div class="trustrow">
          <span class="faces">
            <span style="background:#BF1220">GK</span><span style="background:#1D4F91">DL</span>
            <span style="background:#0A0F1A">BS</span><span style="background:#A50E1C">LL</span>
          </span>
          {stars()}
          <span><strong>4.9/5</strong> from 218+ reviews · <strong>2,000+</strong> projects completed</span>
        </div>
      </div>

      <div>
        <div class="nvr">
          <div class="nvr__bar"><i></i><i></i><i></i><span class="t">FDS-NVR-01 · CABLED &amp; COMMISSIONED</span>
            <span class="live"><i></i>LIVE</span></div>
          <div class="feedwall">
            {feed("drive","CAM 01","FRONT DRIVE",("feed__box feed__box--car","VEHICLE 98%"),"IR")}
            {feed("dock","CAM 02","LOADING DOCK",("feed__box feed__box--person","PERSON 96%"),"4K")}
            {feed("lobby","CAM 03","LOBBY",None,"4K")}
            {feed("thermal","CAM 04","PERIMETER",("feed__box feed__box--heat feed__box--amber","THERMAL 34.1°C"),"THRM")}
          </div>
          <div class="nvr__foot"><span><b>4 of 16</b> channels · 4K @ 30fps</span><span>30-day retention · Los Angeles, CA</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="statstrip">
      <div class="statbox" data-reveal><b><span data-count="2000" data-suf="+">0</span></b><span>Security projects delivered</span></div>
      <div class="statbox" data-reveal><b><span data-count="17">0</span></b><span>Years serving Southern California</span></div>
      <div class="statbox" data-reveal><b><span data-count="1000" data-suf="+">0</span></b><span>CCTV systems installed</span></div>
      <div class="statbox" data-reveal><b><span data-count="47" data-suf="s">0s</span></b><span>Average first response time</span></div>
    </div>
  </div>
</section>

{speed_to_lead()}

<section class="section" id="quote">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <span class="eyebrow">Free Estimate</span>
        <h2>Tell us about the property. We'll do the rest.</h2>
        <p class="lead">Two minutes of your time gets you a licensed technician on site, a coverage plan drawn to your
        actual floorplan, and a fixed written price.</p>
        <ul class="checklist">
          <li>{I['check']}<span><b>Callback in under 60 seconds</b> during business hours — not "within 24–48 hours".</span></li>
          <li>{I['check']}<span><b>Free on-site assessment</b> with camera angles and cable runs mapped before you commit.</span></li>
          <li>{I['check']}<span><b>Fixed written quote.</b> The price on the estimate is the price on the invoice.</span></li>
          <li>{I['check']}<span><b>Our own technicians.</b> Licensed, bonded, insured and background-checked — never subcontracted.</span></li>
        </ul>
      </div>
      <div class="leadcard leadcard--light" data-reveal>
        <div class="leadcard__top"><h3>Get Your Free Estimate</h3><p>Takes 40 seconds. A technician calls you back in under a minute.</p></div>
        <div class="leadcard__body">{lead_form("Homepage — Free Estimate","hero",compact=True)}</div>
      </div>
    </div>
  </div>
</section>

<section class="section--tight" style="padding:0 0 64px">
  <div class="container"><p class="center" style="font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-bottom:18px">Serving 24 cities across 4 counties</p></div>
  {areas_marquee()}
</section>

<section class="section section--alt" id="services">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">What We Do</span>
      <h2>Complete security &amp; surveillance services</h2>
      <p>One company for cameras, access control, intercom and the cabling behind it all — so there's never a second contractor to chase.</p>
    </div>
    {bento_services()}
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <span class="eyebrow">AI Analytics</span>
        <h2>Cameras that know the difference between a person and a passing cat</h2>
        <p class="lead">Motion alerts that fire on shadows and headlights get ignored within a week. Deep-learning
        analytics classify what they see — person, vehicle, plate, heat signature — so the only alerts you get are
        the ones worth opening.</p>
        <ul class="checklist">
          <li>{I['check']}<span><b>Person, vehicle and object classification</b> with confidence scoring</span></li>
          <li>{I['check']}<span><b>Line-crossing, loitering and intrusion zones</b> you draw yourself</span></li>
          <li>{I['check']}<span><b>License plate capture</b> at gates and drives, searchable by plate</span></li>
          <li>{I['check']}<span><b>Thermal detection</b> that works in zero light, smoke and fog</span></li>
          <li>{I['check']}<span><b>Up to 90% fewer false alerts</b> than standard motion detection</span></li>
        </ul>
        <p style="margin-top:28px"><a class="btn btn--red" href="solutions.html">Explore AI solutions {I['arrow']}</a></p>
      </div>
      <div data-reveal>
        <div class="nvr">
          <div class="nvr__bar"><i></i><i></i><i></i><span class="t">AI EVENT REVIEW</span><span class="live"><i></i>DETECTING</span></div>
          <div class="feedwall">
            {feed("drive","CAM 07","GATE · LPR",("feed__box feed__box--car feed__box--red","PLATE · 7ARL429"),"LPR")}
            {feed("thermal","CAM 09","YARD · THERMAL",("feed__box feed__box--heat feed__box--amber","HUMAN 97%"),"THRM")}
          </div>
          <div class="nvr__foot"><span><b>2 events</b> in the last 60s</span><span>False-alert filter: ON</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Why FDS</span>
      <h2>Why Los Angeles property owners choose us</h2>
      <p>We're family owned, not a franchise. The person who quotes your job is accountable for it.</p>
    </div>
    <div class="grid grid-3">
      <article class="benefit" data-reveal><div class="benefit__n">01</div><h3>Expert</h3><p>Trained, accredited installers and competitive custom quotes across the greater Los Angeles area — 17 years and 2,000+ projects deep.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">02</div><h3>Fast</h3><p>Sub-60-second callbacks, same-week site visits in most cities, and a single-day install on most residential systems.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">03</div><h3>Professional</h3><p>Clean cable runs, labeled terminations, full app setup and training so you actually know how to use what you paid for.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">04</div><h3>Trusted</h3><p>Over 1,000 CCTV installations, a 4.9 average review score and a 9/10 customer satisfaction rating.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">05</div><h3>Convenient</h3><p>One stop for products, consultation, installation, repair and ongoing service — no chasing a second contractor.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">06</div><h3>Accountable</h3><p>Licensed, bonded and insured, with our own W-2 technicians on every job. If something needs fixing, you call us — not a subcontractor.</p></article>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">How It Works</span>
      <h2>From first call to live cameras in under a week</h2>
    </div>
    <div class="steps">
      <div class="step" data-reveal><div class="step__n">01</div><h3>60-Second Callback</h3><p>You submit; the system texts you and rings a technician immediately. No queue, no voicemail.</p></div>
      <div class="step" data-reveal><div class="step__n">02</div><h3>On-Site Assessment</h3><p>A licensed tech walks the property, maps camera angles and cable runs, and hands you a fixed written quote.</p></div>
      <div class="step" data-reveal><div class="step__n">03</div><h3>Professional Install</h3><p>Our own crew installs, terminates, tests and labels everything — clean runs, no exposed cable.</p></div>
      <div class="step" data-reveal><div class="step__n">04</div><h3>Training &amp; Support</h3><p>We set up your phone app, walk you through playback, and stay on call for service.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Products</span>
      <h2>The equipment we install</h2>
      <p>Commercial-grade hardware from the manufacturers we trust — supplied, installed and warrantied by us.</p>
    </div>
    <div class="grid grid-4">{prod}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Service Areas</span>
      <h2>CCTV installation across Southern California</h2>
      <p>Serving Los Angeles, Orange, San Bernardino and Riverside counties — same-week appointments in most cities.</p>
    </div>
    {areas_list()}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Reviews</span>
      <h2>What our customers say</h2>
      <p>4.9 average across 218+ verified Google and Yelp reviews.</p>
    </div>
    {testimonial_grid(6)}
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal><span class="eyebrow">FAQ</span><h2>Security camera questions, answered</h2></div>
    {faq_block()}
  </div>
</section>"""
    page("index.html",
     "CCTV Installation Los Angeles | 60-Second Callback | First Digital Surveillance",
     "Los Angeles' #1 rated CCTV installation company. 17+ years, 2,000+ security projects, 47-second average callback. 4K security cameras, AI analytics, access control, intercom & structured cabling. Free on-site estimate — (310) 901-4954.",
     body,
     [local_business(), faq_schema(), breadcrumbs([("Home","")])],
     "cctv installation los angeles, security camera installation los angeles, security camera installers near me, ai security cameras los angeles, business security cameras los angeles, home security camera installation, access control los angeles, cctv repair los angeles")


def build_services():
    blocks = []
    for i,(key,name,slug,blurb,bullets) in enumerate(SERVICES):
        rev = " split--rev" if i % 2 else ""
        bl = "".join(f'<li>{I["check"]}<span>{b}</span></li>' for b in bullets)
        scene = ["drive","lobby","dock","thermal"][i % 4]
        cams = [("CAM 01","FRONT DRIVE"),("CAM 03","LOBBY"),("CAM 02","LOADING DOCK"),("CAM 09","PERIMETER")][i % 4]
        boxes = [("feed__box feed__box--car","VEHICLE 98%"),None,("feed__box feed__box--person","PERSON 96%"),
                 ("feed__box feed__box--heat feed__box--amber","THERMAL")][i % 4]
        blocks.append(f"""
<section class="section{' section--alt' if i%2 else ''}" id="{slug}">
  <div class="container">
    <div class="split{rev}">
      <div data-reveal>
        <span class="eyebrow">Service {i+1:02d}</span>
        <h2>{name}</h2>
        <p class="lead">{blurb}</p>
        <ul class="checklist">{bl}</ul>
        <p style="margin-top:28px">
          <a class="btn btn--red" href="contact.html">Get a quote</a>
          <a class="btn btn--ghost" href="tel:{PHONE_RAW}" style="margin-left:8px">Call {PHONE}</a>
        </p>
      </div>
      <div data-reveal>
        <div class="nvr" style="background:linear-gradient(160deg,#111A2C,#070B14);border-color:rgba(255,255,255,.1)">
          <div class="nvr__bar"><i></i><i></i><i></i><span class="t">{name.replace('&amp;','&').upper()}</span><span class="live"><i></i>LIVE</span></div>
          {feed(scene, cams[0], cams[1], boxes, "4K")}
          <div class="nvr__foot"><span><b>FDS</b> · Los Angeles</span><span>4K @ 30fps</span></div>
        </div>
      </div>
    </div>
  </div>
</section>""")

    body = f"""
<section class="pagehero">
  <div class="hero__mesh"></div><div class="hero__grid"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Services</p>
    <h1>Security camera &amp; low-voltage services in Los Angeles</h1>
    <p>Nine services, one accountable company. From a four-camera home system to a multi-site access-controlled
    campus — design, cabling, installation, training and service, all in house.</p>
  </div>
</section>

<section class="section section--tight">
  <div class="container">{bento_services()}</div>
</section>

{"".join(blocks)}

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal><span class="eyebrow">FAQ</span><h2>Common questions about our services</h2></div>
    {faq_block(6)}
  </div>
</section>"""
    svc_schema = [{"@context":"https://schema.org","@type":"Service","serviceType":s[1].replace('&amp;','&'),
                   "name":s[1].replace('&amp;','&')+" in Los Angeles","description":s[3],
                   "provider":{"@id":SITE+"/#business"},
                   "areaServed":[{"@type":"City","name":c} for c in CITIES[:8]]} for s in SERVICES]
    page("services.html",
     "Security Camera Installation Services Los Angeles | CCTV, AI, Access Control | FDS",
     "CCTV installation, AI camera systems, door access control, video intercom, structured cabling, license plate recognition, thermal imaging and 24/7 remote monitoring across Los Angeles, Orange, San Bernardino & Riverside counties.",
     body,
     [local_business(), breadcrumbs([("Home",""),("Services","services.html")]), faq_schema()] + svc_schema,
     "security camera installation services los angeles, cctv installation, ai security cameras, door access control los angeles, video intercom installation, structured cabling los angeles, license plate recognition, thermal cameras, remote video monitoring")


def build_solutions():
    industries = [
     ("build","Retail &amp; Restaurants","Loss prevention, POS overlay, employee safety and after-hours coverage."),
     ("cable","Warehouses &amp; Industrial","Dock doors, yard perimeters, forklift lanes and thermal fire detection."),
     ("lock","Apartments &amp; HOAs","Video intercom, fob access, package rooms, parking and common areas."),
     ("dome","Offices &amp; Professional","Lobby, server room and suite-level access with discreet cameras."),
     ("plate","Auto Dealers &amp; Lots","License plate capture, gate control and full lot coverage after close."),
     ("shield","Homes &amp; Estates","Driveways, entries, gates and side yards with true 4K night vision."),
     ("monitor","Construction Sites","Rapid-deploy cameras with live guard tours and copper-theft deterrence."),
     ("ai","Schools &amp; Worship","Entry lockdown, visitor management and campus-wide analytics."),
    ]
    prod = "".join(f'<article class="tile" data-reveal><div class="tile__ico">{I[k]}</div><h3>{n}</h3><p>{d}</p></article>' for k,n,d in PRODUCTS)
    ind = "".join(f'<article class="bcard" data-reveal><div class="bcard__ico">{I[k]}</div><h3>{n}</h3><p>{d}</p></article>' for k,n,d in industries)
    body = f"""
<section class="pagehero">
  <div class="hero__mesh"></div><div class="hero__grid"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Solutions</p>
    <h1>Products &amp; industry solutions</h1>
    <p>Commercial-grade cameras, recorders, intercoms and AI analytics — matched to how your property actually
    operates, then installed and warrantied by our own technicians.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Hardware</span>
      <h2>Equipment we supply and install</h2>
      <p>Brand-flexible so the system fits the job — Hikvision, Dahua, Uniview, Hanwha, Axis, Avigilon, Aiphone, DoorKing and more.</p>
    </div>
    <div class="grid grid-4">{prod}</div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">See It Live</span>
      <h2>What your wall looks like on day one</h2>
      <p>Multi-site live wall, AI classification on every channel, and playback you can actually search.</p>
    </div>
    <div class="nvr" data-reveal>
      <div class="nvr__bar"><i></i><i></i><i></i><span class="t">FDS CLOUD · 3 SITES</span><span class="live"><i></i>LIVE</span></div>
      <div class="feedwall feedwall--3">
        {feed("drive","CAM 01","WILSHIRE · DRIVE",("feed__box feed__box--car","VEHICLE 98%"),"LPR")}
        {feed("dock","CAM 02","VERNON · DOCK",("feed__box feed__box--person","PERSON 96%"),"4K")}
        {feed("thermal","CAM 03","TORRANCE · YARD",("feed__box feed__box--heat feed__box--amber","THERMAL 34.1°C"),"THRM")}
      </div>
      <div class="nvr__foot"><span><b>3 sites</b> · 48 channels online</span><span>30-day retention · cloud backup enabled</span></div>
    </div>
    <p class="center" style="margin-top:30px" data-reveal>
      <a class="btn btn--red btn--lg" href="contact.html">{I['bolt']}Get my system designed</a></p>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal><span class="eyebrow">Industries</span><h2>Built for how your property runs</h2></div>
    <div class="bento">{ind}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <span class="eyebrow">Remote Monitoring</span>
        <h2>Live operators watching — not just recording</h2>
        <p class="lead">Recorded footage tells you what happened. Monitored footage stops it. Our off-site operators run
        virtual guard tours, issue live voice talk-downs and dispatch verified police response.</p>
        <ul class="checklist">
          <li>{I['check']}<span>24/7 live operators and scheduled virtual guard tours</span></li>
          <li>{I['check']}<span>Real-time voice talk-down through on-site speakers</span></li>
          <li>{I['check']}<span>Verified alarm dispatch — higher police priority than standard alarms</span></li>
          <li>{I['check']}<span>Typically a fraction of the cost of on-site guards</span></li>
        </ul>
        <p style="margin-top:28px"><a class="btn btn--red" href="contact.html">Price remote monitoring</a></p>
      </div>
      <div data-reveal>
        <div class="nvr" style="background:linear-gradient(160deg,#111A2C,#070B14)">
          <div class="nvr__bar"><i></i><i></i><i></i><span class="t">CENTRAL STATION 4</span><span class="live"><i></i>TALK-DOWN ARMED</span></div>
          <div class="feedwall">
            {feed("thermal","CAM 11","PERIMETER",("feed__box feed__box--heat feed__box--red","INTRUDER"),"THRM")}
            {feed("dock","CAM 12","YARD",("feed__box feed__box--person feed__box--red","PERSON · AFTER HOURS"),"4K")}
          </div>
          <div class="nvr__foot"><span><b>Avg response</b> 38s</span><span>Verified dispatch enabled</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal><span class="eyebrow">Reviews</span><h2>Trusted across Southern California</h2></div>
    {testimonial_grid(3)}
  </div>
</section>"""
    page("solutions.html",
     "Security Camera Products & Industry Solutions | AI, Thermal, LPR | FDS Los Angeles",
     "HD and 4K IP cameras, DVRs and NVRs, video intercom, thermal imaging, license plate recognition and AI analytics — plus tailored security solutions for retail, warehouses, HOAs, dealerships and homes in Los Angeles.",
     body,
     [local_business(), breadcrumbs([("Home",""),("Solutions","solutions.html")])],
     "hd security cameras los angeles, ip camera systems, nvr dvr installation, thermal camera solutions, license plate recognition cameras, ai security cameras, warehouse security cameras, retail loss prevention cameras")


def build_areas():
    cards = "".join(f"""<article class="bcard" id="{c.lower().replace(' ','-')}" data-reveal>
  <div class="bcard__ico">{I['pin']}</div>
  <h3>CCTV Installation {c}</h3>
  <p>Security camera installation, repair, access control and intercom service throughout {c} and the surrounding
  neighborhoods. Free on-site estimates and same-week appointments.</p>
  <a class="bcard__link" href="contact.html">Get a {c} quote {I['arrow']}</a></article>""" for c in CITIES)

    body = f"""
<section class="pagehero">
  <div class="hero__mesh"></div><div class="hero__grid"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Service Areas</p>
    <h1>Security camera installation across Southern California</h1>
    <p>First Digital Surveillance serves Los Angeles County, Orange County, San Bernardino County and Riverside
    County — 24 cities and every neighborhood in between.</p>
  </div>
</section>

<section class="section section--tight">
  <div class="container">{areas_marquee()}</div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Counties Served</span>
      <h2>Four counties, one local crew</h2>
      <p>Our technicians are based in Los Angeles and dispatch daily across the region. Not sure you're in range?
      Call <a href="tel:{PHONE_RAW}">{PHONE}</a> — we'll tell you straight.</p>
    </div>
    <div class="grid grid-4">
      <article class="benefit" data-reveal><div class="benefit__n">LA</div><h3>Los Angeles County</h3><p>Los Angeles, Long Beach, Santa Clarita, Glendale, Lancaster, Pomona, Torrance, Pasadena, Burbank, Downey, Inglewood, Culver City, Van Nuys, Woodland Hills, Beverly Hills, Alhambra.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">OC</div><h3>Orange County</h3><p>Anaheim, Irvine, Santa Ana, Huntington Beach, Fullerton, Orange, Costa Mesa, Garden Grove, Newport Beach and surrounding cities.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">SB</div><h3>San Bernardino County</h3><p>San Bernardino, Ontario, Rancho Cucamonga, Fontana, Chino, Upland, Redlands and the Inland Empire.</p></article>
      <article class="benefit" data-reveal><div class="benefit__n">RC</div><h3>Riverside County</h3><p>Riverside, Corona, Moreno Valley, Temecula, Murrieta, Palm Springs, Palm Desert and the Coachella Valley.</p></article>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Cities</span><h2>Find your city</h2>
      <p>Every area gets the same licensed in-house crew, the same fixed pricing and the same warranty.</p>
    </div>
    <div class="bento">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <span class="eyebrow">Local Response</span>
        <h2>Why local matters for security work</h2>
        <p class="lead">A camera system is only as good as the company standing behind it. National installers
        subcontract the work and disappear once the invoice clears.</p>
        <ul class="checklist">
          <li>{I['check']}<span><b>Same-week site visits</b> in most Southern California cities</span></li>
          <li>{I['check']}<span><b>Our own W-2 technicians</b> — never a subcontracted crew</span></li>
          <li>{I['check']}<span><b>Permit-aware installs</b> that pass inspection the first time</span></li>
          <li>{I['check']}<span><b>Service calls answered by people you've already met</b></span></li>
        </ul>
      </div>
      <div class="leadcard leadcard--light" data-reveal>
        <div class="leadcard__top"><h3>Free Estimate in Your City</h3><p>Tell us where you are — we'll confirm same-week availability.</p></div>
        <div class="leadcard__body">{lead_form("Service Areas — City Availability","areas",compact=True)}</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal><span class="eyebrow">Reviews</span><h2>From customers across the region</h2></div>
    {testimonial_grid(6)}
  </div>
</section>"""
    page("service-areas.html",
     "Security Camera Installation Near Me | LA, Orange, San Bernardino & Riverside | FDS",
     "First Digital Surveillance installs and services CCTV, access control and intercom systems in Los Angeles, Long Beach, Glendale, Torrance, Anaheim, Irvine, Riverside, San Bernardino, Palm Springs and 24+ Southern California cities.",
     body,
     [local_business(), breadcrumbs([("Home",""),("Service Areas","service-areas.html")])],
     "security camera installation near me, cctv installation long beach, security cameras glendale, cctv installer torrance, security camera installation anaheim, cctv riverside, san bernardino security cameras, palm springs cctv")


def build_contact():
    body = f"""
<section class="pagehero">
  <div class="hero__mesh"></div><div class="hero__grid"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Contact</p>
    <h1>Get your free security assessment</h1>
    <p>Call, chat or fill out the form. A licensed First Digital Surveillance technician walks your property, maps
    the coverage and hands you a fixed written quote — at no cost, and we call back in under a minute.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <span class="eyebrow">Talk To Us</span>
        <h2>Three ways to reach First Digital Surveillance</h2>
        <div class="grid" style="gap:14px;margin:28px 0 34px">
          <article class="bcard" style="padding:24px">
            <div class="bcard__ico">{I['phone']}</div>
            <h3>Call us</h3>
            <p style="margin-bottom:10px">Fastest option — most calls are answered in under 20 seconds during business hours.</p>
            <a class="btn btn--red" href="tel:{PHONE_RAW}"><span data-phone>{PHONE}</span></a>
          </article>
          <article class="bcard" style="padding:24px">
            <div class="bcard__ico">{I['chat']}</div>
            <h3>Chat with Ava, then a live tech</h3>
            <p style="margin-bottom:10px">Our AI assistant prices your job in about a minute, then hands you to a live agent.</p>
            <span class="ghl-tag">{I['bot']} AI + live agent · bottom right</span>
          </article>
          <article class="bcard" style="padding:24px">
            <div class="bcard__ico">{I['mail']}</div>
            <h3>Email</h3>
            <p style="margin-bottom:10px">Send plans, photos or a scope and we'll come back with a written estimate.</p>
            <a class="btn btn--ghost" href="mailto:{EMAIL}">{EMAIL}</a>
          </article>
        </div>

        <h3>Office &amp; hours</h3>
        <ul class="checklist">
          <li>{I['pin']}<span><b>First Digital Surveillance</b><br>{ADDR}<br>{CITY}, {STATE} {ZIP}</span></li>
          <li>{I['clock']}<span><b>Mon–Fri</b> 7:00AM – 7:00PM &nbsp;·&nbsp; <b>Sat–Sun</b> 9:00AM – 5:00PM</span></li>
          <li>{I['shield']}<span>Licensed · Bonded · Insured low-voltage contractor</span></li>
          <li>{I['bolt']}<span><b>Average first response: <span data-avg>47s</span></b> — every enquiry triggers an instant text and a callback.</span></li>
        </ul>
        <div style="margin-top:26px">{socials_html("socials--dark")}</div>
      </div>

      <div class="leadcard leadcard--light" id="quote" data-reveal>
        <div class="leadcard__top"><h3>Request a Free Quote</h3><p>Instant text and email confirmation, then a callback in under a minute.</p></div>
        <div class="leadcard__body">{lead_form("Contact Page — Free Quote","contact")}</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <span class="eyebrow">Speed to Lead</span>
        <h2>What happens the second you hit send</h2>
        <div class="timeline" style="margin-top:26px">
          <div class="tstep tstep--done"><span class="tstep__t">0:00</span><div><h4>Request logged</h4><p>Tagged by city, job size and urgency, and pushed to the dispatch board.</p></div></div>
          <div class="tstep tstep--done"><span class="tstep__t">0:08</span><div><h4>Confirmation text</h4><p>From a local number, telling you exactly what happens next.</p></div></div>
          <div class="tstep"><span class="tstep__t">0:45</span><div><h4>A technician calls you</h4><p>The workflow rings available techs until one picks up.</p></div></div>
          <div class="tstep"><span class="tstep__t">2:30</span><div><h4>Site visit booked</h4><p>Confirmed by text and email with automatic reminders.</p></div></div>
        </div>
      </div>
      <div data-reveal>
        <div class="nvr">
          <div class="nvr__bar"><i></i><i></i><i></i><span class="t">FDS-NVR-01 · DEMO WALL</span><span class="live"><i></i>LIVE</span></div>
          <div class="feedwall">
            {feed("drive","CAM 01","FRONT DRIVE",("feed__box feed__box--car","VEHICLE 98%"),"IR")}
            {feed("lobby","CAM 03","LOBBY",None,"4K")}
            {feed("dock","CAM 02","LOADING DOCK",("feed__box feed__box--person","PERSON 96%"),"4K")}
            {feed("thermal","CAM 04","PERIMETER",("feed__box feed__box--heat feed__box--amber","THERMAL"),"THRM")}
          </div>
          <div class="nvr__foot"><span><b>Live demo</b> · book a walkthrough</span><span>Los Angeles, CA</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <span class="eyebrow">Book Instantly</span>
      <h2>Pick your own site-visit time</h2>
      <p>Prefer to skip the phone tag? Choose a window that works and we'll confirm by text.</p>
    </div>
    <div class="booker" data-reveal>
      <div class="booker__head">
        <div><b>Book your free site visit</b><small>Pick a day and a window — we confirm by text within minutes.</small></div>
        <span class="booker__badge"><i></i>4 slots left this week</span>
      </div>
      <div class="booker__days"></div>
      <div class="booker__slots"></div>
      <div class="booker__foot">
        <span class="booker__sel">Select a day, then a time window</span>
        <button class="btn btn--red booker__go" type="button" disabled>Confirm my visit</button>
      </div>
      <div class="booker__done">
        <span class="booker__tick">&#10003;</span>
        <div><b>Booked &mdash; <span class="bk-when"></span></b>
        <small>Confirmation text and calendar invite sent. A technician will call to confirm the address and gate access.</small></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal><span class="eyebrow">FAQ</span><h2>Before you call</h2></div>
    {faq_block()}
  </div>
</section>

<section class="section section--alt section--tight">
  <div class="container">
    <div class="section-head center" data-reveal><span class="eyebrow">Find Us</span><h2>Serving greater Los Angeles from Wilshire Blvd</h2></div>
    <div class="mapcard" data-reveal>
      <svg class="mapcard__svg" viewBox="0 0 900 340" preserveAspectRatio="xMidYMid slice" aria-label="Service area map">
        <rect width="900" height="340" fill="#EEF2F7"/>
        <g stroke="#DDE4EE" stroke-width="10">
          <path d="M0 60h900M0 140h900M0 220h900M0 300h900"/>
          <path d="M90 0v340M230 0v340M370 0v340M510 0v340M650 0v340M790 0v340"/>
        </g>
        <g fill="#E4EAF3">
          <rect x="100" y="70" width="120" height="60" rx="3"/><rect x="240" y="70" width="120" height="60" rx="3"/>
          <rect x="380" y="150" width="120" height="60" rx="3"/><rect x="520" y="70" width="120" height="60" rx="3"/>
          <rect x="660" y="230" width="120" height="60" rx="3"/><rect x="100" y="230" width="120" height="60" rx="3"/>
        </g>
        <path d="M-20 250 L940 90" stroke="#F6C64B" stroke-width="16" opacity=".85"/>
        <path d="M-20 250 L940 90" stroke="#FFF" stroke-width="2" stroke-dasharray="14 12" opacity=".7"/>
        <text x="620" y="150" font-family="Inter,sans-serif" font-size="15" fill="#93A1B5" font-weight="600">WILSHIRE BLVD</text>
        <g fill="none" stroke="#BF1220">
          <circle cx="450" cy="176" r="52" opacity=".2" stroke-width="2"/>
          <circle cx="450" cy="176" r="88" opacity=".13" stroke-width="2"/>
          <circle cx="450" cy="176" r="128" opacity=".08" stroke-width="2"/>
        </g>
        <circle cx="450" cy="176" r="46" fill="#BF1220" opacity=".08"/>
        <g transform="translate(450,176)">
          <path d="M0-34c-11 0-20 9-20 20 0 15 20 32 20 32s20-17 20-32c0-11-9-20-20-20z" fill="#BF1220"/>
          <circle cy="-14" r="7" fill="#fff"/>
        </g>
      </svg>
      <div class="mapcard__info">
        <b>First Digital Surveillance</b>
        <span>{ADDR}<br>{CITY}, {STATE} {ZIP}</span>
        <span class="mapcard__chip">{I['pin']}Serving Los Angeles · Orange · San Bernardino · Riverside</span>
        <a class="btn btn--ghost" href="tel:{PHONE_RAW}">{I['phone']}<span data-phone>{PHONE}</span></a>
      </div>
    </div>
  </div>
</section>"""
    contact_schema = {"@context":"https://schema.org","@type":"ContactPage",
        "name":"Contact First Digital Surveillance","url":SITE+"/contact.html",
        "mainEntity":{"@id":SITE+"/#business"}}
    page("contact.html",
     "Contact First Digital Surveillance | Free CCTV Quote Los Angeles | (310) 901-4954",
     "Get a free on-site security camera estimate in Los Angeles with a 60-second callback. Call (310) 901-4954, chat with our AI assistant and a live agent, or book your site visit online. Mon-Fri 7am-7pm, Sat-Sun 9am-5pm.",
     body,
     [local_business(), contact_schema, faq_schema(), breadcrumbs([("Home",""),("Contact","contact.html")])],
     "contact cctv installer los angeles, free security camera quote, security camera estimate los angeles, book cctv installation, first digital surveillance phone number")


def build_seo_files():
    pages = [("","1.0","weekly"),("services.html","0.9","monthly"),("solutions.html","0.8","monthly"),
             ("service-areas.html","0.9","monthly"),("contact.html","0.8","monthly")]
    urls = "\n".join(f"  <url>\n    <loc>{SITE}/{p}</loc>\n    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
                     for p,pr,c in pages)
    (OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+"\n</urlset>\n", encoding="utf-8")
    (OUT/"robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\n# AI crawlers welcome — helps FDS get cited in AI answer engines\n"
        f"User-agent: GPTBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    build_home(); build_services(); build_solutions(); build_areas(); build_contact(); build_seo_files()
    print("done")
