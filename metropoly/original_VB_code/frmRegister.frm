VERSION 5.00
Object = "{20C62CAE-15DA-101B-B9A8-444553540000}#1.1#0"; "MSMAPI32.OCX"
Begin VB.Form frmRegister 
   BackColor       =   &H00C0C0C0&
   BorderStyle     =   3  'Fixed Dialog
   ClientHeight    =   4080
   ClientLeft      =   45
   ClientTop       =   285
   ClientWidth     =   5145
   Icon            =   "frmRegister.frx":0000
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form2"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   4080
   ScaleWidth      =   5145
   ShowInTaskbar   =   0   'False
   StartUpPosition =   3  'Windows Default
   Begin MSMAPI.MAPISession MAPISession1 
      Left            =   3180
      Top             =   510
      _ExtentX        =   1005
      _ExtentY        =   1005
      _Version        =   327680
      DownloadMail    =   -1  'True
      LogonUI         =   -1  'True
      NewSession      =   0   'False
   End
   Begin MSMAPI.MAPIMessages MAPImsg 
      Left            =   3270
      Top             =   420
      _ExtentX        =   1005
      _ExtentY        =   1005
      _Version        =   327680
      AddressEditFieldCount=   1
      AddressModifiable=   0   'False
      AddressResolveUI=   0   'False
      FetchSorted     =   0   'False
      FetchUnreadOnly =   0   'False
   End
   Begin VB.CommandButton cmdClose 
      Caption         =   "Close"
      Height          =   345
      Left            =   3240
      TabIndex        =   31
      Top             =   3695
      Width           =   1860
   End
   Begin VB.CommandButton cmdEnterSN 
      DownPicture     =   "frmRegister.frx":030A
      Height          =   585
      Left            =   4515
      Picture         =   "frmRegister.frx":0614
      Style           =   1  'Graphical
      TabIndex        =   30
      Top             =   2265
      Width           =   615
   End
   Begin VB.CommandButton cmdSendemail 
      DownPicture     =   "frmRegister.frx":091E
      Height          =   585
      Left            =   3855
      Picture         =   "frmRegister.frx":0C28
      Style           =   1  'Graphical
      TabIndex        =   29
      Top             =   2265
      Width           =   615
   End
   Begin VB.CommandButton cmdSendmail 
      DownPicture     =   "frmRegister.frx":0F32
      Height          =   585
      Left            =   3855
      Picture         =   "frmRegister.frx":123C
      Style           =   1  'Graphical
      TabIndex        =   28
      Top             =   2265
      Width           =   615
   End
   Begin VB.CommandButton cmdPrint 
      Height          =   585
      Left            =   3195
      Picture         =   "frmRegister.frx":1546
      Style           =   1  'Graphical
      TabIndex        =   27
      Top             =   2265
      Width           =   615
   End
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Interval        =   42
      Left            =   3225
      Top             =   165
   End
   Begin VB.Frame Frame1 
      BackColor       =   &H00C0C0C0&
      Height          =   4035
      Left            =   15
      TabIndex        =   0
      Top             =   0
      Width           =   3045
      Begin VB.CheckBox Check1 
         Height          =   240
         Left            =   105
         TabIndex        =   24
         Top             =   3720
         Width           =   2850
      End
      Begin VB.Frame Frame5 
         BackColor       =   &H00C0C0C0&
         Height          =   1500
         Index           =   1
         Left            =   60
         TabIndex        =   15
         Top             =   2175
         Width           =   2910
         Begin VB.TextBox txtmail 
            Height          =   285
            Index           =   3
            Left            =   1260
            TabIndex        =   19
            Top             =   1155
            Width           =   1560
         End
         Begin VB.TextBox txtmail 
            Height          =   285
            Index           =   2
            Left            =   1260
            TabIndex        =   18
            Top             =   840
            Width           =   1560
         End
         Begin VB.TextBox txtmail 
            Height          =   285
            Index           =   1
            Left            =   1260
            TabIndex        =   17
            Top             =   540
            Width           =   1560
         End
         Begin VB.TextBox txtmail 
            Height          =   285
            Index           =   0
            Left            =   1260
            TabIndex        =   16
            Top             =   240
            Width           =   1560
         End
         Begin VB.Label labelmail 
            Alignment       =   1  'Right Justify
            BackStyle       =   0  'Transparent
            Caption         =   "Name:"
            Height          =   270
            Index           =   3
            Left            =   105
            TabIndex        =   23
            Top             =   1170
            Width           =   1095
         End
         Begin VB.Label labelmail 
            Alignment       =   1  'Right Justify
            BackStyle       =   0  'Transparent
            Caption         =   "Name:"
            Height          =   270
            Index           =   2
            Left            =   105
            TabIndex        =   22
            Top             =   870
            Width           =   1095
         End
         Begin VB.Label labelmail 
            Alignment       =   1  'Right Justify
            BackStyle       =   0  'Transparent
            Caption         =   "Name:"
            Height          =   270
            Index           =   1
            Left            =   105
            TabIndex        =   21
            Top             =   555
            Width           =   1095
         End
         Begin VB.Label labelmail 
            Alignment       =   1  'Right Justify
            BackStyle       =   0  'Transparent
            Caption         =   "Name:"
            Height          =   270
            Index           =   0
            Left            =   105
            TabIndex        =   20
            Top             =   255
            Width           =   1095
         End
      End
      Begin VB.Frame Frame5 
         BackColor       =   &H00C0C0C0&
         Height          =   615
         Index           =   0
         Left            =   60
         TabIndex        =   13
         Top             =   2175
         Width           =   2910
         Begin VB.TextBox txtemail 
            Height          =   285
            Left            =   90
            TabIndex        =   14
            Top             =   240
            Width           =   2745
         End
      End
      Begin VB.Frame Frame3 
         BackColor       =   &H00C0C0C0&
         Height          =   1095
         Left            =   60
         TabIndex        =   6
         Top             =   1080
         Width           =   1800
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   4
            Left            =   120
            TabIndex        =   9
            TabStop         =   0   'False
            Tag             =   "default"
            Top             =   240
            Width           =   1545
         End
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   5
            Left            =   120
            TabIndex        =   8
            TabStop         =   0   'False
            Top             =   480
            Width           =   1575
         End
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   6
            Left            =   120
            TabIndex        =   7
            TabStop         =   0   'False
            Top             =   720
            Width           =   1575
         End
      End
      Begin VB.Frame Frame2 
         BackColor       =   &H00C0C0C0&
         Height          =   825
         Left            =   60
         TabIndex        =   1
         Top             =   195
         Width           =   2925
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   3
            Left            =   1440
            TabIndex        =   5
            TabStop         =   0   'False
            Tag             =   "disabled"
            Top             =   480
            Width           =   1215
         End
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   2
            Left            =   1440
            TabIndex        =   4
            TabStop         =   0   'False
            Tag             =   "disabled"
            Top             =   240
            Width           =   1215
         End
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   3
            TabStop         =   0   'False
            Tag             =   "default"
            Top             =   480
            Width           =   1215
         End
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   2
            TabStop         =   0   'False
            Top             =   240
            Width           =   1215
         End
      End
      Begin VB.Frame Frame4 
         BackColor       =   &H00C0C0C0&
         Height          =   1095
         Left            =   1800
         TabIndex        =   10
         Top             =   1080
         Width           =   1185
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   8
            Left            =   120
            TabIndex        =   12
            TabStop         =   0   'False
            Tag             =   "default"
            Top             =   480
            Width           =   975
         End
         Begin VB.OptionButton Option1 
            BackColor       =   &H00C0C0C0&
            Height          =   255
            Index           =   7
            Left            =   120
            TabIndex        =   11
            TabStop         =   0   'False
            Top             =   240
            Width           =   945
         End
      End
      Begin VB.Image Image1 
         Height          =   480
         Index           =   1
         Left            =   1725
         Picture         =   "frmRegister.frx":1850
         Top             =   2925
         Width           =   480
      End
      Begin VB.Image Image1 
         Height          =   480
         Index           =   2
         Left            =   1260
         Picture         =   "frmRegister.frx":1B5A
         Top             =   3060
         Width           =   480
      End
      Begin VB.Image Image1 
         Height          =   480
         Index           =   0
         Left            =   675
         Picture         =   "frmRegister.frx":1E64
         Top             =   3060
         Width           =   480
      End
   End
   Begin VB.CommandButton Command1 
      Caption         =   "OK"
      Height          =   345
      Left            =   2160
      TabIndex        =   25
      Top             =   3695
      Width           =   840
   End
   Begin VB.CheckBox checkGame 
      BackColor       =   &H00C0C0C0&
      Height          =   285
      Index           =   0
      Left            =   3300
      TabIndex        =   26
      Top             =   945
      Width           =   3045
   End
   Begin VB.Image Image2 
      Appearance      =   0  'Flat
      Height          =   870
      Left            =   3795
      Picture         =   "frmRegister.frx":216E
      Stretch         =   -1  'True
      Top             =   315
      Width           =   900
   End
   Begin VB.Line Line1 
      X1              =   3120
      X2              =   3120
      Y1              =   120
      Y2              =   4005
   End
   Begin VB.Image Image3 
      Height          =   645
      Left            =   4335
      Picture         =   "frmRegister.frx":2478
      Top             =   135
      Width           =   690
   End
   Begin VB.Label labelprice 
      Alignment       =   1  'Right Justify
      BackStyle       =   0  'Transparent
      Caption         =   "18 $"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   238
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   270
      Index           =   2
      Left            =   2280
      TabIndex        =   34
      Top             =   3360
      Width           =   2775
   End
   Begin VB.Label labelprice 
      Alignment       =   1  'Right Justify
      BackStyle       =   0  'Transparent
      Caption         =   "18 $"
      Height          =   210
      Index           =   1
      Left            =   2685
      TabIndex        =   33
      Top             =   3150
      Width           =   2355
   End
   Begin VB.Label labelprice 
      Alignment       =   1  'Right Justify
      BackStyle       =   0  'Transparent
      Caption         =   "18 $"
      Height          =   210
      Index           =   0
      Left            =   2850
      TabIndex        =   32
      Top             =   2940
      Width           =   2190
   End
   Begin VB.Image Image5 
      Height          =   1365
      Left            =   3330
      Picture         =   "frmRegister.frx":30CA
      Top             =   1170
      Visible         =   0   'False
      Width           =   1965
   End
   Begin VB.Image Image4 
      Height          =   1365
      Left            =   3315
      Picture         =   "frmRegister.frx":BDD0
      Top             =   1170
      Width           =   1965
   End
