# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from App import app

def run_admin_tests():
    print("=== STARTING ADMIN & GEMINI SETTINGS TESTS ===")
    client = app.test_client()

    # 1. Test GET / contains Login button & Modals
    res = client.get('/')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'headerLoginBtn' in html, "headerLoginBtn missing"
    assert 'adminLoginModal' in html, "adminLoginModal missing"
    assert 'adminSettingsModal' in html, "adminSettingsModal missing"
    assert 'Danam' in html, "Danam missing"
    print("✔ [1/4] GET / verified: Login button & Admin Modals are present")

    # 2. Test Login API
    # 2.1 Bad credentials
    res = client.post('/api/admin/login', json={'user_id': 'Wrong', 'password': '123'})
    assert res.status_code == 401
    print("✔ [2/4] Bad credentials rejected (HTTP 401)")

    # 2.2 Correct credentials: Danam / Danam
    res = client.post('/api/admin/login', json={'user_id': 'Danam', 'password': 'Danam'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True and data['user'] == 'Danam'
    print("✔ [3/4] Login with User Id 'Danam' and Password 'Danam' succeeded (HTTP 200)")

    # 3. Test Settings API (GET and POST)
    res = client.get('/api/admin/settings')
    assert res.status_code == 200
    settings_data = res.get_json()['settings']
    assert 'prompts' in settings_data
    assert 'gemini_api_keys' in settings_data

    # Update prompts and keys
    new_keys = [{'key': 'AIzaSyMockKeyForTesting1234567890', 'label': 'Test Key 1'}]
    new_prompts = {'passport': 'Updated Custom Passport Studio Prompt for 300 DPI'}
    res = client.post('/api/admin/settings', json={
        'gemini_api_keys': new_keys,
        'prompts': new_prompts
    })
    assert res.status_code == 200
    updated_data = res.get_json()
    assert updated_data['success'] is True

    # Verify on disk
    with open('settings.json', 'r', encoding='utf-8') as f:
        disk_data = json.load(f)
    assert disk_data['prompts']['passport'] == 'Updated Custom Passport Studio Prompt for 300 DPI'
    assert len(disk_data['gemini_api_keys']) == 1

    # Restore original rich prompt
    client.post('/api/admin/settings', json={'prompts': {'passport': settings_data['prompts']['passport']}})
    print("✔ [4/4] Gemini API Keys and Photo Prompts saved and verified on disk")

    print("\n===========================================")
    print("🎉 ALL ADMIN & GEMINI SETTINGS TESTS PASSED!")
    print("===========================================")

if __name__ == '__main__':
    run_admin_tests()

