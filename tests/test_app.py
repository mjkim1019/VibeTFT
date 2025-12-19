"""
VibeTFT 앱 단위 테스트

테스트 실행 방법:
0. 가상환경 설정: python3 -m venv .venv
1. 테스트 의존성 설치: pip3 install -r requirements.txt
2. 모든 테스트 실행: python3 -m pytest tests/ -v
3. 특정 테스트 파일 실행: python3 -m pytest tests/test_app.py -v
4. 커버리지 포함 실행: python3 -m pytest tests/ --cov=app --cov-report=html
5. 특정 테스트만 실행: python3 -m pytest tests/test_app.py::TestVibeTFTApp::test_app_configuration -v

또는 개별 파일 실행:
cd tests && python3 test_app.py
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import tempfile

# Streamlit 앱을 import하기 전에 환경 설정
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

class TestVibeTFTApp(unittest.TestCase):
    """VibeTFT 앱의 주요 기능 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        self.test_dir = tempfile.mkdtemp()
    
    def test_static_files_exist(self):
        """PWA 필수 파일들이 존재하는지 확인"""
        # manifest.json 파일 존재 확인
        manifest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'manifest.json')
        self.assertTrue(os.path.exists(manifest_path), "manifest.json 파일이 존재해야 합니다")
        
        # service worker 파일 존재 확인
        sw_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'sw.js')
        self.assertTrue(os.path.exists(sw_path), "service worker 파일이 존재해야 합니다")
    
    def test_manifest_json_content(self):
        """manifest.json 파일의 필수 내용 확인"""
        import json
        manifest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'manifest.json')
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # 필수 필드 확인
        required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
        for field in required_fields:
            self.assertIn(field, manifest, f"manifest.json에 {field} 필드가 있어야 합니다")
        
        # PWA 설정 확인
        self.assertEqual(manifest['name'], 'VibeTFT', "앱 이름이 올바르게 설정되어야 합니다")
        self.assertEqual(manifest['display'], 'standalone', "standalone 모드로 설정되어야 합니다")
        self.assertEqual(manifest['lang'], 'ko', "한국어로 설정되어야 합니다")
    
    def test_service_worker_content(self):
        """service worker 파일의 기본 구조 확인"""
        sw_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'sw.js')
        
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw_content = f.read()
        
        # 필수 이벤트 리스너 확인
        self.assertIn('install', sw_content, "install 이벤트 리스너가 있어야 합니다")
        self.assertIn('fetch', sw_content, "fetch 이벤트 리스너가 있어야 합니다")
        self.assertIn('activate', sw_content, "activate 이벤트 리스너가 있어야 합니다")
        
        # 캐시 관련 코드 확인
        self.assertIn('CACHE_NAME', sw_content, "캐시 이름이 정의되어야 합니다")
        self.assertIn('caches.open', sw_content, "캐시 열기 기능이 있어야 합니다")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.components.v1.html')
    def test_app_configuration(self, mock_html, mock_config):
        """앱 설정이 올바르게 되는지 확인"""
        # app.py를 import하여 설정 확인
        import importlib.util
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        spec = importlib.util.spec_from_file_location("app", app_path)
        app_module = importlib.util.module_from_spec(spec)
        
        # 모든 streamlit 관련 함수들을 mock
        with patch('streamlit.title'), \
             patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.button', return_value=False), \
             patch('streamlit.success'):
            
            spec.loader.exec_module(app_module)
        
        # set_page_config 호출 확인
        mock_config.assert_called_once()
        call_args = mock_config.call_args[1]  # kwargs
        
        self.assertEqual(call_args['page_title'], 'VibeTFT', "페이지 제목이 올바르게 설정되어야 합니다")
        self.assertEqual(call_args['page_icon'], '🎮', "페이지 아이콘이 올바르게 설정되어야 합니다")
        self.assertEqual(call_args['layout'], 'wide', "와이드 레이아웃으로 설정되어야 합니다")
        self.assertEqual(call_args['initial_sidebar_state'], 'collapsed', "사이드바가 숨김으로 설정되어야 합니다")
    
    def test_requirements_file(self):
        """requirements.txt 파일 확인"""
        requirements_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requirements.txt')
        self.assertTrue(os.path.exists(requirements_path), "requirements.txt 파일이 존재해야 합니다")
        
        with open(requirements_path, 'r') as f:
            requirements = f.read()
        
        self.assertIn('streamlit', requirements, "streamlit 의존성이 있어야 합니다")
    
    def test_pwa_meta_tags(self):
        """PWA meta 태그가 포함되는지 확인"""
        import importlib.util
        app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
        
        with open(app_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # PWA 관련 meta 태그 확인
        pwa_tags = [
            'apple-mobile-web-app-capable',
            'mobile-web-app-capable',
            'apple-mobile-web-app-title',
            'manifest',
            'serviceWorker'
        ]
        
        for tag in pwa_tags:
            self.assertIn(tag, app_content, f"PWA {tag} 설정이 있어야 합니다")

def run_tests():
    """테스트 실행 함수"""
    print("🧪 VibeTFT 단위 테스트 시작...")
    unittest.main(verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()