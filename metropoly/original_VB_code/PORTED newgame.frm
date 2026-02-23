VERSION 5.00
Begin VB.Form NewGame 
   Caption         =   "New Game"
   ClientHeight    =   3780
   ClientLeft      =   60
   ClientTop       =   300
   ClientWidth     =   3180
   Icon            =   "newgame.frx":0000
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form2"
   ScaleHeight     =   3780
   ScaleWidth      =   3180
   StartUpPosition =   3  'Windows Default
   Begin VB.Frame Frame1 
      Height          =   585
      Left            =   60
      TabIndex        =   24
      Top             =   2400
      Width           =   3075
      Begin VB.TextBox Text1 
         Height          =   285
         Index           =   0
         Left            =   210
         TabIndex        =   27
         TabStop         =   0   'False
         Top             =   200
         Width           =   375
      End
      Begin VB.TextBox Text1 
         Height          =   285
         Index           =   1
         Left            =   825
         TabIndex        =   26
         TabStop         =   0   'False
         Top             =   200
         Width           =   375
      End
      Begin VB.ComboBox Combo1 
         Height          =   315
         ItemData        =   "newgame.frx":08CA
         Left            =   1665
         List            =   "newgame.frx":08CC
         TabIndex        =   25
         TabStop         =   0   'False
         Top             =   200
         Width           =   1335
      End
      Begin VB.Label Label1 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "x:"
         Height          =   270
         Index           =   0
         Left            =   -15
         TabIndex        =   30
         Top             =   200
         Width           =   210
      End
      Begin VB.Label Label1 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "y:"
         Height          =   270
         Index           =   1
         Left            =   525
         TabIndex        =   29
         Top             =   200
         Width           =   300
      End
      Begin VB.Label Label1 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "map:"
         Height          =   270
         Index           =   2
         Left            =   1125
         TabIndex        =   28
         Top             =   200
         Width           =   540
      End
   End
   Begin VB.FileListBox File1 
      Height          =   1065
      Left            =   1695
      Pattern         =   "*.map"
      TabIndex        =   23
      Top             =   4380
      Visible         =   0   'False
      Width           =   1335
   End
   Begin VB.CommandButton CommandCancel 
      Caption         =   "Cancel"
      Height          =   360
      Left            =   1665
      TabIndex        =   22
      Top             =   3225
      Width           =   915
   End
   Begin VB.CommandButton CommandOK 
      Caption         =   "OK"
      Height          =   360
      Left            =   495
      TabIndex        =   21
      Top             =   3225
      Width           =   900
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   13
      Left            =   2415
      TabIndex        =   20
      TabStop         =   0   'False
      ToolTipText     =   "Computer?"
      Top             =   2085
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   12
      Left            =   2415
      TabIndex        =   19
      TabStop         =   0   'False
      ToolTipText     =   "Computer?"
      Top             =   1740
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   11
      Left            =   2415
      TabIndex        =   18
      TabStop         =   0   'False
      ToolTipText     =   "Computer?"
      Top             =   1395
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   10
      Left            =   2415
      TabIndex        =   17
      TabStop         =   0   'False
      ToolTipText     =   "Computer?"
      Top             =   1050
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   9
      Left            =   2415
      TabIndex        =   16
      TabStop         =   0   'False
      ToolTipText     =   "Computer?"
      Top             =   720
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   8
      Left            =   2415
      TabIndex        =   15
      TabStop         =   0   'False
      ToolTipText     =   "Computer?"
      Top             =   405
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   7
      Left            =   2415
      TabIndex        =   14
      TabStop         =   0   'False
      ToolTipText     =   "Computer?"
      Top             =   75
      Width           =   360
   End
   Begin VB.TextBox ImeIgralca 
      Height          =   285
      Index           =   6
      Left            =   780
      TabIndex        =   13
      TabStop         =   0   'False
      Text            =   "Player7"
      Top             =   2100
      Width           =   1560
   End
   Begin VB.TextBox ImeIgralca 
      Height          =   285
      Index           =   5
      Left            =   780
      TabIndex        =   12
      TabStop         =   0   'False
      Text            =   "Player6"
      Top             =   1770
      Width           =   1560
   End
   Begin VB.TextBox ImeIgralca 
      Height          =   285
      Index           =   4
      Left            =   780
      TabIndex        =   11
      TabStop         =   0   'False
      Text            =   "Player5"
      Top             =   1425
      Width           =   1560
   End
   Begin VB.TextBox ImeIgralca 
      Height          =   285
      Index           =   3
      Left            =   780
      TabIndex        =   10
      TabStop         =   0   'False
      Text            =   "Player4"
      Top             =   1095
      Width           =   1560
   End
   Begin VB.TextBox ImeIgralca 
      Height          =   285
      Index           =   2
      Left            =   780
      TabIndex        =   9
      TabStop         =   0   'False
      Text            =   "Player3"
      Top             =   765
      Width           =   1560
   End
   Begin VB.TextBox ImeIgralca 
      Height          =   285
      Index           =   1
      Left            =   780
      TabIndex        =   8
      TabStop         =   0   'False
      Text            =   "Player2"
      Top             =   435
      Width           =   1560
   End
   Begin VB.TextBox ImeIgralca 
      Height          =   285
      Index           =   0
      Left            =   780
      TabIndex        =   7
      TabStop         =   0   'False
      Text            =   "Player1"
      Top             =   105
      Width           =   1560
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   6
      Left            =   435
      TabIndex        =   6
      TabStop         =   0   'False
      ToolTipText     =   "Select who will play"
      Top             =   2115
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   5
      Left            =   435
      TabIndex        =   5
      TabStop         =   0   'False
      ToolTipText     =   "Select who will play"
      Top             =   1770
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   4
      Left            =   435
      TabIndex        =   4
      TabStop         =   0   'False
      ToolTipText     =   "Select who will play"
      Top             =   1425
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   3
      Left            =   435
      TabIndex        =   3
      TabStop         =   0   'False
      ToolTipText     =   "Select who will play"
      Top             =   1080
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   2
      Left            =   435
      TabIndex        =   2
      TabStop         =   0   'False
      ToolTipText     =   "Select who will play"
      Top             =   750
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   1
      Left            =   435
      TabIndex        =   1
      TabStop         =   0   'False
      ToolTipText     =   "Select who will play"
      Top             =   435
      Value           =   1  'Checked
      Width           =   360
   End
   Begin VB.CheckBox Aliigra 
      Height          =   270
      Index           =   0
      Left            =   435
      TabIndex        =   0
      TabStop         =   0   'False
      ToolTipText     =   "Select who will play"
      Top             =   120
      Value           =   1  'Checked
      Width           =   360
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   6
      Left            =   50
      Stretch         =   -1  'True
      Top             =   1755
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   5
      Left            =   50
      Stretch         =   -1  'True
      Top             =   1425
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   4
      Left            =   50
      Stretch         =   -1  'True
      Top             =   1080
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   3
      Left            =   50
      Stretch         =   -1  'True
      Top             =   750
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   2
      Left            =   50
      Stretch         =   -1  'True
      Top             =   405
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   1
      Left            =   50
      Stretch         =   -1  'True
      Top             =   60
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   7
      Left            =   50
      Stretch         =   -1  'True
      Top             =   2085
      Width           =   315
   End
   Begin VB.Shape BarvaIgralca 
      FillColor       =   &H00C000C0&
      FillStyle       =   0  'Solid
      Height          =   225
      Index           =   6
      Left            =   2775
      Top             =   2130
      Width           =   225
   End
   Begin VB.Shape BarvaIgralca 
      FillColor       =   &H00FF0000&
      FillStyle       =   0  'Solid
      Height          =   225
      Index           =   5
      Left            =   2775
      Top             =   1785
      Width           =   225
   End
   Begin VB.Shape BarvaIgralca 
      FillColor       =   &H00008000&
      FillStyle       =   0  'Solid
      Height          =   225
      Index           =   4
      Left            =   2775
      Top             =   1425
      Width           =   225
   End
   Begin VB.Shape BarvaIgralca 
      FillColor       =   &H0000FF00&
      FillStyle       =   0  'Solid
      Height          =   225
      Index           =   3
      Left            =   2775
      Top             =   1095
      Width           =   225
   End
   Begin VB.Shape BarvaIgralca 
      FillColor       =   &H0000FFFF&
      FillStyle       =   0  'Solid
      Height          =   225
      Index           =   2
      Left            =   2775
      Top             =   750
      Width           =   225
   End
   Begin VB.Shape BarvaIgralca 
      FillColor       =   &H000080FF&
      FillStyle       =   0  'Solid
      Height          =   225
      Index           =   1
      Left            =   2775
      Top             =   405
      Width           =   225
   End
   Begin VB.Shape BarvaIgralca 
      FillColor       =   &H000000FF&
      FillStyle       =   0  'Solid
      Height          =   225
      Index           =   0
      Left            =   2775
      Top             =   90
      Width           =   225
   End
