Attribute VB_Name = "Module1"
Declare Function TextOut Lib "gdi32" Alias "TextOutA" (ByVal hdc As Long, ByVal x As Long, ByVal y As Long, ByVal lpString As String, ByVal nCount As Long) As Long
''Declare Function sndPlaySound Lib "mmsystem.dll" Alias "sndplaysound" (ByVal nam$, ByVal flags%) As Integer
''zvok = sndplaysound(app.Path + "\zvok\kocka.wav", 1)
Declare Function sndPlaySound Lib "winmm.dll" Alias "sndPlaySoundA" (ByVal lpszSoundName As String, ByVal uFlags As Long) As Long

Type playertip
 id As Integer
 tip As Integer
 ime As Variant
 barva As Long
 money As Integer
 smer As Integer
 izobrazba As Integer
 x As Integer
 y As Integer
 jobpayment As Integer
 statland As Integer
 stathouse As Integer
End Type

Type maptip
 tip As Integer
 semafor As Integer
 price As Integer
 stage As Integer
 owner As Integer
End Type

Global numpl
Global player(7) As playertip
Global map(100, 100) As maptip
Global dimx As Integer, dimy As Integer
Global startx As Integer, starty As Integer, startsmer As Integer, jailx As Integer, jaily As Integer
Global faza, curpl
Global kocka, cakajKocko

Global zoomfaktor As Double

Global dayOfWeek
Global dayOfWeekName(7)
Global clkMode              'click on form 0=info, 1=sell, 2=build road, ...
Global izobrazbaNaziv(6)
Global semaforData(81)

Global openSaveFileName
Global openSaveMode         '0-open, 1-save, 2-save map
Global buyDialogAnswer
Global gameTurnSmer, gameTurnVpadnica   'doloca kako obrniti semaforje
Global keyboardShortcut(5)              'orders
Global mapEditorMode                    '0=game 123=map editor
Global mapCurrentTool
Global pauseGame1, pauseGame2           'used to remember timers

Global serialNumber     'register
Global selectedLanguage, lngg(150)      'txt filename


Sub set_data()
    'init
    clkMode = 0
    dayOfWeek = 1: gameTurnVpadnica = 0: gameTurnSmer = 0
    mapEditorMode = 0
    
    dayOfWeekName(1) = lngg(128)    '"Monday"
    dayOfWeekName(2) = lngg(129)
    dayOfWeekName(3) = lngg(130)
    dayOfWeekName(4) = lngg(131)
    dayOfWeekName(5) = lngg(132)
    dayOfWeekName(6) = lngg(133)
    dayOfWeekName(7) = lngg(134)
    
    izobrazbaNaziv(0) = ""
    izobrazbaNaziv(1) = lngg(135)   '"pupil"
    izobrazbaNaziv(2) = lngg(136)
    izobrazbaNaziv(3) = lngg(137)
    izobrazbaNaziv(4) = lngg(138)
    izobrazbaNaziv(5) = lngg(139)

    semaforData(1) = "211133363942"
    semaforData(2) = "211233363943"
    semaforData(3) = "211333363944"
    semaforData(4) = "212133364042"
    semaforData(5) = "212233364043"
    semaforData(6) = "212333364044"
    semaforData(7) = "214133364142"
    semaforData(8) = "214233364143"
    semaforData(9) = "214333364144"
    semaforData(10) = "231133373942"
    semaforData(11) = "231233373943"
    semaforData(12) = "231333373944"
    semaforData(13) = "232133374042"
    semaforData(14) = "232233374043"
    semaforData(15) = "232333374044"
    semaforData(16) = "234133374142"
    semaforData(17) = "234233374143"
    semaforData(18) = "234333374144"
    semaforData(19) = "241133383942"
    semaforData(20) = "241233383943"
    semaforData(21) = "241333383944"
    semaforData(22) = "242133384042"
    semaforData(23) = "242233384043"
    semaforData(24) = "242333384044"
    semaforData(25) = "244133384142"
    semaforData(26) = "244233384143"
    semaforData(27) = "244333384144"
    semaforData(28) = "311134363942"
    semaforData(29) = "311234363943"
    semaforData(30) = "311334363944"
    semaforData(31) = "312134364042"
    semaforData(32) = "312234364043"
    semaforData(33) = "312334364044"
    semaforData(34) = "314134364142"
    semaforData(35) = "314234364143"
    semaforData(36) = "314334364144"
    semaforData(37) = "331134373942"
    semaforData(38) = "331234373943"
    semaforData(39) = "331334373944"
    semaforData(40) = "332134374042"
    semaforData(41) = "332234374043"
    semaforData(42) = "332334374044"
    semaforData(43) = "334134374142"
    semaforData(44) = "334234374143"
    semaforData(45) = "334334374144"
    semaforData(46) = "341134383942"
    semaforData(47) = "341234383943"
    semaforData(48) = "341334383944"
    semaforData(49) = "342134384042"
    semaforData(50) = "342234384043"
    semaforData(51) = "342334384044"
    semaforData(52) = "344134384142"
    semaforData(53) = "344234384143"
    semaforData(54) = "344334384144"
    semaforData(55) = "411135363942"
    semaforData(56) = "411235363943"
    semaforData(57) = "411335363944"
    semaforData(58) = "412135364042"
    semaforData(59) = "412235364043"
    semaforData(60) = "412335364044"
    semaforData(61) = "414135364142"
    semaforData(62) = "414235364143"
    semaforData(63) = "414335364144"
    semaforData(64) = "431135373942"
    semaforData(65) = "431235373943"
    semaforData(66) = "431335373944"
    semaforData(67) = "432135374042"
    semaforData(68) = "432235374043"
    semaforData(69) = "432335374044"
    semaforData(70) = "434135374142"
    semaforData(71) = "434235374143"
    semaforData(72) = "434335374144"
    semaforData(73) = "441135383942"
    semaforData(74) = "441235383943"
    semaforData(75) = "441335383944"
    semaforData(76) = "442135384042"
    semaforData(77) = "442235384043"
    semaforData(78) = "442335384044"
    semaforData(79) = "444135384142"
    semaforData(80) = "444235384143"
    semaforData(81) = "444335384144"

End Sub


Sub sviraj(fn)
    On Error Resume Next     'zvok requires mmsystem.dll
    If Game.mnuSound.Checked Then
        zvok = sndPlaySound(App.Path + "\sound\" & fn, 1)
    End If
    
End Sub

