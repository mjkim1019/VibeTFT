import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(
    page_title='VibeTFT',
    page_icon='🎮',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# PWA 설정을 위한 meta 태그 및 manifest 링크 추가
components.html("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="VibeTFT">
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="manifest" href="/static/manifest.json">
    <link rel="apple-touch-icon" href="/static/icon-192x192.png">

    <!--
    Service Worker 등록은 HTTPS 환경 및 static 파일 서빙 설정 후 활성화
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/sw.js')
                .then(function(registration) {
                    console.log('SW registered: ', registration);
                }).catch(function(registrationError) {
                    console.log('SW registration failed: ', registrationError);
                });
        }
    </script>
    -->
    
    <style>
        .main > div {
            padding-top: 2rem;
        }
        
        @media (max-width: 768px) {
            .main > div {
                padding: 1rem 0.5rem;
            }
        }
        
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            height: 3rem;
            font-size: 1.1rem;
        }
    </style>
</head>
""", height=0)

# Wake Lock and Background audio combined component
# Load and encode audio file
with open('static/audio/background.mp3', 'rb') as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode()

audio_html = f"""
<style>
#audio-btn {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: #4CAF50;
    border: none;
    cursor: pointer;
    font-size: 24px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    z-index: 9999;
    transition: all 0.3s;
}}
#audio-btn:hover {{
    transform: scale(1.1);
}}
#audio-btn.playing {{
    background: #f44336;
}}
</style>

<button id="audio-btn" title="배경음악 재생 & 화면 켜짐 유지">🎵</button>

<audio id="background-audio" loop>
    <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
</audio>

<script>
const audio = document.getElementById('background-audio');
const btn = document.getElementById('audio-btn');
let wakeLock = null;

console.log('VibeTFT: Audio & Wake Lock component loaded');

// Wake Lock function
async function enableWakeLock() {{
    if ('wakeLock' in navigator) {{
        try {{
            wakeLock = await navigator.wakeLock.request('screen');
            console.log('VibeTFT: Wake Lock active');
        }} catch (e) {{
            console.log('VibeTFT: Wake Lock failed', e);
        }}
    }}
}}

// Play/Pause toggle - also enables wake lock on first play
btn.addEventListener('click', async () => {{
    // Enable wake lock on first interaction
    if (wakeLock === null) {{
        await enableWakeLock();
    }}

    if (audio.paused) {{
        audio.play()
            .then(() => {{
                console.log('VibeTFT: Background audio playing');
                btn.textContent = '🔊';
                btn.classList.add('playing');
                btn.title = '배경음악 정지';
            }})
            .catch(e => console.log('VibeTFT: Audio play failed', e));
    }} else {{
        audio.pause();
        console.log('VibeTFT: Background audio paused');
        btn.textContent = '🎵';
        btn.classList.remove('playing');
        btn.title = '배경음악 재생 & 화면 켜짐 유지';
    }}
}});

// Handle visibility changes - reacquire wake lock when returning to app
document.addEventListener('visibilitychange', async () => {{
    if (document.visibilityState === 'visible') {{
        // Reacquire wake lock
        if (wakeLock !== null) {{
            await enableWakeLock();
        }}
        // Resume audio if it was playing
        if (!audio.paused) {{
            audio.play().catch(e => console.log('VibeTFT: Resume failed', e));
        }}
    }}
}});
</script>
"""

components.html(audio_html, height=80)

st.title('🎮 VibeTFT')
st.write('Welcome to VibeTFT - Your TFT companion app!')

st.markdown("""
### Features
- Mobile-optimized interface
- PWA support for app-like experience
- Responsive design for all screen sizes
""")

if st.button('Get Started'):
    st.success('Welcome to VibeTFT!')