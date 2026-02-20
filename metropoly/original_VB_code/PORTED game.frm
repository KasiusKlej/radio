VERSION 5.00
Begin VB.Form Game 
   AutoRedraw      =   -1  'True
   Caption         =   "Metropoly"
   ClientHeight    =   4275
   ClientLeft      =   165
   ClientTop       =   645
   ClientWidth     =   7035
   Icon            =   "game.frx":0000
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form1"
   ScaleHeight     =   4275
   ScaleWidth      =   7035
   StartUpPosition =   3  'Windows Default
   Begin VB.Timer TimerSkokFigure 
      Enabled         =   0   'False
      Interval        =   500
      Left            =   1725
      Top             =   3585
   End
   Begin VB.Timer TimerMetKocke 
      Enabled         =   0   'False
      Interval        =   300
      Left            =   1230
      Top             =   3585
   End
   Begin VB.Timer TimerRefreshFigure 
      Interval        =   400
      Left            =   120
      Top             =   4980
   End
   Begin VB.PictureBox mapa 
      Appearance      =   0  'Flat
      AutoRedraw      =   -1  'True
      BackColor       =   &H80000005&
      ForeColor       =   &H80000008&
      Height          =   840
      Left            =   855
      ScaleHeight     =   54
      ScaleMode       =   3  'Pixel
      ScaleWidth      =   96
      TabIndex        =   0
      Top             =   4755
      Visible         =   0   'False
      Width           =   1470
   End
   Begin VB.Frame FrameStatus 
      Height          =   4215
      Left            =   3780
      TabIndex        =   1
      Top             =   0
      Width           =   3240
      Begin VB.PictureBox PictureStatus 
         AutoRedraw      =   -1  'True
         Height          =   4020
         Left            =   60
         ScaleHeight     =   3960
         ScaleWidth      =   3060
         TabIndex        =   2
         Top             =   150
         Width           =   3120
         Begin VB.Image ImageLandInfo 
            Height          =   1080
            Left            =   1005
            Stretch         =   -1  'True
            Top             =   375
            Visible         =   0   'False
            Width           =   1080
         End
         Begin VB.Label LabelStatus 
            BackStyle       =   0  'Transparent
            Height          =   195
            Left            =   15
            TabIndex        =   3
            Top             =   3750
            Width           =   3075
         End
      End
   End
   Begin VB.Frame FrameMapEditor 
      Height          =   4215
      Left            =   2490
      TabIndex        =   4
      Top             =   525
      Visible         =   0   'False
      Width           =   3240
      Begin VB.OptionButton OptionSelectedTool 
         Height          =   630
         Index           =   0
         Left            =   405
         TabIndex        =   9
         Top             =   375
         Value           =   -1  'True
         Width           =   500
      End
      Begin VB.OptionButton OptionSelectedTool 
         Height          =   630
         Index           =   1
         Left            =   405
         TabIndex        =   8
         Top             =   1110
         Width           =   500
      End
      Begin VB.OptionButton OptionSelectedTool 
         Height          =   630
         Index           =   2
         Left            =   405
         TabIndex        =   7
         Top             =   1860
         Width           =   500
      End
      Begin VB.OptionButton OptionSelectedTool 
         Height          =   630
         Index           =   3
         Left            =   405
         TabIndex        =   6
         Top             =   2610
         Width           =   500
      End
      Begin VB.OptionButton OptionSelectedTool 
         Height          =   630
         Index           =   4
         Left            =   405
         TabIndex        =   5
         Top             =   3360
         Width           =   500
      End
      Begin VB.Image ImageSelectedTool 
         Height          =   750
         Index           =   0
         Left            =   1005
         Stretch         =   -1  'True
         Top             =   285
         Width           =   750
      End
      Begin VB.Image ImageSelectedTool 
         Height          =   750
         Index           =   1
         Left            =   1005
         Stretch         =   -1  'True
         Top             =   1050
         Width           =   750
      End
      Begin VB.Image ImageSelectedTool 
         Height          =   750
         Index           =   2
         Left            =   1005
         Stretch         =   -1  'True
         Top             =   1800
         Width           =   750
      End
      Begin VB.Image ImageSelectedTool 
         Height          =   750
         Index           =   3
         Left            =   1005
         Stretch         =   -1  'True
         Top             =   2550
         Width           =   750
      End
      Begin VB.Image ImageSelectedTool 
         Height          =   750
         Index           =   4
         Left            =   1005
         Stretch         =   -1  'True
         Top             =   3285
         Width           =   750
      End
   End
   Begin VB.Image ImageBuyDialog 
      Height          =   1335
      Index           =   0
      Left            =   855
      Picture         =   "game.frx":08CA
      Stretch         =   -1  'True
      Top             =   1650
      Visible         =   0   'False
      Width           =   2415
   End
   Begin VB.Image ImageBuyDialog 
      Height          =   1335
      Index           =   1
      Left            =   225
      Picture         =   "game.frx":1594
      Stretch         =   -1  'True
      Top             =   195
      Visible         =   0   'False
      Width           =   2415
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   54
      Left            =   6645
      Top             =   7965
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   53
      Left            =   6525
      Top             =   7785
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   52
      Left            =   6450
      Top             =   7650
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   51
      Left            =   6360
      Top             =   7560
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   50
      Left            =   6285
      Top             =   7455
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   49
      Left            =   5640
      Top             =   7965
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   48
      Left            =   5535
      Top             =   7860
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   47
      Left            =   5430
      Top             =   7740
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   46
      Left            =   5355
      Top             =   7605
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   45
      Left            =   5265
      Top             =   7470
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   44
      Left            =   4140
      Top             =   7755
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   43
      Left            =   4035
      Top             =   7650
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   42
      Left            =   3930
      Top             =   7500
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   41
      Left            =   3345
      Top             =   7710
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   40
      Left            =   3255
      Top             =   7605
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   39
      Left            =   3135
      Top             =   7470
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   38
      Left            =   2565
      Top             =   7665
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   37
      Left            =   2475
      Top             =   7530
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   36
      Left            =   2385
      Top             =   7425
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   35
      Left            =   1785
      Top             =   7575
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   34
      Left            =   1680
      Top             =   7485
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   33
      Left            =   1545
      Top             =   7425
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   1
      Left            =   885
      Stretch         =   -1  'True
      Top             =   6030
      Visible         =   0   'False
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   7
      Left            =   4650
      Stretch         =   -1  'True
      Top             =   6165
      Visible         =   0   'False
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   320
      Index           =   6
      Left            =   4065
      Stretch         =   -1  'True
      Top             =   6180
      Visible         =   0   'False
      Width           =   320
   End
   Begin VB.Image figura 
      Height          =   320
      Index           =   5
      Left            =   3420
      Stretch         =   -1  'True
      Top             =   6120
      Visible         =   0   'False
      Width           =   320
   End
   Begin VB.Image figura 
      Height          =   320
      Index           =   4
      Left            =   2685
      Stretch         =   -1  'True
      Top             =   6105
      Visible         =   0   'False
      Width           =   320
   End
   Begin VB.Image figura 
      Height          =   315
      Index           =   3
      Left            =   1995
      Stretch         =   -1  'True
      Top             =   6150
      Visible         =   0   'False
      Width           =   315
   End
   Begin VB.Image figura 
      Height          =   320
      Index           =   2
      Left            =   1350
      Stretch         =   -1  'True
      Top             =   6105
      Visible         =   0   'False
      Width           =   320
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   32
      Left            =   840
      Top             =   7515
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   31
      Left            =   600
      Top             =   7590
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   30
      Left            =   510
      Top             =   7560
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   29
      Left            =   375
      Top             =   7515
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   28
      Left            =   300
      Top             =   7440
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   27
      Left            =   225
      Top             =   7380
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   26
      Left            =   8190
      Top             =   6855
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   25
      Left            =   8055
      Top             =   6780
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   24
      Left            =   7980
      Top             =   6675
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   23
      Left            =   7920
      Top             =   6600
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   22
      Left            =   7350
      Top             =   6735
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   21
      Left            =   7290
      Top             =   6660
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   20
      Left            =   7215
      Top             =   6570
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   19
      Left            =   6540
      Top             =   6825
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   18
      Left            =   6435
      Top             =   6720
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   17
      Left            =   6330
      Top             =   6630
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   16
      Left            =   5700
      Top             =   6555
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   15
      Left            =   5460
      Top             =   6795
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   14
      Left            =   5130
      Top             =   6555
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   13
      Left            =   4815
      Top             =   6780
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   12
      Left            =   4470
      Top             =   6570
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   11
      Left            =   4140
      Top             =   6810
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   10
      Left            =   3630
      Top             =   6585
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   9
      Left            =   3300
      Top             =   6765
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   8
      Left            =   2940
      Top             =   6645
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   7
      Left            =   2685
      Top             =   6750
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   6
      Left            =   2130
      Top             =   6645
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   5
      Left            =   1845
      Top             =   6840
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   4
      Left            =   1530
      Top             =   6690
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   3
      Left            =   1140
      Top             =   6780
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   2
      Left            =   990
      Top             =   6645
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   1
      Left            =   480
      Top             =   6570
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageResource 
      Height          =   450
      Index           =   0
      Left            =   255
      Top             =   6705
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Menu mnuFile 
      Caption         =   "&File"
      Begin VB.Menu mnuNew 
         Caption         =   "&New"
      End
      Begin VB.Menu mnuOpen 
         Caption         =   "&Open"
      End
      Begin VB.Menu mnuSave 
         Caption         =   "&Save"
      End
      Begin VB.Menu mnuSaveMap 
         Caption         =   "&Save map"
         Visible         =   0   'False
      End
      Begin VB.Menu mnuExitMapEditor 
         Caption         =   "E&xit Map Editor"
         Visible         =   0   'False
      End
      Begin VB.Menu mnuSep1 
         Caption         =   "-"
      End
      Begin VB.Menu mnuExit 
         Caption         =   "E&xit"
      End
   End
   Begin VB.Menu mnuOrders 
      Caption         =   "O&rders"
      Begin VB.Menu mnuRoad 
         Caption         =   "Build &road"
         Shortcut        =   {F5}
      End
      Begin VB.Menu mnuSell 
         Caption         =   "&Sell"
         Shortcut        =   {F6}
      End
      Begin VB.Menu mnuSemaphors 
         Caption         =   "Sema&phors"
         Begin VB.Menu mnuCreateSemafors 
            Caption         =   "&Create semaphor"
         End
         Begin VB.Menu mnuRemoveSemaphor 
            Caption         =   "&Remove semaphor"
         End
         Begin VB.Menu mnuRotateSemaphors 
            Caption         =   "Rotate &semaphors"
            Shortcut        =   {F7}
         End
      End
      Begin VB.Menu mnuEndTurn 
         Caption         =   "End &turn"
         Shortcut        =   {F8}
      End
   End
   Begin VB.Menu mnuOptions 
      Caption         =   "&Options"
      Begin VB.Menu mnuFast 
         Caption         =   "&Fast"
         Shortcut        =   {F2}
      End
      Begin VB.Menu mnuShowGrid 
         Caption         =   "Show &grid"
         Shortcut        =   {F3}
      End
      Begin VB.Menu mnuAutoEndTurn 
         Caption         =   "&Automatic end turn"
         Shortcut        =   {F4}
      End
      Begin VB.Menu mnuSep2 
         Caption         =   "-"
      End
      Begin VB.Menu mnuSound 
         Caption         =   "&Sound"
         Checked         =   -1  'True
      End
      Begin VB.Menu mnuGraphics 
         Caption         =   "&Graphics..."
      End
      Begin VB.Menu mnuLanguage 
         Caption         =   "&Language"
         Begin VB.Menu mnuLngg 
            Caption         =   "&English"
            Index           =   0
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "&Spanish"
            Index           =   1
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Portugese"
            Index           =   2
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Italian"
            Index           =   3
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "French"
            Index           =   4
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "German"
            Index           =   5
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Chinese"
            Index           =   6
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Japanese"
            Index           =   7
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Korean"
            Index           =   8
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Slovenian"
            Index           =   9
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Russian"
            Index           =   10
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Serbocroatian"
            Index           =   11
            Visible         =   0   'False
         End
         Begin VB.Menu mnuLngg 
            Caption         =   "Other..."
            Index           =   12
            Visible         =   0   'False
         End
      End
   End
   Begin VB.Menu mnuTools 
      Caption         =   "&Tools"
      Begin VB.Menu mnuMapEditor 
         Caption         =   "&Map editor"
      End
   End
   Begin VB.Menu mnuHelp 
      Caption         =   "&Help"
      Begin VB.Menu mnuContents 
         Caption         =   "&Contents"
         Shortcut        =   {F1}
      End
      Begin VB.Menu mnuAbout 
         Caption         =   "&About"
      End
      Begin VB.Menu mnuRegister 
         Caption         =   "&Register"
      End
   End
