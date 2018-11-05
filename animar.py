"""
Este archivo tiene funciones utiles para cargar en forma directa y graficar en forma animada cosas en jupyer lab
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc

# Definimos algunos parametros del sistema

x_ini = 0
x_fin = 1
dx = 0.01
t_ini = 0
t_fin = 1
dt = 0.01
pasos = None

print ('Para ayuda de como utilizar animar ejecute animar.help()')

def help():
    print ('Este modulo es un frontend de matplotlib para facilitar el grafico de funciones dependientes del tiempo.')
    print ('Para ejecutarlo se deben tener definidas funciones de la forma f=f(x,t) dependientes de x y de t donde se recorre los graficos modificando el valor de t.')
    print ('animar.estacionaria es un ejemplo preconstruido de onda estacionaria.')
    print ('animar.viajera es un ejemplo preconstruido de onda viajera.')
    print ('animar.gauss_viajera es un ejemplo preconstruido de una gaussiana viajera.')
    print ('Para visualizar las funciones en el entorno de jupyter notebook se debe convertir a formato HTML las animaciones. Para ello se debe importar ´from IPython.display import HTML´ y luego ejecutar ´HTML(anim.to_html5_video())´ donde anim es la animacion creada con ´anim = animar.animar(f)´.')
    print ('El paquete animar posee parametros default que se enuncian a continuacion, si se desean modificar se deden sobreescribir al crear la animación.')
    print ("""\n 
    x_ini = 0 \n
    x_fin = 1 \n
    dx = 0.01 \n
    t_ini = 0 \n
    t_fin = 1 \n
    dt = 0.01 \n
    pasos = None""")
    print ('Un ejemplo simple para comenzar podria ser: HTML(animar.animar(animar.viajera,x_ini=-3,x_fin=3).to_html5_video())')
        
def estacionaria(x,t):
    return np.cos(2*np.pi*x)*np.sin(2*np.pi*t)

def viajera(x,t):
    return np.cos(2*np.pi*x-2*np.pi*t)
                  
def gauss_viajera(x,t):
    return np.exp(-(x-(t))**2/0.1**2)

def limites(f,x,t):
    """
    Esta funcion asume que f es una funcion matematica de x,t[i] que posee un maximos y un minimo.
    """
    y_min = min(f(x,t[0]))
    y_max = max(f(x,t[0]))
    for tiempo in t:
        if (min(f(x,tiempo))<y_min): y_min = min(f(x,tiempo))
        if (max(f(x,tiempo))>y_max): y_max = max(f(x,tiempo))
    return y_min,y_max
    
def animar(f, x_ini=x_ini, x_fin=x_fin, dx=dx, t_ini=t_ini, t_fin=t_fin, dt=dt, ajustarTiempo=True, pasos=pasos):
    """
    Funcion para realizar animaciones. Toma como entrada una funcion
        f(x,t)
    donde el primer argumento es la coordenada espacial y el segundo la temporal.
    
    Requiere tener instalada en el sistema operativo la libreria ffmpeg.
    
    Ademas pide como argumento de entrada
        x_ini - la coordenada x inicial
        x_fin - la coordenada x final
        dx - el valor entre dos puntos sucesivos de x
        t_ini - la coordenada t inicial
        t_fin - la coordenada t final
        dt - el valor entre dos puntos sucesivos de t
        
            
    Esta harcodeado el tiempo entre dos frames en 5ms. Pero se puede cambiar cambiando el valor de 
        `interval` que aparece mas abajo.
    """
    if pasos:
        dt = (t_fin-t_ini)/pasos
    if ajustarTiempo:
        delay = 20
    else:
        delay = dt
    
    # Definimos los intervalos para graficar
    x = np.linspace(x_ini,x_fin,int((x_fin-x_ini)/dx))
    t = np.linspace(t_ini,t_fin,int((t_fin-t_ini)/dt))
    
    # Ponemos los ejes para la figura
    fig, ax = plt.subplots()

    ax.set_xlim((x_ini, x_fin))
    ax.set_ylim(limites(f,x,t))

    line, = ax.plot([], [], lw=2)
    
    # Definimos la funcion que crea un grafico vacio
    def init():
        line.set_data([], [])
        return (line,)
    
    # Funcion que crea cada frame
    def animate(i):
        y = f(x,i)
        line.set_data(x, y)
        return (line,)
    
    # Creamos el objeto animado
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=t, interval=delay, blit=True)
    
    return anim