from sqlalchemy import create_engine, text
import bcrypt

# Conectamos a la base de datos
engine = create_engine('sqlite:///device_systems.db')
conn = engine.connect()

# Hasheamos la contraseña '123456' directamente con bcrypt
plain_password = '123456'
hashed_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
new_password_hashed = hashed_bytes.decode('utf-8')

# Actualizamos usando la columna correcta 'hashed_password'
conn.execute(
    text('UPDATE users SET hashed_password = :pwd WHERE email = :email'),
    {'pwd': new_password_hashed, 'email': 'Luis@gmail.com'}
)
conn.commit()
conn.close()

print("¡Contraseña actualizada con éxito para Luis@gmail.com!")