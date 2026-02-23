Attribute VB_Name = "MoneyParameters"
Function pay_money_price(stage, price)
    Dim r
    r = (stage + 1) * price
    If stage = 0 Then r = Int(price / 5 * 2)
    
    pay_money_price = r
End Function

Function buy_land_price(price)
    'buy_land_price = price
    buy_land_price = price * 2
End Function

Function build_houses_price(stage, price)
    build_houses_price = price * 2  ' * (stage + 1)
End Function

Function earn_price(izobrazba)
    'earn_price = 50 + izobrazba * 50
    Dim r
    Select Case izobrazba
    Case 0
        r = 50
    Case 1
        r = 80
    Case 2
        r = 100
    Case 3
        r = 150
    Case 4
        r = 250
    Case 5
        r = 300
    End Select
    earn_price = r

End Function

Function learn_price(izobrazba)
    learn_price = 50 + izobrazba * 20
End Function

Function sell_price(stage, price)
    Dim r, pl, ph
    pl = buy_land_price(price)
    ph = build_houses_price(stage, price)
    
    Select Case stage
    Case 0
        r = Int(3 / 2 * pl)
    Case 1
        r = Int(1 / 2 * ph)
    Case 2
        r = Int(3 / 4 * ph)
    Case 3
        r = ph
    Case 4
        r = Int(5 / 4 * ph)
    Case 5
        r = Int(6 / 4 * ph)
    End Select
    sell_price = r
    
End Function

Function road_price(x, y)
    road_price = -100
End Function

Function rotateSemafor_price()
    rotateSemafor_price = 5
End Function

Function create_semaphor_price(x, y)
    create_semaphor_price = 15
End Function

Function delete_semaphor_price(x, y)
    delete_semaphor_price = 50
End Function

