VERSION 5.00
Begin VB.Form frmBuyDialog 
   Appearance      =   0  'Flat
   BackColor       =   &H00C0C0C0&
   BorderStyle     =   0  'None
   ClientHeight    =   735
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   1485
   ControlBox      =   0   'False
   ForeColor       =   &H00000000&
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   735
   ScaleWidth      =   1485
   ShowInTaskbar   =   0   'False
   StartUpPosition =   3  'Windows Default
   Begin VB.CommandButton CommandNo 
      Caption         =   "&no"
      Height          =   255
      Left            =   795
      TabIndex        =   2
      Top             =   435
      Width           =   630
   End
   Begin VB.CommandButton CommandYes 
      Caption         =   "&yes"
      Height          =   255
      Left            =   105
      TabIndex        =   1
      Top             =   435
      Width           =   630
   End
   Begin VB.Label LabelQuestion 
      Alignment       =   2  'Center
      BackStyle       =   0  'Transparent
      Caption         =   "Label1"
      Height          =   735
      Left            =   0
      TabIndex        =   0
      Top             =   0
      Width           =   1395
   End
End
Attribute VB_Name = "frmBuyDialog"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub CommandNo_Click()
    buyDialogAnswer = vbNo
    Me.Hide
End Sub

Private Sub CommandYes_Click()
    buyDialogAnswer = vbYes
    Me.Hide
End Sub

Private Sub CommandNo_LostFocus()
    Game.display_status
End Sub

Private Sub CommandYes_LostFocus()
    Game.display_status
End Sub
