# ParkingWeb
Aplicación web para la gestión de un Parking haciendo uso del framework de FastApi.

Para lanzar la aplicación hacer la instalación de los paquetes que figuran en el archivo de "requirements.txt".

```
pip install -r requirements.txt
```

Además de instalar el siguiente módulo:

```
npm install request
```

Una vez hecho esto crea un fichero txt en el directorio de "app", que se llame "mysql-user.txt", en donde se tendrá que agregar el nombre de usuario de mysql en la primera línea y en la segunda, la contraseña.

```
username
password
```

Una vez hecho esto, solo toca lanzar la aplicación, abre dos terminales en el directorio "app". Primero lanza el servidor con el siguiente comando.

```
uvicorn main:app --reload
```

Luego lanza el servicio de node, mientras el servidor está lanzado de la siguiente forma.

```
node carModels.js
```
