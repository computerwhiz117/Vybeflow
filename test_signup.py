import sys
sys.path.insert(0, 'c:\\Users\\josue\\OneDrive\\Documents\\GitHub\\Vybeflow')

try:
    from app import app
    
    with app.test_request_context():
        from flask import url_for
        
        client = app.test_client()
        response = client.get('/signup')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 500:
            print("\n=== ERROR CONTENT ===")
            print(response.data.decode()[:2000])
        else:
            print("SUCCESS - Page loaded correctly!")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
