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