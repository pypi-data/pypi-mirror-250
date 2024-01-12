#!/usr/bin/env python
#
# iolConn es un conector python para la API Invertir Online -
# api.invertironline.com.ar
#
# iolConn is an API connector for Invertir Online -
# api.invertironline.com.ar
#
# Copyright (c) 2023 Diego L. Pedro <diegolpedro@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from datetime import datetime
import json                         # Manejo de archivos json.
import requests                     # Requests HTTP post y get.
from .common import NoDataException, NoAuthException

version = '0.4.2'

# Variables de Iol
# https://api.invertironline.com/Help
url_base = "https://api.invertironline.com/"
url_titulo_cot = "api/BCBA/Titulos/DICA/Cotizacion"
url_cot_panel_bonos = "api/Cotizaciones/bonos/PanelGeneral/Argentina"
url_cot_panel_acciones = "api/Cotizaciones/acciones/Panel%20General/argentina"
url_token = "token"
url_cot_opciones = {
    "GGAL": "/api/v2/BCBA/Titulos/GGAL/Opciones",
    "PAMP": "/api/v2/BCBA/Titulos/PAMP/Opciones",
}


# Clase para menejo de API iol
class Iol:

    def __init__(self, user, password):
        self.hora_actual = datetime.now()
        self.user = user
        self.password = password

    # Gestion de API tokens
    #
    # :param      type:     Tipo de gestion
    # :type       type:     { string }
    # :param      url:      Url para solicitar la operacion
    # :type       url:      { type_description }
    def gestionar(self):

        url = url_base + url_token

        if hasattr(self, 'bearer_time'):

            diferencia = (datetime.now() - self.bearer_time)

            if int(diferencia.total_seconds() / 60) < 15:
                pass
                return 0

            else:
                print("Bearer vencido. Gestionando bearer refresh...")

                # Se convierten en json.
                payload = "\"refresh_token\": \"" + self.refresh_token + \
                    "\", \"grant_type\": \"refresh_token\""

        else:
            print("Gestionando bearer...")

            payload = '\"username\": \"' + self.user + \
                '\", \"password\": \"' + self.password + \
                '\", \"grant_type\": \"password\"'

        # Se convierten en json.
        payload = "{" + payload + "}"

        valor = json.loads(payload)

        # Se hace peticion de bearer token a IOL.
        req = requests.post(url, data=valor)

        # Interpretamos respuesta y guardamos los resultados.
        if req.status_code == 200:
            json_obj = json.loads(req.text)

            self.bearer = json_obj['access_token']
            self.refresh_token = json_obj['refresh_token']
            self.bearer_time = datetime.now()
            return 0
        elif req.status_code == 401:
            err = "Invalid user or password."
            raise NoAuthException(err)
        else:
            err = "Error: " + str(req.status_code)

        raise NoDataException(err)

    # Funcion: Descargar()
    #
    # Parametros:
    # panelGeneralAcciones  -> Obtenemos cotizaciones de panel general de
    #                          acciones.
    # panelGeneralBonos     -> Obtenemos cotizaciones de panel general de
    #                          bonos.
    # opciones              -> Obtenemos cotizaciones de las distintas bases
    #                          de opciones de un subyacente x.

    def descargar(self, solicitud, activo=None):

        # Verifica bearer token
        self.gestionar()

        print("Obteniendo: ", solicitud)
        print("Sobre: ", activo)

        # Chequeamos que queremos obtener
        if solicitud == "panelGeneralAcciones":
            url = url_base + url_cot_panel_acciones
        elif solicitud == "panelGeneralBonos":
            url = url_base + url_cot_panel_bonos
        elif solicitud == "opciones":
            url = url_base + url_cot_opciones[activo.upper()]

        req = requests.get(
            url,
            headers={"Authorization": "Bearer " + self.bearer})

        return json.loads(req.text)

    # Descarga de ultima cotizacion
    # :param      mercado:  Mercado donde opera el titulo
    # :type       mercado:  str { bcba/nyse/nasdaq }
    # :param      titulo:   Titulo a consultar
    # :type       titulo:   str
    # :returns:   Json con 'ultimoPrecio', 'variacion', 'apertura', 'maximo',
    #             'minimo', 'fechaHora', 'tendencia', 'cierreAnterior',
    #             'montoOperado', 'volumenNominal', 'precioPromedio', 'moneda',
    #             'precioAjuste', 'interesesAbiertos', 'puntas',
    #             'cantidadOperaciones
    # :rtype:     json object
    def price_to_json(self, mercado='bcba', simbolo=None):

        # Verifica bearer token
        self.gestionar()

        url = url_base + "api/v2/" +\
            mercado + "/Titulos/" + simbolo + "/Cotizacion"
        # print(url)

        req = requests.get(
            url,
            headers={"Authorization": "Bearer " + self.bearer})

        # Interpretamos respuesta y guardamos los resultados.
        if req.status_code == 200:
            return json.loads(req.text)
        elif req.status_code == 401:
            err = "Invalid user or password."
            raise NoAuthException(err)
        else:
            err = "Error: " + str(req.status_code)

        raise NoDataException(err)

    # Descarga de valores temporales para periodo particular
    # :param      mercado:  Mercado
    # :type       mercado:  str
    # :param      titulo:   Titulo
    # :type       titulo:   str
    # :returns:   Cotizacion historica del periodo especificado para el titulo
    # :rtype:     Json_object
    def hist_price_to_json(self, mercado='bcba', simbolo=None,
                           desde=None, hasta=None):

        # Verifica bearer token
        self.gestionar()

        url = url_base + "api/v2/" + mercado + "/Titulos/" + simbolo +\
            "/Cotizacion/seriehistorica/" + desde + "/" + hasta + "/ajustada"
        req = requests.get(
            url,
            headers={"Authorization": "Bearer " + self.bearer})
        if req.status_code == 200:
            return json.loads(req.text)
        else:
            print("ERR -", req.status_code, req.text)
            return False
