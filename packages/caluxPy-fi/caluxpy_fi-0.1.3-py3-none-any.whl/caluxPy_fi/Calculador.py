import numpy as np, pandas as pd, math, time, os, logging, sys
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from tkinter import messagebox
from pathlib import Path
#sys.path.append(str(Path(__file__).resolve().parent.parent))
from caluxPy_fi.Soporte import Soporte

class Calculador:

    counter = 0
    
    def __init__(self, fecha_liquidacion, fecha_emision, fecha_vencimiento, cupon, rendimiento, monto, emisor, metodologia, periodicidad, tipo_pago, tipo_cupones, 
                 forward_date, fecha_inicio_amortizaciones, cantidad_amortizaciones, periodicidad_amortizaciones, porcentaje_amortizable, 
                 margen_repos = '', tasa_repos = '', plazo_repos = '', date_format = '', multiple = False):
        
        #region ---> Logger

        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), 'calculador'), mode = 'w', encoding = 'utf-8')
        fileHandler.setFormatter(logFormatter)
        self.logger.addHandler(fileHandler)
        #consoleHandler = logging.StreamHandler()
        #consoleHandler.setFormatter(logFormatter)
        #self.logger.addHandler(consoleHandler)

        #endregion ---> Logger
        
        Calculador.counter += 1
        self.logger.info(f'Iniciando cálculo de título: {Calculador.counter}')
        self.multiple = multiple
        self.resultados = {}
        self.tipo_valor = {}

        self.tipo_valoracion = 'normal'
        self._tiempo_inicio_calculo = time.perf_counter()

         #region ---> Tratamiento de las Fechas
        
        if date_format == '': 
            self._date_format = '%Y-%m-%d'
        else:
            self._date_format = date_format

        self.fecha_emision = fecha_emision
        try:
            if type(self.fecha_emision) == str: self.fecha_emision = datetime.strptime(fecha_emision, self._date_format).date()
        except ValueError as e:
            self.logger.error(e)
        
        self.fecha_vencimiento = fecha_vencimiento
        try:
            if type(self.fecha_vencimiento) == str: self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, self._date_format).date()
        except ValueError as e:
            self.logger.error(e)
        
        self.fecha_liquidacion = fecha_liquidacion
        try:
            if type(self.fecha_liquidacion) == str: self.fecha_liquidacion = datetime.strptime(fecha_liquidacion, self._date_format).date()
        except ValueError as e:
            self.logger.error(e)
        self.logger.info(f'Fecha de Liquidación -> {self.fecha_liquidacion} Tipo -> {type(self.fecha_liquidacion)}')
        self.logger.info(f'Fecha de Vencimiento -> {self.fecha_vencimiento} Tipo -> {type(self.fecha_vencimiento)}')
        
        #endregion ---> Tratamiento de las Fechas
        
        try:
            if self.fecha_vencimiento >= self.fecha_liquidacion:
                self.cupon = Soporte.conversion_tasas(cupon)
                self.rendimiento = Soporte.conversion_tasas(rendimiento)
                self.tipo_pago = tipo_pago
                self.metodologia = metodologia

                #De esto dependen muchas cosas
                self.periodicidad = Soporte.conversion_periodicidad(periodicidad)
                self.a_vencimiento = True if periodicidad == 'vencimiento' else False

                self.emisor = emisor
                self.tipo_cupones = tipo_cupones
                self.monto = float(monto)
                self.años = Soporte.calculo_años(self.fecha_emision, self.fecha_vencimiento)
                self.forward_date = forward_date

                if self.tipo_cupones == 'normal':
                    self.forward_date = None
                elif tipo_cupones == 'fw1' or tipo_cupones == 'fw2':
                    self.forward_date = datetime(self.fecha_vencimiento.year - math.trunc(self.años),self.fecha_vencimiento.month,self.fecha_vencimiento.day,0,0).date()
                else:
                    if forward_date != '': 
                        try:
                            if type(self.forward_date) == str: self.forward_date = datetime.strptime(fecha_liquidacion,self._date_format).date()
                        except ValueError as e:
                            self.logger.error(e)    
                    else:
                        self.forward_date = None

                self.fecha_inicio_amortizaciones = fecha_inicio_amortizaciones
                #Si es bullet para evitar cualquier incongruencia se elimina cualquier atributo de amortizado
                if self.tipo_pago == 'bullet':
                    self.fecha_inicio_amortizaciones = None
                    self.cantidad_amortizaciones = None
                    self.periodicidad_amortizaciones = None
                    self.porcentaje_amortizable = None
                else:
                    #Si no es bullet se dejan todas las características que se especificaron y se verifican que cumplan los parámetros
                    if fecha_inicio_amortizaciones != '':
                        try:
                            if type(self.fecha_inicio_amortizaciones) == str: self.fecha_inicio_amortizaciones = datetime.strptime(fecha_inicio_amortizaciones,self._date_format).date()
                        except ValueError as e:
                            self.logger.error(e)
                        else: self.fecha_inicio_amortizaciones = fecha_inicio_amortizaciones
                    if cantidad_amortizaciones != '':
                        self.cantidad_amortizaciones = int(cantidad_amortizaciones)
                    else:
                        self.cantidad_amortizaciones = None
                    if periodicidad_amortizaciones != '':
                        self.periodicidad_amortizaciones = Soporte.conversion_periodicidad_amort(periodicidad_amortizaciones)
                    else:
                        self.periodicidad_amortizaciones = None
                    if porcentaje_amortizable != '':
                        self.porcentaje_amortizable = Soporte.conversion_tasas(porcentaje_amortizable)
                    else:
                        self.porcentaje_amortizable = None

                self.plazo_residual = self.fecha_vencimiento - self.fecha_liquidacion #plazo residual
                self._total_cupones = self.periodicidad * self.años #cantidad total de cupones del instrumento
                #Este debajo es el vencimiento esperado que tendría el instrumento
                self.vencimiento_esperado = self.VencimientoEsperado(total_cupones = self._total_cupones, 
                                                                     fecha_vencimiento = self.fecha_vencimiento, 
                                                                     fecha_emision = self.fecha_emision, 
                                                                     años = self.años)
                
                #Determinación del nper, esta parte determina la cantidad de flujos, si es a vencimiento será 1 sólo flujo
                self._nper = math.trunc(Soporte.ln_nper(self.fecha_emision, self.fecha_vencimiento, self.periodicidad, self.tipo_cupones, self.a_vencimiento)) - 1

                #La periodicidad numérica del pago de cupones, si es a vencimiento siempre será 1 igual que anual, pero no debe de ser 0
                self._per = (12 / self.periodicidad) if self.a_vencimiento == False else 1 

                #Esta es la determinación de la existencia de una discrepancia entre la fecha de vencimiento y la de vencimiento esperado
                if (self.fecha_vencimiento.day - self.fecha_emision.day) != 0 or self.fecha_vencimiento != self.vencimiento_esperado:
                    self._discrepancia = "Si"
                else:
                    self._discrepancia = "No"

                #Determinación de las fechas de pago de cupones
                self.fechas_cupones = np.array(self.fechasCupones(nper = self._nper, 
                                                                  per = self._per, 
                                                                  fecha_emision = self.fecha_emision, 
                                                                  fecha_vencimiento = self.fecha_vencimiento, 
                                                                  tipo_cupones = self.tipo_cupones, 
                                                                  forward_date = self.forward_date,
                                                                  a_vencimiento = self.a_vencimiento))
                self.logger.info(self.fechas_cupones)
                #Itera en la lista de las fechas de cupones buscando cuál es mayor a la fecha de liquidación y la primera que sea mayor es el cupón vigente
                self.cupon_actual = (self.fechas_cupones > self.fecha_liquidacion).nonzero()[0][0]
                self.dias_cupon, self.no_flujo = self.diasCupon_noFlujo(nper = self._nper, 
                                                                        fechas_cupones = self.fechas_cupones, 
                                                                        fecha_emision = self.fecha_emision)
                self.dias_acumulados = self.diasAcumulados(metodologia = self.metodologia, 
                                                        fecha_emision = self.fecha_emision, 
                                                        fecha_liq = self.fecha_liquidacion, 
                                                        cupon_actual = self.cupon_actual, 
                                                        fechas_cupones = self.fechas_cupones)
                self.dias_al_vencimiento = np.array(self.diasAlVencimiento(nper = self._nper, 
                                                                        dias_cupon = self.dias_cupon))
                self.base_de_calculo = np.array(self.baseDeCalculo(metodologia = self.metodologia, 
                                                                nper = self._nper, 
                                                                fechas_cupones = self.fechas_cupones))
                self.w_cupon = self.wCupon(metodologia = self.metodologia, 
                                        dias_cupon = self.dias_cupon, 
                                        cupon_actual = self.cupon_actual, 
                                        dias_acumulados = self.dias_acumulados, 
                                        periodicidad = self.periodicidad)
                if self.tipo_pago == 'amortized' or self.tipo_pago == 'a' or self.tipo_pago == '2' or self.tipo_pago == 'pik' or self.tipo_pago == 'p' or self.tipo_pago == '3':
                    self.valor_nocional, self.monto_amortizacion, self.monto_ajustado, self.resultados_fechas = self.modulo_amortizacion (self.tipo_pago, self.fecha_inicio_amortizaciones, self.fecha_vencimiento, 
                                                                                                                                        self.cantidad_amortizaciones, self.periodicidad_amortizaciones, 
                                                                                                                                        self.porcentaje_amortizable, self.fecha_liquidacion, self.monto, 
                                                                                                                                        self.fechas_cupones, self.cupon_actual, self._nper, self.periodicidad)
                else: self.valor_nocional = float(self.monto)
                self.cupon_corrido = self.cuponCorrido(metodologia = self.metodologia, 
                                                    valor_nocional = self.valor_nocional, 
                                                    cupon = self.cupon, 
                                                    periodicidad = self.periodicidad, 
                                                    dias_cupon = self.dias_cupon, 
                                                    cupon_actual = self.cupon_actual, 
                                                    dias_acumulados = self.dias_acumulados, 
                                                    base_de_calculo = self.base_de_calculo)
                self.flujo_cupon = []
                self.resultados = {}
                self.logger.info('SUCCESS: Calculadas las variables necesarias! Procediendo a calcular los flujos..')
                if (self.tipo_pago == 'bullet' or self.tipo_pago == 'b' or self.tipo_pago == '1'):
                    self.flujo_cupon = np.array(self.tipoPagoBullet(monto = self.monto, 
                                                                    cupon = self.cupon, 
                                                                    periodicidad = self.periodicidad, 
                                                                    nper = self._nper, 
                                                                    per = self._per, 
                                                                    metodologia = self.metodologia, 
                                                                    base_de_calculo = self.base_de_calculo, 
                                                                    dias_cupon = self.dias_cupon, 
                                                                    cupon_actual = self.cupon_actual))
                elif (self.tipo_pago == 'amortized' or self.tipo_pago == 'a' or self.tipo_pago == '2'):
                    self.flujo_cupon = np.array(self.tipoPagoAmortizado(metodologia = self.metodologia, 
                                                                        cupon_actual = self.cupon_actual, 
                                                                        resultados_fechas = self.resultados_fechas, 
                                                                        monto_ajustado = self.monto_ajustado, 
                                                                        cupon = self.cupon, 
                                                                        periodicidad = self.periodicidad, 
                                                                        monto_amortizacion = self.monto_amortizacion, 
                                                                        base_de_calculo = self.base_de_calculo, 
                                                                        dias_cupon = self.dias_cupon, 
                                                                        porcentaje_amortizable = self.porcentaje_amortizable, 
                                                                        nper = self._nper, 
                                                                        per = self._per))
                elif (self.tipo_pago == 'pik' or self.tipo_pago == 'p' or self.tipo_pago == '3'):
                    self.flujo_cupon = np.array(self.tipoPagoPIK(metodologia = self.metodologia, 
                                                                cupon_actual = self.cupon_actual, 
                                                                resultados_fechas = self.resultados_fechas, 
                                                                valor_nocional = self.valor_nocional, 
                                                                cupon = self.cupon, 
                                                                periodicidad = self.periodicidad, 
                                                                base_de_calculo = self.base_de_calculo, 
                                                                dias_cupon = self.dias_cupon, 
                                                                nper = self._nper, 
                                                                per = self._per))
                self.logger.info('SUCCESS: Flujos calculados! Procediendo a calcular el valor presente..')
                resValoracion = self.tipoValoracionNormal(cupon_actual = self.cupon_actual, 
                                                        nper = self._nper, 
                                                        w_cupon = self.w_cupon, 
                                                        discrepancia = self._discrepancia, 
                                                        tipo_cupones = self.tipo_cupones, 
                                                        fecha_vencimiento = self.fecha_vencimiento, 
                                                        vencimiento_esperado = self.vencimiento_esperado, 
                                                        dias_cupon = self.dias_cupon, 
                                                        rendimiento = self.rendimiento, 
                                                        periodicidad = self.periodicidad, 
                                                        flujo_cupon = self.flujo_cupon, 
                                                        tipo_pago = self.tipo_pago, 
                                                        emisor = self.emisor, 
                                                        valor_nocional = self.valor_nocional, 
                                                        cupon_corrido = self.cupon_corrido)
                
                self._tiempo_final_calculo = time.perf_counter()
                self._tiempo_calculo = self._tiempo_final_calculo - self._tiempo_inicio_calculo
                self.logger.info('SUCCESS: Valor Presente calculado! Procediendo a retornar los resultados a la función principal..')
                self.valores_presentes = resValoracion[9]
                #Resultados del Cálculo Normal
                if self.multiple == False:
                    self.resultados['valorPresente'] = resValoracion[0]
                    self.resultados['precio'] = resValoracion[1]
                    self.resultados['valorCompra'] = resValoracion[2]
                    self.resultados['precioLimpio'] = resValoracion[3]
                    self.resultados['duracion'] = resValoracion[4]
                    self.resultados['duracionModificada'] = resValoracion[5] 
                    self.resultados['dv01'] = resValoracion[6]
                    self.resultados['convexidad'] = resValoracion[7]
                    self.resultados['valorPresentePreliminar'] = resValoracion[8]
                    self.resultados['tiempoCalculo'] = self._tiempo_calculo
                elif self.multiple == True:
                    self.resultados['Fecha Vencimiento'] = self.fecha_vencimiento
                    self.resultados['Monto'] = self.monto
                    self.resultados['Rendimiento'] = self.rendimiento
                    self.resultados['Cupón Corrido'] = self.cupon_corrido
                    self.resultados['Valor Presente'] = resValoracion[0]
                    self.resultados['Precio Sucio'] = resValoracion[1]
                    self.resultados['Valor Compra'] = resValoracion[2]
                    self.resultados['Precio Limpio'] = resValoracion[3]
                    self.resultados['Duración'] = resValoracion[4]
                    self.resultados['Duración Modificada'] = resValoracion[5] 
                    self.resultados['DV01'] = resValoracion[6]
                    self.resultados['Convexidad'] = resValoracion[7]
                    self.resultados['Valor Presente Preliminar'] = resValoracion[8]
                    self.resultados['Tiempo de Cálculo'] = self._tiempo_calculo

                #Otras operaciones
                try:
                    self.margen_repos = margen_repos
                    self.tasa_repos = tasa_repos
                    self.plazo_repos = plazo_repos
                    if self.margen_repos != '' and self.tasa_repos != '' and self.plazo_repos != '':
                        resultado_repos = self.Repos(margen = self.margen_repos,
                                                    tasa_repo = self.tasa_repos,
                                                    plazo = self.plazo_repos)
                        self.resultados['valor_de_ida'] = resultado_repos[0]
                        self.resultados['valor_de_vuelta'] = resultado_repos[1]
                except Exception:
                    pass

                self.logger.info('SUCCESS: Resultados retornados! Preparando la visualización de los resultados y pantalla de flujos..')

                valores = {}
                est_flujos_exp = []
                flujos_exp = []
                vpresentes_exp = []
                dias_acumulados_exp = []

                dias = 0
                for i in range(len(self.no_flujo)):
                    dias += self.dias_cupon[i]
                    dias_acumulados_exp.append(dias)
                    if i < self.cupon_actual:
                        est_flujos_exp.append('Vencido')
                        flujos_exp.append(0)
                        vpresentes_exp.append(0)
                    else:
                        est_flujos_exp.append('Vigente')
                        flujos_exp.append(self.flujo_cupon[i - self.cupon_actual])
                        vpresentes_exp.append(self.valores_presentes[i - self.cupon_actual])

                valores['Flujo'] = np.array(self.no_flujo)
                valores['Fecha Cupón'] = np.array(self.fechas_cupones)
                valores['Días Cupón'] = np.array(self.dias_cupon)
                valores['Días Acumulados'] = np.array(dias_acumulados_exp)
                valores['Flujo Cupón'] = np.array(flujos_exp)
                valores['Valor Presente'] = np.array(vpresentes_exp)
                valores['Vigencia'] = np.array(est_flujos_exp)

                self.df_results = pd.DataFrame(valores)
                self.logger.info('SUCCESS: Visualización de resultados preparada! Saliendo de este procedimiento..')
            else:
                if self.multiple == False:
                    self.resultados['valorPresente'] = None
                    self.resultados['precio'] = None
                    self.resultados['valorCompra'] = None
                    self.resultados['precioLimpio'] = None
                    self.resultados['duracion'] = None
                    self.resultados['duracionModificada'] = None 
                    self.resultados['dv01'] = None
                    self.resultados['convexidad'] = None
                    self.resultados['valorPresentePreliminar'] = None
                    self.resultados['tiempoCalculo'] = None
                elif self.multiple == True:
                    Calculador.counter += 1
                    self.resultados['Fecha Vencimiento'] = None
                    self.resultados['Monto'] = None
                    self.resultados['Rendimiento'] = None
                    self.resultados['Cupón Corrido'] = None
                    self.resultados['Valor Presente'] = None
                    self.resultados['Precio Sucio'] = None
                    self.resultados['Valor Compra'] = None
                    self.resultados['Precio Limpio'] = None
                    self.resultados['Duración'] = None
                    self.resultados['Duración Modificada'] = None
                    self.resultados['DV01'] = None
                    self.resultados['Convexidad'] = None
                    self.resultados['Valor Presente Preliminar'] = None
                    self.resultados['Tiempo de Cálculo'] = None
        except Exception as e:
            self.logger.exception(e)
            if self.multiple == False:
                self.resultados['valorPresente'] = None
                self.resultados['precio'] = None
                self.resultados['valorCompra'] = None
                self.resultados['precioLimpio'] = None
                self.resultados['duracion'] = None
                self.resultados['duracionModificada'] = None 
                self.resultados['dv01'] = None
                self.resultados['convexidad'] = None
                self.resultados['valorPresentePreliminar'] = None
                self.resultados['tiempoCalculo'] = None
            elif self.multiple == True:
                Calculador.counter += 1
                self.resultados['Fecha Vencimiento'] = None
                self.resultados['Monto'] = None
                self.resultados['Rendimiento'] = None
                self.resultados['Cupón Corrido'] = None
                self.resultados['Valor Presente'] = None
                self.resultados['Precio Sucio'] = None
                self.resultados['Valor Compra'] = None
                self.resultados['Precio Limpio'] = None
                self.resultados['Duración'] = None
                self.resultados['Duración Modificada'] = None
                self.resultados['DV01'] = None
                self.resultados['Convexidad'] = None
                self.resultados['Valor Presente Preliminar'] = None
                self.resultados['Tiempo de Cálculo'] = None
                self.logger.error('Título Vencido')
            self.logger.error('Proceso cancelado por Error')
        finally:
            self.logger.removeHandler(fileHandler)
            fileHandler.close()
    
    def validacionFechaAmortizacion(self, cupones, fechaAmortizacion, fechaVencimiento, cantidadAmortizaciones, periodicidadAmortizaciones, fechasCupones):
        
        if (fechaAmortizacion in fechasCupones) == False:
            oldDate = fechaAmortizacion
            fechaAmortizacion = Soporte.fechaCercana(cupones, fechaAmortizacion)
            prompt = '\n*ERROR! \nLa fecha de inicio de amortizaciones indicada no existe en los flujos de cupones, el programa procederá a buscar el cupon vigente más cercano.. ' + \
            '\n-Fecha Original: ' + str(oldDate.day) + '/' + str(oldDate.month) + '/' + str(oldDate.year) + \
            '\n-Fecha Nueva: ' + str(fechaAmortizacion.day) + '/' + str(fechaAmortizacion.month) + '/' + str(fechaAmortizacion.year)
            print(prompt , file = self.log)
            messagebox.showwarning('ValueError', prompt)
        fechaTest = fechaAmortizacion + relativedelta(months =+ ((cantidadAmortizaciones - 1) * periodicidadAmortizaciones))
        if fechaTest > fechaVencimiento:
            prompt = '\n*ERROR! \nLa fecha estimada de última amortización supera la fecha de vencimiento!' + \
                 '\n-Fecha de Vencimiento: ' + str(fechaVencimiento.day) + '/' + str(fechaVencimiento.month) + '/' + str(fechaVencimiento.year) + \
                 '\n-Fecha estimada: ' + str(fechaTest.day) + '/' + str(fechaTest.month) + '/' + str(fechaTest.year)
            print(prompt, file = self.log)
            messagebox.showerror('ValueError', prompt)
            return fechaAmortizacion, False
        else: return fechaAmortizacion, True

    def VencimientoEsperado(self, total_cupones, fecha_vencimiento, fecha_emision, años):
        #Determinación del Vencimiento Esperado
        if total_cupones-math.trunc(total_cupones) > 0 or fecha_vencimiento.day != fecha_emision.day:
            vencimiento_esperado = date(fecha_emision.year + math.trunc(años),fecha_emision.month,fecha_emision.day)
        else:
            vencimiento_esperado = fecha_vencimiento
        return vencimiento_esperado

    def fechasCupones(self, nper, per, fecha_emision, fecha_vencimiento, tipo_cupones, forward_date, a_vencimiento = False): #Determinación de Fechas de Pago de Cupones
        fechas_cupones = []
        if a_vencimiento == False:
            i = 0
            while i <= nper:
                if i == 0:
                    if tipo_cupones == 'fw1' or tipo_cupones == '2':
                        fechas_cupones.append((forward_date + relativedelta(months=+per)))
                    elif (tipo_cupones == 'fw2' or tipo_cupones == '3') or (tipo_cupones == 'fw3' or tipo_cupones == '4'):
                            fechas_cupones.append(forward_date)
                    else:
                        fechas_cupones.append((fecha_emision + relativedelta(months=+per)))
                else:
                    if i == nper:
                        fechas_cupones.append(fecha_vencimiento)
                    elif (tipo_cupones == 'fw2' or tipo_cupones == '3') or (tipo_cupones == 'fw3' or tipo_cupones == '4'):
                        fechas_cupones.append((forward_date + relativedelta(months=+per * i)))
                    else:
                        fechas_cupones.append((fecha_emision + relativedelta(months=+per*(1+i))))   
                i += 1
        else:
           fechas_cupones.append(fecha_vencimiento) 
        return fechas_cupones

    def diasCupon_noFlujo(self, nper, fechas_cupones, fecha_emision): #Determinación de los días de vigencia de los cupones y de los números de los flujos
        dias_cupon = []
        no_flujo = []
        i = 0
        while i <= nper:
            no_flujo.append(i)
            if i == 0:
                dias_cupon.append((fechas_cupones[0] - fecha_emision).days)
            else:
                dias_cupon.append((fechas_cupones[i] - fechas_cupones[i - 1]).days)
            i += 1
        return dias_cupon, no_flujo

    def diasAcumulados(self, metodologia, fecha_emision, fecha_liq, cupon_actual, fechas_cupones): #Cálculo de los días acumulados
        if (metodologia != "isma-30-360" and metodologia != '5') and cupon_actual == 0:
            dias_acumulados = (fecha_liq - fecha_emision).days
        elif (metodologia != "isma-30-360" and metodologia != '5') and cupon_actual != 0:
            dias_acumulados = (fecha_liq - fechas_cupones[cupon_actual-1]).days
        elif (metodologia == "isma-30-360" or metodologia == '5') and cupon_actual == 0:
            dias_acumulados = (Soporte.days360(fecha_emision,fecha_liq)).days
        elif (metodologia == "isma-30-360" or metodologia == '5') and cupon_actual != 0:
            dias_acumulados = (Soporte.days360(fechas_cupones[cupon_actual-1],fecha_liq))
        return dias_acumulados

    def wCupon(self, metodologia, dias_cupon, cupon_actual, dias_acumulados, periodicidad): #Cálculo del w Cupón
        if (metodologia == 'isma-30-360' or metodologia == '5'):
            w_cupon = ((360 / periodicidad) - dias_acumulados) / (360 / periodicidad)
        else:
            w_cupon = (dias_cupon[cupon_actual] - dias_acumulados) / dias_cupon[cupon_actual]
        return w_cupon

    def diasAlVencimiento(self, nper, dias_cupon): #Cálculo de los días al vencimiento de cada cupón
        dias_al_vencimiento = []
        i = 0
        while i <= nper:
            if i == 0:
                dias_al_vencimiento.append(dias_cupon[0])
            else:
                dias_al_vencimiento.append(dias_al_vencimiento[i - 1] + dias_cupon[i])
            i += 1 
        return dias_al_vencimiento

    def baseDeCalculo(self, metodologia, nper, fechas_cupones): #Determinación de las Bases de Cálculo
        base_de_calculo = []
        i = 0
        while i <= nper:
            if (metodologia == 'actual/365' or metodologia == '3'):
                base_de_calculo.append(365)
            elif (metodologia == 'actual/360' or metodologia == '4') or (metodologia == 'isma-30-360' or metodologia == '5'):
                base_de_calculo.append(360)
            else:
                base_de_calculo.append((fechas_cupones[i] - (fechas_cupones[i] - relativedelta(months=+12))).days)
            i += 1
        return base_de_calculo

    def modulo_amortizacion(self, tipo_pago, fecha_inicio_amortizaciones, fecha_vencimiento, cantidad_amortizaciones, periodicidad_amortizaciones, porcentaje_amortizable, 
                            fecha_liq, monto, fechas_cupones, cupon_actual, nper, periodicidad): #Ejecución de todo el proceso de amortización y cálculos necesarios para valoración
        #Primero las validaciones
        while True:
            fecha_inicio_amortizaciones, validacion = self.validacionFechaAmortizacion(fechas_cupones, fecha_inicio_amortizaciones, fecha_vencimiento, cantidad_amortizaciones, periodicidad_amortizaciones, fechas_cupones)
            if validacion == False:
                while True:
                    seleccion = input('\nQue desea modificar para solucionar el error? ' + 
                              '\n1-Fecha de Inicio de las Amortizaciones' + 
                              '\n2-Periodicidad de las Amortizaciones' + 
                              '\n3-Cantidad de Amortizaciones' + 
                              '\nRespuesta: ')
                    if seleccion in ['1','2','3']:
                        if seleccion == '1': 
                            fecha_inicio_amortizaciones = self.inputFecha('Fecha de Inicio de Amotizaciones')
                            break
                        elif seleccion == '2':
                            while True:
                                periodicidad_amortizaciones = self.conversion_periodicidad_amort(self.inputPrompt('periodicidad de amortizaciones', ['mensual','m','1','bimensual','b','2','trimestral','t','3','cuatrimestral','c','4','semestral','s','5','anual','a','6'], 3))
                                if (periodicidad_amortizaciones == 12 / periodicidad) or (periodicidad_amortizaciones == (12 / periodicidad) * 2):
                                    break
                                else:
                                    prompt = 'Valor inválido: la periodicidad de las amortizaciones debe de ser igual o el doble de la periodicidad de pagos de cupones..'
                                    print(prompt, file = self.log)
                                    messagebox.showerror('ValueError', prompt)
                                    periodicidad_amortizaciones, 12 / periodicidad
                                    continue
                            break
                        elif seleccion == '3':
                            cantidad_amortizaciones = self.inputIntegers()
                            break
                    else:
                        prompt = 'Opción inválida, inténtelo de nuevo..'
                        print(prompt, file = self.log)
                        messagebox.showerror('InputError', prompt)
                        continue
                continue
            else: break

        #Determinación de las Fechas en las que se Amortiza el Instrumento
        monto_amortizacion = 0
        fechas_amortizacion = []
        resultados_fechas = []
        if (tipo_pago == 'amortized' or tipo_pago == 'a' or tipo_pago == '2') or (tipo_pago == 'pik' or tipo_pago == 'p' or tipo_pago == '3'):
            conteo_fechas = 0
            if fecha_inicio_amortizaciones < fecha_liq:
                conteo_fechas = 1
            i = 0
            while i <= int(cantidad_amortizaciones) - 1:
                if i == 0:
                    fechas_amortizacion.append(fecha_inicio_amortizaciones)
                else:
                    fechas_amortizacion.append(fechas_amortizacion[i - 1] + relativedelta(months=+periodicidad_amortizaciones))
                    if fechas_amortizacion[i] <= fecha_liq:
                        conteo_fechas += 1
                i += 1
            fechas_amortizacion = np.array(fechas_amortizacion)
            i = 0
            posicion = 0
            while i <= np.count_nonzero(fechas_amortizacion) - 1:
                posicion = np.where(fechas_cupones == fechas_amortizacion[i])[0]
                if posicion != 0: resultados_fechas.append(posicion)
                i += 1
            monto_amortizacion = (monto * porcentaje_amortizable) / cantidad_amortizaciones
            resultados_fechas = np.array(resultados_fechas)
        #Calculando el Valor Nocional y los Montos Ajustados
        amortizado_previo = 0
        valor_nocional = 0
        monto_ajustado = []
        if (tipo_pago == 'amortized' or tipo_pago == 'a' or tipo_pago == '2'):
            if cantidad_amortizaciones > 0:
                if np.count_nonzero(resultados_fechas) != conteo_fechas:
                    amortizado_previo = monto_amortizacion * conteo_fechas
                valor_nocional = monto - amortizado_previo
            conteo = 0
            i = cupon_actual
            while i <= nper:
                if np.where(resultados_fechas == i)[0].size > 0:
                    conteo += 1
                    if conteo <= (cantidad_amortizaciones - (cantidad_amortizaciones - np.count_nonzero(resultados_fechas))):
                        monto_ajustado.append(valor_nocional - (monto_amortizacion * (conteo - 1)))
                    else:
                        monto_ajustado.append(monto)
                else:
                    monto_ajustado.append(valor_nocional - (monto_amortizacion * conteo))
                i += 1
            monto_ajustado = np.array(monto_ajustado)

        return valor_nocional, monto_amortizacion, monto_ajustado, resultados_fechas

    def cuponCorrido(self, metodologia, valor_nocional, cupon, periodicidad, dias_cupon, cupon_actual, dias_acumulados, base_de_calculo): #Cálculo del Cupón Corrido
        cupon_corrido = 0
        if (metodologia == 'icma' or metodologia == '1'):
            cupon_corrido = (valor_nocional * cupon / periodicidad) / dias_cupon[cupon_actual] * dias_acumulados
        elif (metodologia == 'actual/actual' or metodologia == '2') or (metodologia == 'actual/365' or metodologia == '3') or (metodologia == 'actual/360' or metodologia == '4'):
            cupon_corrido = valor_nocional * cupon / base_de_calculo[cupon_actual] * dias_acumulados
        elif (metodologia == 'isma-30-360' or metodologia == '5'):
            cupon_corrido = valor_nocional * cupon / 360 * dias_acumulados
        return cupon_corrido

    def tipoPagoBullet(self, monto, cupon, periodicidad, nper, per, metodologia, base_de_calculo, dias_cupon, cupon_actual):
        flujo_cupon = []
        i = cupon_actual
        while i <= nper:
            if (metodologia == 'icma' or metodologia == '1'):
                flujo_cupon.append((monto * cupon) / periodicidad)
            elif (metodologia == 'isma-30-360' or metodologia == '5'):
                flujo_cupon.append((monto * cupon) / 12 * per)
            elif (metodologia == 'actual/actual' or metodologia == '2') or (metodologia == 'actual/365' or metodologia == '3') or (metodologia == 'actual/360' or metodologia == '4'):
                flujo_cupon.append(monto * cupon / base_de_calculo[i] * dias_cupon[i])
            if i == nper:
                flujo_cupon[int(nper - cupon_actual)] = monto + flujo_cupon[int(nper - cupon_actual)]
            i += 1
        return flujo_cupon
    
    def tipoPagoAmortizado(self, metodologia, cupon_actual, resultados_fechas, monto_ajustado, cupon, periodicidad, monto_amortizacion, base_de_calculo, dias_cupon, porcentaje_amortizable, nper, per):
        i = cupon_actual
        flujo_cupon = []
        x = 0
        while i <= nper:
            if (metodologia == 'icma' or metodologia == '1'):
                if np.where(resultados_fechas == i)[0].size > 0: #este cupón amortiza
                    flujo_cupon.append((monto_ajustado[x] * cupon / periodicidad) + monto_amortizacion)
                else:#cupón normal
                    flujo_cupon.append(monto_ajustado[x] * cupon / periodicidad)
            elif (metodologia == 'isma-30-360' or metodologia == '5'):
                if np.where(resultados_fechas == i)[0].size > 0: #este cupón amortiza
                    flujo_cupon.append(((monto_ajustado[x] * cupon) / 12 * per) + monto_amortizacion)
                else: #cupón normal
                    flujo_cupon.append((monto_ajustado[x] * cupon) / 12 * per)
            elif (metodologia == 'actual/actual' or metodologia == '2') or (metodologia == 'actual/365' or metodologia == '3') or (metodologia == 'actual/360' or metodologia == '4'):
                if np.where(resultados_fechas == i)[0].size > 0: #este cupón�n amortiza
                    flujo_cupon.append((monto_ajustado[x] * cupon / base_de_calculo[i] * dias_cupon[i]) + monto_amortizacion)
                else: #cupón normal
                    flujo_cupon.append(monto_ajustado[x] * cupon / base_de_calculo[i] * dias_cupon[i])
            if i == nper:
                if np.where(resultados_fechas == i)[0].size > 0:
                    if porcentaje_amortizable == 1: #si amortiza al 100%
                        flujo_cupon[nper - cupon_actual] = flujo_cupon [x]
                    else: #si no amortiza al 100%
                        flujo_cupon[x] = monto_ajustado[x] + flujo_cupon[x] + monto_amortizacion
                else: 
                    flujo_cupon[x] = monto_ajustado[x] + flujo_cupon[x]
            x += 1
            i += 1
        return flujo_cupon
    
    def tipoPagoPIK(self, metodologia, cupon_actual, resultados_fechas, valor_nocional, cupon, periodicidad, base_de_calculo, dias_cupon, nper, per):
        i = cupon_actual
        flujo_cupon = []
        x = 0
        while i <= nper:
            if (metodologia == 'icma' or metodologia == '1'):
                if np.where(resultados_fechas == i)[0].size > 0:
                    if i == cupon_actual:
                        flujo_cupon.append(valor_nocional + (valor_nocional * cupon / periodicidad))
                    else:
                        flujo_cupon.append(flujo_cupon[x - 1] + (flujo_cupon[x - 1] * cupon / periodicidad))
                else:
                    flujo_cupon.append(flujo_cupon[x - 1] * cupon / periodicidad)
            elif (metodologia == 'isma-30-360' or metodologia == '5'):
                if np.where(resultados_fechas == i)[0].size > 0:
                    if i == cupon_actual:
                        flujo_cupon.append(valor_nocional + (valor_nocional * cupon) / 12 * per)
                    else:
                        flujo_cupon.append(flujo_cupon[x - 1] + ((flujo_cupon[x - 1] * cupon) / 12 * per))
                else:
                    flujo_cupon.append(flujo_cupon[x - 1] * cupon / 12 * per)
            elif (metodologia == 'actual/Actual' or metodologia == '2') or (metodologia == 'actual/365' or metodologia == '3') or (metodologia == 'actual/360' or metodologia == '4'):
                if np.where(resultados_fechas == i)[0].size > 0:
                    if i == cupon_actual:
                        flujo_cupon.append(valor_nocional + (valor_nocional * cupon / base_de_calculo[i] * dias_cupon[i]))
                    else:
                        flujo_cupon.append(flujo_cupon[x - 1] + (flujo_cupon[x - 1] * cupon / base_de_calculo[i] * dias_cupon[i]))
                else:
                    flujo_cupon.append(flujo_cupon[x - 1] * cupon / base_de_calculo[i] * dias_cupon[i])
            x += 1
            i += 1
        return flujo_cupon

    def tipoValoracionNormal(self, cupon_actual, nper, w_cupon, discrepancia, tipo_cupones, fecha_vencimiento, vencimiento_esperado, dias_cupon, rendimiento, periodicidad, 
                             flujo_cupon, tipo_pago, emisor, valor_nocional, cupon_corrido): #Cálculo de los Valores Presentes
        fraccion = 0
        factor = 0
        valor_presente_preliminar = 0
        valor_presente_final = 0
        precio_limpio = 0
        precio_sucio = 0
        valor_compra = 0
        valores_presentes = []
        valores_presentes_factor = []
        valores_cvx = []
        i = cupon_actual
        while i <= nper:
            if (i + w_cupon - cupon_actual) < 0:
                factor = 0
            else:
                if discrepancia == 'Si' and i == nper:
                    if (tipo_cupones == 'fw1' or tipo_cupones == '2') or (tipo_cupones == 'fw2' or tipo_cupones == '3'):
                        fraccion = 0
                    else:
                        fraccion = ((fecha_vencimiento - vencimiento_esperado).days) / dias_cupon[nper - 1]
                factor = (i + w_cupon - cupon_actual) + fraccion
            if emisor == 'Hacienda' and i == cupon_actual:
                if cupon_actual == nper:
                    valores_presentes.append((flujo_cupon[i - cupon_actual] / (1 + (rendimiento / periodicidad)) ** factor) -
                    (flujo_cupon[i - cupon_actual] * (1 - w_cupon)) + (valor_nocional / (1 + (rendimiento / periodicidad)) ** factor))
                else:
                    valores_presentes.append((flujo_cupon[i - cupon_actual] / (1 + (rendimiento / periodicidad)) ** factor) -
                    (flujo_cupon[i - cupon_actual] * (1 - w_cupon)))
            else:
                valores_presentes.append(flujo_cupon[i - cupon_actual] / (1 + rendimiento / periodicidad) ** factor)
            valores_presentes_factor.append(valores_presentes[i - cupon_actual] * factor)
            valores_cvx.append(valores_presentes[i - cupon_actual] * (factor ** 2 + factor))
            i += 1
        #Conversión del Array a Numpy
        valores_presentes = np.array(valores_presentes)
        valores_presentes_factor = np.array(valores_presentes_factor) #Para la duraci�n
        valores_cvx = np.array(valores_cvx) #Para la convexidad
        #Dependiendo del Tipo de Pago, cambia el valor presente del instrumento
        if (tipo_pago == 'pik' or tipo_pago == 'p' or tipo_pago == '3'):
            valor_presente_preliminar = valores_presentes [-1]
        else:
            valor_presente_preliminar = valores_presentes.sum()
        #Cálculo de los precios y Valores Finales dependiendo del Emisor
        if emisor != 'Hacienda':
            valor_presente_final = valor_presente_preliminar
            precio_sucio = round(valor_presente_final / valor_nocional,10)
            precio_limpio = round((valor_presente_final - cupon_corrido) / valor_nocional,10)
            valor_compra = round(valor_presente_final - cupon_corrido,2)
            valor_presente_final = round(valor_presente_final,2)
        else:
            precio_limpio = round(valor_presente_preliminar / valor_nocional,6)
            valor_presente_final = round((valor_nocional * precio_limpio) + cupon_corrido,2)
            precio_sucio = round(valor_presente_final / valor_nocional,6)
            valor_compra = round(valor_nocional * precio_limpio,2)
        duracion = (np.sum(valores_presentes_factor) / valor_presente_preliminar) / periodicidad
        duracion_modificada = duracion / (1 + (rendimiento / periodicidad))
        dv01 = precio_sucio * (duracion_modificada / 100) * valor_nocional / 100
        convexidad = np.sum(valores_cvx) / (1 + (rendimiento / periodicidad)) ** 2 / valor_presente_preliminar / periodicidad ** 2
        return valor_presente_final, precio_sucio, valor_compra, precio_limpio, duracion, duracion_modificada, dv01, convexidad, valor_presente_preliminar, valores_presentes

    def Repos(self, margen, tasa_repo, plazo):
        fecha_flujo = {}
        fecha_liquidacion = self.fecha_liquidacion
        valor_de_ida = 0
        valor_de_vuelta = 0
        try:
            valor_presente = self.resultados['valorPresentePreliminar']
        except Exception:
            valor_presente = self.resultados['Valor Presente Preliminar']

        fechas_flujos = self.fechas_cupones
        flujos = self.flujo_cupon

        vencimiento_repo = fecha_liquidacion + relativedelta(days =+ plazo)
        if vencimiento_repo > self.fecha_vencimiento:
            prompt = 'ERROR: Título Vence antes que el Repo..'
        else:
            conteo = -1
            for fecha in fechas_flujos:
                if fecha > fecha_liquidacion:
                    conteo += 1
                    fecha_flujo[fecha] = flujos[conteo]

            flujos_ganados = 0
            for fecha in fechas_flujos:
                if fecha > fecha_liquidacion and fecha < vencimiento_repo:
                    flujos_ganados += fecha_flujo[fecha]

            valor_presente_ajustado = valor_presente - flujos_ganados
            valor_de_ida = valor_presente_ajustado * ( 1 - margen)
            valor_de_vuelta = valor_de_ida * (1 + tasa_repo / 365 * plazo)

        return valor_de_ida, valor_de_vuelta

    def Medida(self, monto_solicitado, regla):
        v_pres = 0
        monto_disponible = 0
        nocional_objetivo = 0

        v_pres = self.resultados['valorPresentePreliminar'] / self.valor_nocional
        monto_disponible = self.resultados['valorPresentePreliminar'] / regla
        nocional_objetivo = Soporte.solver(self.valor_nocional, v_pres, monto_solicitado, regla) #se pudiera hacer el round a -4.. ponderar

        return monto_disponible, nocional_objetivo
    
    def get_results(self):
            
        return self.resultados

    def __str__(self):
        try:
            if self.fecha_liquidacion <= self.fecha_vencimiento:
                return(f'\nInformaciones Título:\n \n \
Fecha de Emisión: {self.fecha_emision}\n \
Fecha de Vencimiento: {self.fecha_vencimiento}\n \
Tasa Cupón: {self.cupon}\n \
Rendimiento: {self.rendimiento}\n \
Tipo de Pago: {self.tipo_pago}\n \
Tipo de Cupones: {self.tipo_cupones}\n \
Periodicidad: {self.periodicidad}\n \
Metodología: {self.metodologia}\n \
Monto: {self.monto}\n \
Valor Presente: {self.resultados["valorPresente"]}\n \
Precio: {self.resultados["precio"]}\n \
Valor de Compra: {self.resultados["valorCompra"]}\n \
Precio Limpio: {self.resultados["precioLimpio"]}\n \
Duración: {self.resultados["duracion"]}\n \
Duración Modificada: {self.resultados["duracionModificada"]}\n \
DV01: {self.resultados["dv01"]}\n \
Convexidad: {self.resultados["convexidad"]}\n \
Valor Presente Preliminar: {self.resultados["valorPresentePreliminar"]}\n \
Tiempo de Cálculo: {self.resultados["tiempoCalculo"]}\n')
            else:
                return f'Titulo Vencido por: {self.fecha_vencimiento - self.fecha_liquidacion} días'
        except Exception:
            return f'Error en título'

class Letras:
    def __init__(self, fecha_liquidacion, fecha_vencimiento, rendimiento, monto, margen_repos = '', tasa_repos = '', plazo_repos = '', date_format = '', multiple = False) -> None:
        self.fecha_liquidacion = fecha_liquidacion
        self.fecha_vencimiento = fecha_vencimiento
        self.rendimiento = rendimiento
        self.monto = monto
        self.margen_repos = margen_repos
        self.tasa_repos = tasa_repos
        self.plazo_repos = plazo_repos
        self.date_format = date_format
        self.multiple = multiple

        self.dias_al_vencimiento = self.fecha_vencimiento - self.fecha_liquidacion
        self.precio = 360 / (360 + self.rendimiento * self.dias_al_vencimiento)
        self.valor_compra = self.monto * self.precio
        self.descuento = self.monto - self.valor_compra