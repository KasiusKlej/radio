VERSION 5.00
Begin VB.Form frmGraphics 
   Caption         =   "Metropoly"
   ClientHeight    =   3915
   ClientLeft      =   60
   ClientTop       =   300
   ClientWidth     =   4215
   Icon            =   "frmGraphics.frx":0000
   KeyPreview      =   -1  'True
   LinkTopic       =   "Form1"
   ScaleHeight     =   3915
   ScaleWidth      =   4215
   StartUpPosition =   3  'Windows Default
   Begin VB.CommandButton CommandCancel 
      Caption         =   "Cancel"
      Height          =   360
      Left            =   1485
      TabIndex        =   1
      Top             =   3180
      Width           =   915
   End
   Begin VB.CommandButton CommandOK 
      Caption         =   "OK"
      Height          =   360
      Left            =   435
      TabIndex        =   0
      Top             =   3180
      Width           =   900
   End
   Begin VB.Label Label1 
      Alignment       =   2  'Center
      BackStyle       =   0  'Transparent
      Caption         =   "Click to browse graphics, right-click to browse reversly, control-click to browse details."
      Height          =   885
      Left            =   225
      TabIndex        =   2
      Top             =   2175
      Width           =   2445
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   34
      Left            =   10815
      Picture         =   "frmGraphics.frx":08CA
      Top             =   135
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   33
      Left            =   10815
      Picture         =   "frmGraphics.frx":1594
      Top             =   660
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   32
      Left            =   10815
      Picture         =   "frmGraphics.frx":225E
      Top             =   1200
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   31
      Left            =   10815
      Picture         =   "frmGraphics.frx":2F28
      Top             =   1725
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   30
      Left            =   10815
      Picture         =   "frmGraphics.frx":3BF2
      Top             =   2250
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   29
      Left            =   10815
      Picture         =   "frmGraphics.frx":48BC
      Top             =   2790
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   28
      Left            =   10815
      Picture         =   "frmGraphics.frx":5586
      Top             =   3315
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   41
      Left            =   11460
      Picture         =   "frmGraphics.frx":6250
      Top             =   4965
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   40
      Left            =   11460
      Picture         =   "frmGraphics.frx":6F1A
      Top             =   5475
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   39
      Left            =   11445
      Picture         =   "frmGraphics.frx":7BE4
      Top             =   6000
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   38
      Left            =   11460
      Picture         =   "frmGraphics.frx":88AE
      Top             =   6540
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   37
      Left            =   11460
      Picture         =   "frmGraphics.frx":9578
      Top             =   7050
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   36
      Left            =   11445
      Picture         =   "frmGraphics.frx":A242
      Top             =   7575
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   35
      Left            =   11445
      Picture         =   "frmGraphics.frx":AF0C
      Top             =   8130
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   29
      Left            =   6750
      Picture         =   "frmGraphics.frx":BBD6
      Top             =   3345
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   28
      Left            =   7260
      Picture         =   "frmGraphics.frx":C8A0
      Top             =   3345
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   27
      Left            =   7605
      Picture         =   "frmGraphics.frx":D56A
      Top             =   3375
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   26
      Left            =   7950
      Picture         =   "frmGraphics.frx":E234
      Top             =   3375
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   25
      Left            =   8325
      Picture         =   "frmGraphics.frx":EEFE
      Top             =   3375
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   24
      Left            =   8700
      Picture         =   "frmGraphics.frx":FBC8
      Top             =   3345
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   23
      Left            =   9045
      Picture         =   "frmGraphics.frx":10892
      Top             =   3330
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   22
      Left            =   7260
      Picture         =   "frmGraphics.frx":1155C
      Top             =   3660
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   21
      Left            =   7605
      Picture         =   "frmGraphics.frx":12226
      Top             =   3690
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   20
      Left            =   7980
      Picture         =   "frmGraphics.frx":12EF0
      Top             =   3675
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   17
      Left            =   7935
      Picture         =   "frmGraphics.frx":13BBA
      Top             =   2820
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   16
      Left            =   7425
      Picture         =   "frmGraphics.frx":13EC4
      Top             =   2835
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   15
      Left            =   6915
      Picture         =   "frmGraphics.frx":141CE
      Top             =   2820
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   14
      Left            =   7905
      Picture         =   "frmGraphics.frx":144D8
      Top             =   2400
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   13
      Left            =   7395
      Picture         =   "frmGraphics.frx":147E2
      Top             =   2400
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   12
      Left            =   6900
      Picture         =   "frmGraphics.frx":14AEC
      Top             =   2400
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   32
      Left            =   9090
      Picture         =   "frmGraphics.frx":14DF6
      Top             =   720
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   31
      Left            =   8610
      Picture         =   "frmGraphics.frx":15AC0
      Top             =   705
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   30
      Left            =   8130
      Picture         =   "frmGraphics.frx":1678A
      Top             =   690
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   29
      Left            =   7650
      Picture         =   "frmGraphics.frx":17454
      Top             =   690
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   28
      Left            =   7155
      Picture         =   "frmGraphics.frx":1811E
      Top             =   675
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   27
      Left            =   6705
      Picture         =   "frmGraphics.frx":18DE8
      Top             =   675
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   26
      Left            =   8595
      Picture         =   "frmGraphics.frx":19AB2
      Top             =   195
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   25
      Left            =   8115
      Picture         =   "frmGraphics.frx":1A77C
      Top             =   195
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   24
      Left            =   7620
      Picture         =   "frmGraphics.frx":1B446
      Top             =   195
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   23
      Left            =   7125
      Picture         =   "frmGraphics.frx":1C110
      Top             =   195
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   22
      Left            =   6660
      Picture         =   "frmGraphics.frx":1CDDA
      Top             =   195
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   35
      Left            =   8400
      Picture         =   "frmGraphics.frx":1DAA4
      Top             =   6450
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   34
      Left            =   7905
      Picture         =   "frmGraphics.frx":1DDAE
      Top             =   6435
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   33
      Left            =   7395
      Picture         =   "frmGraphics.frx":1E0B8
      Top             =   6420
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   32
      Left            =   6915
      Picture         =   "frmGraphics.frx":1E982
      Top             =   6435
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   31
      Left            =   8910
      Picture         =   "frmGraphics.frx":1F64C
      Top             =   5955
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   30
      Left            =   8400
      Picture         =   "frmGraphics.frx":20316
      Top             =   5985
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   29
      Left            =   7935
      Picture         =   "frmGraphics.frx":20FE0
      Top             =   5970
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   28
      Left            =   7410
      Picture         =   "frmGraphics.frx":21CAA
      Top             =   5940
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   27
      Left            =   6915
      Picture         =   "frmGraphics.frx":22974
      Top             =   5955
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   34
      Left            =   11400
      Picture         =   "frmGraphics.frx":2363E
      Top             =   165
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   33
      Left            =   11415
      Picture         =   "frmGraphics.frx":24308
      Top             =   675
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   32
      Left            =   11400
      Picture         =   "frmGraphics.frx":24FD2
      Top             =   1200
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   31
      Left            =   11415
      Picture         =   "frmGraphics.frx":25C9C
      Top             =   1740
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   30
      Left            =   11415
      Picture         =   "frmGraphics.frx":26966
      Top             =   2250
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   29
      Left            =   11400
      Picture         =   "frmGraphics.frx":27630
      Top             =   2775
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   28
      Left            =   11400
      Picture         =   "frmGraphics.frx":282FA
      Top             =   3330
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   27
      Left            =   9555
      Picture         =   "frmGraphics.frx":28FC4
      Top             =   5010
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   26
      Left            =   9555
      Picture         =   "frmGraphics.frx":292CE
      Top             =   5535
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   25
      Left            =   9555
      Picture         =   "frmGraphics.frx":295D8
      Top             =   6075
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   24
      Left            =   9555
      Picture         =   "frmGraphics.frx":298E2
      Top             =   6600
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   23
      Left            =   9555
      Picture         =   "frmGraphics.frx":29BEC
      Top             =   7125
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   22
      Left            =   9555
      Picture         =   "frmGraphics.frx":29EF6
      Top             =   7665
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   21
      Left            =   9555
      Picture         =   "frmGraphics.frx":2A200
      Top             =   8190
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   27
      Left            =   10140
      Picture         =   "frmGraphics.frx":2A50A
      Top             =   5025
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   26
      Left            =   10140
      Picture         =   "frmGraphics.frx":2B1D4
      Top             =   5535
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   25
      Left            =   10125
      Picture         =   "frmGraphics.frx":2BE9E
      Top             =   6060
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   24
      Left            =   10140
      Picture         =   "frmGraphics.frx":2CB68
      Top             =   6600
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   23
      Left            =   10140
      Picture         =   "frmGraphics.frx":2D832
      Top             =   7110
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   22
      Left            =   10125
      Picture         =   "frmGraphics.frx":2E4FC
      Top             =   7635
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   21
      Left            =   10125
      Picture         =   "frmGraphics.frx":2F1C6
      Top             =   8190
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   26
      Left            =   8490
      Picture         =   "frmGraphics.frx":2FE90
      Top             =   1755
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   25
      Left            =   7980
      Picture         =   "frmGraphics.frx":30B5A
      Top             =   1755
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   24
      Left            =   7515
      Picture         =   "frmGraphics.frx":30E64
      Top             =   1770
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   23
      Left            =   6930
      Picture         =   "frmGraphics.frx":31B2E
      Top             =   1740
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   22
      Left            =   8880
      Picture         =   "frmGraphics.frx":327F8
      Top             =   1320
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   21
      Left            =   8400
      Picture         =   "frmGraphics.frx":334C2
      Top             =   1290
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   20
      Left            =   7920
      Picture         =   "frmGraphics.frx":3418C
      Top             =   1305
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   19
      Left            =   7410
      Picture         =   "frmGraphics.frx":34E56
      Top             =   1275
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   18
      Left            =   6960
      Picture         =   "frmGraphics.frx":35B20
      Top             =   1230
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   20
      Left            =   9645
      Picture         =   "frmGraphics.frx":367EA
      Top             =   105
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   19
      Left            =   9645
      Picture         =   "frmGraphics.frx":374B4
      Top             =   630
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   18
      Left            =   9645
      Picture         =   "frmGraphics.frx":3817E
      Top             =   1170
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   17
      Left            =   9645
      Picture         =   "frmGraphics.frx":38E48
      Top             =   1695
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   16
      Left            =   9645
      Picture         =   "frmGraphics.frx":39B12
      Top             =   2220
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   15
      Left            =   9645
      Picture         =   "frmGraphics.frx":3A7DC
      Top             =   2760
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   14
      Left            =   9645
      Picture         =   "frmGraphics.frx":3B4A6
      Top             =   3285
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   20
      Left            =   10230
      Picture         =   "frmGraphics.frx":3C170
      Top             =   120
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   19
      Left            =   10230
      Picture         =   "frmGraphics.frx":3CE3A
      Top             =   630
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   18
      Left            =   10215
      Picture         =   "frmGraphics.frx":3DB04
      Top             =   1155
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   17
      Left            =   10230
      Picture         =   "frmGraphics.frx":3E7CE
      Top             =   1695
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   16
      Left            =   10230
      Picture         =   "frmGraphics.frx":3F498
      Top             =   2205
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   15
      Left            =   10215
      Picture         =   "frmGraphics.frx":40162
      Top             =   2730
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   14
      Left            =   10215
      Picture         =   "frmGraphics.frx":40E2C
      Top             =   3285
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   19
      Left            =   1440
      Picture         =   "frmGraphics.frx":41AF6
      Top             =   8400
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   18
      Left            =   1080
      Picture         =   "frmGraphics.frx":41E00
      Top             =   8415
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   17
      Left            =   720
      Picture         =   "frmGraphics.frx":4210A
      Top             =   8385
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   16
      Left            =   2505
      Picture         =   "frmGraphics.frx":42414
      Top             =   8055
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   15
      Left            =   2160
      Picture         =   "frmGraphics.frx":4271E
      Top             =   8070
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   14
      Left            =   1785
      Picture         =   "frmGraphics.frx":42A28
      Top             =   8100
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   13
      Left            =   1410
      Picture         =   "frmGraphics.frx":42D32
      Top             =   8100
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   12
      Left            =   1065
      Picture         =   "frmGraphics.frx":4303C
      Top             =   8100
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   11
      Left            =   720
      Picture         =   "frmGraphics.frx":43346
      Top             =   8085
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   480
      Index           =   10
      Left            =   210
      Picture         =   "frmGraphics.frx":43650
      Top             =   8070
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   9
      Left            =   5700
      Top             =   5925
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   8
      Left            =   5325
      Top             =   5940
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   7
      Left            =   4980
      Top             =   5910
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   6
      Left            =   6765
      Top             =   5580
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   5
      Left            =   6420
      Top             =   5595
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   4
      Left            =   6045
      Top             =   5625
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   3
      Left            =   5670
      Top             =   5625
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   450
      Index           =   2
      Left            =   1215
      Top             =   1200
      Width           =   435
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   1
      Left            =   4980
      Top             =   5610
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageGauge 
      Height          =   405
      Index           =   0
      Left            =   4470
      Top             =   5595
      Visible         =   0   'False
      Width           =   450
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   13
      Left            =   3990
      Picture         =   "frmGraphics.frx":4395A
      Top             =   8175
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   12
      Left            =   3990
      Picture         =   "frmGraphics.frx":44624
      Top             =   7620
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   11
      Left            =   4005
      Picture         =   "frmGraphics.frx":452EE
      Top             =   7095
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   10
      Left            =   4005
      Picture         =   "frmGraphics.frx":45FB8
      Top             =   6585
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   9
      Left            =   3990
      Picture         =   "frmGraphics.frx":46C82
      Top             =   6045
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   8
      Left            =   4005
      Picture         =   "frmGraphics.frx":4794C
      Top             =   5520
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   480
      Index           =   7
      Left            =   4005
      Picture         =   "frmGraphics.frx":48616
      Top             =   5010
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   13
      Left            =   3435
      Picture         =   "frmGraphics.frx":492E0
      Top             =   8175
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   12
      Left            =   3420
      Picture         =   "frmGraphics.frx":495EA
      Top             =   7650
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   11
      Left            =   3420
      Picture         =   "frmGraphics.frx":498F4
      Top             =   7110
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   10
      Left            =   3420
      Picture         =   "frmGraphics.frx":49BFE
      Top             =   6585
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   9
      Left            =   3420
      Picture         =   "frmGraphics.frx":49F08
      Top             =   6060
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   8
      Left            =   3420
      Picture         =   "frmGraphics.frx":4A212
      Top             =   5520
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImagePlayer 
      Height          =   480
      Index           =   7
      Left            =   3420
      Picture         =   "frmGraphics.frx":4A51C
      Top             =   4995
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   11
      Left            =   1185
      Picture         =   "frmGraphics.frx":4A826
      Top             =   7515
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   10
      Left            =   690
      Picture         =   "frmGraphics.frx":4AB30
      Top             =   7515
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   9
      Left            =   195
      Picture         =   "frmGraphics.frx":4AE3A
      Top             =   7515
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   8
      Left            =   1185
      Picture         =   "frmGraphics.frx":4B144
      Top             =   7095
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   7
      Left            =   690
      Picture         =   "frmGraphics.frx":4B44E
      Top             =   7095
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageKocka 
      Height          =   480
      Index           =   6
      Left            =   195
      Picture         =   "frmGraphics.frx":4B758
      Top             =   7095
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   17
      Left            =   1650
      Picture         =   "frmGraphics.frx":4BA62
      Top             =   6555
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   16
      Left            =   1170
      Picture         =   "frmGraphics.frx":4C72C
      Top             =   6555
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   15
      Left            =   690
      Picture         =   "frmGraphics.frx":4D3F6
      Top             =   6570
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   14
      Left            =   210
      Picture         =   "frmGraphics.frx":4E0C0
      Top             =   6555
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   13
      Left            =   2130
      Picture         =   "frmGraphics.frx":4ED8A
      Top             =   6090
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   12
      Left            =   1650
      Picture         =   "frmGraphics.frx":4FA54
      Top             =   6090
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   11
      Left            =   1170
      Picture         =   "frmGraphics.frx":5071E
      Top             =   6090
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   10
      Left            =   690
      Picture         =   "frmGraphics.frx":513E8
      Top             =   6090
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageHouse 
      Height          =   480
      Index           =   9
      Left            =   210
      Picture         =   "frmGraphics.frx":520B2
      Top             =   6090
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   21
      Left            =   2610
      Picture         =   "frmGraphics.frx":52D7C
      Top             =   5445
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   20
      Left            =   2100
      Picture         =   "frmGraphics.frx":53A46
      Top             =   5445
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   19
      Left            =   1635
      Picture         =   "frmGraphics.frx":54710
      Top             =   5460
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   18
      Left            =   1140
      Picture         =   "frmGraphics.frx":553DA
      Top             =   5460
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   17
      Left            =   660
      Picture         =   "frmGraphics.frx":560A4
      Top             =   5460
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   16
      Left            =   180
      Picture         =   "frmGraphics.frx":56D6E
      Top             =   5460
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   15
      Left            =   2295
      Picture         =   "frmGraphics.frx":57A38
      Top             =   4935
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   14
      Left            =   1725
      Picture         =   "frmGraphics.frx":58702
      Top             =   4920
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   13
      Left            =   1125
      Picture         =   "frmGraphics.frx":593CC
      Top             =   4890
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   12
      Left            =   600
      Picture         =   "frmGraphics.frx":5A096
      Top             =   4875
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageRoad 
      Height          =   480
      Index           =   11
      Left            =   120
      Picture         =   "frmGraphics.frx":5AD60
      Top             =   4905
      Visible         =   0   'False
      Width           =   480
   End
   Begin VB.Image ImageFlag 
      Height          =   495
      Index           =   6
      Left            =   3465
      Top             =   3285
      Width           =   525
   End
   Begin VB.Image ImageFlag 
      Height          =   495
      Index           =   5
      Left            =   3465
      Top             =   2760
      Width           =   525
   End
   Begin VB.Image ImageFlag 
      Height          =   495
      Index           =   4
      Left            =   3465
      Top             =   2250
      Width           =   525
   End
   Begin VB.Image ImageFlag 
      Height          =   495
      Index           =   3
      Left            =   3465
      Top             =   1725
      Width           =   525
   End
   Begin VB.Image ImageFlag 
      Height          =   495
      Index           =   2
      Left            =   3465
      Top             =   1185
      Width           =   525
   End
   Begin VB.Image ImageFlag 
      Height          =   495
      Index           =   1
      Left            =   3465
      Top             =   660
      Width           =   525
   End
   Begin VB.Image ImageFlag 
      Height          =   495
      Index           =   0
      Left            =   3465
      Top             =   135
      Width           =   525
   End
   Begin VB.Image ImagePlayer 
      Height          =   510
      Index           =   6
      Left            =   2880
      Top             =   3285
      Width           =   555
   End
   Begin VB.Image ImagePlayer 
      Height          =   510
      Index           =   5
      Left            =   2880
      Top             =   2760
      Width           =   555
   End
   Begin VB.Image ImagePlayer 
      Height          =   510
      Index           =   4
      Left            =   2880
      Top             =   2250
      Width           =   555
   End
   Begin VB.Image ImagePlayer 
      Height          =   510
      Index           =   3
      Left            =   2880
      Top             =   1725
      Width           =   555
   End
   Begin VB.Image ImagePlayer 
      Height          =   510
      Index           =   2
      Left            =   2880
      Top             =   1185
      Width           =   555
   End
   Begin VB.Image ImagePlayer 
      Height          =   510
      Index           =   1
      Left            =   2880
      Top             =   660
      Width           =   555
   End
   Begin VB.Image ImagePlayer 
      Height          =   510
      Index           =   0
      Left            =   2880
      Top             =   135
      Width           =   555
   End
   Begin VB.Image ImageKocka 
      Height          =   435
      Index           =   5
      Left            =   5430
      Top             =   5085
      Visible         =   0   'False
      Width           =   510
   End
   Begin VB.Image ImageKocka 
      Height          =   435
      Index           =   4
      Left            =   4935
      Top             =   5085
      Visible         =   0   'False
      Width           =   510
   End
   Begin VB.Image ImageKocka 
      Height          =   435
      Index           =   3
      Left            =   4440
      Top             =   5085
      Visible         =   0   'False
      Width           =   510
   End
   Begin VB.Image ImageKocka 
      Height          =   435
      Index           =   2
      Left            =   735
      Top             =   1200
      Width           =   510
   End
   Begin VB.Image ImageKocka 
      Height          =   435
      Index           =   1
      Left            =   4935
      Top             =   4665
      Visible         =   0   'False
      Width           =   510
   End
   Begin VB.Image ImageKocka 
      Height          =   435
      Index           =   0
      Left            =   4440
      Top             =   4665
      Visible         =   0   'False
      Width           =   510
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   8
      Left            =   1680
      Top             =   660
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   7
      Left            =   1200
      Top             =   660
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   6
      Left            =   720
      Top             =   660
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   5
      Left            =   240
      Top             =   660
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   4
      Left            =   2175
      Top             =   135
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   3
      Left            =   1695
      Top             =   135
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   2
      Left            =   1215
      Top             =   135
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   1
      Left            =   735
      Top             =   135
      Width           =   495
   End
   Begin VB.Image ImageHouse 
      Height          =   435
      Index           =   0
      Left            =   255
      Top             =   135
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   10
      Left            =   6840
      Top             =   4125
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   9
      Left            =   6360
      Top             =   4125
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   8
      Left            =   5880
      Top             =   4140
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   7
      Left            =   5400
      Top             =   4125
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   6
      Left            =   4920
      Top             =   4140
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   5
      Left            =   4440
      Top             =   4140
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   4
      Left            =   6360
      Top             =   3690
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   3
      Left            =   5880
      Top             =   3690
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   2
      Left            =   255
      Top             =   1200
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   1
      Left            =   4920
      Top             =   3690
      Visible         =   0   'False
      Width           =   495
   End
   Begin VB.Image ImageRoad 
      Height          =   450
      Index           =   0
      Left            =   4440
      Top             =   3690
      Visible         =   0   'False
      Width           =   495
   End