End
Attribute VB_Name = "frmRegister"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
Dim t1, sendbymailprompt, tprice(3), tTo, tSubject, tEnterSN
Dim y1     'orig top position for frame
Dim y2     'hidden position
Dim y      'during scroll
Dim yreq   'required position
Dim amount As Integer

Private Sub Check1_Click()
    If Check1.Value = 1 Then
        'hide frame1
        yreq = y2
        y = Frame1.Top
        cmdPrint.Enabled = False
        Timer1.Enabled = True
    Else
    End If
    calcprice   'mora biti tu zaradi updatea
End Sub


Private Sub checkGame_Click(Index As Integer)
    calcprice
End Sub

Private Sub cmdClose_Click()
    Unload Me
End Sub

Private Sub cmdEnterSN_Click()
    Beep
    
'    Dim s, i, j, napak, ini(50)
'    s = InputBox(tEnterSN, , serialNumber)
'    If Len(s) <> 20 Then Exit Sub
'    napak = False
'    For i = 1 To 20
'        If InStr(1, "ABCDEFGHIJKLMNOPRSTQRSTUVWXYZ", Mid(s, i, 1)) = 0 Then napak = True
'    Next i
'    If napak Then Exit Sub
'
'    'change SN
'    serialNumber = s
'
'    If Year(Now) > 2100 Then    'make freeware
'        serialNumber = "R" & Right(serialNumber, 19)
'    End If
'
'    'visibliraj igre
'    If Left(serialNumber, 1) = "R" Then
'        For i = 0 To Form1.mnuGames.Count - 1
'            If Not Form1.mnuGames.Item(i).Visible Then Form1.mnuGames.Item(i).Visible = True
'            If Not Form1.mnuGames.Item(i).Enabled Then Form1.mnuGames.Item(i).Enabled = True
'        Next i
'    End If
'    If Left(serialNumber, 1) = "P" Then
'        For i = 0 To Form1.mnuGames.Count - 1
'            If InStr(1, "AEIOU", Mid(serialNumber, i + 2, 1)) = 0 Then
'                If Not Form1.mnuGames.Item(i).Enabled Then Form1.mnuGames.Item(i).Enabled = True
'            End If
'            If InStr(1, "BCDFG", Mid(serialNumber, i + 2, 1)) = 0 Then
'                If Not Form1.mnuGames.Item(i).Visible Then Form1.mnuGames.Item(i).Visible = True
'            End If
'        Next i
'    End If
'
'    'write sn v ini
'    Open App.Path & "\cardgame.ini" For Input As 1
'    i = 0
'    Do
'        i = i + 1
'        Line Input #1, ini(i)
'        If i > 1 Then
'            If ini(i - 1) = "[SHAREWARE]" Then
'                If Left(ini(i), 13) = "SerialNumber=" Then 'new sn
'                    ini(i) = "SerialNumber=" & serialNumber
'                End If
'            End If
'        End If
'    Loop Until EOF(1)
'    Close 1
'    Open App.Path & "\cardgame.ini" For Output As 1
'    For j = 1 To i
'        Print #1, ini(j)
'    Next j
'    Close 1