End
Attribute VB_Name = "Game"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
Dim figuraXoffset(7)
Dim figuraYoffset(7)
Dim figuraZaRefreshat

Dim whereOnFormClickedX As Single
Dim whereOnFormClickedY As Single
Private Sub Form_Load()
    Randomize
    numpl = 0
    load_language
    switch_language
    set_data
    zoomfaktor = 1  '''must be 1
    
    Me.Left = (Screen.Width - Me.Width) / 2
    Me.Top = (Screen.Height - Me.Height) / 2
    
    'kako risati figure
    figuraXoffset(1) = 0 * Screen.TwipsPerPixelX: figuraYoffset(1) = 0 * Screen.TwipsPerPixelY
    figuraXoffset(2) = 0 * Screen.TwipsPerPixelX: figuraYoffset(2) = 16 * Screen.TwipsPerPixelY
    figuraXoffset(3) = 16 * Screen.TwipsPerPixelX: figuraYoffset(3) = 0 * Screen.TwipsPerPixelY
    figuraXoffset(4) = 16 * Screen.TwipsPerPixelX: figuraYoffset(4) = 16 * Screen.TwipsPerPixelY
    figuraXoffset(5) = 0 * Screen.TwipsPerPixelX: figuraYoffset(5) = 10 * Screen.TwipsPerPixelY
    figuraXoffset(6) = 10 * Screen.TwipsPerPixelX: figuraYoffset(6) = 0 * Screen.TwipsPerPixelY
    figuraXoffset(7) = 10 * Screen.TwipsPerPixelX: figuraYoffset(7) = 10 * Screen.TwipsPerPixelY
    figuraZaRefreshat = 1
    
    load_resources
    
    'custom graphics
    On Error Resume Next
    Dim mustCustomize, s
    mustCustomize = False
    Open App.Path & "\metropoly.ini" For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[Graphics]"
    If s = "[Graphics]" Then
        Line Input #1, s
        Line Input #1, s
        Line Input #1, s
        If Not EOF(1) Then mustCustomize = True
    End If
    Close 1
    If mustCustomize Then
        frmGraphics.load_graphics_from_ini      ''this way of calling form may call (unexpected) sub frmGraphics_loadForm
    End If
    
    load_keyboard_shortcuts
    
End Sub


Private Sub Form_Unload(Cancel As Integer)
    End
End Sub

Private Sub ImageLandInfo_Click()
    'hide land info
    display_status
End Sub

Private Sub ImageSelectedTool_Click(Index As Integer)
    'OptionSelectedTool_Click Index
    mapCurrentTool = Index
    OptionSelectedTool(Index).Value = True
End Sub

Private Sub mnuAbout_Click()
    frmAbout.Show vbModal
End Sub

Private Sub mnuAutoEndTurn_Click()
    mnuAutoEndTurn.Checked = Not mnuAutoEndTurn.Checked
End Sub

Private Sub mnuContents_Click()
    Help.Show vbModal
End Sub


Private Sub mnuCreateSemafors_Click()
    If player(curpl).tip = 0 Then
        display_land_info player(curpl).x, player(curpl).y  'display road when building
        LabelStatus.Caption = lngg(83)
        clkMode = 3
    End If

End Sub

Private Sub mnuExit_Click()
    End
End Sub


Private Sub mnuFast_Click()
    mnuFast.Checked = Not mnuFast.Checked
    If mnuFast.Checked Then
        TimerMetKocke.Interval = 30
        TimerSkokFigure.Interval = 50
    Else
        TimerMetKocke.Interval = 300
        TimerSkokFigure.Interval = 500
    End If
End Sub

Private Sub mnuMapEditor_Click()
    frmMapEditor.Text1(0).Text = ""
    frmMapEditor.Text1(1).Text = ""
    frmMapEditor.Combo1.Text = ""
    frmMapEditor.Show vbModal
End Sub

Private Sub mnuNew_Click()
    NewGame.Combo1.Text = ""    '''
    NewGame.Show vbModal        'set player, map
    If numpl = 0 Then Exit Sub
    
    'start new game
    draw_map
    draw_players
    
    clkMode = 0     'info mode
    dayOfWeek = 1: gameTurnVpadnica = 0: gameTurnSmer = 0
    
    curpl = Int(numpl * Rnd + 1)
    next_player
    
End Sub
Sub draw_players()
    '(at beginning of game all players are in jail)
    Dim i, p
    For i = 1 To 7
        figura(i).Visible = False
    Next i
    For i = 1 To numpl
        p = player(i).id
        figura(p).Visible = True
        draw_player player(i).x, player(i).y, p
    Next i
End Sub
Sub draw_player(x, y, p)
    Dim dx, dy
    Dim x1 As Single
    Dim y1 As Single
    dx = 32 * zoomfaktor * Screen.TwipsPerPixelX
    dy = 32 * zoomfaktor * Screen.TwipsPerPixelY
    x1 = (x - 1) * dx: y1 = (y - 1) * dy
    
    If nekdo_ze_stoji_tle(x, y, p) Then
        figura(p).Top = y1 + figuraYoffset(p)
        figura(p).Left = x1 + figuraXoffset(p)
    Else
        figura(p).Top = y1 + 8 * Screen.TwipsPerPixelY
        figura(p).Left = x1 + 8 * Screen.TwipsPerPixelX
    End If
End Sub

Function kje_so_sosednje_ceste(x, y)
    '1=cesta, 0=ni ceste
    Dim s1, s2, s3, s4 As String    'nswe
    s1 = "0": s2 = "0": s3 = "0": s4 = "0"
    If (y - 1) > 0 Then
        If (map(x, y - 1).tip = 0) Or (map(x, y - 1).tip = 5) Then
            s1 = "1"
        End If
    End If
    
    If (y + 1) <= dimy Then
        If (map(x, y + 1).tip = 0) Or (map(x, y + 1).tip = 5) Then
            s2 = "1"
        End If
    End If
    
    If (x - 1) > 0 Then
        If (map(x - 1, y).tip = 0) Or (map(x - 1, y).tip = 5) Then
            s3 = "1"
        End If
    End If
    
    If (x + 1) <= dimx Then
        If (map(x + 1, y).tip = 0) Or (map(x + 1, y).tip = 5) Then
            s4 = "1"
        End If
    End If
    kje_so_sosednje_ceste = s1 + s2 + s3 + s4
End Function
Sub risipolje(x, y, kaj)
    Dim dx, dy
    Dim x1 As Single
    Dim y1 As Single
    dx = 32 * zoomfaktor
    dy = 32 * zoomfaktor
    x1 = (x - 1) * dx: y1 = (y - 1) * dy
    
    Me.PaintPicture ImageResource(kaj).Picture, x1 * Screen.TwipsPerPixelX, y1 * Screen.TwipsPerPixelY
    
End Sub