End
Attribute VB_Name = "frmGraphics"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
Dim nb(6)   'stevilo bank
Dim ni(6)   'stevilo ikon v banki

'in ini file------
Dim ub(6)       'used bank
Dim ubPlayer(7), uiPlayer(7) '(detailed use: player,flag, house,school,job,jail)
Dim ubFlag(7), uiFlag(7)
Dim ubHouse(9), uiHouse(9)
'-----------------

Dim shiftsmer   '1=naprej, -1=nazaj
Dim shiftbank   'katero banko
Dim shiftDetaljnaIzbira  '0=shift cela banka, 1=detajlno

Private Sub CommandCancel_Click()
    Me.Hide
End Sub

Private Sub CommandOK_Click()
    apply_icons
    write_graphics_to_ini
    
    'refresh
    Game.draw_map
    Game.display_status
    
    Me.Hide
End Sub

Private Sub Form_Load()
    Dim i
    Me.Left = (Screen.Width - Me.Width) / 2
    Me.Top = (Screen.Height - Me.Height) / 2
    
    display_icons       'displays currently used icons

    'set deafults to bank1
    For i = 0 To 6
        uiPlayer(i) = i: ubPlayer(i) = 1
        uiFlag(i) = i: ubFlag(i) = 1
        uiHouse(i) = i: ubHouse(i) = 1
    Next i
    ub(1) = 1
    ub(2) = 1
    ub(3) = 1
    ub(4) = 1
    ub(5) = 1
    ub(6) = 1
   
    'form konstante
    nb(1) = 2 'ceste
    nb(2) = 3 'hise, school,job,jail
    nb(3) = 2 'kocka
    nb(4) = 2 'gauge
    nb(5) = 4 'figure
    nb(6) = 5 'flags
    ni(1) = 11
    ni(2) = 9
    ni(3) = 6
    ni(4) = 10
    ni(5) = 7
    ni(6) = 7
    
    shiftsmer = 1   'naprej
    shiftDetaljnaIzbira = 0
    