End Sub

Private Sub cmdPrint_Click()
    'data validation
    If Option1(7).Value Then    'mail
        If (txtmail(0).Text = "") Or (txtmail(1).Text = "") Or (txtmail(2).Text = "") Or (txtmail(3).Text = "") Then
            Beep
            Exit Sub
        End If
    Else    'email
        If (txtemail.Text = "") Or (InStr(1, txtemail.Text, "@") = 0) Then
            Beep
            Exit Sub
        End If
    End If
    Screen.MousePointer = vbHourglass
    On Error Resume Next
    
    'prepare info o delni registraciji
    Dim i, orig1, orig2, orig3, orig4, c
    c = QBColor(15)
    orig4 = Me.BackColor
    For i = 0 To checkGame.Count - 1: checkGame(i).Enabled = False: Next i
    orig1 = Frame1.Left   '=x1
    If Check1.Value = 1 Then
        For i = 0 To checkGame.Count - 1: checkGame(i).BackColor = c: Next i
        Frame1.Left = Frame1.Left + Check1.Height
    End If
    cmdPrint.Visible = False
    orig2 = cmdSendmail.Visible: cmdSendmail.Visible = False
    orig3 = cmdSendemail.Visible: cmdSendemail.Visible = False
    cmdEnterSN.Visible = False
    For i = 0 To 2: labelprice(i).Visible = False: Next i
    cmdClose.Visible = False
    'white
    Me.BackColor = c
    Image4.Visible = False: Image5.Visible = True
    For i = 0 To 8: Option1(i).BackColor = c: Next i
    Frame1.BackColor = c: Frame2.BackColor = c: Frame3.BackColor = c: Frame4.BackColor = c
    Frame5(0).BackColor = c: Frame5(1).BackColor = c
    txtemail.BackColor = c
    For i = 0 To 3: txtmail(i).BackColor = c: Next i
    Check1.BackColor = c
    
    '--------------
    Me.PrintForm
    '--------------

    'unprepare
    For i = 1 To checkGame.Count - 1: checkGame(i).Enabled = True: Next i
    If Check1.Value = 1 Then
        If Frame1.Left <> orig1 Then Frame1.Left = orig1
        For i = 0 To checkGame.Count - 1: checkGame(i).BackColor = c: Next i
    End If
    cmdPrint.Visible = True
    cmdSendmail.Visible = orig2
    cmdSendemail.Visible = orig3
    cmdEnterSN.Visible = True
    For i = 0 To 2: labelprice(i).Visible = True: Next i
    cmdClose.Visible = True
    'gray
    c = orig4
    Me.BackColor = c
    Image4.Visible = True: Image5.Visible = False
    For i = 0 To 8: Option1(i).BackColor = c: Next i
    Frame1.BackColor = c: Frame2.BackColor = c: Frame3.BackColor = c: Frame4.BackColor = c
    Frame5(0).BackColor = c: Frame5(1).BackColor = c
    txtemail.BackColor = c
    For i = 0 To 3: txtmail(i).BackColor = c: Next i
    Check1.BackColor = c
    Screen.MousePointer = vbDefault
