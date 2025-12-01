from app import bcrypt

def test_hash_and_check():
    """
    Test that bcrypt can hash a password and verify it correctly.
    """
    pw = "MyS3cureP@ss!"
    hashed = bcrypt.generate_password_hash(pw).decode()

    # Correct password should match
    assert bcrypt.check_password_hash(hashed, pw) is True

    # Incorrect password should not match
    assert bcrypt.check_password_hash(hashed, "wrong") is False