End
Attribute VB_Name = "NewGame"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
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

Private Sub Form_Load()
    'load defaults
    On Error Resume Next
    Dim s, i
    Me.Left = (Screen.Width - Me.Width) / 2
    Me.Top = (Screen.Height - Me.Height) / 2
    fill_combo
    For i = 0 To 6
        figura(i + 1).Picture = Game.figura(i + 1).Picture
    Next i

    Open App.Path & "\metropoly.ini" For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[DefaultPlayers]"
    If s = "[DefaultPlayers]" Then
        For i = 1 To 7
            Line Input #1, s
            If Left(s, 1) = "1" Then
                Aliigra(i - 1).Value = 1
            Else
                Aliigra(i - 1).Value = 0
            End If
            s = Right(s, Len(s) - 1)
            If Left(s, 1) = "1" Then
                Aliigra(i - 1 + 7).Value = 1
            Else
                Aliigra(i - 1 + 7).Value = 0
            End If
            s = Right(s, Len(s) - 1)
            ImeIgralca(i - 1).Text = s
        Next i
    End If
    Close 1
    
End Sub

Sub init_players()
    Dim i
    numpl = 0
    For i = 0 To 6
        If Aliigra(i).Value = 1 Then
            numpl = numpl + 1
            player(numpl).id = i + 1
            If Aliigra(i + 7).Value = 1 Then 'pc
                player(numpl).tip = 1
            Else
                player(numpl).tip = 0
            End If
            player(numpl).ime = ImeIgralca(i)
            player(numpl).barva = BarvaIgralca(i).FillColor
            
            player(numpl).money = 1000
            player(numpl).smer = startsmer
            player(numpl).izobrazba = 0
            'player(numpl).delay = 0
            player(numpl).x = jailx
            player(numpl).y = jaily
            player(numpl).jobpayment = 0
            player(numpl).statland = 0
            player(numpl).stathouse = 0
        End If
        
    Next i
