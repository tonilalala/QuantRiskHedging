def f(x):
    sum_total = 0
    for k in range(0,193):
        if date[k] not in tail_days:
            sum_total = sum_total + (x[0]*(price_1[k+1]-price_1[k])/price_1[k]+x[1]*(price_2[k+1]-price_2[k])/price_2[k])
        
    result = -(1/(len(date)-4))*sum_total 
    return(result)

def constaints_tails(portfolio_price,price_1,price_2,i,x,Multiple):
    Constraint = x[0]*(price_1[i]-price_1[i-1])/price_1[i-1] \
                +x[1]*(price_2[i]-price_2[i-1])/price_2[i-1] \
                + Multiple*((portfolio_price[i]-portfolio_price[i-1])/portfolio_price[i-1])
    print(Constraint)
    return (Constraint)

def Check_Constraints(price_1,price_2,x):
    check = 0
    for i in [0,1,2,3]:
        Constraint = constaints_tails(price_1,price_2,tail_index[i],x,8)
        if Constraint < 0:
            check +=1
    print ('Constraints satisfied'+check == 0)
    return (check == 0)
