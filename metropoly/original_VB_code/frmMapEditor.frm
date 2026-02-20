VERSION 5.00
Begin VB.Form frmMapEditor 
   Caption         =   "Map Editor"
   ClientHeight    =   2535
   ClientLeft      =   60
   ClientTop       =   300
   ClientWidth     =   2580
   Icon            =   "frmMapEditor.frx":0000
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form1"
   ScaleHeight     =   2535
   ScaleWidth      =   2580
   StartUpPosition =   3  'Windows Default
   Begin VB.Frame Frame2 
      Caption         =   "New"
      Height          =   1000
      Left            =   45
      TabIndex        =   5
      Top             =   0
      Width           =   2475
      Begin VB.TextBox Text1 
         Enabled         =   0   'False
         Height          =   285
         Index           =   3
         Left            =   1845
         TabIndex        =   11
         TabStop         =   0   'False
         Text            =   "1"
         Top             =   210
         Width           =   500
      End
      Begin VB.TextBox Text1 
         Enabled         =   0   'False
         Height          =   285
         Index           =   2
         Left            =   1845
         TabIndex        =   10
         TabStop         =   0   'False
         Text            =   "1"
         Top             =   510
         Width           =   500
      End
      Begin VB.TextBox Text1 
         Height          =   285
         Index           =   0
         Left            =   570
         TabIndex        =   7
         TabStop         =   0   'False
         Top             =   210
         Width           =   500
      End
      Begin VB.TextBox Text1 
         Height          =   285
         Index           =   1
         Left            =   570
         TabIndex        =   6
         TabStop         =   0   'False
         Top             =   510
         Width           =   500
      End
      Begin VB.Image Image2 
         Height          =   300
         Left            =   1440
         Stretch         =   -1  'True
         Top             =   495
         Width           =   300
      End
      Begin VB.Image Image1 
         Height          =   300
         Left            =   1440
         Stretch         =   -1  'True
         Top             =   195
         Width           =   300
      End
      Begin VB.Label Label1 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "x:"
         Height          =   270
         Index           =   0
         Left            =   75
         TabIndex        =   9
         Top             =   225
         Width           =   420
      End
      Begin VB.Label Label1 
         Alignment       =   1  'Right Justify
         BackStyle       =   0  'Transparent
         Caption         =   "y:"
         Height          =   270
         Index           =   1
         Left            =   75
         TabIndex        =   8
         Top             =   510
         Width           =   420
      End
   End
   Begin VB.FileListBox File1 
      Height          =   1845
      Left            =   1785
      Pattern         =   "*.sav;*.map"
      TabIndex        =   2
      Top             =   3270
      Visible         =   0   'False
      Width           =   1335
   End
   Begin VB.CommandButton CommandCancel 
      Caption         =   "Cancel"
      Height          =   360
      Left            =   1395
      TabIndex        =   1
      Top             =   2100
      Width           =   915
   End
   Begin VB.CommandButton CommandOK 
      Caption         =   "OK"
      Height          =   360
      Left            =   360
      TabIndex        =   0
      Top             =   2100
      Width           =   900
   End
   Begin VB.Frame Frame1 
      Caption         =   "Open"
      Height          =   1000
      Left            =   60
      TabIndex        =   3
      Top             =   1020
      Width           =   2475
      Begin VB.ComboBox Combo1 
         Height          =   315
         ItemData        =   "frmMapEditor.frx":08CA
         Left            =   135
         List            =   "frmMapEditor.frx":08CC
         TabIndex        =   4
         TabStop         =   0   'False
         Top             =   270
         Width           =   1710
      End
   End
End
Attribute VB_Name = "frmMapEditor"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Dim fn  '.map file to open

Private Sub CommandCancel_Click()
    Me.Hide
End Sub

Private Sub CommandOK_Click()
    Dim x, y, i, j, c
    'prepare map, mapeditorMode:  1-new/2-current/3-open map
    mapEditorMode = 0   ''mode not found yet
    'current
    If (Text1(0).Text = "") And (Text1(1).Text = "") And (Combo1.Text = "") Then
        mapEditorMode = 2
        'current map is used
    End If
    'new
    If (Text1(0).Text <> "") And (Text1(1).Text <> "") Then
        x = Val(Text1(0))
        y = Val(Text1(1))
        If x < 7 Then x = 7
        If y < 7 Then y = 7
        mapEditorMode = 1
        'create empty map
        dimx = x: dimy = y
        For i = 1 To dimx
            For j = 1 To dimy
                map(i, j).tip = 1
                map(i, j).owner = 0
                map(i, j).stage = 0
                c = Mid("ABCDEFGHIJKLMNOPQRSTUVWXWZ", Int((25 - 1 + 1) * Rnd + 1), 1)
                map(i, j).price = Asc(c) - 45
                map(i, j).semafor = 33 '''naj bo nek default za vsak slucaj
            Next j
        Next i
        map(Int(dimx / 4), Int(dimy / 4)).tip = 2       'school
        map(Int(3 * dimx / 4), Int(dimy / 4)).tip = 3   'job
        map(Int(dimx / 2), Int(dimy / 2)).tip = 4       'jail
        map(Int(dimx / 2), Int(dimy / 2) + 1).tip = 0   'road
        map(Int(dimx / 2) + 1, Int(dimy / 2) + 1).tip = 0 'road
        map(Int(dimx / 2) - 1, Int(dimy / 2) + 1).tip = 0 'road
        
        jailx = Int(dimx / 2): jaily = Int(dimy / 2)
        startx = jailx: starty = jaily + 1: startsmer = 4   'desno
        Game.draw_map
        
    End If
    'open
    If Combo1.Text <> "" Then
        mapEditorMode = 3
        'open map
        NewGame.load_map App.Path & "\" & Combo1.Text
        Game.draw_map
    End If
    
    'prepare interface
    Game.begin_map_editor
    
    Me.Hide
    
End Sub

Private Sub Form_KeyPress(KeyAscii As Integer)
    If KeyAscii = 27 Then CommandCancel_Click
End Sub

Private Sub Form_Load()
    Me.Left = (Screen.Width - Me.Width) / 2
    Me.Top = (Screen.Height - Me.Height) / 2
    Image1.Picture = Game.ImageResource(17)     'school
    Image2.Picture = Game.ImageResource(18)     'job
    
    Dim i
    If File1.ListCount > 0 Then
        For i = 0 To File1.ListCount - 1
            Combo1.AddItem File1.List(i)
        Next i
    End If
End Sub

Private Sub Text1_Change(Index As Integer)
    'new excludes open
    Combo1.Text = ""
End Sub