Sub draw_map()
    Dim x, y, sosed, road, kaj, s
    
    'map size
    Dim twipx, pixx, twipy, pixy
    pixx = 32 * zoomfaktor * dimx
    twipx = pixx * Screen.TwipsPerPixelX
    pixy = 32 * zoomfaktor * dimy
    twipy = pixy * Screen.TwipsPerPixelY
    FrameStatus.Left = twipx + 5 * Screen.TwipsPerPixelX
    FrameStatus.Top = 0
    FrameMapEditor.Left = FrameStatus.Left
    FrameMapEditor.Top = FrameStatus.Top
    Me.Width = twipx + FrameStatus.Width + 15 * Screen.TwipsPerPixelX
    If twipy > FrameStatus.Height Then
        '''FrameStatus.Height = twipy
        Me.Height = twipy + 40 * Screen.TwipsPerPixelY
    Else
        Me.Height = FrameStatus.Height + 40 * Screen.TwipsPerPixelY
    End If
    Me.Left = (Screen.Width - Me.Width) / 2
    Me.Top = (Screen.Height - Me.Height) / 2
    
    'draw
    Me.Cls
    For y = 1 To dimy
        For x = 1 To dimx
            risipolje x, y, 11        'risi podlago
            'ce je cesta
            sosed = ""
            If (map(x, y).tip = 0) Or (map(x, y).tip = 5) Then
                risi_cesto x, y
            End If
            'ce je other
            If map(x, y).tip = 2 Then
                risipolje x, y, 17
            End If
            If map(x, y).tip = 3 Then
                risipolje x, y, 18
            End If
            If map(x, y).tip = 4 Then
                risipolje x, y, 19
            End If
            'ce je house
            If map(x, y).stage > 0 Then
                risipolje x, y, 11 + Val(map(x, y).stage)
            End If
            
            'ce je lastnik - zastavica
            If map(x, y).owner > 0 Then
                risipolje x, y, 19 + Val(player(map(x, y).owner).id)
            End If
            
        Next x
    Next y
    
End Sub



Private Sub mnuRegister_Click()
    frmRegister.Show vbModal
End Sub

Private Sub mnuRemoveSemaphor_Click()
    If player(curpl).tip = 0 Then
        display_land_info player(curpl).x, player(curpl).y  'display road when building
        'LabelStatus.Caption = "Click on a semaphore to remove it."
        LabelStatus.Caption = lngg(84)
        clkMode = 4
    End If

End Sub

Private Sub mnuShowGrid_Click()
    mnuShowGrid.Checked = Not mnuShowGrid.Checked
    If mnuShowGrid.Checked Then
        display_grid
    Else
        draw_map     'hide grid
    End If

End Sub

Private Sub mnuSound_Click()
    mnuSound.Checked = Not mnuSound.Checked
End Sub

Private Sub OptionSelectedTool_Click(Index As Integer)
    mapCurrentTool = Index
End Sub

Private Sub PictureStatus_Click()
    'hide land info
    display_status
End Sub

Private Sub TimerMetKocke_Timer()
    'risi 2 kocki
    Dim kocka1, kocka2, x, y
    display_status      'podlaga za met kocke
    kocka1 = Int((6 - 1 + 1) * Rnd + 1)
    kocka2 = Int((6 - 1 + 1) * Rnd + 1)
    x = 35 * 3 * Screen.TwipsPerPixelX
    y = (curpl - 1) * 35 * Screen.TwipsPerPixelY
    PictureStatus.PaintPicture ImageResource(26 + kocka1).Picture, x, y
    x = 35 * 4 * Screen.TwipsPerPixelX
    PictureStatus.PaintPicture ImageResource(26 + kocka2).Picture, x, y
    
    cakajKocko = cakajKocko - 1
    If cakajKocko <= 0 Then
        TimerMetKocke.Enabled = False
        kocka = kocka1 + kocka2
        faza = 3
        TimerSkokFigure.Enabled = True
    End If
End Sub

Private Sub TimerRefreshFigure_Timer()
    Dim i
    If numpl = 0 Then Exit Sub
    If figura(figuraZaRefreshat).Visible Then figura(figuraZaRefreshat).ZOrder
    figuraZaRefreshat = figuraZaRefreshat + 1
    If figuraZaRefreshat > 7 Then figuraZaRefreshat = 1
    
End Sub

Sub display_status()
    Dim x, y, dx, dy, i, tx, ty
    Dim nter, ter, nhou, hou
    Dim l As Long
    Dim s As String
    
    PictureStatus.Cls
    ImageLandInfo.Visible = False
    x = 0: y = 0: tx = 0: ty = 0
    dy = 35 * Screen.TwipsPerPixelY
    nter = 0: nhou = 0
    For i = 1 To numpl
        nter = nter + player(i).statland
        nhou = nhou + player(i).stathouse
    Next i
    
    For i = 1 To numpl
        x = 0
        PictureStatus.PaintPicture figura(player(i).id).Picture, x, y
        x = x + 35 * Screen.TwipsPerPixelX
        PictureStatus.PaintPicture ImageResource(19 + player(i).id).Picture, x, y
        
        If nter > 0 Then    'gauge
            ter = 45 + Int((player(i).statland / nter) * 9)
            PictureStatus.PaintPicture ImageResource(ter).Picture, x + 3.8 * 35 * Screen.TwipsPerPixelX, y + 2 * Screen.TwipsPerPixelY
        End If
        If nhou > 0 Then
            hou = 45 + Int((player(i).stathouse / nhou) * 9)
            PictureStatus.PaintPicture ImageResource(hou).Picture, x + 3.5 * 35 * Screen.TwipsPerPixelX, y + 3 * Screen.TwipsPerPixelY
        End If
        
        
        PictureStatus.ForeColor = player(i).barva
        s = player(i).ime
        tx = 35: ty = (i - 1) * 35
        If i = curpl Then PictureStatus.FontBold = True
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
        
        PictureStatus.ForeColor = 0
        's = Str(player(i).money) & " $   " & izobrazbaNaziv(player(i).izobrazba)
        s = Str(player(i).money) & " " & lngg(85) & "   " & izobrazbaNaziv(player(i).izobrazba)
        tx = 32 + 32: ty = (i - 1) * 35 + 16
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
        PictureStatus.FontBold = False
        
        'assets
        s = player(i).ime & " " ''& Chr(13) & Chr(10)
        s = s & lngg(86) & player(i).statland & " "
        s = s & lngg(87) & player(i).stathouse & " " ''& Chr(13) & Chr(10)
        s = s & lngg(88) & player(i).jobpayment & lngg(89)
        figura(player(i).id).ToolTipText = s
        
        y = y + dy
    Next i
End Sub

Private Sub TimerSkokFigure_Timer()
    Dim kamx, kamy, sosed, smer, newsmer, zvok
    kamx = jailx: kamy = jaily  'default
    newsmer = 0
    'premakni figuro
    If (player(curpl).x = jailx) And (player(curpl).y = jaily) Then
        kamx = startx
        kamy = starty
    Else
        sosed = kje_so_sosednje_ceste(player(curpl).x, player(curpl).y)
        smer = player(curpl).smer           ''bug?: smer ni vedno ok
        If Mid(sosed, smer, 1) = "1" Then   'cesta obstaja
            Select Case smer
            Case 1
                kamy = player(curpl).y - 1
                kamx = player(curpl).x
            Case 2
                kamy = player(curpl).y + 1
                kamx = player(curpl).x
            Case 3
                kamx = player(curpl).x - 1
                kamy = player(curpl).y
            Case 4
                kamx = player(curpl).x + 1
                kamy = player(curpl).y
            End Select
        Else    'find_alternative_road
            newsmer = 0
            find_alternative_road sosed, smer, player(curpl).x, player(curpl).y, kamx, kamy, newsmer
        End If
              
    End If
    

    If newsmer <> 0 Then                    'ovinek: newsmer preklice semaforsmer
        player(curpl).smer = newsmer
    End If

    If map(kamx, kamy).tip = 5 Then    'semafor
        If player(curpl).y - kamy = -1 Then  'gor
            player(curpl).smer = Mid(semaforData(map(kamx, kamy).semafor), 1, 1)
        End If
        If player(curpl).y - kamy = 1 Then  'dol
            player(curpl).smer = Mid(semaforData(map(kamx, kamy).semafor), 2, 1)
        End If
        If player(curpl).x - kamx = -1 Then  'levo
            player(curpl).smer = Mid(semaforData(map(kamx, kamy).semafor), 3, 1)
        End If
        If player(curpl).x - kamx = 1 Then  'w
            player(curpl).smer = Mid(semaforData(map(kamx, kamy).semafor), 4, 1)
        End If
    End If

    player(curpl).x = kamx: player(curpl).y = kamy
    draw_player player(curpl).x, player(curpl).y, player(curpl).id
    sviraj "figura.wav"
    
'''    '''na levo krug (bug: dvakrat se obrne)
'''    If map(player(curpl).x, player(curpl).y).tip = 5 Then
'''        Select Case player(curpl).smer      'vpadnica
'''        Case 1
'''            player(curpl).smer = Mid(semaforData(map(player(curpl).x, player(curpl).y).semafor), 1, 1)
'''        Case 2
'''            player(curpl).smer = Mid(semaforData(map(player(curpl).x, player(curpl).y).semafor), 2, 1)
'''        Case 3
'''            player(curpl).smer = Mid(semaforData(map(player(curpl).x, player(curpl).y).semafor), 3, 1)
'''        Case 4
'''            player(curpl).smer = Mid(semaforData(map(player(curpl).x, player(curpl).y).semafor), 4, 1)
'''        End Select
'''        ''''
'''    End If
    
    
    kocka = kocka - 1
    If kocka <= 0 Then
        TimerSkokFigure.Enabled = False
        faza = 4
        pristanek
        
    End If

End Sub
Sub find_alternative_road(sosed, smer, x, y, ByRef kamx, ByRef kamy, ByRef newsmer)
    Dim found  'alternative roads
    found = False
    Select Case smer
    Case 1    'gor
        If Mid(sosed, 3, 1) = "1" Then  'levo
            kamx = x - 1: kamy = y
            newsmer = 3
            found = True
        End If
        'desno pravilo zavijanja
        If found Then
            If Rnd > 0.25 Then
                If Mid(sosed, 4, 1) = "1" Then  'desno (maybe)
                    kamx = x + 1: kamy = y
                    newsmer = 4
                    found = True
                End If
            End If
        Else
            If Mid(sosed, 4, 1) = "1" Then  'desno
                kamx = x + 1: kamy = y
                newsmer = 4
                found = True
            End If
        End If
        
        If Not found Then               'backroad
            If Mid(sosed, 2, 1) = "1" Then
                kamy = y + 1: kamx = x
                newsmer = 2
                found = True
            End If
        End If
    Case 2   'dol
        If Mid(sosed, 3, 1) = "1" Then  'levo
            kamx = x - 1: kamy = y
            newsmer = 3
            found = True
        End If
        If found Then
            If Rnd > 0.25 Then
                If Mid(sosed, 4, 1) = "1" Then
                    kamx = x + 1: kamy = y
                    newsmer = 4
                    found = True
                End If
            End If
        Else
            If Mid(sosed, 4, 1) = "1" Then
                kamx = x + 1: kamy = y
                newsmer = 4
                found = True
            End If
        End If
        If Not found Then               'backroad
            If Mid(sosed, 1, 1) = "1" Then
                kamy = y - 1: kamx = x
                newsmer = 1
                found = True
            End If
        End If
    Case 3  'levo
        If Mid(sosed, 1, 1) = "1" Then  'gor
            kamy = y - 1: kamx = x
            newsmer = 1
            found = True
        End If
        If found Then
            If Rnd > 0.25 Then
                If Mid(sosed, 2, 1) = "1" Then
                    kamy = y + 1: kamx = x
                    newsmer = 2
                    found = True
                End If
            End If
        Else
            If Mid(sosed, 2, 1) = "1" Then
                kamy = y + 1: kamx = x
                newsmer = 2
                found = True
            End If
        End If
        If Not found Then               'backroad
            If Mid(sosed, 4, 1) = "1" Then
                kamx = x + 1: kamy = y
                newsmer = 4
                found = True
            End If
        End If
    Case 4  'desno
        If Mid(sosed, 1, 1) = "1" Then  'gor
            kamy = y - 1: kamx = x
            newsmer = 1
            found = True
        End If
        If found Then
            If Rnd > 0.25 Then
                If Mid(sosed, 2, 1) = "1" Then
                    kamy = y + 1: kamx = x
                    newsmer = 2
                    found = True
                End If
            End If
        Else
            If Mid(sosed, 2, 1) = "1" Then
                kamy = y + 1: kamx = x
                newsmer = 2
                found = True
            End If
        End If
        If Not found Then               'backroad
            If Mid(sosed, 3, 1) = "1" Then
                kamx = x - 1: kamy = y
                newsmer = 3
                found = True
            End If
        End If
    End Select
End Sub

Sub next_player()
    Dim zvok
    faza = 1    'next player
    display_status
    
    If player(curpl).money < 0 Then
        eliminate_player
        faza = 1    'next player
        display_status
    End If
    
    If numpl > 1 Then
        faza = 2    'met
        kocka = 0: cakajKocko = 5 + Int((6 - 1 + 1) * Rnd + 1)
        TimerMetKocke.Enabled = True    'ko timer se izklopi faza = 3, nato 4
        sviraj "kocka.wav"        'zvok
    End If
End Sub

Private Sub mnuEndTurn_Click()
    If faza = 4 Then
        curpl = curpl + 1
        If curpl > numpl Then   'nov dan
            curpl = 1
            dayOfWeek = dayOfWeek + 1
            If dayOfWeek > 7 Then dayOfWeek = 1
            LabelStatus.Caption = dayOfWeekName(dayOfWeek)
            If (dayOfWeek = 6) Or (dayOfWeek = 3) Then turn_semaphores
            If dayOfWeek = 7 Then pay_wages
        End If
        next_player
    End If
End Sub

Sub pristanek()
    Dim x, y, sx, sy, p, ok, multiPay
    x = player(curpl).x
    y = player(curpl).y
    'pay
    multiPay = ""
    If x > 1 Then       'levi sosed
        sx = x - 1: sy = y
        pay_money sx, sy, multiPay
    End If
    If x < dimx Then
        sx = x + 1: sy = y
        pay_money sx, sy, multiPay
    End If
    If y > 1 Then
        sx = x: sy = y - 1
        pay_money sx, sy, multiPay
    End If
    If y < dimy Then
        sx = x: sy = y + 1
        pay_money sx, sy, multiPay
    End If
    If multiPay <> "" Then
        multiPay = multiPay & "."
        LabelStatus.Caption = multiPay
    End If
    
    'build, buy, learn, earn
    If x > 1 Then       'levi sosed
        sx = x - 1: sy = y
        earn_learn sx, sy
        build_houses sx, sy
        buy_land sx, sy
    End If
    If x < dimx Then
        sx = x + 1: sy = y
        earn_learn sx, sy
        build_houses sx, sy
        buy_land sx, sy
    End If
    If y > 1 Then
        sx = x: sy = y - 1
        earn_learn sx, sy
        build_houses sx, sy
        buy_land sx, sy
    End If
    If y < dimy Then
        sx = x: sy = y + 1
        earn_learn sx, sy
        build_houses sx, sy
        buy_land sx, sy
    End If
    display_status
    
    'end turn
    If player(curpl).tip = 1 Then   'pc
        pc_intelig_moves
        mnuEndTurn_Click
    Else
        If mnuAutoEndTurn.Checked Then
            ok = vbYes
        Else
            ok = MsgBox(lngg(90), vbYesNo, player(curpl).ime)
        End If
        If ok = vbYes Then
            mnuEndTurn_Click
        End If
    End If
    
    'sell and other commands and then end turn
    
End Sub

Sub pay_money(sx, sy, ByRef multiPay)
    Dim p
    Dim s As String
    Dim l As Long
    If map(sx, sy).tip = 1 Then
        If map(sx, sy).owner <> curpl Then
            If map(sx, sy).owner <> 0 Then
                p = pay_money_price(map(sx, sy).stage, map(sx, sy).price)
                player(curpl).money = player(curpl).money - p
                player(map(sx, sy).owner).money = player(map(sx, sy).owner).money + p
                If multiPay = "" Then
                    multiPay = player(curpl).ime & " " & lngg(91) & " " & p & " " & lngg(92) & " " & player(map(sx, sy).owner).ime
                Else
                    multiPay = multiPay & ", " & p & lngg(92) & " " & player(map(sx, sy).owner).ime
                End If
            End If
        End If
    End If
End Sub

Sub buy_land(sx, sy)
    Dim p, ok
    Dim s As String
    Dim l As Long
    If map(sx, sy).tip = 1 Then
        If map(sx, sy).owner = 0 Then
                p = buy_land_price(map(sx, sy).price)
                If player(curpl).money >= p Then
                    ok = vbYes          'default for pc
                    If player(curpl).money < 200 Then ok = vbNo
                    If player(curpl).tip = 0 Then
                        buy_dialog sx, sy, p, 0
                        ok = buyDialogAnswer
                    End If
                    If ok = vbYes Then  'buy
                        player(curpl).money = player(curpl).money - p
                        player(curpl).statland = player(curpl).statland + 1
                        map(sx, sy).owner = curpl
                        risipolje sx, sy, 19 + Val(player(map(sx, sy).owner).id)
                        display_status
                        LabelStatus.Caption = player(curpl).ime & " " & lngg(93) & " " & p & lngg(85) & "."
                    End If
                End If
        End If
    End If
End Sub

Sub build_houses(sx, sy)
    Dim p, ok
    Dim s As String
    Dim l As Long
    If map(sx, sy).tip = 1 Then
        If map(sx, sy).owner = curpl Then
            If map(sx, sy).stage < 5 Then
                p = build_houses_price(map(sx, sy).stage, map(sx, sy).price)
                If player(curpl).money >= p Then
                    ok = vbYes          ''default for pc
                    If player(curpl).money < 300 Then ok = vbNo
                    If player(curpl).tip = 0 Then
                        buy_dialog sx, sy, p, 1
                        ok = buyDialogAnswer
                    End If
                    If ok = vbYes Then  'build
                        player(curpl).money = player(curpl).money - p
                        player(curpl).stathouse = player(curpl).stathouse + 1
                        map(sx, sy).stage = map(sx, sy).stage + 1
                        risipolje sx, sy, 11    'brisi spodnje
                        risipolje sx, sy, 11 + Val(map(sx, sy).stage)
                        risipolje sx, sy, 19 + Val(player(map(sx, sy).owner).id)
                        display_status
                        LabelStatus.Caption = player(curpl).ime & " " & lngg(94) & " " & Trim(Str(map(sx, sy).stage)) & " " & lngg(95) & " " & p & lngg(85) & "."
                        If mnuShowGrid.Checked Then display_grid
                    End If
                End If
            End If
        End If
    End If

End Sub

Sub earn_learn(sx, sy)
    Dim p, ok
    Dim s As String
    Dim l As Long
    If map(sx, sy).tip = 3 Then 'job
        p = earn_price(player(curpl).izobrazba)
        player(curpl).jobpayment = p    'weekly payment
        LabelStatus.Caption = player(curpl).ime & " " & lngg(96) & " " & p & lngg(89)
        
    End If
    If map(sx, sy).tip = 2 Then 'school
        If player(curpl).izobrazba < 5 Then
            p = learn_price(player(curpl).izobrazba)
            
            ok = vbYes          'default for pc
            If Rnd > 0.75 Then ok = vbNo
            
            If player(curpl).money >= p Then
                display_land_info sx, sy
                If player(curpl).tip = 0 Then
                    '''ok = MsgBox(lngg(98) & " " & p & lngg(101), vbYesNo, player(curpl).ime)
                    ok = MsgBox(lngg(98) & " " & p & lngg(101), vbYesNo, player(curpl).ime)
                End If
                If ok = vbYes Then  'visit
                    player(curpl).money = player(curpl).money - p
                    player(curpl).izobrazba = player(curpl).izobrazba + 1
                    '''display_status
                End If
                display_status
            End If
        End If
    End If
    
End Sub

Private Sub mnuSell_Click()
    If player(curpl).tip = 0 Then
        LabelStatus.Caption = lngg(100)
        clkMode = 1
    End If
End Sub

Private Sub Form_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
    whereOnFormClickedX = x
    whereOnFormClickedY = y
End Sub

Private Sub Form_Click()
    Dim x, y, p, ok 'info, sell
    Dim sosed, kaj  'build road
    x = 0: y = 0
    x = Int(whereOnFormClickedX / Screen.TwipsPerPixelX / 32) + 1
    y = Int(whereOnFormClickedY / Screen.TwipsPerPixelY / 32) + 1
    If (x < 1) Or (x > dimx) Or (y < 1) Or (y > dimy) Then Exit Sub
    
    Select Case clkMode
    Case 0  'land info
        display_land_info x, y
        LabelStatus.Caption = ""
    Case 1  'sell
        display_land_info x, y
        LabelStatus.Caption = ""
        If map(x, y).owner = curpl Then
            If map(x, y).stage > 0 Then 'sell house
                p = sell_price(map(x, y).stage, map(x, y).price)
                ok = MsgBox(lngg(100) & " " & p & lngg(101), vbYesNo, player(curpl).ime)
                If ok = vbYes Then
                    player(curpl).money = player(curpl).money + p
                    player(curpl).stathouse = player(curpl).stathouse - 1
                    map(x, y).stage = map(x, y).stage - 1
                    risipolje x, y, 11 + 0                      'brisi hise
                    risipolje x, y, 11 + Val(map(x, y).stage)   'risi hise
                    risipolje x, y, 19 + Val(player(map(x, y).owner).id)
                    display_status
                End If
            Else    'sell land
                p = sell_price(map(x, y).stage, map(x, y).price)
                ok = MsgBox(lngg(100) & " " & p & lngg(101), vbYesNo, player(curpl).ime)
                If ok = vbYes Then
                    player(curpl).money = player(curpl).money + p
                    player(curpl).statland = player(curpl).statland - 1
                    map(x, y).owner = 0
                    risipolje x, y, 11 + Val(map(x, y).stage)   'brisi zastavico
                    display_status
                    clkMode = 0: LabelStatus.Caption = ""
                End If
            End If
            If mnuShowGrid.Checked Then display_grid
        Else
            Beep
            clkMode = 0: LabelStatus.Caption = ""
        End If
        
    Case 2  'build road
        LabelStatus.Caption = ""
        If (map(x, y).owner = curpl) And (map(x, y).tip = 1) Then
            p = road_price(x, y)    ''= - 100
            ''If player(curpl).money >= p Then
                map(x, y).stage = 0
                map(x, y).owner = 0
                map(x, y).tip = 0
                risi_cesto x, y
                popravi_sosednje_ceste x, y
                player(curpl).money = player(curpl).money - p
                player(curpl).statland = player(curpl).statland - 1
                player(curpl).stathouse = player(curpl).stathouse - map(x, y).stage
                display_status
                LabelStatus.Caption = lngg(103)
                expand_terit x, y
            ''End If
        End If
        clkMode = 0
        
    Case 3  'create semaphor
        LabelStatus.Caption = ""
        If map(x, y).tip = 0 Then
            p = create_semaphor_price(x, y)
            If player(curpl).money >= p Then
                If semafor_je_mozen(x, y) Then
                    create_semaphor x, y
                    ''map(x, y).tip = 5
                    ''risi_cesto x, y
                    player(curpl).money = player(curpl).money - p
                    display_status
                    LabelStatus.Caption = lngg(104)
                End If
            End If
        End If
        clkMode = 0
        
    Case 4  'remove semaphor
        LabelStatus.Caption = ""
        If map(x, y).tip = 5 Then
            p = delete_semaphor_price(x, y)
            If player(curpl).money >= p Then
                map(x, y).tip = 0
                risi_cesto x, y
                player(curpl).money = player(curpl).money - p
                display_status
                LabelStatus.Caption = lngg(105)
            End If
        End If
        clkMode = 0
        
    Case 33     '''map editor
        edit_map x, y
    
    End Select