End Sub

Private Sub cmdSendemail_Click()
    Beep
'    'set To, Subject
'    'required serialnumber
'    'amount
'    'e-mail, addr
'    'options (cd,floppy)
'
'    'data validation
'    If Option1(7).Value Then    'mail
'        If (txtmail(0).Text = "") Or (txtmail(1).Text = "") Or (txtmail(2).Text = "") Or (txtmail(3).Text = "") Then
'            Beep
'            Exit Sub
'        End If
'    Else    'email
'        If (txtemail.Text = "") Or (InStr(1, txtemail.Text, "@") = 0) Then
'            Beep
'            Exit Sub
'        End If
'    End If
'
'    Dim sn, a, addr, o, s
'    sn = "AFULLREGISTRATIONPLE"                 'full reg. - POTEM NAROCNIKU VRNEM "RFULLREGISTRATIONPLE" (prva crka bistvena)
'    If Check1.Value = 1 Then sn = calcreqSN     'part reg. - potem vrnem "P..."
'
'    s = "CardGames registration request from "
'    s = s & txtemail
''    s = s & " , " & txtmail(0) & " , "
''    s = s & " , " & txtmail(1)
''    s = s & " , " & txtmail(2)
'    s = s & " . His temp. s.n.=" & sn
'    s = s & ". He will pay " & amount & " $."
'    If Option1(0).Value Then s = s & " Method of payment: cash."
'    If Option1(1).Value Then s = s & " Method of payment: money order."
'    'If Option1(2).Value Then s = s & " Method of payment: cheque."
'    'If Option1(3).Value Then s = s & " Method of payment: credit card."
'    ''If Option1(5).Value Then s = s & " He requests floppy disc version."
'    ''If Option1(6).Value Then s = s & " He requests CD-ROM version."
'
'    On Error GoTo mapierr
'    MAPISession1.SignOn
'    MAPImsg.Compose
'    MAPImsg.RecipAddress = "miha11@yahoo.com"
'    MAPImsg.MsgSubject = s
'    'mapimsg.show
'    MAPImsg.Send (1)        'MAPImsg.Send (vdialog)
'    MAPISession1.SignOff
'
'
'    Exit Sub
'mapierr:
'    Dim erd
'    erd = Err.Description & Chr(13) & Chr(10) & Chr(13) & Chr(10)
'    erd = erd & tTo & " miha11@yahoo.com" & Chr(13) & Chr(10)
'    erd = erd & tSubject & " " & s
'    MsgBox erd
End Sub
Function calcreqSN()
    Dim s, i
    s = "P" 'part registration (only to certain games)
    For i = 0 To checkGame.Count - 1
        If checkGame(i).Value = 1 Then
            s = s & Mid("JKLMN", Int(Rnd * 5) + 1, 1)
        Else
            s = s & Mid("AEIOU", Int(Rnd * 5) + 1, 1)
        End If
    Next i
    s = s & "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
    s = Left(s, 20)
    calcreqSN = s
