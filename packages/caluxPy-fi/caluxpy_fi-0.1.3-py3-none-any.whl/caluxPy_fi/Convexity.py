import numpy as np, pandas as pd, matplotlib.pyplot as plt, logging, os
from pathlib import Path
import sys
#sys.path.append(str(Path(__file__).resolve().parent.parent))
from caluxPy_fi.Calculador import Calculador

class Convexity(Calculador):

    def __init__(self, fecha_liquidacion, fecha_emision, fecha_vencimiento, cupon, rendimiento, monto, emisor, metodologia, periodicidad, tipo_pago, tipo_cupones, 
                 forward_date, fecha_inicio_amortizaciones, cantidad_amortizaciones, periodicidad_amortizaciones, porcentaje_amortizable, date_format = '', multiple = False, pbs = 100):
        super().__init__(fecha_liquidacion, fecha_emision, fecha_vencimiento, cupon, rendimiento, monto, emisor, metodologia, periodicidad, tipo_pago, tipo_cupones, 
                         forward_date, fecha_inicio_amortizaciones, cantidad_amortizaciones, periodicidad_amortizaciones, porcentaje_amortizable, date_format = '', multiple = False)

        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), 'convex'), mode = 'w', encoding = 'utf-8')
        fileHandler.setFormatter(logFormatter)
        self.logger.addHandler(fileHandler)

        self.tipo_valoracion = 'convexity'
        self.pbs = pbs

        self.max_gain = 0
        self.max_loss = 0
        self.avg_gain = 0
        self.avg_loss = 0
        self.std_gain = 0
        self.std_loss = 0
        self.chart_data = {}

        self.logger.info(f'Fecha Liquidación -> {fecha_liquidacion}')
        self.logger.info(f'Fecha Emisión -> {fecha_emision}')
        self.logger.info(f'Fecha Vencimiento -> {fecha_vencimiento}')
        self.logger.info(f'Cupón -> {cupon}')
        self.logger.info(f'Rendimiento -> {rendimiento}')
        self.logger.info(f'Monto -> {monto}')
        self.logger.info(f'Emisor -> {emisor}')
        self.logger.info(f'Metodología -> {metodologia}')
        self.logger.info(f'Periodicidad -> {periodicidad}')
        self.logger.info(f'Tipo de Pago -> {tipo_pago}')
        self.logger.info(f'Tipo de Cupones -> {tipo_cupones}')
        self.logger.info(f'Fecha Forward -> {forward_date}')
        self.logger.info(f'Fecha de Inicio de Amortizaciones -> {fecha_inicio_amortizaciones}')
        self.logger.info(f'Cantidad de Amortizaciones -> {cantidad_amortizaciones}')
        self.logger.info(f'Periodicidad de Amortizaciones -> {periodicidad_amortizaciones}')
        self.logger.info(f'Porcentaje Amortizable -> {porcentaje_amortizable}\n--------------------------------------------------------------------------------------------------------------------------------------\n')

        try:
            self.logger.info(f'Cupón Actual -> {self.cupon_actual}')
            self.logger.info(f'Cupón Actual -> {self.cupon_actual}')
            self.logger.info(f'NPER -> {self._nper}')
            self.logger.info(f'w Cupón -> {self.w_cupon}')
            self.logger.info(f'Discrepancia -> {self._discrepancia}')
            self.logger.info(f'Tipo de Cupones -> {self.tipo_cupones}')
            self.logger.info(f'Fecha de Vencimiento -> {self.fecha_vencimiento}')
            self.logger.info(f'Vencimiento Esperado -> {self.vencimiento_esperado}')
            self.logger.info(f'Días Cupón -> {self.dias_cupon}')
            self.logger.info(f'Rendimiento -> {self.rendimiento}')
            self.logger.info(f'Periodicidad -> {self.periodicidad}')
            self.logger.info(f'Flujo Cupón -> {self.flujo_cupon}')
            self.logger.info(f'Tipo de Pago -> {self.tipo_pago}')
            self.logger.info(f'Emisor -> {self.emisor}')
            self.logger.info(f'Valor Nocional -> {self.valor_nocional}')
            self.logger.info(f'Cupón Corrido -> {self.cupon_corrido}')
            self.logger.info(f'Puntos Básicos -> {pbs}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
            
            self.tipoValoracionConvexidad(self.cupon_actual, self._nper, self.w_cupon, self._discrepancia, self.tipo_cupones, self.fecha_vencimiento, self.vencimiento_esperado, 
                                          self.dias_cupon, self.rendimiento, self.periodicidad, self.flujo_cupon, self.tipo_pago, self.emisor, self.valor_nocional, self.cupon_corrido, 
                                          pbs)
            self.logger.info('SUCCESS: Cálculo realizado..')
        except Exception as e:
            self.logger.exception(e)


        self.logger.removeHandler(fileHandler)
        fileHandler.close()

    def tipoValoracionConvexidad(self, cupon_actual, nper, w_cupon, discrepancia, tipo_cupones, fecha_vencimiento, vencimiento_esperado, dias_cupon, rendimiento, periodicidad, 
                                 flujo_cupon, tipo_pago, emisor, valor_nocional, cupon_corrido, pbs):
        
        listPBS = []
        listRendimientos = []
        listPrecioLimpio = []
        listPrecioSucio = []
        listDuracion = []
        listDuracionMod = []
        listDV01 = []
        listConvexity= []
        listDuracion2 = []
        dicDV01 = {}
        
        y = -int(pbs)
        while y <= int(pbs):
            rendimiento2 = rendimiento + (y / 10000)
            resValoracion = self.tipoValoracionNormal(cupon_actual, nper, w_cupon, discrepancia, tipo_cupones, fecha_vencimiento, vencimiento_esperado, dias_cupon, rendimiento2, periodicidad, flujo_cupon, tipo_pago, emisor, valor_nocional, cupon_corrido)
            #return valor_presente_final, precio_sucio, valor_compra, duracion, precio_limpio, duracion_modificada, dv01, convexidad, valor_presente_preliminar
            listPBS.append(y)
            listRendimientos.append(rendimiento2)
            listPrecioLimpio.append(resValoracion[4] * 100)
            listPrecioSucio.append(resValoracion[1] * 100)
            listDuracion.append(resValoracion[3])
            listDuracionMod.append(resValoracion[5])
            dv01 = (resValoracion[5] / 100) * (resValoracion[1]) * (valor_nocional / 100)
            listDV01.append(dv01)
            dicDV01[y] = dv01
            y += 1
        listPBS = np.array(listPBS)
        listRendimientos = np.array(listRendimientos)
        listPrecioLimpio = np.array(listPrecioLimpio)
        listPrecioSucio = np.array(listPrecioSucio)
        listDuracion = np.array(listDuracion)
        listDuracionMod = np.array(listDuracionMod)
        listDV01 = np.array(listDV01)
        self.df_convex = pd.DataFrame({'pbs': listPBS, 'dv01': listDV01})
        self.df_convex['Negative'] = self.df_convex['pbs'] < 0
        max_values_by_category = self.df_convex.groupby('Negative')['dv01'].max()
        avg_values_by_category = self.df_convex.groupby('Negative')['dv01'].mean()
        std_values_by_category = self.df_convex.groupby('Negative')['dv01'].std()

        self.neg_vals = self.df_convex.groupby('Negative')

        self.logger.info(f'{self.df_convex}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')
        self.logger.info(f'Max Values by Category -> {max_values_by_category}')
        self.logger.info(f'Average Values by Category -> {max_values_by_category}')
        self.logger.info(f'Standard Deviations by Category -> {max_values_by_category}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')

        self.max_gain = max_values_by_category[True]
        self.max_loss = max_values_by_category[False]
        self.avg_gain = avg_values_by_category[True]
        self.avg_loss = avg_values_by_category[False]
        self.std_gain = std_values_by_category[True]
        self.std_loss = std_values_by_category[False]

        self.logger.info(f'Max Gain -> {self.max_gain}')
        self.logger.info(f'Max Loss -> {self.max_loss}')
        self.logger.info(f'Average Gain -> {self.avg_gain}')
        self.logger.info(f'Average Loss -> {self.avg_loss}')
        self.logger.info(f'Standard Deviation of Gains -> {self.std_gain}')
        self.logger.info(f'Standard Deviation of Losses -> {self.std_loss}\n\n--------------------------------------------------------------------------------------------------------------------------------------\n')

        i = 0
        while i <= int(pbs):
            if i == 0:
                listConvexity.append(0)
            else:
                listConvexity.append(listConvexity[i - 1] - dicDV01[i])
            i += 1
        i = -1
        while i >= -int(pbs):
            if i == -1:
                listConvexity.append(dicDV01[i])
            else:
                listConvexity.append(listConvexity[-1] + dicDV01[i])
            i -= 1
        listConvexity = np.array(listConvexity)
        listConvexity[::-1].sort()
        i = -int(pbs)
        while i <= int(pbs):
            listDuracion2.append(dicDV01[0] * (0 - i))
            i += 1
        listDuracion2 = np.array(listDuracion2)

        self.chart_data['x'] = listPBS
        self.chart_data['y1'] = listDuracion2
        self.chart_data['y2'] = listConvexity

        x = listPBS
        y1 = listDuracion2
        y2 = listConvexity
        
        plt.figure(figsize=(10,6))
        plt.plot(x,y1)
        plt.plot(x,y2, linestyle='--')
        plt.title("Gráfico de Duración-Convexidad")
        plt.xlabel("Puntos Básicos")
        plt.ylabel("Valores Duración y Convexidad")
        #plt.gcf().canvas.set_window_title('Gráfico')
        #plt.suptitle('Gráfico')
        #plt.show()

    def show_graph(
                  self):
        return plt.show()

    def save_graph(self, filename):
        plt.savefig(filename, bbox_inches = 'tight', dpi = 300)
        plt.close()
    
    def get_results(self):
        results = {'Max Gain': self.max_gain, 'Max Loss': self.max_loss, 'Average Gain': self.avg_gain, 'Average Loss': self.avg_loss, 'Deviations in Gains': self.std_gain, 
                   'Deviations in Losses': self.std_loss}
        return results

    def __str__(self):
        return f'\
Max Gain: {self.max_gain} \n \
Max Loss: {self.max_loss} \n \
Average Gain: {self.avg_gain} \n \
Average Loss: {self.avg_loss} \n \
Deviation in Gains: {self.std_gain} \n \
Deviation in Losses: {self.std_loss}'