End Sub

Sub eliminate_player()
    Dim i, ok, x, y
    ok = MsgBox(player(curpl).ime & lngg(106), vbOKOnly, "")
    figura(player(curpl).id).Visible = False
    'odvzem terit
    For x = 1 To dimx
        For y = 1 To dimy
            If (map(x, y).tip = 1) And (map(x, y).owner = curpl) Then
                map(x, y).stage = 0
                map(x, y).owner = 0
                risipolje x, y, 11  'brisi flag
            End If
        Next y
    Next x
    player(curpl).stathouse = 0: player(curpl).statland = 0
    
    If numpl > 1 Then               'elim player
        If curpl = 1 Then
            For i = 1 To numpl - 1
                player(i) = player(i + 1)
                shift_map_owners i, i + 1
            Next i
            curpl = 1
        End If
        If (curpl > 1) And (curpl < numpl) Then
            For i = curpl To numpl - 1
                player(i) = player(i + 1)
                shift_map_owners i, i + 1
            Next i
        End If
        If curpl = numpl Then
            curpl = 1
        End If
        
        numpl = numpl - 1
    End If
    display_status
    If mnuShowGrid.Checked Then display_grid
    
    If numpl <= 1 Then '''end game
        TimerMetKocke.Enabled = False
        TimerSkokFigure.Enabled = False
        LabelStatus.Caption = lngg(107) & player(1).ime
        ok = MsgBox(player(1).ime & lngg(108), vbInformation, lngg(15))
    End If
End Sub

Sub shift_map_owners(i, o)
    'after player elimination
    Dim x, y
    For x = 1 To dimx
        For y = 1 To dimy
            If (map(x, y).tip = 1) And (map(x, y).owner = o) Then
                map(x, y).owner = i
            End If
        Next y
    Next x
    
End Sub

Sub pay_wages()
    'every week
    Dim i, s, ok
    s = ""
    For i = 1 To numpl
        player(i).money = player(i).money + player(i).jobpayment
        s = s & player(i).statland & lngg(109) & player(i).stathouse & lngg(110)
        s = s & player(i).ime
        If player(i).jobpayment > 0 Then
            s = s & lngg(111) & player(i).jobpayment & lngg(89)
        End If
        s = s & Chr(13) & Chr(10)
    Next i
    ok = MsgBox(s, vbOKOnly, lngg(112))
End Sub

Private Sub mnuRoad_Click()
    If player(curpl).tip = 0 Then
        display_land_info player(curpl).x, player(curpl).y  'display road when building
        LabelStatus.Caption = lngg(113)
        clkMode = 2
    End If
End Sub

Sub popravi_sosednje_ceste(x, y)
    Dim x1, y1, sosed
    sosed = kje_so_sosednje_ceste(x, y) 'nswe
    If (x > 1) And (Mid(sosed, 3, 1) = "1") Then
        x1 = x - 1: y1 = y
        risi_cesto x1, y1
        'ce je nastalo novo krizisce
        dodaj_kak_semafor x1, y1
    End If
    
    If (x < dimx) And (Mid(sosed, 4, 1) = "1") Then
        x1 = x + 1: y1 = y
        risi_cesto x1, y1
        dodaj_kak_semafor x1, y1
    End If
    
    If (y > 1) And (Mid(sosed, 1, 1) = "1") Then
        x1 = x: y1 = y - 1
        risi_cesto x1, y1
        dodaj_kak_semafor x1, y1
    End If
    
    If (y < dimy) And (Mid(sosed, 2, 1) = "1") Then
        x1 = x: y1 = y + 1
        risi_cesto x1, y1
        dodaj_kak_semafor x1, y1
    End If
    
End Sub

Sub risi_cesto(x, y)
    Dim sosed, kaj, s
    sosed = kje_so_sosednje_ceste(x, y)
    Select Case sosed   'nswe
        Case "1100"
            kaj = 3
        Case "0011"
            kaj = 2
        Case "0110"
            kaj = 0
        Case "0101"
            kaj = 1
        Case "1010"
            kaj = 4
        Case "1001"
            kaj = 5
        Case "0111"
            kaj = 6
        Case "1011"
            kaj = 9
        Case "1101"
            kaj = 8
        Case "1110"
            kaj = 7
        Case "1111"
            kaj = 10
        Case "1000"     'slepa ulica
            kaj = 3
        Case "0100"
            kaj = 3
        Case "0010"
            kaj = 2
        Case "0001"
            kaj = 2
        Case "0000"     'v map editorju
            If mapEditorMode > 0 Then
                kaj = 2
            Else
                kaj = 11
            End If
    End Select
    risipolje x, y, 11      'brisi spodnje
    risipolje x, y, kaj
    
    'ce je semafor
    If map(x, y).tip = 5 Then
        s = semaforData(map(x, y).semafor)
        If Mid(sosed, 4, 1) = "1" Then  'if vpadnica
            risipolje x, y, Val(Right(s, 2))    'e
        End If
        s = Left(s, Len(s) - 2)
        If Mid(sosed, 3, 1) = "1" Then
            risipolje x, y, Val(Right(s, 2))    'w
        End If
        s = Left(s, Len(s) - 2)
        If Mid(sosed, 2, 1) = "1" Then
            risipolje x, y, Val(Right(s, 2))    's
        End If
        s = Left(s, Len(s) - 2)
        If Mid(sosed, 1, 1) = "1" Then
            risipolje x, y, Val(Right(s, 2))    'n
        End If
    End If

    
    If mnuShowGrid.Checked Then display_grid
End Sub

Sub expand_terit(x, y)
    Dim i, j, expa, c
    expa = False
    
    If x = 1 Then   'scroll right
        If dimx < 100 Then
            dimx = dimx + 1: expa = True
            startx = startx + 1: jailx = jailx + 1
            For i = dimx To 2 Step -1
                For j = 1 To dimy
                    map(i, j) = map(i - 1, j)
                Next j
            Next i
            i = 1
            For j = 1 To dimy
                map(i, j).tip = 1
                map(i, j).stage = 0
                map(i, j).owner = 0
                c = Mid("ABCDEFGHIJKLMNOPQRSTUVWXWZ", Int((25 - 1 + 1) * Rnd + 1), 1)
                map(x, y).price = Asc(c) - 45
            Next j
            For i = 1 To numpl
                player(i).x = player(i).x + 1
            Next i
        End If
    End If
    
    If x = dimx Then    'add right side
        If dimx < 100 Then
            dimx = dimx + 1: expa = True
            i = dimx
            For j = 1 To dimy
                map(i, j).tip = 1
                map(i, j).stage = 0
                map(i, j).owner = 0
                c = Mid("ABCDEFGHIJKLMNOPQRSTUVWXWZ", Int((25 - 1 + 1) * Rnd + 1), 1)
                map(i, j).price = Asc(c) - 45
            Next j
        End If
    End If
    
    If y = 1 Then   'scroll down
        If dimy < 100 Then
            dimy = dimy + 1: expa = True
            starty = starty + 1: jaily = jaily + 1
            For j = dimy To 2 Step -1
                For i = 1 To dimx
                    map(i, j) = map(i, j - 1)
                Next i
            Next j
            j = 1
            For i = 1 To dimx
                map(i, j).tip = 1
                map(i, j).stage = 0
                map(i, j).owner = 0
                c = Mid("ABCDEFGHIJKLMNOPQRSTUVWXWZ", Int((25 - 1 + 1) * Rnd + 1), 1)
                map(x, y).price = Asc(c) - 45
            Next i
            For i = 1 To numpl
                player(i).y = player(i).y + 1
            Next i
        End If
    End If
    
    If y = dimy Then    'add bottom line
        If dimy < 100 Then
            dimy = dimy + 1: expa = True
            j = dimy
            For i = 1 To dimx
                map(i, j).tip = 1
                map(i, j).stage = 0
                map(i, j).owner = 0
                c = Mid("ABCDEFGHIJKLMNOPQRSTUVWXWZ", Int((25 - 1 + 1) * Rnd + 1), 1)
                map(i, j).price = Asc(c) - 45
            Next i
        End If
    End If
    
    If expa Then    'refresh
        draw_map
        If mapEditorMode = 0 Then draw_players
        If mnuShowGrid.Checked Then display_grid
    End If
End Sub

Sub display_land_info(i, j)
    Dim x, y, tx, ty, dy, k, ss
    Dim l As Long
    Dim s As String
    
    PictureStatus.Cls
    If map(i, j).tip = 1 Then
        ImageLandInfo.Picture = ImageResource(11 + map(i, j).stage).Picture
        ImageLandInfo.Visible = True
        tx = 35: ty = 3 * 35: dy = 14
        
        s = lngg(114) & Str(buy_land_price(map(i, j).price)) & lngg(85)
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
        ty = ty + dy
        
        s = lngg(115) & Str(sell_price(map(i, j).stage, map(i, j).price)) & lngg(85)
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
        ty = ty + dy
        
        s = lngg(116) & Str(build_houses_price(map(i, j).stage, map(i, j).price)) & lngg(85)
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
        ty = ty + dy
        
'        x = 1 * 32 * Screen.TwipsPerPixelX
'        y = 4 * 32 * Screen.TwipsPerPixelY
        x = 1 * 32 * Screen.TwipsPerPixelX
        y = 2 * 32 * Screen.TwipsPerPixelY
        If map(i, j).owner <> 0 Then
'            For k = 1 To 9
'                PictureStatus.PaintPicture ImageResource(19 + player(map(i, j).owner).id).Picture, x, y
'                x = x + 16 * Screen.TwipsPerPixelX
'            Next k
            PictureStatus.PaintPicture ImageResource(19 + player(map(i, j).owner).id).Picture, x, y
        End If
        
        
        ty = ty + Int(dy / 2)
        s = lngg(117)
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
        ty = ty + dy
        
        For k = 0 To 5
            s = lngg(118) & Trim(Str(k)) & " " & lngg(119)
            ss = Str(pay_money_price(k, map(i, j).price)) & lngg(85)
            s = s & String(Abs(25 - Len(s) - Len(ss)), ".")
            s = s & ss
            If map(i, j).stage = k Then PictureStatus.FontBold = True
            l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
            PictureStatus.FontBold = False
            ty = ty + dy
        Next k

    End If
    
    If (map(i, j).tip = 0) Or (map(i, j).tip = 5) Then
        ImageLandInfo.Picture = ImageResource(2).Picture
        ImageLandInfo.Visible = True
        tx = 35: ty = 3 * 35
        s = lngg(120)   '"Road"
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
    End If
    If (map(i, j).tip = 2) Then
        ImageLandInfo.Picture = ImageResource(17).Picture
        ImageLandInfo.Visible = True
        tx = 35: ty = 3 * 35
        s = lngg(121)
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
    End If
    If (map(i, j).tip = 3) Then
        ImageLandInfo.Picture = ImageResource(18).Picture
        ImageLandInfo.Visible = True
        tx = 35: ty = 3 * 35
        s = lngg(122)
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
    End If
    If (map(i, j).tip = 4) Then
        ImageLandInfo.Picture = ImageResource(19).Picture
        ImageLandInfo.Visible = True
        tx = 35: ty = 3 * 35
        s = lngg(123)
        l = TextOut(PictureStatus.hdc, tx, ty, s, Len(s))
    End If

End Sub

Sub display_grid()
    Dim i, j, x, y, dx, dy, c
    c = QBColor(8)
    dx = 32 * zoomfaktor * Screen.TwipsPerPixelX
    dy = 32 * zoomfaktor * Screen.TwipsPerPixelY
    x = 1: y = 1
    
    For i = 0 To dimx
        Me.Line (x, 0)-(x, dimy * dy), c
        x = x + dx
    Next i
    For j = 0 To dimy
        Me.Line (0, y)-(dimx * dx, y), c
        y = y + dy
    Next j
End Sub

Private Sub mnuSave_Click()
    'save game
    openSaveMode = 2: openSaveFileName = ""
    ''GameOpenSave.Caption = "Save": GameOpenSave.TextFN.Text = "game.sav"
    GameOpenSave.Caption = lngg(57): GameOpenSave.TextFN.Text = "game.sav"
    GameOpenSave.File1.Refresh
    NewGame.fill_combo
    GameOpenSave.Show vbModal
End Sub

Private Sub mnuOpen_Click()
    'open game
    openSaveMode = 1: openSaveFileName = ""
    ''GameOpenSave.Caption = "Open": GameOpenSave.TextFN.Text = ""
    GameOpenSave.Caption = lngg(56): GameOpenSave.TextFN.Text = ""
    GameOpenSave.File1.Refresh
    GameOpenSave.Show vbModal
End Sub

Sub buy_dialog(sx, sy, p, LandOrHouse)
    'prep dialog
    Dim x, y, s
    display_land_info sx, sy
    LabelStatus.Caption = ""
    If LandOrHouse = 0 Then
        s = lngg(124) & " " & p & lngg(101)
    Else
        s = lngg(125) & " " & p & lngg(101)
    End If
    If sy <= dimy / 2 Then
        x = (sx - 1) * 32 * Screen.TwipsPerPixelX + 32 / 2 * Screen.TwipsPerPixelX
        y = (sy - 1) * 32 * Screen.TwipsPerPixelY + 32 / 2 * Screen.TwipsPerPixelY
        ImageBuyDialog(0).Left = x
        ImageBuyDialog(0).Top = y
        ImageBuyDialog(0).Visible = True
        ImageBuyDialog(0).ZOrder
    Else
        x = (sx - 1) * 32 * Screen.TwipsPerPixelX + 32 / 2 * Screen.TwipsPerPixelX
        y = (sy - 1) * 32 * Screen.TwipsPerPixelY - ImageBuyDialog(1).Height + 32 / 2 * Screen.TwipsPerPixelY
        ImageBuyDialog(1).Left = x
        ImageBuyDialog(1).Top = y
        ImageBuyDialog(1).Visible = True
        ImageBuyDialog(1).ZOrder
        y = y + ImageBuyDialog(1).Height / 6 'korekcija
    End If
    
    frmBuyDialog.LabelQuestion.Caption = s
    frmBuyDialog.Top = Me.Top + y + 20 * Screen.TwipsPerPixelY + ImageBuyDialog(1).Height / 3
    frmBuyDialog.Left = Me.Left + x + ImageBuyDialog(1).Width / 4
    frmBuyDialog.Show vbModal
    
    ImageBuyDialog(0).Visible = False
    ImageBuyDialog(1).Visible = False
    
End Sub

Sub turn_semaphores()
    'every wednesday, saturday
    Dim x, y, sosed, kaj, s, i
    LabelStatus.Caption = lngg(126)
    For x = 1 To dimx
        For y = 1 To dimy
            If map(x, y).tip = 5 Then
                turn_semaphore x, y
                risi_cesto x, y                'risi nov semafor
            End If
        Next y
    Next x
    gameTurnVpadnica = (gameTurnVpadnica + 1) Mod 4
    gameTurnSmer = (gameTurnSmer + 1) Mod 3
    If mnuShowGrid.Checked Then display_grid
End Sub
Sub turn_semaphore(x, y)
    'turn/create rule: semaf=f(gameturn)=n1,w1,e1,s1 / n2,w1,e1,s1 / ...
    Dim s, ss, sosed, i, smr, nsmr, nova_smr, found
    
    smr = gameTurnVpadnica      'nswe - katero vpadnico obrniti
    nsmr = gameTurnSmer         'kam obrniti
    
    sosed = kje_so_sosednje_ceste(x, y)
    If Mid(sosed, smr + 1, 1) = "0" Then Exit Sub   'ni mozno
    
    s = semaforData(map(x, y).semafor)
    s = Left(s, 4)  'stanje
    ss = ""
    Select Case smr
    Case 0
        nova_smr = Mid("234", nsmr + 1, 1)
        If Mid(sosed, Val(nova_smr), 1) = "1" Then ss = nova_smr & Right(s, 3)
    Case 1
        nova_smr = Mid("134", nsmr + 1, 1)
        If Mid(sosed, Val(nova_smr), 1) = "1" Then ss = Left(s, 1) & nova_smr & Right(s, 2)
    Case 2
        nova_smr = Mid("124", nsmr + 1, 1)
        If Mid(sosed, Val(nova_smr), 1) = "1" Then ss = Left(s, 2) & nova_smr & Right(s, 1)
    Case 3
        nova_smr = Mid("123", nsmr + 1, 1)
        If Mid(sosed, Val(nova_smr), 1) = "1" Then ss = Left(s, 3) & nova_smr
    End Select
    
    If ss <> "" Then
        found = 0
        For i = 1 To 81
            If Left(semaforData(i), 4) = ss Then
                found = i
            End If
        Next i
        If found > 0 Then
            map(x, y).semafor = found
        End If
    End If
    
End Sub

Private Sub mnuRotateSemaphors_Click()
    Dim p
    p = rotateSemafor_price
    If player(curpl).tip = 0 Then
        If player(curpl).money >= p Then
            turn_semaphores
            player(curpl).money = player(curpl).money - p
            display_status
        End If
    End If
End Sub

Function nekdo_ze_stoji_tle(x, y, p)
    Dim i, r
    r = False
    For i = 1 To numpl
        If player(i).id <> p Then
            If (player(i).x = x) And (player(i).y = y) Then
                r = True
            End If
        End If
    Next i
    nekdo_ze_stoji_tle = r
End Function

Private Sub mnuGraphics_Click()
    frmGraphics.Show vbModal
End Sub

Sub load_resources()
    Dim i
    figura(1).Picture = LoadPicture(App.Path & "\icons\p1.ico")
    figura(2).Picture = LoadPicture(App.Path & "\icons\p2.ico")
    figura(3).Picture = LoadPicture(App.Path & "\icons\p3.ico")
    figura(4).Picture = LoadPicture(App.Path & "\icons\p4.ico")
    figura(5).Picture = LoadPicture(App.Path & "\icons\p5.ico")
    figura(6).Picture = LoadPicture(App.Path & "\icons\p6.ico")
    figura(7).Picture = LoadPicture(App.Path & "\icons\p7.ico")
    
    ImageResource(0).Picture = LoadPicture(App.Path & "\icons\roaddl.ico")
    ImageResource(1).Picture = LoadPicture(App.Path & "\icons\roaddr.ico")
    ImageResource(2).Picture = LoadPicture(App.Path & "\icons\roadlr.ico")
    ImageResource(3).Picture = LoadPicture(App.Path & "\icons\roadud.ico")
    ImageResource(4).Picture = LoadPicture(App.Path & "\icons\roadul.ico")
    ImageResource(5).Picture = LoadPicture(App.Path & "\icons\roadur.ico")
    ImageResource(6).Picture = LoadPicture(App.Path & "\icons\road3n.ico")
    ImageResource(7).Picture = LoadPicture(App.Path & "\icons\road3e.ico")
    ImageResource(8).Picture = LoadPicture(App.Path & "\icons\road3w.ico")
    ImageResource(9).Picture = LoadPicture(App.Path & "\icons\road3s.ico")
    ImageResource(10).Picture = LoadPicture(App.Path & "\icons\road4.ico")
    
    ImageResource(11).Picture = LoadPicture(App.Path & "\icons\h0.ico")
    ImageResource(12).Picture = LoadPicture(App.Path & "\icons\h1.ico")
    ImageResource(13).Picture = LoadPicture(App.Path & "\icons\h2.ico")
    ImageResource(14).Picture = LoadPicture(App.Path & "\icons\h3.ico")
    ImageResource(15).Picture = LoadPicture(App.Path & "\icons\h4.ico")
    ImageResource(16).Picture = LoadPicture(App.Path & "\icons\h5.ico")
    ImageResource(17).Picture = LoadPicture(App.Path & "\icons\school.ico")
    ImageResource(18).Picture = LoadPicture(App.Path & "\icons\job.ico")
    ImageResource(19).Picture = LoadPicture(App.Path & "\icons\jail.ico")
    
    ImageResource(20).Picture = LoadPicture(App.Path & "\icons\flag1.ico")
    ImageResource(21).Picture = LoadPicture(App.Path & "\icons\flag2.ico")
    ImageResource(22).Picture = LoadPicture(App.Path & "\icons\flag3.ico")
    ImageResource(23).Picture = LoadPicture(App.Path & "\icons\flag4.ico")
    ImageResource(24).Picture = LoadPicture(App.Path & "\icons\flag5.ico")
    ImageResource(25).Picture = LoadPicture(App.Path & "\icons\flag6.ico")
    ImageResource(26).Picture = LoadPicture(App.Path & "\icons\flag7.ico")
    
    ImageResource(27).Picture = LoadPicture(App.Path & "\icons\dice1.ico")
    ImageResource(28).Picture = LoadPicture(App.Path & "\icons\dice2.ico")
    ImageResource(29).Picture = LoadPicture(App.Path & "\icons\dice3.ico")
    ImageResource(30).Picture = LoadPicture(App.Path & "\icons\dice4.ico")
    ImageResource(31).Picture = LoadPicture(App.Path & "\icons\dice5.ico")
    ImageResource(32).Picture = LoadPicture(App.Path & "\icons\dice6.ico")
    
    ImageResource(33).Picture = LoadPicture(App.Path & "\icons\n2.ico")
    ImageResource(34).Picture = LoadPicture(App.Path & "\icons\n3.ico")
    ImageResource(35).Picture = LoadPicture(App.Path & "\icons\n4.ico")
    ImageResource(36).Picture = LoadPicture(App.Path & "\icons\s1.ico")
    ImageResource(37).Picture = LoadPicture(App.Path & "\icons\s3.ico")
    ImageResource(38).Picture = LoadPicture(App.Path & "\icons\s4.ico")
    ImageResource(39).Picture = LoadPicture(App.Path & "\icons\w1.ico")
    ImageResource(40).Picture = LoadPicture(App.Path & "\icons\w2.ico")
    ImageResource(41).Picture = LoadPicture(App.Path & "\icons\w4.ico")
    ImageResource(42).Picture = LoadPicture(App.Path & "\icons\e1.ico")
    ImageResource(43).Picture = LoadPicture(App.Path & "\icons\e2.ico")
    ImageResource(44).Picture = LoadPicture(App.Path & "\icons\e3.ico")
    
    ImageResource(45).Picture = LoadPicture(App.Path & "\icons\gaug0.ico")
    ImageResource(46).Picture = LoadPicture(App.Path & "\icons\gaug1.ico")
    ImageResource(47).Picture = LoadPicture(App.Path & "\icons\gaug2.ico")
    ImageResource(48).Picture = LoadPicture(App.Path & "\icons\gaug3.ico")
    ImageResource(49).Picture = LoadPicture(App.Path & "\icons\gaug4.ico")
    ImageResource(50).Picture = LoadPicture(App.Path & "\icons\gaug5.ico")
    ImageResource(51).Picture = LoadPicture(App.Path & "\icons\gaug6.ico")
    ImageResource(52).Picture = LoadPicture(App.Path & "\icons\gaug7.ico")
    ImageResource(53).Picture = LoadPicture(App.Path & "\icons\gaug8.ico")
    ImageResource(54).Picture = LoadPicture(App.Path & "\icons\gaug9.ico")
    
    'map editor resources
    ImageSelectedTool(0).Picture = ImageResource(2)
    ImageSelectedTool(1).Picture = ImageResource(11)
    ImageSelectedTool(2).Picture = ImageResource(17)
    ImageSelectedTool(3).Picture = ImageResource(18)
    ImageSelectedTool(4).Picture = ImageResource(33)
    
End Sub

Sub create_semaphor(x, y)
    Dim i, j
    If semafor_je_mozen(x, y) Then
        map(x, y).tip = 5
        map(x, y).semafor = 22      ''default (ki sicer ni najbolj pravi)
        For i = 1 To 4                  'obrni vse 4 vpadnice
            For j = 1 To 3              'v vse mozne smeri da bo ena prava
                gameTurnVpadnica = (gameTurnVpadnica + 1) Mod 4
                gameTurnSmer = (gameTurnSmer + 1) Mod 3
                turn_semaphore x, y
            Next j
        Next i
        risi_cesto x, y
    
    End If
    
End Sub

Function semafor_je_mozen(x, y)
    Dim sosed, s1, s2, s3, s4
    sosed = kje_so_sosednje_ceste(x, y)
    s1 = Mid(sosed, 1, 1)
    s2 = Mid(sosed, 2, 1)
    s3 = Mid(sosed, 3, 1)
    s4 = Mid(sosed, 4, 1)
    If Val(s1) + Val(s2) + Val(s3) + Val(s4) > 2 Then
        semafor_je_mozen = True
    Else
        semafor_je_mozen = False
    End If
End Function

Sub dodaj_kak_semafor(x, y)
     'kadar je nastalo novo krizisce
     If Rnd > 0.66 Then
        create_semaphor x, y
     End If
End Sub

Private Sub Form_KeyPress(KeyAscii As Integer)
    If KeyAscii = Asc(keyboardShortcut(1)) Then mnuRoad_Click
    If KeyAscii = Asc(keyboardShortcut(2)) Then mnuSell_Click
    If KeyAscii = Asc(keyboardShortcut(3)) Then mnuCreateSemafors_Click
    If KeyAscii = Asc(keyboardShortcut(4)) Then mnuRotateSemaphors_Click
    If KeyAscii = Asc(keyboardShortcut(5)) Then mnuEndTurn_Click
End Sub

Sub load_keyboard_shortcuts()
    Dim s, i
    Open App.Path & "\metropoly.ini" For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[OrdersKeyboardShortcuts]"
    If s = "[OrdersKeyboardShortcuts]" Then
        For i = 1 To 5
            keyboardShortcut(i) = ""
            If Not EOF(1) Then
                Line Input #1, s
                keyboardShortcut(i) = s
            End If
        Next i
        
    End If
    Close 1
End Sub

Sub edit_map(x, y)
    'modify map depending on selectedTool
    If map(x, y).tip <> 4 Then
        Select Case mapCurrentTool
        Case 1  'land
            map(x, y).tip = 1
            map(x, y).stage = 0
            map(x, y).owner = 0
            risipolje x, y, 11
            popravi_sosednje_ceste x, y
        Case 0  'road
            map(x, y).tip = 0
            map(x, y).stage = 0
            map(x, y).owner = 0
            risi_cesto x, y
            popravi_sosednje_ceste x, y
            expand_terit x, y
        Case 2  'school
            map(x, y).tip = 2
            map(x, y).stage = 0
            map(x, y).owner = 0
            risipolje x, y, 17
        Case 3  'job
            map(x, y).tip = 3
            map(x, y).stage = 0
            map(x, y).owner = 0
            risipolje x, y, 18
        Case 4  'semaf
            If map(x, y).tip = 0 Then
                map(x, y).tip = 5
                create_semaphor x, y
            End If
        End Select
    End If
End Sub

Sub begin_map_editor()
    Dim i
    'prepare interface
    mnuNew.Visible = False
    mnuOpen.Visible = False
    mnuSave.Visible = False
    mnuOrders.Visible = False
    mnuOptions.Visible = False
    mnuTools.Visible = False
    mnuContents.Visible = False
    FrameStatus.Visible = False
    TimerRefreshFigure.Enabled = False
    
    mnuSaveMap.Visible = True
    mnuExitMapEditor.Visible = True
    FrameMapEditor.Top = FrameStatus.Top
    FrameMapEditor.Left = FrameStatus.Left
    FrameMapEditor.Visible = True
    OptionSelectedTool(0).Value = True
    mapCurrentTool = 0
    
    'pause game
    If numpl > 0 Then
        For i = 1 To numpl
            figura(player(i).id).Visible = False
        Next i
    End If
    pauseGame1 = TimerMetKocke.Enabled
    pauseGame2 = TimerSkokFigure.Enabled
    TimerMetKocke.Enabled = False
    TimerSkokFigure.Enabled = False
    
    clkMode = 33        '''
    