End Function
Private Sub cmdSendmail_Click()
    MsgBox sendbymailprompt, , lngg(15)
End Sub

Private Sub Command1_Click()
    'hide game list (show frame1)
    yreq = y1
    y = Frame1.Top
    Timer1.Enabled = True
    calcprice
    cmdPrint.Enabled = True
End Sub

Private Sub Form_KeyDown(KeyCode As Integer, Shift As Integer)
    Select Case KeyCode
    Case 27
        Unload Me
    Case 112    'F1
        MsgBox t1   'a zazene se tudi help file
    End Select
End Sub

Private Sub Form_Load()
    Me.Top = (Screen.Height - Me.Height) / 2
    Me.Left = (Screen.Width - Me.Width) / 2
    preparehiddengamelist
    formcaptions
    y1 = Frame1.Top
    y2 = y1 + Frame1.Height + Check1.Height
End Sub

Sub formcaptions()
    'captions
    On Error GoTo failregister
    Dim i, s
    For i = 0 To 8
        If Option1(i).Tag = "default" Then
            Option1(i).Value = True
        End If
    Next i
    
    Open App.Path & "\" & selectedLanguage & ".txt" For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[Registration form]"
    If s = "[Registration form]" Then
        Line Input #1, s: Me.Caption = s
        
        Line Input #1, s    '---
        t1 = ""
        Do
            Line Input #1, s
            If s <> "---" Then t1 = t1 & Chr(13) & Chr(10) & s
        Loop Until s = "---" Or EOF(1)
        If EOF(1) Then GoTo failregister
        'Image1(0).ToolTipText = t1
        
        Line Input #1, s    'I want to buy Card Games
        Frame1.Caption = s
        Line Input #1, s    'empty line (n/a)
        
        Line Input #1, s    'I will pay with
        Frame2.Caption = s
        
        Line Input #1, s
        Option1(0).Caption = s
        Line Input #1, s
        Option1(1).Caption = s
        Line Input #1, s
        Option1(2).Caption = s
        Line Input #1, s
        Option1(3).Caption = s
        Line Input #1, s    'visa
        Line Input #1, s    'mastercard
        Line Input #1, s    'other...
        Line Input #1, s    '
        
        Line Input #1, s    'I want to receive
        Frame3.Caption = s
        Line Input #1, s
        Option1(4).Caption = s
        Line Input #1, s
        Option1(5).Caption = s
        Line Input #1, s
        Option1(6).Caption = s
        Line Input #1, s
        
        Line Input #1, s    'I want to receive the product
        Line Input #1, s    'by mail
        Option1(7).Caption = s
        Line Input #1, s    'by e-mail
        Option1(8).Caption = s
        For i = 0 To 8
            If Option1(i).Tag = "disabled" Then Option1(i).Enabled = False
        Next i
        
        Line Input #1, s    'my address
        Frame5(1).Caption = s
        Line Input #1, s    'my e-mail
        Frame5(0).Caption = s
        Line Input #1, s    'name
        labelmail(0).Caption = s
        Line Input #1, s    'street
        labelmail(1).Caption = s
        Line Input #1, s    'city
        labelmail(2).Caption = s
        Line Input #1, s    'ZIP code
        Line Input #1, s    'state
        Line Input #1, s    'country
        labelmail(3).Caption = s
        Line Input #1, s    '
        
        Line Input #1, s    'I don't want all of the games
        Check1.Caption = s
        Line Input #1, s    '(this will reduce the cost)
        Check1.ToolTipText = s
        Line Input #1, s    '
        
        Line Input #1, s    'Amount
        tprice(0) = s
        Line Input #1, s    'Shipment cost
        tprice(1) = s
        Line Input #1, s    'Total amount
        tprice(2) = s
        Line Input #1, s    '---
        
        Line Input #1, s    'Print registration; Form
        cmdPrint.ToolTipText = s & " "
        Line Input #1, s    'Send order by mail
        cmdSendmail.ToolTipText = s & " "
        Line Input #1, s    'To send order by mail, print registration form and send it to ...
        sendbymailprompt = s
        Line Input #1, s    'Send order by e-mail
        cmdSendemail.ToolTipText = s & " "
        If Option1(7).Value Then
            cmdSendmail.Visible = True
            cmdSendemail.Visible = False
        Else
            cmdSendmail.Visible = False
            cmdSendemail.Visible = True
        End If
        Line Input #1, s    'Enter serial number
        cmdEnterSN.ToolTipText = s & " "
        tEnterSN = s
        Line Input #1, s    'OK
        Command1.Caption = s
        Line Input #1, s    'Close
        cmdClose.Caption = s
        
        Line Input #1, s    '---
        Line Input #1, s    'To:
        tTo = s
        Line Input #1, s    'Subject:
        tSubject = s
        
        calcprice
        
        
    Else
        GoTo failregister
    End If
    
    Close 1
    Exit Sub


