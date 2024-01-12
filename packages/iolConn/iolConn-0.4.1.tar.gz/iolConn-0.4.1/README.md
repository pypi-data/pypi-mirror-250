iolConn - Conector [Invertir Online® API](https://api.invertironline.com/)
=====================================
![PyPI pyversions](https://img.shields.io/badge/python-3.7+-blue.svg?style=flat)
[![PyPI version shields.io](https://img.shields.io/pypi/v/iolConn.svg)](https://pypi.org/project/iolConn/0.4.1/)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/diegolpedro)
[![Invitame un cafecito](https://cdn.cafecito.app/imgs/buttons/button_4.svg)](https://cafecito.app/diegolpedro)

## Descripción
Conector python para API de [InvertirOnline](https://www.invertironline.com). Permite obtener datos de cotizaciones en tiempo real, informacion historica y operar*.

**El ingreso de operaciones no se encuentra al momento disponible.*

Preparación
-----------
### Seteo del entorno
Para utilizar el conector primero preparar un entorno de ejecución. En este caso se utilizó Anaconda y Python 3.7.
```
conda create -n "\<nombre\>" python==3.7
conda activate \<nombre\>
```
Una vez activado el entorno, instalamos los requerimientos.
```
pip3 install -r requirements.txt
```
Utilización
-----------
Puede encontrarse multiples ejemplos de uso dentro del directorio ejemplos. Los mismos traerán desde la API de Iol, la última cotización de Grupo Galicia en el mercado de Buenos Aires, historicos de cotizaciones y paneles completos.
```
python3 example.py
```
Conector
--------
El conector permite gestionar los bearings correspondientes, reutiliza los gestionados y renueva los vencidos. Consta de una clase que debe instanciarse para utilizar las distintas funcionalidades. Las mismas al 31/07/2023 son:
```
gestionar()                                         # Gestion de API tokens.
descargar(solicitud, activo=None)                   # Descargar lotes de cotizaciones.
price_to_json(mercado='bcba', simbolo=None)         # Descargar ultima cotizacion de un simbolo.
hist_price_to_json(mercado='bcba', simbolo=None,    # Descarga de valores temporales para periodo 
                   desde=None, hasta=None)          # particular.
```
### Opciones
Mercados al 08/06/21
- bCBA
- nYSE
- nASDAQ
- aMEX 
- bCS
- rOFX 
### Solicitudes para función descargar
- panelGeneralAcciones  -> Obtenemos cotizaciones de panel general de acciones.
- panelGeneralBonos     -> Obtenemos cotizaciones de panel general de bonos.
- opciones              -> Obtenemos cotizaciones de las distintas bases de opciones de un subyacente x.
### Fechas
- Fechas en formato 2023-07-23

Documentación
-------------
[https://api.invertironline.com/](https://api.invertironline.com/)