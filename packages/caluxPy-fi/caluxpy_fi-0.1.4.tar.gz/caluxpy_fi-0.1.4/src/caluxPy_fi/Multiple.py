import pandas as pd, time, os, logging, sys
from pathlib import Path
#sys.path.append(str(Path(__file__).resolve().parent.parent))
from caluxPy_fi.Calculador import Calculador

class Multiple:

    def __init__(self, data, lang = 'eng'):

        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), 'cMult'), mode = 'w', encoding = 'utf-8')
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)
        #consoleHandler = logging.StreamHandler()
        #consoleHandler.setFormatter(logFormatter)
        #logger.addHandler(consoleHandler)
    
        self.tiempo_inicio_calculo = time.perf_counter()
        self.data = data
        self.mResults = []
        i = 0
        while i < len(data):
            for key, values in data[i].items():
                setattr(self, key[2:], values)
            
            fecha_liquidacion = self.settlementDate if lang == 'eng' else self.fecha_liquidacion if lang == 'esp' else ''
            fecha_emision = self.issuanceDate if lang == 'eng' else self.fecha_emision if lang == 'esp' else ''
            fecha_vencimiento = self.maturityDate if lang == 'eng' else self.fecha_vencimiento if lang == 'esp' else ''
            cupon = self.coupon if lang == 'eng' else self.cupon if lang == 'esp' else ''
            rendimiento = self.ytm if lang == 'eng' else self.rendimiento if lang == 'esp' else ''
            monto = self.facialValue if lang == 'eng' else self.monto if lang == 'esp' else ''
            emisor = self.issuer if lang == 'eng' else self.emisor if lang == 'esp' else ''
            metodologia = self.methodology if lang == 'eng' else self.metodologia if lang == 'esp' else ''
            periodicidad = self.periodicity if lang == 'eng' else self.periodicidad if lang == 'esp' else ''
            tipo_pago = self.paymentType if lang == 'eng' else self.tipo_pago if lang == 'esp' else ''
            tipo_cupones = self.couponType if lang == 'eng' else self.tipo_cupones if lang == 'esp' else ''
            forward_date = self.forwardDate if lang == 'eng' else self.forward_date if lang == 'esp' else ''
            fecha_inicio_amortizaciones = self.amotizationDate if lang == 'eng' else self.fecha_inicio_amortizaciones if lang == 'esp' else ''
            cantidad_amortizaciones = self.amortizationTimes if lang == 'eng' else self.cantidad_amortizaciones if lang == 'esp' else ''
            periodicidad_amortizaciones = self.amortizationPeriodicity if lang == 'eng' else self.periodicidad_amortizaciones if lang == 'esp' else ''
            porcentaje_amortizable = self.amortizablePercentage if lang == 'eng' else self.porcentaje_amortizable if lang == 'esp' else ''
            
            try:
                margen_repos = self.margin if lang == 'eng' else self.margen if lang == 'esp' else ''
            except Exception:
                margen_repos = None
            try:
                tasa_repos = self.interestRate if lang == 'eng' else self.tasaInteres if lang == 'esp' else ''
            except Exception:
                tasa_repos = None
            try:
                plazo_repos = self.repoTenure if lang == 'eng' else self.plazoRepos if lang == 'esp' else ''
            except Exception:
                plazo_repos = None

            calculador_results = Calculador(fecha_liquidacion = fecha_liquidacion, 
                                            fecha_emision = fecha_emision, 
                                            fecha_vencimiento = fecha_vencimiento, 
                                            cupon = cupon, 
                                            rendimiento = rendimiento, 
                                            monto = monto, 
                                            emisor = emisor, 
                                            metodologia = metodologia, 
                                            periodicidad = periodicidad, 
                                            tipo_pago = tipo_pago, 
                                            tipo_cupones = tipo_cupones, 
                                            forward_date = forward_date, 
                                            fecha_inicio_amortizaciones = fecha_inicio_amortizaciones, 
                                            cantidad_amortizaciones = cantidad_amortizaciones, 
                                            periodicidad_amortizaciones = periodicidad_amortizaciones, 
                                            porcentaje_amortizable = porcentaje_amortizable, 
                                            date_format = '%Y-%m-%d', 
                                            multiple = True,
                                            margen_repos = margen_repos,
                                            tasa_repos = tasa_repos,
                                            plazo_repos = plazo_repos).get_results()
            #calculador_results['Order'] = i + 1
            self.mResults.append(calculador_results)
            logger.info(f'Calculados - {i + 1} de {len(data)}')
            i += 1

        self.df_resultados_multiples = pd.DataFrame(self.mResults)
        self.tiempo_final_calculo = time.perf_counter()
        self.tiempo_calculo = self.tiempo_final_calculo - self.tiempo_inicio_calculo
        logger.info(f'{self.tiempo_calculo} segs')

        logger.removeHandler(fileHandler)
        fileHandler.close()
        #logging.shutdown()

    def get_results(self):

        return self.mResults

    def get_results_df(self):

        return self.df_resultados_multiples
    
    def processTime(self):

        return self.tiempo_calculo