failregister:   'error in language file (missing text)
    On Error Resume Next
    Close 1     'bug??
    'Unload Me  'zablokira
    Me.Hide
End Sub



Private Sub Option1_Click(Index As Integer)
    Select Case Index
    Case 4      'serial number
        'can be sent by e-mail
        Option1(8).Enabled = True
        If Not Option1(8).Value Then Option1_Click (8)
        calcprice
    Case 5, 6   'floppy, cd-rom
        'cant be sent by e-mail
        If Option1(8).Value Then Option1_Click (7)
        Option1(8).Enabled = False
        calcprice
    Case 7  'mail
        Option1(7).Value = True
        Frame5(0).Visible = False
        Frame5(1).Visible = True
        calcprice
    Case 8  'e-mail
        Option1(8).Value = True
        Frame5(0).Visible = True
        Frame5(1).Visible = False
        calcprice
    End Select
    
    If (Index = 7) Or (Index = 8) Then
        If Option1(7).Value Then
            cmdSendmail.Visible = True
            cmdSendemail.Visible = False
        Else
            cmdSendmail.Visible = False
            cmdSendemail.Visible = True
        End If
    End If
End Sub

Private Sub Timer1_Timer()
    'animate show/hide frame
    Dim d
    If y = yreq Then
        Timer1.Enabled = False
    
    Else
        d = Abs(y - yreq) / 10
    
        If y > yreq Then y = y - d
        If y < yreq Then y = y + d
        If d < 10 Then y = yreq
        Frame1.Top = y
    End If
    
