VERSION 5.00
Begin VB.Form Help 
   Caption         =   "Metropoly Help"
   ClientHeight    =   3180
   ClientLeft      =   60
   ClientTop       =   300
   ClientWidth     =   4680
   Icon            =   "help.frx":0000
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form1"
   ScaleHeight     =   3180
   ScaleWidth      =   4680
   StartUpPosition =   3  'Windows Default
   Begin VB.CommandButton CommandOK 
      Caption         =   "OK"
      Height          =   390
      Left            =   1830
      TabIndex        =   0
      Top             =   2655
      Width           =   1065
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "houses  on your land."
      Height          =   300
      Index           =   10
      Left            =   2415
      TabIndex        =   11
      Top             =   2040
      Width           =   1920
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "land. Buy "
      Height          =   300
      Index           =   9
      Left            =   1095
      TabIndex        =   10
      Top             =   2040
      Width           =   1545
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "Buy"
      Height          =   300
      Index           =   8
      Left            =   75
      TabIndex        =   9
      Top             =   2040
      Width           =   1395
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "money to earn."
      Height          =   300
      Index           =   7
      Left            =   3570
      TabIndex        =   8
      Top             =   1440
      Width           =   1110
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "school to learn and go to"
      Height          =   300
      Index           =   6
      Left            =   1155
      TabIndex        =   7
      Top             =   1440
      Width           =   2100
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "Go to "
      Height          =   300
      Index           =   5
      Left            =   75
      TabIndex        =   6
      Top             =   1440
      Width           =   1395
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "road."
      Height          =   300
      Index           =   4
      Left            =   3585
      TabIndex        =   5
      Top             =   915
      Width           =   735
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "dice and walk on the "
      Height          =   300
      Index           =   3
      Left            =   1410
      TabIndex        =   4
      Top             =   915
      Width           =   2100
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "You throw"
      Height          =   300
      Index           =   2
      Left            =   45
      TabIndex        =   3
      Top             =   915
      Width           =   1395
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "jail."
      Height          =   300
      Index           =   1
      Left            =   1590
      TabIndex        =   2
      Top             =   315
      Width           =   1395
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "You begin in"
      Height          =   300
      Index           =   0
      Left            =   60
      TabIndex        =   1
      Top             =   315
      Width           =   1395
   End
   Begin VB.Image Image7 
      Height          =   480
      Left            =   1785
      Picture         =   "help.frx":08CA
      Top             =   1875
      Width           =   480
   End
   Begin VB.Image Image6 
      Height          =   480
      Left            =   540
      Picture         =   "help.frx":1594
      Top             =   1860
      Width           =   480
   End
   Begin VB.Image Image5 
      Height          =   480
      Left            =   3000
      Picture         =   "help.frx":225E
      Top             =   1245
      Width           =   480
   End
   Begin VB.Image Image4 
      Height          =   480
      Left            =   675
      Picture         =   "help.frx":2568
      Top             =   1215
      Width           =   480
   End
   Begin VB.Image Image3 
      Height          =   480
      Left            =   2985
      Picture         =   "help.frx":3232
      Top             =   705
      Width           =   480
   End
   Begin VB.Image Image2 
      Height          =   480
      Left            =   915
      Picture         =   "help.frx":3E76
      Top             =   705
      Width           =   480
   End
   Begin VB.Image Image1 
      Height          =   480
      Left            =   1065
      Picture         =   "help.frx":4180
      Top             =   150
      Width           =   480
   End
End
Attribute VB_Name = "Help"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub CommandOK_Click()
    Me.Hide
End Sub

Private Sub Form_KeyPress(KeyAscii As Integer)
    If KeyAscii = 27 Then CommandOK_Click
End Sub

Private Sub Form_Load()
    Me.Left = (Screen.Width - Me.Width) / 2
    Me.Top = (Screen.Height - Me.Height) / 2
    Image1.Picture = LoadPicture(App.Path & "\icons\jail.ico")
    Image2.Picture = LoadPicture(App.Path & "\icons\dice5.ico")
    Image3.Picture = LoadPicture(App.Path & "\icons\roadlr.ico")
    Image4.Picture = LoadPicture(App.Path & "\icons\school.ico")
    Image5.Picture = LoadPicture(App.Path & "\icons\job.ico")
    Image6.Picture = LoadPicture(App.Path & "\icons\h0.ico")
    Image7.Picture = LoadPicture(App.Path & "\icons\h3.ico")
    
End Sub
