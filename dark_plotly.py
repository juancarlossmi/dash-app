# Dash = modulo que nos permite conectar a la libreria "dash", crear un servidor para poder ver el grafico que se introduce en un html creado por la libreria
# dcc = modulo que nos permite crear los complementos de un dash-app, en este ejemplo con "dcc" se crea un radioitems para poder cambiar de grafico
# html = modulo que permite interactuar con el html que se renderiza en el servidor
# Input = modulo que permite definir la informacion de entrada, es decir la informaicon que recibira nuestra dash-app para crear y rederizar en el servidor un grafico interactivo
# Output = modulo que permite devolver la informacion obtenida del Input
from dash import Dash, dcc, html, Input, Output
# plotly.express. libreria que nos permite crear graficos plotly
import plotly.express as px
# Libreria para poder cambiar el color de fondo del grafico
import plotly.io as pio
# La biblioteca "dash-mantine-components" proporciona componentes que se pueden utilizar dentro de tus aplicaciones Dash
import dash_mantine_components as dmc
# inicialzamos un dash-app
app = Dash(__name__)
# creamos un layout para poder agregar los componentes y graficos que queramos ver, fijate como usamos una etiqueta div para poder cnotener un titulo, etiqueta p y componentes radioitems

server = app.server
app.layout = html.Div(children=[
    # MantineProvider = biblioteca de componentes y estilos para React
    # La biblioteca "dash-mantine-components" proporciona componentes de Mantine que se pueden utilizar dentro de tus aplicaciones Dash
    # Esto te permite combinar la potencia de Dash y Mantine para crear aplicaciones web atractivas con una experiencia de usuario moderna.
    dmc.MantineProvider(
        id="app-theme",
        theme={
            "colorScheme": "white",
        },
        inherit=True,
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            dmc.Header(
                height=90,
                withBorder=True,
                style={"padding": "16px", "display": "flex",
                       "justifyContent": "space-between"},
                children=[
                    dmc.Text(
                        "Aplicacion Dash con modo oscuro",
                        style={"fontSize": 36},
                    ),
                    dmc.Switch(
                        id="switch-theme",
                        size="lg",
                        radius="sm",
                        label="modo oscuro",
                        checked=True
                    ),
                ],
            ),
            html.Div([
                html.H4('conjunto de datos Gapminder: PIB y población mundial a traves del tiempo', style={
                        'text-align': 'center'}),
                html.P("Selecciona un área del grafico para poder filtrar la información:", style={
                       'text-align': 'center'}),
                dcc.RadioItems(
                    id='selection',
                    options=[{'label': ' Animacion: PIB Mundial', 'value': 'GDP - Scatter'},
                             {'label': ' Animacion: Población Mundial', 'value': 'Population - Bar'}],
                    value='GDP - Scatter',
                ),
                # Animacion en forma de cubo que aparece mientras dash, carga la informacion del grafico seleccionado
                dcc.Loading(dcc.Graph(id="graph"), type="cube")
            ]),
        ],
    )
])

# NOTA: por cada funcion creada debes crear una seccion de callbacks

# Seccion de callback para la funcion switch_theme : recuerda esta seccion hace interactuar el layout con los componentes
@app.callback(
    Output('app-theme', 'theme'),
    Input('app-theme', 'theme'),
    Input("switch-theme", "checked"),
    prevent_initial_call=True)
# Funcion que crea la logica del switch para cambiar el tema de fondo de oscuro a blanco
def switch_theme(theme, checked):
    if not checked:
        theme.update({'colorScheme': 'dark'})
    else:
        theme.update({'colorScheme': 'white'})
    return theme
# Seccion de callback para la funcion display_animated_graph : recuerda esta seccion hace interactuar el layout con los componentes
@app.callback(
    Output("graph", "figure"),
    Input("selection", "value"),
    Input("switch-theme", "checked"))  # Agregar el estado del interruptor como entrada
