# Cadena de caracteres para realizar el cifrado y descifrado del mensaje.
letras = ("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
# Palabra clave para realizar el cifrado y desifrado.
clave = "SEZAMI"
# Longitud de la cadena letras
tam_letras = len(letras)
# Longitud de la cadena clave
tam_clave = len(clave)

# Función que cifra una cadena de caracteres.
def cifrar(mensaje):
    # Cadena que almacena la cadena cifrada.
    mensaje_cifrado = ""
    # Entero que indica la posición actual del carácter de la clave que se tomará.
    indice_clave = 0
    # Iterar cada caracter en la cadena a cifrar.
    for caracter in mensaje:
        # Se busca caracter en la cadena letras y regresa el índice de este en la cadena letras. 
        posicion = letras.find(caracter.upper())
        # Si posición == -1 significa que caracter no se encontró en la cadena letras.
        if posicion != -1:
            # Se le suma a posision el índice del carácter de la clave en indice_clave en la cadena letras.
            posicion+=letras.find(clave[indice_clave])
            # posicion se iguala a posision módulo tam_letras.
            posicion %= tam_letras
            # Si caracter es mayúsculas.
            if caracter.isupper():
                # mensaje_cifrado se le agrega el carácter en posicion en la cadena letras.
                mensaje_cifrado=mensaje_cifrado+letras[posicion]
            else:
                # mensaje_cifrado se le agrega el carácter en posicion en la cadena letras en minúscula.
                mensaje_cifrado=mensaje_cifrado+letras[posicion].lower()
            # Se incrementa en 1 indice_clave.
            indice_clave+=1
            # Si indice_clave es igual a el tamaño de la clave.
            if indice_clave==tam_clave:
                # Se asigna a indice_clave  0.
                indice_clave=0
        # Si no se encontro caracter en la cadena letras.
        else:
            # Se añade caracter a mensaje_cifrado.
            mensaje_cifrado+=caracter
    # Regresa mensaje_cifrado.
    return mensaje_cifrado

# Función que descifra una cadena de caracteres.
def descifrar(mensaje):
    # Cadena que almacena la cadena descifrada.
    mensaje_descifrado = ""
    # Entero que indica la posición actual del carácter de la clave que se tomará.
    indice_clave = 0
    # Iterar cada caracter en la cadena a cifrar.
    for caracter in mensaje:
        # Se busca caracter en la cadena letras y regresa el índice de este en la cadena letras. 
        posicion = letras.find(caracter.upper())
        # Si posición == -1 significa que caracter no se encontró en la cadena letras.
        if posicion != -1:
            # Se le resta a posision el índice del carácter de la clave en indice_clave en la cadena letras.
            posicion-=letras.find(clave[indice_clave])
            # posicion se iguala a posision módulo tam_letras.
            posicion %= tam_letras
            # Si caracter es mayúsculas.
            if caracter.isupper():
                # mensaje_cifrado se le agrega el carácter en posicion en la cadena letras.
                mensaje_descifrado=mensaje_descifrado+letras[posicion]
            else:
                # mensaje_cifrado se le agrega el carácter en posicion en la cadena letras en minúscula.
                mensaje_descifrado=mensaje_descifrado+letras[posicion].lower()
            # Se incrementa en 1 indice_clave.
            indice_clave+=1
            # Si indice_clave es igual a el tamaño de la clave.
            if indice_clave==tam_clave:
                # Se asigna a indice_clave  0.
                indice_clave=0
        # Si no se encontro caracter en la cadena letras.
        else:
            # Se añade caracter a mensaje_cifrado.
            mensaje_descifrado+=caracter
    # Regresa mensaje_cifrado.
    return mensaje_descifrado