from werkzeug.security import generate_password_hash

pw_hash = generate_password_hash("god6211q@W")
print(pw_hash)