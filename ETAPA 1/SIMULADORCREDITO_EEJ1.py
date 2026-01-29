run = True

    #Capacidad de pago
'''def payAbility(Income, Expense):
    pA = Income - Expense
    return pA'''

    #valor de la cuota 
'''def feeValue(credit, anualRate, fees):
    if fees <= 0:
        raise ValueError("Número de cuotas inválido")
    monthlyRate = (1 + anualRate)**(1/12) - 1
    return credit * (monthlyRate * (1 + monthlyRate)**fees) / ((1 + monthlyRate)**fees - 1)
'''


    #porcentaje de endeudamiento
'''def debtPercent(fee, income):
    dP = round((fee/income)*100,2) 
    return dP '''

def rates(creditHistory):
    rates = {
        'bueno': 0.18,
        'regular': 0.26,
        'malo': 0.35
    }
    return rates.get(creditHistory.lower())

    

'''def loanTotal(feeNumber, CreditValue, fV):
    totalPaid = round(fV * feeNumber,2)
    totalInterest = round(totalPaid - CreditValue,2)
    return totalPaid, totalInterest'''

def debtorMesagge(name, record, dP, creditHistory, fV, rt, totalPaid, totalInterest):
    debtorMsg = {
                        'Nombre':name,
                        'Estado': record,
                        'Endeudamiento':dP,
                        'Historial':creditHistory,
                        'Cuota': fV,
                        'Tasa E.A': rt,
                        'Total pagado': totalPaid,
                        'Intereses': totalInterest

                            }
    return debtorMsg

def approvalRules(creditHistory, dP, feeNumber):
    history = creditHistory.upper()

    if history == 'BUENO':
        return dP <= 35

    if history == 'REGULAR':
        if feeNumber > 24:
            return dP <= 25
        return dP <= 25

    if history == 'MALO':
        return dP <= 15
    
def recordStatus(isApproved, creditHistory, feeNumber):
    if not isApproved:
        return 'Rechazado'

    if creditHistory.upper() == 'REGULAR' and feeNumber > 24:
        return 'Aprobado con advertencia'

    return 'Aprobado'   

def financialAnalysis(monthlyIncome, monthlyExpense, CreditValue, fees, anualRate ):
    #capacidad de pago 
    payAbility = monthlyIncome - monthlyExpense

    #valor de la cuota 
    if fees <= 0:
        raise ValueError("Número de cuotas inválido")
    monthlyRate = (1 + anualRate)**(1/12) - 1
    feeValue = round(CreditValue * (monthlyRate * (1 + monthlyRate)**fees) / ((1 + monthlyRate)**fees - 1),2)

    #porcentaje de endeudamiento
    debtPercent = round((fees/monthlyIncome)*100,2) 

    #total del prestamo 
    totalPaid = round(feeValue * fees,2)
    totalInterest = round(totalPaid - CreditValue,2)

    return payAbility, feeValue, debtPercent, totalPaid, totalInterest



def evaluate(name, monthlyIncome, monthlyExpense, CreditValue, feeNumber, creditHistory):
    rt = rates(creditHistory)
    if rt is None:
        return {'Estado': 'Error', 'Nota': 'Historial inválido'}

    pA, fV, dP, totalPaid, totalInterest = financialAnalysis(monthlyIncome, monthlyExpense, CreditValue, feeNumber, rt)

    if fV > pA:
        record = 'Rechazado'
    else:
        approved = approvalRules(creditHistory, dP, feeNumber)
        record = recordStatus(approved, creditHistory, feeNumber)

    result = debtorMesagge(
        name, record, dP, creditHistory, fV, rt, totalPaid, totalInterest
    )

    if record.startswith('Aprobado'):
        evaluationsAproved.append(result)
    else:
        evaluationsRefused.append(result)

    return result
    
    
  
        
    
evaluationsAproved = []
evaluationsRefused = []


    

while run:
    
    name = (input('Nombre: '))
    monthlyIncome = float(input('Ingresos mensuales: '))
    monthlyExpense = float(input('Gastos mensuales: '))
    CreditValue = float(input('Valor del credito solicitado: '))
    feeNumber = int(input('Numero de cuotas: '))
    creditHistory = input('Historial crediticio (Bueno, Regular, Malo): ')
    validHistories=['bueno', 'regular', 'malo']
    while creditHistory.lower() not in validHistories:
        print('Ingresa el historial correcto')
        creditHistory = input('Historial crediticio (Bueno, Regular, Malo): ')

    modifyName = name.capitalize()
    print("Resultado de evaluación")
    print("-" * 30)
    result = evaluate(modifyName, monthlyIncome, monthlyExpense, CreditValue, feeNumber,creditHistory)
    if result['Estado'] == 'Aprobado':
        for k, v in result.items():
            print(f"{k:<15}: {v}")
    elif result['Estado'] == 'Rechazado':
        for k, v in result.items():
            print(f"{k:<15}: {v}")
    
    
    

    if run ==True: 
        gm = input('Evaluar otro caso? (y/n):   ')

        if gm == 'y':
            continue
        elif gm == 'n':
            print(f'Total de evaluaciones: {len(evaluationsAproved) + len(evaluationsRefused)}')
            print(f'Creditos aprobados: {len(evaluationsAproved)}')
            print(f'Creditos rechazados: {len(evaluationsRefused)}')
            run = False
            

            break