End Sub


Private Sub ImageRoad_MouseDown(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 1 Then 'left
        shiftsmer = 1
    End If
    If Button = 2 Then 'right
        shiftsmer = -1
    End If
    shiftbank = 1
    shiftDetaljnaIzbira = 0
End Sub

Private Sub ImageHouse_MouseDown(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 1 Then 'left
        shiftsmer = 1
    End If
    If Button = 2 Then 'right
        shiftsmer = -1
    End If
    shiftbank = 2
    If Shift > 0 Then 'ctrl, alt or shift
        shiftDetaljnaIzbira = 1
    Else
        shiftDetaljnaIzbira = 0
    End If
End Sub

Private Sub ImageKocka_MouseDown(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 1 Then 'left
        shiftsmer = 1
    End If
    If Button = 2 Then 'right
        shiftsmer = -1
    End If
    shiftbank = 3
    shiftDetaljnaIzbira = 0
End Sub

Private Sub ImageGauge_MouseDown(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 1 Then 'left
        shiftsmer = 1
    End If
    If Button = 2 Then 'right
        shiftsmer = -1
    End If
    shiftbank = 4
    shiftDetaljnaIzbira = 0
End Sub
Private Sub ImagePlayer_MouseDown(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 1 Then 'left
        shiftsmer = 1
    End If
    If Button = 2 Then 'right
        shiftsmer = -1
    End If
    shiftbank = 5
    If Shift > 0 Then 'ctrl, alt or shift
        shiftDetaljnaIzbira = 1
    Else
        shiftDetaljnaIzbira = 0
    End If
End Sub

Private Sub ImageFlag_MouseDown(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 1 Then 'left
        shiftsmer = 1
    End If
    If Button = 2 Then 'right
        shiftsmer = -1
    End If
    shiftbank = 6
        If Shift > 0 Then 'ctrl, alt or shift
        shiftDetaljnaIzbira = 1
    Else
        shiftDetaljnaIzbira = 0
    End If
End Sub

Private Sub ImageRoad_MouseUp(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    On Error Resume Next
    Dim i
    '1 rotate road
    ub(1) = ub(1) + shiftsmer
    If ub(1) < 1 Then ub(1) = 1
    If ub(1) > nb(1) Then ub(1) = nb(1)
    For i = 0 To 10
        ImageRoad(i).Picture = ImageRoad(i + ub(1) * ni(1)).Picture
    Next i
    
End Sub

Private Sub ImageHouse_MouseUp(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    '2
    On Error Resume Next
    Dim i
    If shiftDetaljnaIzbira = 0 Then 'cela banka
        ub(2) = ub(2) + shiftsmer
        If ub(2) < 1 Then ub(2) = 1
        If ub(2) > nb(2) Then ub(2) = nb(2)
        If Index < 5 Then
            For i = 0 To 4
                ImageHouse(i).Picture = ImageHouse(i + ub(2) * ni(2)).Picture
                uiHouse(i) = i
                ubHouse(i) = ub(2)
            Next i
        Else
            For i = 5 To 8
                ImageHouse(i).Picture = ImageHouse(i + ub(2) * ni(2)).Picture
                uiHouse(i) = i
                ubHouse(i) = ub(2)
            Next i
        End If
    Else
        If Index < 5 Then   '01234 hise detajlno
            uiHouse(Index) = uiHouse(Index) + 1
            If uiHouse(Index) > 4 Then
                uiHouse(Index) = 0
                ubHouse(Index) = ubHouse(Index) + 1
                If ubHouse(Index) > nb(2) Then ubHouse(Index) = 1
            End If
            ImageHouse(Index).Picture = ImageHouse(ubHouse(Index) * ni(2) + uiHouse(Index)).Picture
        Else                '5678 h0,school,job,jail
            ubHouse(Index) = ubHouse(Index) + shiftsmer
            If ubHouse(Index) > nb(2) Then ubHouse(Index) = 1
            If ubHouse(Index) < 1 Then ubHouse(Index) = nb(2)
            ImageHouse(Index).Picture = ImageHouse(ubHouse(Index) * ni(2) + Index).Picture
        End If
    
    End If

End Sub

Private Sub ImageKocka_MouseUp(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    '3
    On Error Resume Next
    Dim i
    ub(3) = ub(3) + shiftsmer
    If ub(3) < 1 Then ub(3) = 1
    If ub(3) > nb(3) Then ub(3) = nb(3)
    For i = 0 To 5
        ImageKocka(i).Picture = ImageKocka(i + ub(3) * ni(3)).Picture
    Next i

End Sub
Private Sub ImageGauge_MouseUp(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    '4
    On Error Resume Next
    Dim i
    ub(4) = ub(4) + shiftsmer
    If ub(4) < 1 Then ub(4) = 1
    If ub(4) > nb(4) Then ub(4) = nb(4)
    For i = 0 To 9
        ImageGauge(i).Picture = ImageGauge(i + ub(4) * ni(4)).Picture
    Next i

End Sub

Private Sub ImagePlayer_MouseUp(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    '5
    On Error Resume Next
    Dim i
    If shiftDetaljnaIzbira = 0 Then 'cela banka
        ub(5) = ub(5) + shiftsmer
        If ub(5) < 1 Then ub(5) = 1
        If ub(5) > nb(5) Then ub(5) = nb(5)
        For i = 0 To 6
            ImagePlayer(i).Picture = ImagePlayer(i + ub(5) * ni(5)).Picture
            uiPlayer(i) = i
            ubPlayer(i) = ub(5)
        Next i
    Else    'detajlno
        'display next icon
        uiPlayer(Index) = uiPlayer(Index) + shiftsmer
        If uiPlayer(Index) >= ni(5) Then
            uiPlayer(Index) = 0
            ubPlayer(Index) = ubPlayer(Index) + 1
            If ubPlayer(Index) > nb(5) Then ubPlayer(Index) = 1
        End If
        If uiPlayer(Index) < 0 Then
            uiPlayer(Index) = ni(5) - 1
            ubPlayer(Index) = ubPlayer(Index) - 1
            If ubPlayer(Index) < 1 Then ubPlayer(Index) = nb(5)
        End If
        
        ImagePlayer(Index).Picture = ImagePlayer(ubPlayer(Index) * ni(5) + uiPlayer(Index)).Picture
    End If

End Sub
Private Sub ImageFlag_MouseUp(Index As Integer, Button As Integer, Shift As Integer, x As Single, y As Single)
    '6
    On Error Resume Next
    Dim i
    If shiftDetaljnaIzbira = 0 Then 'cela banka
        ub(6) = ub(6) + shiftsmer
        If ub(6) < 1 Then ub(6) = 1
        If ub(6) > nb(6) Then ub(6) = nb(6)
        For i = 0 To 6
            ImageFlag(i).Picture = ImageFlag(i + ub(6) * ni(6)).Picture
            uiFlag(i) = i
            ubFlag(i) = ub(6)
        Next i
    Else    'detajlno
        uiFlag(Index) = uiFlag(Index) + shiftsmer
        If uiFlag(Index) >= ni(6) Then
            uiFlag(Index) = 0
            ubFlag(Index) = ubFlag(Index) + 1
            If ubFlag(Index) > nb(6) Then ubFlag(Index) = 1
        End If
        If uiFlag(Index) < 0 Then
            uiFlag(Index) = ni(6) - 1
            ubFlag(Index) = ubFlag(Index) - 1
            If ubFlag(Index) < 1 Then ubFlag(Index) = nb(6)
        End If
        
        ImageFlag(Index).Picture = ImageFlag(ubFlag(Index) * ni(6) + uiFlag(Index)).Picture
    End If

End Sub

Sub display_icons()
    'displays current
    Dim i
    'bank1
    For i = 0 To 10
        ImageRoad(i).Picture = Game.ImageResource(i)
    Next i
    'bank2
    ImageHouse(5).Picture = Game.ImageResource(11)
    ImageHouse(6).Picture = Game.ImageResource(17)
    ImageHouse(7).Picture = Game.ImageResource(18)
    ImageHouse(8).Picture = Game.ImageResource(19)
    For i = 0 To 4
        ImageHouse(i).Picture = Game.ImageResource(i + 12)
    Next i
    'bank3
    For i = 0 To 5
        ImageKocka(i).Picture = Game.ImageResource(i + 27)
    Next i
    'bank4
    For i = 0 To 9
        ImageGauge(i).Picture = Game.ImageResource(i + 45)
    Next i
    'bank5,6
    For i = 0 To 6
        ImagePlayer(i).Picture = Game.figura(i + 1).Picture
        ImageFlag(i).Picture = Game.ImageResource(i + 20)
    Next i

End Sub

Sub apply_icons()
    Dim i
    'bank1
    For i = 0 To 10
        Game.ImageResource(i) = ImageRoad(i).Picture
    Next i
    'bank2
    Game.ImageResource(11) = ImageHouse(5).Picture
    Game.ImageResource(17) = ImageHouse(6).Picture
    Game.ImageResource(18) = ImageHouse(7).Picture
    Game.ImageResource(19) = ImageHouse(8).Picture
    For i = 0 To 4
         Game.ImageResource(i + 12) = ImageHouse(i).Picture
    Next i
    'bank3
    For i = 0 To 5
        Game.ImageResource(i + 27) = ImageKocka(i).Picture
    Next i
    'bank4
    For i = 0 To 9
        Game.ImageResource(i + 45) = ImageGauge(i).Picture
    Next i
    'bank5,6
    For i = 0 To 6
        Game.figura(i + 1).Picture = ImagePlayer(i).Picture
        Game.ImageResource(i + 20) = ImageFlag(i).Picture
        NewGame.figura(i + 1).Picture = ImagePlayer(i).Picture
    Next i
    
    'map editor tools
    Game.ImageSelectedTool(0).Picture = Game.ImageResource(2)
    Game.ImageSelectedTool(1).Picture = Game.ImageResource(11)
    Game.ImageSelectedTool(2).Picture = Game.ImageResource(17)
    Game.ImageSelectedTool(3).Picture = Game.ImageResource(18)
    Game.ImageSelectedTool(4).Picture = Game.ImageResource(33)
    
End Sub

Sub write_graphics_to_ini()
    ''[Graphics] must be last section in ini
    Dim s, i, idp, n, a(200)
    Open App.Path & "\metropoly.ini" For Input As 1
    i = 1
    Do
        Line Input #1, a(i)
        If a(i) = "[Graphics]" Then idp = i
        i = i + 1
    Loop Until EOF(1)
    n = i
    Close 1
        
    Open App.Path & "\metropoly.ini" For Output As 1
    For i = 1 To idp
        Print #1, a(i)
    Next i
    
    If Rnd < 0.9 Then   'every now and then omit this from ini to restart game with default icons
        For i = 0 To 5
            If ub(i) = 0 Then   'this is bug but avoids 0 being print to file (bank 0 cant be applyed, but bank 0 is default icons\*.ico)
                Print #1, "1"
            Else
                Print #1, Trim(Str(ub(i)))
            End If
        Next i
        For i = 0 To 6
            If ubPlayer(i) = 0 Then
                Print #1, "1"
            Else
                Print #1, Trim(Str(ubPlayer(i)))
            End If
            Print #1, Trim(Str(uiPlayer(i)))
        Next i
        For i = 0 To 6
            If ubFlag(i) = 0 Then
                Print #1, "1"
            Else
                Print #1, Trim(Str(ubFlag(i)))
            End If
            Print #1, Trim(Str(uiFlag(i)))
        Next i
        For i = 0 To 8
            If ubHouse(i) = 0 Then
                Print #1, "1"
            Else
                Print #1, Trim(Str(ubHouse(i)))
            End If
            Print #1, Trim(Str(uiHouse(i)))
        Next i
        
    End If
    
    Close 1
End Sub

Sub load_graphics_from_ini()
    'used only at start
    On Error Resume Next
    Me.Show         ''to avoid form_load at this point
    
    Dim s, i
    Open App.Path & "\metropoly.ini" For Input As 1
    Do
        Line Input #1, s
    Loop Until EOF(1) Or s = "[Graphics]"
    If s = "[Graphics]" Then
        For i = 0 To 5
            Line Input #1, s
            ub(i) = Val(s)
            ''If ub(i) = 0 Then ub(i) = 1     'bank 0 je current in ne more veljati zato 1 (zal je v ini filu lahko 0 - bug)
        Next i
        For i = 0 To 6
            Line Input #1, s
            ubPlayer(i) = Val(s)
            ''If ubPlayer(i) = 0 Then ubPlayer(i) = 1
            Line Input #1, s
            uiPlayer(i) = Val(s)
            ''If uiPlayer(i) = 0 Then uiPlayer(i) = 1
        Next i
        For i = 0 To 6
            Line Input #1, s
            ubFlag(i) = Val(s)
            ''If ubFlag(i) = 0 Then ubFlag(i) = 1
            Line Input #1, s
            uiFlag(i) = Val(s)
            ''If uiFlag(i) = 0 Then uiFlag(i) = 1
        Next i
        For i = 0 To 8
            Line Input #1, s
            ubHouse(i) = Val(s)
            ''If ubHouse(i) = 0 Then ubHouse(i) = 1
            Line Input #1, s
            uiHouse(i) = Val(s)
            ''If uiHouse(i) = 0 Then uiHouse(i) = 1
        Next i
    End If
    Close 1
    
    'load default, cez pa custom details
    '1
    For i = 0 To 10
        ImageRoad(i).Picture = ImageRoad(i + ub(1) * ni(1)).Picture
    Next i
    '2
    For i = 1 To 8
        ImageHouse(i).Picture = ImageHouse(i + ub(2) * ni(2)).Picture
    Next i
    For i = 0 To 8
        ImageHouse(i).Picture = ImageHouse(uiHouse(i) + ubHouse(i) * ni(2)).Picture
    Next i
    '3
    For i = 0 To 5
        ImageKocka(i).Picture = ImageKocka(i + ub(3) * ni(3)).Picture
    Next i
    '4
    For i = 0 To 9
        ImageGauge(i).Picture = ImageGauge(i + ub(4) * ni(4)).Picture
    Next i
    '5
    For i = 0 To 6
        ImagePlayer(i).Picture = ImagePlayer(i + ub(5) * ni(5)).Picture
    Next i
    For i = 0 To 6
        ImagePlayer(i).Picture = ImagePlayer(uiPlayer(i) + ubPlayer(i) * ni(5)).Picture
    Next i
    '6
    For i = 0 To 6
        ImageFlag(i).Picture = ImageFlag(i + ub(5) * ni(6)).Picture
    Next i
    For i = 0 To 6
        ImageFlag(i).Picture = ImageFlag(uiFlag(i) + ubFlag(i) * ni(6)).Picture
    Next i
    
    apply_icons
    
    Me.Hide
End Sub

Private Sub Form_KeyPress(KeyAscii As Integer)
    If KeyAscii = 27 Then CommandCancel_Click
End Sub