# Funcion para poder cambiar el color de fondo del grafico en funcion a el valor del switch es decir si el fondo es oscuro el grafico tambien lo sera e igual con el fondo blanco del grafico y del html
def display_animated_graph(selection, dark_mode):
    if dark_mode:
        pio.templates.default = "plotly"
    else:
        pio.templates.default = "plotly_dark"
    # df = data frame que contiene la informacion que podemos visualizar en los graficos, es decir gapminder contiene la informacion del "PIB mundial" y la "densidad de poblacion a traves del tiempo"
    df = px.data.gapminder()
    # creamos una lista traducida de los continentes del data frame para utilizarlos dentro del grafico
    continent_mapping = {
        "Asia": "Asia",
        "Europe": "Europa",
        "Africa": "África",
        "Americas": "América",
        "Oceania": "Oceanía"
    }
    # agregamos la lista traducida a los graficos sin alterar la informacion original, exytaida de gapminder
    df['continent'] = df['continent'].map(continent_mapping)
    # animations = en esta variable se crean los 2 graficos disponibles, ya que esta variable es un diccionario, es decir puede recibir mas graficos dentro de esta variable
    animations = {
        # Aqui obtenemos el primer grafico "PIB mundial", en forma de dispersion
        'GDP - Scatter': px.scatter(
            # cargamos el dataframe y obtenemos las variables contenidas en el data frame, 
            # donde :
                # x = gdpPercap: El PIB per cápita del país en ese año.
                # y = lifeExp: La esperanza de vida promedio en ese país y año.
                # animation_frame = year: El año en que se registraron los datos.
                # animation_group = country: El nombre del país.
                # size = pop: La población del país en ese año.
                # color = continent: El continente al que pertenece el país.
                # hover_name = country: El nombre del país.
            df, x="gdpPercap", y="lifeExp", animation_frame="year",
            animation_group="country", size="pop", color="continent",
            hover_name="country", log_x=True, size_max=55,
            # range_x = rango de capital desde 100 dolares hasta 100mil por persona
            # range_y = edad promedio de la persona
            range_x=[100, 100000], range_y=[25, 90]).update_layout(
            # Cambiamos el titulo del eje x
            xaxis_title="PIB per cápita",
            # Cambiamos el titulo del eje y
            yaxis_title="Expectativa de Vida",
            # Cambiamos el titulo del grafico
            title="Gráfico de PIB y Expectativa de Vida por Año"
        ),
        # Aqui obtenemos el segundo grafico "poblacion mundial a traves del tiempo", en forma de graficos de barras
        'Population - Bar': px.bar(
            # x = continent: El continente al que pertenece el país.
            # y = pop: La población del país en ese año.
            # animation_frame = year: El año en que se registraron los datos.
            # animation_group = country: El nombre del país.
            # size = pop: La población del país en ese año.
            # color = continent: El continente al que pertenece el país.
            # hover_name = country: El nombre del país.
            # range_y = pais con poblacion promedio desde 0 hasta 4 bilones
            df, x="continent", y="pop", color="continent", hover_name="country",
            animation_frame="year", animation_group="country",
            range_y=[0, 4000000000]).update_layout(
            # Cambiamos el titulo del eje x
            xaxis_title="Continente",
            # Cambiamos el titulo del eje y
            yaxis_title="Población",
            # Cambiamos el titulo del grafico
            title="Gráfico de Población por Continente y Año"
        ),
    }
    # Devolvemos el grafico seleccionado por medo del radio items, ademas de que si se selecciona un area dentro del grafico esta sera filtrada y mostrara la logica del codigo dentro del area elegida
    return animations[selection]
# if __name__ == "__main__": = comprobar si el script se está ejecutando directamente como el programa principal o si se está importando como un módulo en otro scrip
if __name__ == "__main__":
    # Corremos el servidor
    app.run_server(debug=False)