End Sub

Sub end_map_editor()
    Dim i
    'interface
    mnuNew.Visible = True
    mnuOpen.Visible = True
    mnuSave.Visible = True
    mnuOrders.Visible = True
    mnuOptions.Visible = True
    mnuTools.Visible = True
    mnuContents.Visible = True
    FrameStatus.Visible = True
    TimerRefreshFigure.Enabled = True
    
    mnuSaveMap.Visible = False
    mnuExitMapEditor.Visible = False
    FrameMapEditor.Visible = False
    
    'resume game (on current map), new game(on new,opened map)
    If numpl > 0 Then
        For i = 1 To numpl
            figura(player(i).id).Visible = True
        Next i
    End If
    TimerMetKocke.Enabled = pauseGame1
    TimerSkokFigure.Enabled = pauseGame2

    Select Case mapEditorMode
    Case 1  'new map was made
        'start new game on curent map
        mnuNew_Click
    Case 2  'current map was modified
        'continue game
    Case 3  'map was opened and modified
        'start new game on curent map
        mnuNew_Click
    End Select
        
    mapEditorMode = 0
    clkMode = 0                 ''map has been modified and game can continue

End Sub

Private Sub mnuSaveMap_Click()
    'save map
    openSaveMode = 3: openSaveFileName = ""
    ''GameOpenSave.Caption = "Save map": GameOpenSave.TextFN.Text = "my.map"
    GameOpenSave.Caption = lngg(58): GameOpenSave.TextFN.Text = "my.map"
    GameOpenSave.File1.Refresh
    GameOpenSave.Show vbModal
    frmMapEditor.File1.Refresh
    NewGame.File1.Refresh: NewGame.fill_combo
