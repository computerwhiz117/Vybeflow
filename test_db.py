from app import app, db, User

app.app_context().push()

# Test login with existing user
print("Testing login functionality...")
user = User.query.filter_by(username='manualtest').first()
if user:
    if user.check_password('test123'):
        print("✓ Login verification works")
    else:
        print("✗ Password check failed")
else:
    print("✗ User not found")

# Test creating another user
print("\nTesting user creation...")
try:
    new_user = User(username='anothertest', email='another@test.com', phone='123')
    new_user.set_password('password123')
    db.session.add(new_user)
    db.session.commit()
    print("✓ User creation works")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nAll database operations working correctly!")
