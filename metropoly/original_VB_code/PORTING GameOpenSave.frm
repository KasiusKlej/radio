VERSION 5.00
Begin VB.Form GameOpenSave 
   ClientHeight    =   2400
   ClientLeft      =   60
   ClientTop       =   300
   ClientWidth     =   3105
   Icon            =   "GameOpenSave.frx":0000
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form1"
   ScaleHeight     =   2400
   ScaleWidth      =   3105
   StartUpPosition =   3  'Windows Default
   Begin VB.CommandButton CommandCancel 
      Caption         =   "Cancel"
      Height          =   360
      Left            =   1695
      TabIndex        =   4
      Top             =   1920
      Width           =   900
   End
   Begin VB.CommandButton CommandOK 
      Caption         =   "OK"
      Height          =   360
      Left            =   450
      TabIndex        =   3
      Top             =   1920
      Width           =   900
   End
   Begin VB.FileListBox File1 
      Height          =   1260
      Left            =   510
      Pattern         =   "*.sav"
      TabIndex        =   2
      Top             =   480
      Width           =   2445
   End
   Begin VB.TextBox TextFN 
      Height          =   285
      Left            =   1380
      TabIndex        =   0
      Top             =   120
      Width           =   1560
   End
   Begin VB.Image Image1 
      Height          =   480
      Left            =   90
      Picture         =   "GameOpenSave.frx":08CA
      Top             =   510
      Width           =   480
   End
   Begin VB.Label Label1 
      Alignment       =   1  'Right Justify
      BackStyle       =   0  'Transparent
      Caption         =   "File Name:"
      Height          =   285
      Left            =   105
      TabIndex        =   1
      Top             =   150
      Width           =   1170
   End
End
Attribute VB_Name = "GameOpenSave"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub CommandCancel_Click()
    openSaveFileName = ""
    Me.Hide
End Sub

Private Sub CommandOK_Click()
    If TextFN.Text <> "" Then
        openSaveFileName = TextFN.Text
        If (Right(openSaveFileName, 4) <> ".sav") And (Right(openSaveFileName, 4) <> ".map") Then
            If openSaveMode = 3 Then
                openSaveFileName = openSaveFileName & ".map"
            Else
                openSaveFileName = openSaveFileName & ".sav"
            End If
        End If
        'open/save
        If openSaveMode = 1 Then
            open_game openSaveFileName
        Else
            If openSaveMode = 2 Then
                save_game openSaveFileName, False
            Else    'seve map
                save_game openSaveFileName, True
            End If
        End If
    End If
    Me.Hide
End Sub

Private Sub File1_Click()
    On Error Resume Next
    TextFN.Text = File1.List(File1.ListIndex)
End Sub

Private Sub Form_KeyPress(KeyAscii As Integer)
    If KeyAscii = 27 Then CommandCancel_Click
End Sub

Private Sub Form_Load()
    Me.Left = (Screen.Width - Me.Width) / 2
    Me.Top = (Screen.Height - Me.Height) / 2
    File1.Path = App.Path
    File1.Pattern = "*.sav"
End Sub