End Sub
Private Sub mnuExitMapEditor_Click()
    end_map_editor
End Sub

Sub load_language()
    On Error Resume Next
    Dim s, i
    Open App.Path & "\metropoly.ini" For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[Language]"
    If s = "[Language]" Then
        Line Input #1, s
        selectedLanguage = Left(s, Len(s) - 4)
        Line Input #1, s
        For i = 1 To 13
            If Mid(s, i, 1) = "1" Then
                mnuLngg(i - 1).Visible = True
            Else
                mnuLngg(i - 1).Visible = False
            End If
        Next i
    End If
    Close 1
End Sub


Sub switch_language()
    On Error Resume Next    ''ker unicode format se ne deluje
    
    Dim s, i
    Open App.Path & "\" & selectedLanguage & ".txt" For Input As 1
    For i = 1 To 150
        Line Input #1, lngg(i)
    Next i
    Close 1

    'language
    For i = 1 To 13
        mnuLngg(i - 1).Caption = lngg(i)
    Next i
    mnuLanguage.Caption = lngg(14)
    Me.Caption = lngg(15)
    frmAbout.Caption = lngg(15)
    
    mnuFile.Caption = lngg(17)
    mnuNew.Caption = lngg(18)
    mnuOpen.Caption = lngg(19)
    mnuSave.Caption = lngg(20)
    mnuSaveMap.Caption = lngg(21)
    mnuExitMapEditor.Caption = lngg(22)
    mnuExit.Caption = lngg(23)
    
    mnuOrders.Caption = lngg(25)
    mnuRoad.Caption = lngg(26)
    mnuSell.Caption = lngg(27)
    mnuSemaphors.Caption = lngg(28)
    mnuCreateSemafors.Caption = lngg(29)
    mnuRemoveSemaphor.Caption = lngg(30)
    mnuRotateSemaphors.Caption = lngg(31)
    mnuEndTurn.Caption = lngg(32)
    
    mnuOptions.Caption = lngg(34)
    mnuFast.Caption = lngg(35)
    mnuShowGrid.Caption = lngg(36)
    mnuAutoEndTurn.Caption = lngg(37)
    mnuSound.Caption = lngg(38)
    mnuGraphics.Caption = lngg(39)
    
    mnuTools.Caption = lngg(41)
    mnuMapEditor.Caption = lngg(42)
    
    mnuHelp.Caption = lngg(44)
    mnuContents.Caption = lngg(45)
    mnuAbout.Caption = lngg(46)
    mnuRegister.Caption = lngg(47)
    
    NewGame.Caption = lngg(49)
    NewGame.Label1(0).Caption = lngg(50)
    NewGame.Label1(1).Caption = lngg(51)
    NewGame.Label1(2).Caption = lngg(52)
    NewGame.CommandOK.Caption = lngg(53)        'Ok
    Help.CommandOK.Caption = lngg(53)
    GameOpenSave.CommandOK.Caption = lngg(53)
    frmMapEditor.CommandOK.Caption = lngg(53)
    frmGraphics.CommandOK.Caption = lngg(53)
    frmAbout.Command1.Caption = lngg(53)
    NewGame.CommandCancel.Caption = lngg(54)    'cancel
    GameOpenSave.CommandCancel.Caption = lngg(54)
    frmMapEditor.CommandCancel.Caption = lngg(54)
    frmGraphics.CommandCancel.Caption = lngg(54)
    
    'open
    'save
    'save map
    GameOpenSave.Label1.Caption = lngg(59)
    
    frmGraphics.Caption = lngg(61)
    frmGraphics.Label1.Caption = lngg(62)
    
    frmMapEditor.Caption = lngg(64)
    frmMapEditor.Frame2.Caption = lngg(65)
    frmMapEditor.Label1(0).Caption = lngg(66)
    frmMapEditor.Label1(1).Caption = lngg(67)
    frmMapEditor.Frame1.Caption = lngg(68)
    
    Help.Caption = lngg(70)
    Help.Label1(0).Caption = lngg(71)
    Help.Label1(1).Caption = lngg(72)
    Help.Label1(2).Caption = lngg(73)
    Help.Label1(3).Caption = lngg(74)
    Help.Label1(4).Caption = lngg(75)
    Help.Label1(5).Caption = lngg(76)
    Help.Label1(6).Caption = lngg(77)
    Help.Label1(7).Caption = lngg(78)
    Help.Label1(8).Caption = lngg(79)
    Help.Label1(9).Caption = lngg(80)
    Help.Label1(10).Caption = lngg(81)
    
    '83-143
    
    frmBuyDialog.CommandYes.Caption = lngg(144)     'yes
    frmBuyDialog.CommandNo.Caption = lngg(145)      'no
    
    frmRegister.formcaptions
    
