from ..models.users_model import User 
from ..models.exceptions import UserNotFound,UsernameExists
from flask import request, session, jsonify
import datetime as dt

class UserController:
    """Clase de controlador de usuarios."""

    @classmethod
    def login(cls):
        """del login trae un objeto json"""
        data = request.json
        print("Desde login_controller",data)
        user = User(
            username = data.get('username'),
            password = data.get('password')
        )
        
        #comprueba si existe el usuario, por el nombre y la contraseña
        existe=User.is_registered(user)#returna true si el usuario se encuentra
        if existe:
            user=User.get(user)#traemos todos los datos por el id
            # print("Lohin",user.user_id) 
            session['username'] = user.username
            session['user_id'] = user.user_id #guarda el id del usuario
            return user.serialize(), 200
        else:
            return {"message": "Usuario o contraseña incorrectos"}, 401
    
    @classmethod
    def show_profile(cls):
        """va y busca al usuario por el id de session y trae sus datos"""
        #print("Hola soy show_profile")
        user_id = session.get('user_id')
        # print("show_profile id-->",user_id) 
        user=User(user_id = user_id)
        user = User.getBy_id(user)
        #print("Desde show_profile", user.__dict__)
        return user
        
        
    @classmethod
    def logout(cls):
        """cierra a session"""
        session.pop('username', None)#se elimina el usuario, o bien se le cambia el valor a none
        return {"message": "Sesion cerrada"}, 200
    
    @classmethod
    def get(cls, username):
        """Get a film by id"""
        user = User(username=username)
        result = User.get(user)

        if result is not None:
            return result
        else:
            raise UserNotFound("usuario no encontrado")
    
    @classmethod
    def register(cls):
        data=request.json
        #print("Json desde Formulario--->",data)
        
        fecha_nac= dt.datetime.fromisoformat(str(data.get("birthdate")))
        data["birthdate"]=fecha_nac
        user=User(**data)
        # print("\nUser:",user.serialize())
        value=User.createUser(user)
        if value is None:
            return {"message":UsernameExists("Este user ya existe!!").serialize()},400
        return value
    
    @classmethod
    def update(cls):
        data = request.json
        if "birthdate" in data:
            fecha_nac= dt.datetime.fromisoformat(str(data.get("birthdate")))
            data["birthdate"]=fecha_nac
        user=User(**data)
        # user.birthdate=""
        print("update....: ", user.__dict__)
        User.updateUser(user)
        return {"message":"User actualizado"}, 200
    
    @classmethod
    def delete(cls,user_id):
       """elimina el usuario por el id"""
       return User.eliminarBy_id(user_id)

    #metodos sencillos
    @classmethod
    def getID(cls,id):
        """retorna los datos de un id pasado por path params"""
        user=User(user_id=id)
        return user.getBy_id(user)
        
    @classmethod
    def getAll(cls):
        """devuelve todos los usuarios"""
        return jsonify(User.getAll()) 

    
    @classmethod
    def registrar(cls):
        """registra un usuario"""
        email= request.args.get("email")
        username= request.args.get("username")
        first_name= request.args.get("first_name")
        # print(first_name)
        last_name= request.args.get("last_name") 
        password= request.args.get("password")
        birthdate= request.args.get("birthdate")
        avatar= request.args.get("avatar")

        print("Registrando usuario....(por query params)")
        user=User(username=username,email=email,first_name=first_name,last_name=last_name,password=password, birthdate=birthdate,avatar=avatar)
        
        return User.registrar(user)
    
    @classmethod
    def actualizar(cls,username):
        user1=User(username=username)
        """actualizar por el nombre de usuario"""
        email= request.args.get("email")
        name_usuario= request.args.get("username")
        first_name= request.args.get("first_name")
        # print(username)
        last_name= request.args.get("last_name") 
        password= request.args.get("password")
        birthdate= request.args.get("birthdate")
        # print(birthdate)        

        user=User(username=name_usuario,email=email,first_name=first_name,last_name=last_name,password=password,birthdate=birthdate)

        return User.actualizar(user1,user)
        
    @classmethod
    def eliminar(cls,username):
        # user=User(username=username)
        return User.eliminar(username)
    
    @classmethod
    def get_servers_user(cls):
        if 'username' in session:
            print("SIIII")
        else:
            print("NOOO")
        #print("USUARIOOO desde users: ", session.get('username'))