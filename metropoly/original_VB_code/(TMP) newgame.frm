Private Sub CommandOK_Click()
    Dim x, y
    
    save_frm_defaults
    x = 6 + Int((15 - 1 + 1) * Rnd + 1)
    y = 5 + Int((10 - 1 + 1) * Rnd + 1)
    
    If (mapEditorMode = 1) Or (mapEditorMode = 3) Then
        '''no need to load map just edited
        Call set_startxy(jailx, jaily, startx, starty, startsmer)
        
    Else
        If Text1(0) = "" And (Text1(1) = "") And ((Combo1.Text = "Random") Or (Combo1.Text = "")) Then
            generate_default_map x, y
            load_map App.Path & "\default.map"     'set global variables
        Else
            If (Combo1.Text <> "Random") And (Combo1.Text <> "") Then
                load_map App.Path & "\" & Combo1.Text
            Else
                x = Val(Text1(0).Text)
                y = Val(Text1(1).Text)
                If x < 7 Then x = 7
                If y < 7 Then y = 7
                generate_default_map x, y
                load_map App.Path & "\default.map"     'set global variables
            End If
        End If
    End If
    
    init_players
    Me.Hide
End Sub

Private Sub CommandCancel_Click()
    Me.Hide
End Sub

Private Sub Form_KeyPress(KeyAscii As Integer)
    If KeyAscii = 27 Then CommandCancel_Click
End Sub


Sub save_frm_defaults()
    Dim s, i, idp, n, a(200)
    Open App.Path & "\metropoly.ini" For Input As 1
    i = 1
    Do
        Line Input #1, a(i)
        If a(i) = "[DefaultPlayers]" Then idp = i
        i = i + 1
    Loop Until EOF(1)
    n = i
    Close 1
    
    Open App.Path & "\metropoly.ini" For Output As 1
    For i = 1 To idp
        Print #1, a(i)
    Next i
    For i = 1 To 7
        If Aliigra(i - 1).Value = 1 Then
            s = "1"
        Else
            s = "0"
        End If
        If Aliigra(i - 1 + 7).Value = 1 Then
            s = s & "1"
        Else
            s = s & "0"
        End If
        s = s & ImeIgralca(i - 1).Text
        Print #1, s
    Next i
    For i = idp + 8 To n - 1
        Print #1, a(i)
    Next i
    
    Close 1
End Sub