End Sub

Sub pc_intelig_moves()
    Dim i, x, y, p
    'pc sell, road
    If player(curpl).money < 90 Then
        LabelStatus.Caption = ""
        Do
            i = i + 1
            x = Int((dimx - 1 + 1) * Rnd + 1)
            y = Int((dimy - 1 + 1) * Rnd + 1)
            If (map(x, y).owner = curpl) And (map(x, y).tip = 1) Then
                If map(x, y).stage > 0 Then 'sell house
                    If Rnd > 0.7 Then
                        p = sell_price(map(x, y).stage, map(x, y).price)
                        player(curpl).money = player(curpl).money + p
                        player(curpl).stathouse = player(curpl).stathouse - 1
                        map(x, y).stage = map(x, y).stage - 1
                        risipolje x, y, 11 + 0                      'brisi hise
                        risipolje x, y, 11 + Val(map(x, y).stage)   'risi hise
                        risipolje x, y, 19 + Val(player(map(x, y).owner).id)
                        display_status
                    End If
                Else    'sell land
                    If Rnd > 0.5 Then
                        p = sell_price(map(x, y).stage, map(x, y).price)
                        player(curpl).money = player(curpl).money + p
                        player(curpl).statland = player(curpl).statland - 1
                        map(x, y).owner = 0
                        risipolje x, y, 11 + Val(map(x, y).stage)   'brisi zastavico
                        display_status
                        clkMode = 0: LabelStatus.Caption = ""
                    Else
                        p = road_price(x, y)    ''= - 100
                        map(x, y).stage = 0
                        map(x, y).owner = 0
                        map(x, y).tip = 0
                        risi_cesto x, y
                        popravi_sosednje_ceste x, y
                        player(curpl).money = player(curpl).money - p
                        player(curpl).statland = player(curpl).statland - 1
                        player(curpl).stathouse = player(curpl).stathouse - map(x, y).stage
                        display_status
                        LabelStatus.Caption = lngg(103)
                        expand_terit x, y
                    End If
                End If
                If mnuShowGrid.Checked Then display_grid
            End If
        Loop Until (i > 55) Or player(curpl).money > 160
    End If
    
End Sub

Private Sub mnuLngg_Click(Index As Integer)
    Dim fnm(13)
    fnm(1) = "eng"
    fnm(2) = "spa"
    fnm(3) = "por"
    fnm(4) = "ita"
    fnm(5) = "fre"
    fnm(6) = "ger"
    fnm(7) = "chi"
    fnm(8) = "jap"
    fnm(9) = "kor"
    fnm(10) = "slo"
    fnm(11) = "rus"
    fnm(12) = "ser"
    fnm(13) = "oth"
        
    selectedLanguage = fnm(Index + 1)
    switch_language
    
    'save lng to ini
    Dim s, i, idp, n, a(200)
    Open App.Path & "\metropoly.ini" For Input As 1
    i = 1
    Do
        Line Input #1, a(i)
        If a(i) = "[Language]" Then idp = i
        i = i + 1
    Loop Until EOF(1)
    n = i
    Close 1
        
    Open App.Path & "\metropoly.ini" For Output As 1
    For i = 1 To idp
        Print #1, a(i)
    Next i
    Print #1, selectedLanguage & ".txt"
    For i = idp + 2 To n - 1
        Print #1, a(i)
    Next i
    Close 1

End Sub

