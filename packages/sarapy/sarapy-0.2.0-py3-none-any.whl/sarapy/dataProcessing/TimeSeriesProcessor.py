"""
La clase TimeSeriesProcessor se encarga de obtener y gestionar los datos referentes a las series temporales del Sarapico.

- Versión de metadatos utilizada: Revision 9
- Apuntes de desarrollo: https://docs.google.com/document/d/1kVH-DS6d572AObMCW5oRBIkn357C0T0XXZbq6C2KuW8/edit#heading=h.qfw1towwg3ot

- Autor: BALDEZZARI Lucas
- Creación: 8 de enero de 2024
"""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import warnings
from datetime import datetime


class TimeSeriesProcessor(BaseEstimator, TransformerMixin):
    """
    La clase TimeSeriesProcessor se encarga de obtener y gestionar los datos referentes a las series temporales del Sarapico.
    
    El objetivo de esta clase es poder obtener los tiempos de Operación, Caminata y Pico abierto correspondiente a las operaciones.

    - Versión de metadatos utilizada: Revision 9
    - Apuntes de desarrollo: https://docs.google.com/document/d/1kVH-DS6d572AObMCW5oRBIkn357C0T0XXZbq6C2KuW8/edit#heading=h.qfw1towwg3ot

    - Autor: BALDEZZARI Lucas
    - Creación: 8 de enero de 2024
    - Version: 0.1.0
    """
    
    def __init__(self):
        """Inicializa la clase TimeSeriesProcessor."""
        
        self.is_fitted = False
        
    def fit(self, X: np.array, y=None)-> np.array:
        """fittea el objeto
        
        - X: array con los datos de timestamp (fecha y hora) en formato Unix timestamp y tiempo de pico abierto. Shape (n, 2). Los datos de Unix timestamp están en segundos.
        
        Returns:
            self: objeto fitteado
        """

        ##asserteamos que X sea un np.array
        assert isinstance(X, np.ndarray), "X debe ser un np.array"
        ##asserteamos que X tenga dos columnas
        assert X.ndim == 2, "X debe ser de la forma (n, 2)"
        ##asserteamos que X no tenga valores nulos
        assert not np.isnan(X).any(), "X no debe tener valores nulos"
        ##chequeamos que X tenga una sola fila, si es así, enviamos un warning y agregamos una fila copiando la única fila que tiene
        if X.shape[0] == 1:
            warnings.warn("X tiene una sola fila, se agregará una fila copiando la única fila que tiene")
            X = np.vstack((X, X))
            
        ##calculamos la diferencia entre los timestamps. La forma de calcular estos tiempos se enecuentra en los apuntes de identificación "Intervalos de tiempo" del siguiente link:
        #https://drive.google.com/file/d/1I7a_AHsGI2n5gPBOBT_oRmsqm-xt9kI9/view?usp=sharing
        
        self._deltaO = np.diff(X[:,0]) #deltaO = Ttiempo operación siguiente - Ttiempo operación actual
        ##agrego un 0 al principio de la serie
        # self._deltaO = np.hstack((0, self._deltaO))
        self._deltaP = X[:,1][1:]
        self._deltaC = self._deltaO - self._deltaP
        ##hago cero el primer vlaor de deltaC
        
        self.is_fitted = True
    
    def transform(self, X: np.array ):
        """Genera un array con los tiempos de operación, caminata y pico abierto.
        
        - X: array con los datos de timestamp (fecha y hora) en formato Unix timestamp y tiempo de pico abierto. Shape (n, 2). Los datos de Unix timestamp están en segundos.
        
        Returns:
            np.array: array con los tiempos de operación, caminata y pico abierto. Shape (n, 3).
        """
        
        if not self.is_fitted:
            raise RuntimeError("El modelo no ha sido fitteado.")
        
        return np.hstack((self._deltaO.reshape(-1, 1), self._deltaC.reshape(-1, 1), self._deltaP.reshape(-1, 1))).round(2)
    
    def fit_transform(self, X: np.array, y=None):
        """fittea el objeto y genera un array con los tiempos de operación, caminata y pico abierto.
        
        - X: array con los datos de timestamp (fecha y hora) en formato Unix timestamp y tiempo de pico abierto. Shape (n, 2). Los datos de Unix timestamp están en segundos.
        
        Returns:
            np.array: array con los tiempos de operación, caminata y pico abierto. Shape (n, 3).
        """
        
        self.fit(X)
        return self.transform(X)
    
    @property
    def deltaO(self):
        """Devuelve el tiempo de operación."""
        return self._deltaO
    
    @property
    def deltaC(self):
        """Devuelve el tiempo de caminata."""
        return self._deltaC
    
    @property
    def deltaP(self):
        """Devuelve el tiempo de pico abierto."""
        return self._deltaP
    
if __name__ == "__main__":
    timestamps = np.array([1697724423, 1697724428, 1697724430, 1697724433])
    tlm_data = np.array(["0010001000001100110000001100001000000000000000001111111000110000",
                         "0010001000001100110000101100000000000000000000001111111000110000",
                         "0010001000001100101100101100000000000000000000001111111000110000",
                         "0010001000001100101100001100000000000000000000001111111000110000"])
    
    from sarapy.dataProcessing import TLMSensorDataExtractor
    tlm_extractor = TLMSensorDataExtractor()
    tlm_extractor.fit(tlm_data)
    
    deltaPicos = tlm_extractor.TIMEAC

    tmsp = TimeSeriesProcessor()
    
    #creamos un array con los timestamps y los tiempos de pico abierto de la forma (n, 2)
    X = np.hstack((timestamps.reshape(-1, 1), deltaPicos.reshape(-1, 1)))
    tmsp.fit(X)
    tmsp.transform(X)
    tmsp.fit_transform(X)
    
    ### PROBAMOS QUÉ SUCEDE SI TENEMOS UNA SOLA FILA
    tlm_data2 = np.array(["0010001000001100110000001100001000000000000000001111111000110000"])
    timestamps2 = np.array([1697724423])
    
    tmsp2 = TimeSeriesProcessor() 
    tlm_extractor2 = TLMSensorDataExtractor()
    
    tlm_extractor2.fit(tlm_data2)
    
    X2 = np.hstack((timestamps2.reshape(-1, 1), tlm_extractor2.TIMEAC.reshape(-1, 1)))
    
    tmsp2.fit(X2)
    tmsp2.transform(X2)