End Sub

Sub load_map(fn)
    Dim i, j, x, y, s, c
    
    Open fn For Input As 1
    
    Line Input #1, s
    dimx = Val(s)
    Line Input #1, s
    dimy = Val(s)
    
    x = 1: y = 1
    For i = 1 To dimy   'tip, semafor
        Line Input #1, s
        x = 1
        For j = 1 To dimx
            c = Mid(s, j, 1)
            If Asc(c) < 53 Then 'tip 01234
                map(x, y).tip = Val(c)
                If Val(c) = 4 Then 'jail
                    jailx = x
                    jaily = y
                    ''''Call set_startxy(jailx, jaily, startx, starty, startsmer)
                End If
            Else    'semafor
                map(x, y).tip = 5 'cesta & semafor
                'decode semaphors
                map(x, y).semafor = Asc(c) - 52 'semaforData(Asc(c) - 52)
            
            End If
            x = x + 1
        Next j
        y = y + 1
    Next i
    Call set_startxy(jailx, jaily, startx, starty, startsmer)


    x = 1: y = 1
    For i = 1 To dimy   'price ranges from 20 to 45 (A to Z)
        Line Input #1, s
        x = 1
        For j = 1 To dimx
            c = Mid(s, j, 1)
            map(x, y).price = Asc(c) - 45
            x = x + 1
        Next j
        y = y + 1
    Next i
    
    x = 1: y = 1
    For i = 1 To dimy   'stage
        Line Input #1, s
        x = 1
        For j = 1 To dimx
            c = Mid(s, j, 1)
            map(x, y).stage = Val(c)
            x = x + 1
        Next j
        y = y + 1
    Next i
    
    x = 1: y = 1
    For i = 1 To dimy   'owner
        Line Input #1, s
        x = 1
        For j = 1 To dimx
            c = Mid(s, j, 1)
            map(x, y).owner = Val(c)
            x = x + 1
        Next j
        y = y + 1
    Next i
    
    Close 1
    
End Sub

Sub set_startxy(jailx, jaily, startx, starty, startsmer)
    'kje je cesta sosedno od jaila
    startsmer = 0
    If (map(jailx, jaily + 1).tip = 0) And (jaily + 1 <= dimy) Then 'najdu cesto
        startx = jailx: starty = jaily + 1
        'smer
        If (map(startx, starty + 1).tip = 0) And (starty + 1 <= dimy) Then 'najdu cesto
            startsmer = 2 'south
        End If
        If (map(startx, starty - 1).tip = 0) And (starty - 1 > 0) Then 'najdu cesto
            startsmer = 1 'north
        End If
        If (map(startx + 1, starty).tip = 0) And (startx + 1 <= dimx) Then 'najdu cesto
            startsmer = 4 'east
        End If
        If (map(startx - 1, starty).tip = 0) And (startx - 1 > 0) Then 'najdu cesto
            startsmer = 3 'west
        End If
    End If
    If (map(jailx, jaily - 1).tip = 0) And (jaily - 1 > 0) Then 'najdu cesto
        startx = jailx: starty = jaily - 1
        'smer
        If (map(startx, starty + 1).tip = 0) And (starty + 1 <= dimy) Then 'najdu cesto
            startsmer = 2 'south
        End If
        If (map(startx, starty - 1).tip = 0) And (starty - 1 > 0) Then 'najdu cesto
            startsmer = 1 'north
        End If
        If (map(startx + 1, starty).tip = 0) And (startx + 1 <= dimx) Then 'najdu cesto
            startsmer = 4 'east
        End If
        If (map(startx - 1, starty).tip = 0) And (startx - 1 > 0) Then 'najdu cesto
            startsmer = 3 'west
        End If
    End If
    If (map(jailx + 1, jaily).tip = 0) And (jailx + 1 <= dimx) Then 'najdu cesto
        startx = jailx + 1: starty = jaily
        'smer
        If (map(startx, starty + 1).tip = 0) And (starty + 1 <= dimy) Then 'najdu cesto
            startsmer = 2 'south
        End If
        If (map(startx, starty - 1).tip = 0) And (starty - 1 > 0) Then 'najdu cesto
            startsmer = 1 'north
        End If
        If (map(startx + 1, starty).tip = 0) And (startx + 1 <= dimx) Then 'najdu cesto
            startsmer = 4 'east
        End If
        If (map(startx - 1, starty).tip = 0) And (startx - 1 > 0) Then 'najdu cesto
            startsmer = 3 'west
        End If
    End If
    If (map(jailx - 1, jaily).tip = 0) And (jailx - 1 > 0) Then 'najdu cesto
        startx = jailx - 1: starty = jaily
        'smer
        If (map(startx, starty + 1).tip = 0) And (starty + 1 <= dimy) Then 'najdu cesto
            startsmer = 2 'south
        End If
        If (map(startx, starty - 1).tip = 0) And (starty - 1 > 0) Then 'najdu cesto
            startsmer = 1 'north
        End If
        If (map(startx + 1, starty).tip = 0) And (startx + 1 <= dimx) Then 'najdu cesto
            startsmer = 4 'east
        End If
        If (map(startx - 1, starty).tip = 0) And (startx - 1 > 0) Then 'najdu cesto
            startsmer = 3 'west
        End If
    End If
    
    If startsmer = 0 Then
        Beep
        startsmer = 1   'default da ne zabagira
    End If
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

Sub generate_default_map(x, y)
    Dim s, xs1, xs2, pm, sema, semb, i
    
    'roads
    sema = ":"  'default semaforja
    semb = "X"
    pm = 1
    If Rnd > 0.5 Then pm = -1
    xs1 = 3 + Int((x - 6 - 1 + 1) * Rnd + 1)
    
    Open App.Path & "\default.map" For Output As #1
    s = Trim(Str(x))
    Print #1, s
    s = Trim(Str(y))
    Print #1, s
    s = String(x, "1")
    s = put_road(s, xs1 + Int((4 - 1 + 1) * Rnd + 1) - 2, "2")        'school
    Print #1, s
    s = "4" & String(x - 2, "0") & "1"  'jail
    s = put_road(s, xs1, sema)
    Print #1, s
    For i = 3 To y - 2  'notranja cesta
        s = "10" & String(x - 4, "1") & "01"
        s = put_road(s, xs1, "0")
        If Rnd > 0.6 Then   'ovinek
            If (xs1 > 3) And (xs1 < (x - 3)) Then
                pm = 1
                If Rnd > 0.5 Then pm = -1
                xs1 = xs1 + pm
                s = put_road(s, xs1, "0")
            End If
        End If
        Print #1, s
    Next i
    s = "1" & String(x - 2, "0") & "3"  'job
    s = put_road(s, xs1, semb)
    Print #1, s
    s = String(x, "1")
    Print #1, s
    
    'price
    For i = 1 To y
        pm = i
        If pm > 24 Then pm = 1
        s = String(x, Mid("ABCDEFGHIJKLMNOPQRSTUVWXYZ", pm, 1))
        Print #1, s
    Next i
    'stage
    For i = 1 To y
        s = String(x, "0")
        Print #1, s
    Next i
    'owner
    For i = 1 To y
        s = String(x, "0")
        Print #1, s
    Next i
    
    Close 1
End Sub

Function put_road(s, x, c)
    Dim ss
    ss = Left(s, x - 1) & c & Right(s, Len(s) - x)
    put_road = ss
End Function

Sub fill_combo()
    Dim i
    Combo1.Clear
    If File1.ListCount > 0 Then
        For i = 0 To File1.ListCount - 1
            Combo1.AddItem File1.List(i)
        Next i
    End If
End Sub
