Tutorial de plotly dash desarrollo interactivo, de aplicaciones web con python

Los 3 pilares de plotly library es lo que componen a un Dash App python

    1. Componentes: (botones, slidebar, filtros, barra de navegacion etc . . .)
    2. Layout: nos permite personalizar los componentes agregandoles, colores, tamaños, etc
    3. Callback: los Callback permiten que el dash app sea interactivo y funcional

Primer Hola mundo: estos pasos son escenciales para la creacion del servidor y poder agregar lo que requerimos en nuestro proyecto dash web

# app = inicializamos un dash app, y debemos escoger un tema para personalizar el dash busca mas informacion con respecto a los temas disponibles
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# my_text = agregamos un h1 o titulo a la hoja, lo que se ingrese en el parametro "children"
my_text = dcc.Markdown(children="Hola mundo")

# app.layout = agregamos el titulo al layout
app.layout = dbc.Container([my_text])

# Corremos la aplicacion en el puerto 8051 para ver los resultados
if __name__=='__main__':
    app.run_server(port = 8051)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

La principal razon por la cual un dash app es interactivo se debe a CallBacks

DEFINIR UN CALLBACK

    1. va definido por medio de un decorador callback

        - @app.callback(
            Output()
            Input()
        )

        donde . . .
            Input = disparadores del Callback, son los componentes que interactuan con la funcion Callback y cambian su estado
            Output = elementos que se actualizan en respuesta a los cambios que hay en Input, son la respuesta a la actualizacion del input

    2. debe tener una funcion CALLBACK
        def nombre_funcion(nombre_parametro):
            return nombre_parametro

NOTAS:
    Cuando un componente de salida cambia su estado o valor, el callback se activa y ejecuta la funcion asociada que realiza una series de funciones 
    y calculos en funcion de los valores de los componentes de entrada y despues actualiza los componentes de salida

    Cuando tenemos 1 o 2 outputs debemos retornar 2 variables
    
    Cuando tenemos 1 input o 2 inputs debemos agregarlos como parametros de la funcion callback
