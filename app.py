import streamlit as st
import streamlit.components.v1 as components

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

# Wake Lock for keeping screen awake during gameplay
components.html("""
<script>
let wakeLock = null;

async function enableWakeLock() {
    if ('wakeLock' in navigator) {
        try {
            wakeLock = await navigator.wakeLock.request('screen');
            console.log('VibeTFT: Wake Lock active');
        } catch (e) {
            console.log('VibeTFT: Wake Lock failed', e);
        }
    }
}

// Handle visibility changes - reacquire wake lock when returning to app
document.addEventListener('visibilitychange', async () => {
    if (wakeLock !== null && document.visibilityState === 'visible') {
        await enableWakeLock();
    }
});

// Initial activation (with user interaction fallback for mobile)
enableWakeLock().catch(() => {
    document.addEventListener('click', enableWakeLock, { once: true });
});
</script>
""", height=0)

# Background audio for keeping app active in background
components.html("""
<audio id="background-audio" loop>
    <source src="/static/audio/background.mp3" type="audio/mpeg">
</audio>

<script>
const audio = document.getElementById('background-audio');

// Auto-play background audio
function playBackgroundAudio() {
    audio.play()
        .then(() => console.log('VibeTFT: Background audio playing'))
        .catch(e => console.log('VibeTFT: Audio play failed', e));
}

// Wait for user interaction (required for mobile autoplay policy)
document.addEventListener('click', playBackgroundAudio, { once: true });

// Resume audio when returning from background
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && audio.paused) {
        playBackgroundAudio();
    }
});
</script>
""", height=0)

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