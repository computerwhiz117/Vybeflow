import requests

print("=== WEBSITE FUNCTIONALITY SCAN ===\n")

session = requests.Session()

# Test Signup Page
print("1. SIGNUP PAGE TEST")
print("-" * 40)
signup_url = 'http://127.0.0.1:5000/signup'
try:
    response = session.get(signup_url)
    print(f"   Status Code: {response.status_code}")
    
    # Check for required elements
    has_csrf = 'csrf_token' in response.text
    has_username = 'id="username"' in response.text
    has_email = 'id="email"' in response.text
    has_password = 'id="password"' in response.text
    has_confirm = 'id="confirm"' in response.text
    has_submit = 'type="submit"' in response.text
    
    print(f"   CSRF Token: {'✓ Present' if has_csrf else '✗ MISSING'}")
    print(f"   Username Field: {'✓ Present' if has_username else '✗ MISSING'}")
    print(f"   Email Field: {'✓ Present' if has_email else '✗ MISSING'}")
    print(f"   Password Field: {'✓ Present' if has_password else '✗ MISSING'}")
    print(f"   Confirm Password: {'✓ Present' if has_confirm else '✗ MISSING'}")
    print(f"   Submit Button: {'✓ Present' if has_submit else '✗ MISSING'}")
    
    if all([has_csrf, has_username, has_email, has_password, has_confirm, has_submit]):
        print("   Result: ✓ SIGNUP PAGE IS WORKING")
    else:
        print("   Result: ✗ SIGNUP PAGE HAS ISSUES")
        
except Exception as e:
    print(f"   ✗ Error accessing signup page: {e}")

print()

# Test Login Page
print("2. LOGIN PAGE TEST")
print("-" * 40)
login_url = 'http://127.0.0.1:5000/login'
try:
    response = session.get(login_url)
    print(f"   Status Code: {response.status_code}")
    
    # Check for required elements
    has_csrf = 'csrf_token' in response.text
    has_username = 'id="username"' in response.text
    has_password = 'id="password"' in response.text
    has_submit = 'type="submit"' in response.text
    
    print(f"   CSRF Token: {'✓ Present' if has_csrf else '✗ MISSING'}")
    print(f"   Username Field: {'✓ Present' if has_username else '✗ MISSING'}")
    print(f"   Password Field: {'✓ Present' if has_password else '✗ MISSING'}")
    print(f"   Submit Button: {'✓ Present' if has_submit else '✗ MISSING'}")
    
    if all([has_csrf, has_username, has_password, has_submit]):
        print("   Result: ✓ LOGIN PAGE IS WORKING")
    else:
        print("   Result: ✗ LOGIN PAGE HAS ISSUES")
        
except Exception as e:
    print(f"   ✗ Error accessing login page: {e}")

print()

# Test Home Page
print("3. HOME PAGE TEST")
print("-" * 40)
home_url = 'http://127.0.0.1:5000/'
try:
    response = session.get(home_url)
    print(f"   Status Code: {response.status_code}")
    print(f"   Result: {'✓ HOME PAGE ACCESSIBLE' if response.status_code == 200 else '✗ ERROR'}")
except Exception as e:
    print(f"   ✗ Error accessing home page: {e}")

print()
print("=== SCAN COMPLETE ===")
