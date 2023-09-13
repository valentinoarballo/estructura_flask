# Imports que son nativos de Python
import os
from datetime import timedelta

# Imports que son nativos del Framework y Librerias
from app import app, db, jwt
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Imports de variables generadas por nosotros
from app.models.models import (
    Localidad,
    Pais,
    Persona,
    Provincia,
    User,
)
from app.schemas.schema import (
    UserAdminSchema,
    UserBasicSchema,
)

@app.route("/users")
@jwt_required()
def get_all_users():
    aditional_info = get_jwt()

    page = request.args.get('page', 1, type=int)
    can = request.args.get('can', 2, type=int)
    users = db.session.query(User).paginate(
        page=page, per_page=can
    )

    print(f'HAS PREV? {users.has_prev}')
    print(f'HAS NEXT? {users.has_next}')
    print(f'NEXT {users.next}')
    print(f'NEXT NUM {users.next_num}')

    print(url_for('get_all_users', page=users.next_num) if users.has_next else None)

    if aditional_info['is_admin']==1:
        return jsonify(
            {
                "results": UserAdminSchema().dump(users, many=True),
                "prev": url_for('get_all_users', page=users.prev_num) if users.has_prev else None,
                "next": url_for('get_all_users', page=users.next_num) if users.has_next else None

            }
        )
    return jsonify(
        {
            "results": UserBasicSchema().dump(users, many=True),
            "prev": url_for('get_all_users', page=users.prev_num) if users.has_prev else None,
            "next": url_for('get_all_users', page=users.next_num) if users.has_next else None
        }
    )

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/agregar_pais', methods=['POST'])
def nuevo_pais():
    if request.method=='POST':
        nombre_pais = request.form['nombre']

        # Inicializo el objeto
        nuevo_pais = Pais(nombre=nombre_pais)
        # Preparo el objeto para enviarlo a la base de datos
        db.session.add(nuevo_pais)
        # Envio el objeto
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/borrar_pais/<id>')
def borrar_pais(id):

    pais = Pais.query.get(id)
    db.session.delete(pais)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_user', methods=['post'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get("is_admin")
    password_hash = generate_password_hash(
        password, method='pbkdf2', salt_length=8
        )
    
    nuevo_usuario = User(
        username=username, 
        password_hash=password_hash, 
        is_admin=is_admin
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "Se recibio la data":"OK",
        "username":username,
        "password_hash":password_hash
        }, 200)

@app.route('/login')
def login():
    
    username = request.authorization.get('username')
    password = request.authorization.get('password')

    user = User.query.filter_by(username=username).first()

    #check_password_hash(contraseña guardada, contraseña recibida)
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=60),
            additional_claims=dict(
                is_admin=user.is_admin,
            )
        )
        return jsonify({"ok":access_token})
    return jsonify(Error="No pude generar el token"),400

@app.route("/ruta_restringida")
@jwt_required()
def ruta_restringida():
    current_user = get_jwt_identity()
    additional_info = get_jwt()
    if additional_info['user_type']==1:
        return jsonify(
            {
                "Mensaje":f"El usuario {current_user} tiene acceso a esta ruta",
                "Info Adicional": additional_info
            }
        )
    return jsonify(
            {
                "Mensaje":f"El usuario {current_user} no tiene acceso a esta ruta",
            }
        )

@jwt.invalid_token_loader
def unauthorized_user(reason):
    return jsonify(mensaje=f"Acceso denegado porque : {reason}"), 401

@app.context_processor
def inject_paises():
    countries = db.session.query(Pais).all()
    return dict(
        paises=countries   
    )

@app.context_processor
def inject_idiomas():
    return dict(
        lang=['US','ES', 'FR']   
    )