End Sub
Sub preparehiddengamelist()
    Dim i, j, h, s, g(50)
    checkGame(0).Top = y1
    checkGame(0).Left = Frame1.Left
    h = Check1.Height * 1.3 'line height
    
    i = 0
    Open App.Path & "\" & selectedLanguage & ".txt" For Input As 1
    Do
        Line Input #1, s
        If s = "[GAMENAME]" Then    'add
            Line Input #1, g(i)
            i = i + 1
        End If
    Loop Until EOF(1) Or i > 50
    Close 1
    
    checkGame(0).Caption = g(0)
    checkGame(0).Value = 1
    For j = 1 To i - 1
        Load checkGame(j)
        checkGame(j).Caption = g(j)
        checkGame(j).Top = y1 + j * h
        checkGame(j).Left = Frame1.Left
        'checkGame(j).ZOrder 1
        checkGame(j).Visible = True
        checkGame(j).Value = 1
    Next j
    checkGame(0).Enabled = False    'Free Cell is obligatory

End Sub

Sub calcprice()
    Dim s, i, a
    Dim enaigra, shipment, shipmente, floppy, cd   'price in $
    enaigra = 3:    shipment = 5:    shipmente = 2
    floppy = 3: cd = 6
    
    'Amount
    a = 0
    If Check1.Value = 1 Then 'some games
        For i = 0 To checkGame.Count - 1
            If checkGame(i).Value = 1 Then a = a + enaigra
        Next i
        If Option1(5).Value Then a = a + floppy
        If Option1(6).Value Then a = a + cd
        's = tprice(0) & "....." & Trim(a) & " $"
        s = tprice(0) & "....." & Trim(a) & " " & lngg(85)
    Else
        a = checkGame.Count
        If a <= 0 Then a = 1
        If Option1(5).Value Then a = a + floppy
        If Option1(6).Value Then a = a + cd
        'if left(serialnumber,1)="P" then 'dokup iger (discount)
        '...
        s = tprice(0) & "....." & Trim(a) & " " & lngg(85)
    End If
        
    
    If s <> labelprice(0) Then labelprice(0) = s
    
    'Shipment
    If Option1(7).Value Then
        s = tprice(1) & "....." & shipment & " " & lngg(85)
        a = a + shipment
    Else    '0
        s = tprice(1) & "....." & shipmente & " " & lngg(85)
        a = a + shipmente
    End If
    If s <> labelprice(1) Then labelprice(1) = s
    
    'Total
    s = tprice(2) & "..." & Trim$(a) & " " & lngg(85)
    If s <> labelprice(2) Then labelprice(2) = s
    amount = Trim(a)
End Sub
