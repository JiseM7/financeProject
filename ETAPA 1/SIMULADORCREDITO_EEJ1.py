run = True


def rates(creditHistory):
    rates = {
        'bueno': 0.18,
        'regular': 0.26,
        'malo': 0.35
    }
    return rates.get(creditHistory.lower())

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

#Entre más alto, menos riesgo para el banco.
#Entre más bajo, más probabilidad de rechazo.
def score(creditHistory, debtPercent, fees, coverageRatio):
    total_score = 0 
    if creditHistory == 'bueno':
        total_score = total_score + 40 
    elif creditHistory == 'regular': 
        total_score = total_score + 20 
    elif creditHistory == 'malo':
        total_score = total_score - 10
    
    if debtPercent <= 25:
        total_score = total_score + 30
    
    elif debtPercent > 25 and debtPercent <= 40: 
        total_score = total_score + 15
    
    elif debtPercent >= 41: 
        total_score = total_score - 10
    
    if coverageRatio >= 2: 
        total_score += 20 
    elif coverageRatio >= 1.1 and coverageRatio < 2: 
        total_score += 10
    elif coverageRatio < 1: 
        total_score += 0 
    
    if fees <= 12: 
        total_score += 10 
    elif fees >= 13 and fees <= 36: 
        total_score += 5 
    elif fees > 36: 
        total_score += 0 


    return max(0, min(100, total_score))


    
def recordStatus(isApproved):
    if isApproved >= 70:
        return 'Aprobado'

    elif isApproved >=50 and isApproved <70:
        return 'Aprobado con advertencia'

    elif isApproved < 50: 
        return 'Rechazado'   

def financialAnalysis(monthlyIncome, monthlyExpense, CreditValue, fees, anualRate ):
    #capacidad de pago 
    payAbility = monthlyIncome - monthlyExpense
    

    #valor de la cuota 
    if fees <= 0:
        raise ValueError("Número de cuotas inválido")
    monthlyRate = (1 + anualRate)**(1/12) - 1
    feeValue = round(CreditValue * (monthlyRate * (1 + monthlyRate)**fees) / ((1 + monthlyRate)**fees - 1),2)

    #porcentaje de endeudamiento
    debtPercent = round((feeValue/monthlyIncome)*100,2) 

    #total del prestamo 
    totalPaid = round(feeValue * fees,2)
    totalInterest = round(totalPaid - CreditValue,2)

    coverage_ratio = payAbility / feeValue

    return payAbility, feeValue, debtPercent, totalPaid, totalInterest, coverage_ratio



def evaluate(name, monthlyIncome, monthlyExpense, CreditValue, feeNumber, creditHistory):
    rt = rates(creditHistory)
    if rt is None:
        return {'Estado': 'Error', 'Nota': 'Historial inválido'}

    pA, fV, dP, totalPaid, totalInterest, cR = financialAnalysis(monthlyIncome, monthlyExpense, CreditValue, feeNumber, rt)

    if fV > pA:
        record = 'Rechazado'
    else:
        #approved = approvalRules(creditHistory, dP, feeNumber)
        final_score = score(creditHistory, dP, feeNumber, cR)
        record = recordStatus(final_score)

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
    print("-" * 30)
    for k, v in result.items():
        print(f"{k:<20}: {v}")
    print("-" * 30)


    
    
    

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