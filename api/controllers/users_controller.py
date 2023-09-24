from ..models.users_model import User 
from ..models.exceptions import UserNotFound,UsernameExists
from flask import request,session,jsonify
import datetime as dt

class UserController:
    """Clase de controlador de usuarios."""

    @classmethod
    def login(cls):
        """del login trae un objeto json"""
        data = request.json
        # print("Desde login_controller",data)
        user = User(
            username = data.get('username'),
            password = data.get('password')
        )
        
        #comprueba si existe el usuario, por el nombre y la contraseña
        if User.is_registered(user):
            session['username'] = data.get('username')#guarda el nombre_de usuario
            return {"message": "Sesion iniciada"}, 200
        else:
            return {"message": "Usuario o contraseña incorrectos"}, 401
    
    @classmethod
    def show_profile(cls):
        """va y busca al usuario y trae sus datos"""
        print("Hola soy show_profile")
        username = session.get('username')
        user = User.get(User(username = username))
        print("Desde show_profile", user.__dict__)

        if user is None:
            return {"message": "Usuario no encontrado"}, 404
        else:
            return user.serialize(), 200
        
    
        
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
        print("Json desde Formulario--->",data)
        
        fecha_nac= dt.datetime.fromisoformat(str(data.get("birthdate")))
        data["birthdate"]=fecha_nac
        user=User(**data)
        # print("\nUser:",user.serialize())

        if User.createUser(user) is None:
            # raise UsernameExists("Este user ya existe!!")
            return {"message":UsernameExists("Este user ya existe!!").serialize()},400
        else:
            return {"message":"todo en orden"},200

    @classmethod
    def update(cls):
        data = request.json
        user=User(**data)
        print("Desde controlador: ", user.__dict__)

        User.updateUser(user)
        return {"message":"User actualizado"}, 200
    
    @classmethod
    def delete(cls):
        """"""

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

        print("Registrando usuario....(por query params)")
        user=User(username=username,email=email,last_name=last_name,password=password, birthdate=birthdate)
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
        print(birthdate)        

        user=User()
        try:
           
            if birthdate !="" and birthdate!=None:
                birthdate= dt.datetime.fromisoformat(birthdate)
                # print("cumple",birthdate)

                user=User(username=name_usuario,email=email,first_name=first_name,last_name=last_name,password=password, birthdate=birthdate)
            else:
                user=User(username=name_usuario,email=email,first_name=first_name,last_name=last_name,password=password)
  
        except ValueError:
            print("La fecha ingresada es Invalida, por favor siga este ejemplo -> YYYY-MMM-DD (Y=year/M=month/D=day)")
        except Exception as err:
            # return f"La fecha ingresaa es Invalid "
            #return ("La fecha ingresaa es Invalida, por favor siga este ejemplo -> YYYY-MMM-DD (Y=year) (M=month) (D=day)  ")
            return (f"Unexpected {err=}, {type(err)=}")
        
        return User.actualizar(user1,user)
        
    @classmethod
    def eliminar(cls,username):
        # user=User(username=username)
        return User.eliminar(username)