Sub save_game(fn, saveJustMap As Boolean)
    'encode map,params,players
    Dim i, j, x, y, c, s
    Open App.Path & "\" & fn For Output As #1
    
    'save map
    Print #1, Trim(Str(dimx))
    Print #1, Trim(Str(dimy))
    
    'roads
    For j = 1 To dimy
        s = "": c = ""
        For i = 1 To dimx
            Select Case map(i, j).tip
            Case 0
                c = "0"
            Case 1
                c = "1"
            Case 2
                c = "2"
            Case 3
                c = "3"
            Case 4
                c = "4"
            Case 5
                c = Chr(map(i, j).semafor + 52)
            End Select
            s = s & c
        Next i
        Print #1, s
    Next j
    'price
    For j = 1 To dimy
        s = "": c = ""
        For i = 1 To dimx
            c = Mid("ABCDEFGHIJKLMNOPQRSTUVWXYZ", map(i, j).price - 19, 1)
            s = s & c
        Next i
        Print #1, s
    Next j
    'stage
    For j = 1 To dimy
        s = "": c = ""
        For i = 1 To dimx
            c = Trim(Str(map(i, j).stage))
            s = s & c
        Next i
        Print #1, s
    Next j
    'owner
    For j = 1 To dimy
        s = "": c = ""
        For i = 1 To dimx
            c = Trim(Str(map(i, j).owner))
            s = s & c
        Next i
        Print #1, s
    Next j
    
    If saveJustMap Then     'useful for map editor
        Close 1
        Exit Sub
    End If
    
    'params  startx,starty,startsmer,jailx,jaily, faza, curpl,
    '        kocka,cakajKocko, dayOfWeek,clkMode, TimerMet, TimerSkok
    Print #1, "[Parameters]"
    Print #1, Trim(Str(startx))
    Print #1, Trim(Str(starty))
    Print #1, Trim(Str(startsmer))
    Print #1, Trim(Str(jailx))
    Print #1, Trim(Str(jaily))
    Print #1, Trim(Str(faza))
    Print #1, Trim(Str(curpl))
    Print #1, Trim(Str(kocka))
    Print #1, Trim(Str(cakajKocko))
    Print #1, Trim(Str(dayOfWeek))
    Print #1, Trim(Str(clkMode))
    If Game.TimerMetKocke.Enabled Then
        Print #1, "y"
    Else
        Print #1, "n"
    End If
    If Game.TimerSkokFigure.Enabled Then
        Print #1, "y"
    Else
        Print #1, "n"
    End If
    
    'players
    Print #1, "[Players]"
    Print #1, Trim(Str(numpl))
    For i = 1 To numpl
        Print #1, Trim(Str(player(i).id))
        Print #1, Trim(Str(player(i).tip))
        Print #1, player(i).ime
        Print #1, Trim(Str(player(i).barva))
        Print #1, Trim(Str(player(i).money))
        Print #1, Trim(Str(player(i).smer))
        Print #1, Trim(Str(player(i).izobrazba))
        Print #1, Trim(Str(player(i).x))
        Print #1, Trim(Str(player(i).y))
        Print #1, Trim(Str(player(i).jobpayment))
        Print #1, Trim(Str(player(i).statland))
        Print #1, Trim(Str(player(i).stathouse))
    Next i
        
    Close 1
End Sub

Sub open_game(fn)
    On Error Resume Next
    Dim s, aktivMet, aktivSkok
    aktivMet = False: aktivSkok = False
    'load_params
    Open App.Path & "\" & fn For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[Parameters]"
    If s = "[Parameters]" Then
        Line Input #1, s: startx = Val(s)
        Line Input #1, s: starty = Val(s)
        Line Input #1, s: startsmer = Val(s)
        Line Input #1, s: jailx = Val(s)
        Line Input #1, s: jaily = Val(s)
        Line Input #1, s: faza = Val(s)
        Line Input #1, s: curpl = Val(s)
        Line Input #1, s: kocka = Val(s)
        Line Input #1, s: cakajKocko = Val(s)
        Line Input #1, s: dayOfWeek = Val(s)
        Line Input #1, s: clkMode = Val(s)
        Line Input #1, s
        If s = "y" Then
            aktivMet = True
        Else
             aktivMet = False
        End If
        Line Input #1, s
        If s = "y" Then
            aktivSkok = True
        Else
             aktivSkok = False
        End If
        
    End If
    Close 1
    
    'load_players
    Open App.Path & "\" & fn For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[Players]"
    If s = "[Players]" Then
        Line Input #1, s: numpl = Val(s)
        For i = 1 To numpl
            Line Input #1, s: player(i).id = Val(s)
            Line Input #1, s: player(i).tip = Val(s)
            Line Input #1, s: player(i).ime = s
            Line Input #1, s: player(i).barva = Val(s)
            Line Input #1, s: player(i).money = Val(s)
            Line Input #1, s: player(i).smer = Val(s)
            Line Input #1, s: player(i).izobrazba = Val(s)
            Line Input #1, s: player(i).x = Val(s)
            Line Input #1, s: player(i).y = Val(s)
            Line Input #1, s: player(i).jobpayment = Val(s)
            Line Input #1, s: player(i).statland = Val(s)
            Line Input #1, s: player(i).stathouse = Val(s)
        Next i
    End If
    
    Close 1
    
    'load map
    NewGame.load_map fn
    
    'run
    Game.display_status
    'Game.LabelStatus.Caption = "It is " & player(curpl).ime & "'s turn."
    Game.LabelStatus.Caption = lngg(141) & " " & player(curpl).ime & lngg(142)
    Game.draw_map
    Game.draw_players
    If aktivMet Then
        Game.TimerMetKocke.Enabled = True
    Else
        Game.TimerMetKocke.Enabled = False
    End If
    If aktivSkok Then
        Game.TimerSkokFigure.Enabled = True
    Else
        Game.TimerSkokFigure.Enabled = False
    End If
    
End Sub
