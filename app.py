import streamlit as st

st.set_page_config(
    page_title='VibeTFT',
    page_icon='🎮',
    layout='wide',
    initial_sidebar_state='collapsed'
)

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