import re, math
from scipy.optimize import minimize
from dateutil.relativedelta import relativedelta
import pandas as pd
import logging, os

class Soporte ():

    def conversion_tasas(tasas):
        if type(tasas) == str and re.search('%',tasas)!=None:
            return float(tasas.replace('%',''))/100
        elif float(tasas) > 1:
            return float(tasas) / 100
        else:
            return float(tasas)
    
    def conversion_periodicidad(per):
        if per in ['anual', 'a', '6', 'vencimiento', 'v', '7']:
            return 1
        elif per == 'semestral' or per == 's' or per == '5':
            return 2
        elif per == 'cuatrimestral' or per == 'c' or per == '4':
            return 3
        elif per == 'trimestral' or per == 't' or per == '3':
            return 4
        elif per == 'bimensual' or per == 'b' or per == '2':
            return 6
        elif per == 'mensual' or per == 'm' or per == '1':
            return 12
    
    def conversion_periodicidad_amort(per):
        if per == 'anual' or per == 'a' or per == '6':
            return 12
        elif per == 'semestral' or per == 's' or per == '5':
            return 6
        elif per == 'cuatrimestral' or per == 'c' or per == '4':
            return 4
        elif per == 'trimestral' or per == 't' or per == '3':
            return 3
        elif per == 'bimensual' or per == 'b' or per == '2':
            return 2
        elif per == 'mensual' or per == 'm' or per == '1':
            return 1

    def seleccionMes(mes):
        if mes == 1:
            return 'enero'
        if mes == 2:
            return 'febrero'
        if mes == 3:
            return 'marzo'
        if mes == 4:
            return 'abril'
        if mes == 5:
            return 'mayo'
        if mes == 6:
            return 'junio'
        if mes == 7:
            return 'julio'
        if mes == 8:
            return 'agosto'
        if mes == 9:
            return 'septiembre'
        if mes == 10:
            return 'octubre'
        if mes == 11:
            return 'noviembre'
        if mes == 12:
            return 'diciembre'
    
    def calculo_años(emision,vencimiento):
        if vencimiento.year % 4 == 0:
            divisor_año = 366
        else:
            divisor_año = 365
        dif_años = relativedelta(vencimiento,emision).years
        dif_meses = relativedelta(vencimiento,emision).months / 12
        dif_dias = relativedelta(vencimiento,emision).days / divisor_año
        return dif_años + dif_meses + dif_dias

    def ln_nper(emision, vencimiento, fper, tipo, a_vencimiento = False):
        if a_vencimiento == False:
            rel_nper = (relativedelta(vencimiento, emision).years * 12 / (12 / fper)) + (relativedelta(vencimiento, emision).months / (12 / fper))
            if (rel_nper - math.trunc(rel_nper)) > 0: 
                if (tipo == 'fw2' or tipo == '3'): 
                    rel_nper += 1
        else:
            rel_nper = 1
        return rel_nper

    def days360(start_date,end_date,method_eu=False):
        
        start_day = start_date.day
        start_month = start_date.month
        start_year = start_date.year
        end_day = end_date.day
        end_month = end_date.month
        end_year = end_date.year
    
        if (
            start_day == 31 or
            (
                method_eu is False and
                start_month == 2 and (
                    start_day == 29 or (
                        start_day == 28 and
                        start_date.is_leap_year is False
                    )
                )
            )
        ):
            start_day = 30
    
        if end_day == 31:
            if method_eu is False and start_day != 30:
                end_day = 1
                if end_month == 12:
                    end_year += 1
                    end_month = 1
                else:
                    end_month += 1 
            else:
                end_day = 30
        return (
            end_day + end_month * 30 + end_year * 360 - 
            start_day - start_month * 30 - start_year * 360)

    def solver(v1, v2, v3, v4):

        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), 'cMult'), mode = 'w', encoding = 'utf-8')
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)
        #consoleHandler = logging.StreamHandler()
        #consoleHandler.setFormatter(logFormatter)
        #logger.addHandler(consoleHandler)

        objetivo = v4
        # Define the objective function
        def objective (x):
            x1 = x[0] #valor nocional
            x2 = x[1] #valor presente
            x3 = x[2] #monto solicitado
            x4 = x[3] #ratio
            return (x1 * x2) / x3

        # Define the constraint function(s)
        def constraint1 (x):
            return ((x[0] * x[1]) / x[2]) - x[3] #equality
        
        # Define the initial guess for the variables
        x0 = [v1, v2, v3, v4]
        logger.info(f'Valor inicial de la función objetivo: {objective(x0)}')

        # Define the bounds for the decision variables
        b1 = (0, None) #variable
        b2 = (v2, v2) #fixed
        b3 = (v3, v3) #fixed
        b4 = (v4, v4) #fixed
        bnds = (b1, b2, b3, b4) #grouping bounds
        con1 = {'type': 'eq', 'fun': constraint1} #set the constraint with type of equality
        cons = [con1] #grouping constraints

        # Define the termination tolerance
        tolerance = 1e-100

        sol = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons, tol = tolerance)
        #print(f'Success? {sol.success}?')
        #print(f'Valor final función : {sol.fun}')

        if abs(sol.fun - objetivo) <= tolerance and sol.success == True and sol.fun > 0:
            t1 = sol.x[0]
            t2 = sol.x[1]
            t3 = sol.x[2]
            test = (t1 * t2) / t3
            logger.info(f'Residual: {test - v4}')
            logger.info(f'Resultados Solver: {sol}')
            logger.removeHandler(fileHandler)
            fileHandler.close()
            #logging.shutdown()
            return sol.x[0]
        else:
            logger.warning("No solution found within the desired tolerance range.")
            logger.removeHandler(fileHandler)
            fileHandler.close()
            #logging.shutdown()
            return 0
            
    def fechaCercana(fechas, buscada):

        return min(fecha for fecha in fechas if fecha >= buscada)
    