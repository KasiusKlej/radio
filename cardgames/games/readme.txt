
			*********************************
			*				*
			*	Card Games for One	*
			*	    for Windows		*
			*				*
			*********************************


	Contents
	1. ADDING NEW GAME
	1.0. Instructions on how to create your own card game.
	1.1  Detailed information on syntax
	2. CUSTOMISING CARD GAMES FOR ONE


                 ---            --- - - --                                                        
            - --     --    ---               - --                                                    
       ----             --         (p) 2000      --                                              
     -        (*)                                     -                                        
       -        made in ljubljana                      -- -                                    
        -         -                                        - -                                
         --    --   -                   (c) miha11@yahoo.com   -                             
           --        -                                          -                          
                      - -         - -         - -                -                      
                         - -    -    -       -    -             -                     
                              --      - -   -      - -         --                        
                                         - -           -   --                            
                                                         -                             
                                                                                        
                                                                                        
                                                                                        

	1. ADDING NEW GAME


	1.0. Instructions on how to create your own card game.

In case you know the rules of another card game for one player
and want to play it on your computer you will have to inscribe 
it into "CardGame.txt" file. You can add the following section
to the end of mentioned file:

-------------------------------------------------------------------------------
[GAMENAME]
My Example
Introduction, description, rules.

[START]
describing start positions (number, position, behaviour of columns)
(see other games for details)

[SPECIAL]
special rules and limitations

[ACTIONS]
redeal some columns, shuffle deck, autoplay, double click,...
rules of computing new situations

[FINISH]
conditions to end the game, scoring system,...
-------------------------------------------------------------------------------


	1.1  Detailed information on syntax





	1.1.1. Gamename section

  Game name can be any text (as can be all data).
Add introduction, description, and by all means rules of the game
one line after game name. 
  When you are using parameters don't use space, for example write 
overlap_x=200 and not overlap_x = 200.








	1.1.2. Start section

  The starting position must be described. Game usually starts with
some columns of cards on table. Column is an entity that gets selected 
and moved to another column by user. User can can usually pick a card 
or more from one column and move it to another if it fits there.


---- Syntax: --------------------------------------------------------------------
[START]					;beginning of section

[DECK]
set=c01,c02,c03,c04,c05,c06,c07,... 	;optional (52 cards and their order)
shuffle_now=1				;optional (use to shufle before new game starts)
many_decks=2				;n/a
[END DECK]

[COLUMNS]
column_name1, position, num_cards, shufle_any_cards 
column_name2, position, num_cards, shufle_any_cards 
column_name3, position, num_cards, shufle_any_cards 
[END COLUMNS]

[COLUMNS DEFAULTS]
overlap_x=200					;optional
overlap_y=350					;optional
zoom=0.75					;optional
[END COLUMNS DEFAULTS]

[COLUMNS BEHAVIOUR]
[column_name1]
max_cards=13					;max num of cards column accepts
suit=1						;=1 - card(s) moved on this column must match suit ascending
card_value=23
alternate=1					
suit_or_card=1
always_allowed_from_columns=0,4,5,6		;
custom_x=320					;pixels, custom position
custom_y=1490					;pixels
overlap_x=0					;pixels, don't set this if you dont want overlaping
overlap_y=default				;pixels or "default"
overlap=1					;n/a any card can be selected in overlaped column
player_can_put_card=no				;optional!
player_can_put_card_if_empty=s12,c12		;certain card(s) or "no" or "yes"(default)
player_can_take_card=yes
contents_at_start=c01,d12,d04,s01,h04,...	;c=clubs, d=diamond, h=hearts, s=spade, "next"
cards_face_up=1,1,1,1,1,...			;optional (use if you used use_facedowns)
dblclick_moves_to=2,3,11			;on double click try to move card to column 2,3 or 11
allways_facedown=1				;column is always face down but is ordinary column (mode1)
after_move_action=0-[action1]			;refers to action described in [ACTIONS] section
attempted_move_action=0,1,2-[action1]		;do action when move attempted from source columns
after_playermove_action=any-[action1]		;does action if player moved to this column from any column
attempted_playermove_action=any-movecolumn=3-1	;do action when player's move attempted from source column
use_facedown=1					;defines that some cards in this column will be face down (mode2)
aces_on_kings=no				;specify no to disable
[END COLUMNS BEHAVIOUR]
--------------------------------------------------------------------------------------















	______________________________________
	C O M M A N D S   A N D   S Y N T A X :
	--------------------------------------



[DECK]
 * set: Describes deck before the game starts. Deck of cards is used when 
starting a game. If some columns have defined contents_at_startup 
then exclude those cards from set(deck).
Whole set is:
set=c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,d01,d02,d03,d04,d05,d06,d07,d08,d09,d10,d11,d12,d13,h01,h02,h03,h04,h05,h06,h07,h08,h09,h10,h11,h12,h13,s01,s02,s03,s04,s05,s06,s07,s08,s09,s10,s11,s12,s13

 * shuffle_now: Set to 1 to shuffle cards in the deck.

 * many_decks: to use mor than one deck. Cards in other decks are named 
C,D,H,S, t,u,v,z, T,U,V,Z. Don't forget to include them in the set.
Don't specify if using only one deck.

[COLUMNS]
 * Column name: can be any text. The order of columns listed determines their
ids from 0 to n-1.

 * Position: There are 50 possible unique positions for columns. Position is coded by 
following table:

  00 01 02 03 04 05 06 07 08 09
  10 11 12 13 14 15 16 17 18 19
  ...
  40 41 42 43 44 45 46 47 48 49  

  If position for column you are describing doesnt fit the table
you could specify custom_x, custom_y (maybe in pixel). 
  In some columns all cards are visible so column takes more space on the table.
If there are verticaly or horizontal overlaping cards in column 
you should specify overlap_x and overlap_y (for verticaly overlap_x=0).

 * num_cards: Number of cards in column at begining of a game.

 * shufle_any_cards parameter (0=false, 1=true) means computer can
imediately display this column by dealing specified number of cards  
from previously shuffled deck. 
You must specify 0 if column has custom(predefined) contents_at_start!


[COLUMNS DEFAULTS]
Describes default values (see example).


[COLUMNS BEHAVIOUR]
 * contents_at_start: could be any of 52 cards described or could be "next"
to take next num_cards available cards from the deck. 

 * cards_face_up: defines wich cards (0) are face down at begining of a game.

 * suit: specify suit=1 or =0 or =any to limit what column will take
if user moves cards onto it. Suit option takes cards that MATCHES 
SUIT ("1"=ascending , "0"=descending "10"=next_in_rank or "any" order)

 * card_value: specify 1 if you want that column accepts cards that match
in value, specify 2 for ascending, 3 for descending(king accepts queen),
23 for alternate regardles of suit.

 * alternate: Matches red, black, red, black, ... (1=ascend, 0=descend, "any")

 * suit_or_card: Matches suit or card value. Queen of hearts could go to
any queen or any hearts card (specify =1). Any card could go (specify =any).

 * player_can_take_card: specify yes to make column take cards. If you don't 
specify it, the cards can't be taken.

 * player_can_put_card: specify yes if player can allways put card on column.
Don't specify if you want alternate, suit, ... options to take effect.
Specify column_id(s) if player can allways put card from those columns.
Don't specify if this column is only for taking cards from.

 * player_can_put_card_if_empty: certain card or "no" or "yes".
Specify this if you want column only to take card when empty.

 * always_allowed_from_columns: specify columns that can give card to this 
column regardles of other column conditions.

 * backstyle: defines appearance of column. 0=transparent 1=opaque

 * backcolor:  works only in opaque mode.
0	Black	8	Gray
1	Blue	9	Light Blue
2	Green	10	Light Green
3	Cyan	11	Light Cyan
4	Red	12	Light Red
5	Magenta	13	Light Magenta
6	Yellow	14	Light Yellow
7	White	15	Bright White

 * dblclick_moves_to: specify column(s) where player wants to move with double click.

 * allways_facedown: specify 1 if column is face down all the game (cards not visible 
but column behaves like any other).

 * after_move_action: to do some action (redeal etc) after card gets sucessfuly
moved from column(s) specified (or "any" column) to this column.

 * attempted_move_action: specify action that will cancel intended move and
do action described in [ACTIONS] section.

 * after_playermove_action: specify action that will happen after player sucessfuly moves 
to this column. 

 * attempted_playermove_action: specify action that will cancel player's intended move and
do action described in [ACTIONS] section. Useful if instead of one card, game
reqiures moving pile of cards. In that case you should use apropriate action.
  The above 4 actions which define how column behaves, can also be changed during 
a game with apropriate action.

 * use_facedowns: Set to 1 if the column requires some cards put face down during 
the game. Double click will turn card around when it is accesible. Facedown card
can't be selected and moved, it has to be double clicked first. Use_facedowns
function kind of doubles your computer's graphics abilities. Use_facedowns excludes
use of allways_facedown function, this two modes can't be used in same game.

 * aces_on_kings: by default aces can go on kings and vice versa. Specify no to restrict.





	1.1.3.  Special section (n/a)

  This section describes exceptions from the above rules. 




























	1.1.4.  Actions section

  This section describes actions. Action can be on user button or on
specific situation. Action usually recalculates columns in some way
or tries to make move (selects card and selects destination column).
  First type of actions are individual actions that get fired every time
a card is moved and new situation comes out. These are every_turn and if()then
actions. They are useful to simulate autoplay feature, etc. This actions act
as if the player is making them.
  Second type of action is block action that can include more commands. 
This actions are useful to redeal cards, check victory conditions, override
player's card move with pile move instead, apply special rules of card moving, 
etc. This actions act as if the system is making them (independently of rules 
of moving cards - if you say movecolumn, the column will be moved no matter what).
  Another special type of action is [autostart] action. Action of this name
gets fired at the beginnoing of the game.














--- Example: -----------------------------------------------------------------------------
[ACTIONS]
every_turn=0-7				;autoplay action
every_turn=parameter00=countempty(5,6)	;set parameter to be used later
every_turn=[beep_action]		;call action
if(empty_columns=0,1,2,3)then[action1]
parameter04=52				;every turn set parameter to be used later

[action1]
setparameter=parameter01=max(parameter00,52)		
setparameter=parameter02=min(parameter00,parameter01)
setparameter=parameter03=cardsrowed(5)		
movecolumn=3-1				;moves column regardless of restrictions
movecolumn=2-1
movecolumn=1-0				;move all cards to column 0
movepile=4,5-6				;top 4 cards from 5 to 6
movepile=4,5-parameter06		;top 4 cards from 5 to column remembered before
trymovepile=52,5-6			;finds deepest card in column5 that matches column6 and piles those cards to column6
ifduringaction(destination_card=d11,h11)then[action2]	
[]

[action2]
shufflecolumn=5				;shuffle column 5
turncolumn=5				;turns cards over
movecard=top,5-6			;n/a moves top card from column5 to column6
movecard=0,5-6				;n/a moves first (bottom) card from column5 to column6
trymovepile=parameter00,selected-6	;you can use keywords "parameterXX", "selected"
trymovepile=max,c1-c2			;syntax
autoplay				;trigers everyturn actions
turncard=col,pos			;n/a in column col turns card in position pos around
[]
------------------------------------------------------------------------------------------

  Action can include: 

 * every_turn: every_turn=0-7 example tries to move 1 card from column0 to column7 
every turn (every time after player moves a card). This is autoplay feature. It 
works only if autoplay option is chosen.
  Parameters can also be set with every_turn as well as with individual action. 
You can also set up to 20 parameter values (that can be later used in actions like 
trymovepile) with every_turn action. Be careful when setting parameters with every_turn 
action since every_turn actions only work when player uses "autoplay" option.
  You can also call action with every_turn.

 * if(condition)then[action]: 

  Condition can be:

	- empty_columns=: specify columns.
	- parameterXX=value, parameterXX=>value, parameterXX=<value


This 2 kind of individual actions get fired every turn (every time player moves a card).


 * seek_parameter=parameterXX=...

 Seek_parameter is special function that doesn act as action (that is, it doesn't 
cancel player's move). It is used with parameter. Seek can retreive source column, 
destination column in parameters. Seek seeks for numeric values.








  Action block can include: 

 * specific action: to call specific action that is declared in [actions] section
 * movecolumn: moves whole column. Move is enforced so destination restrictons don't count.
 * shufflecolumn: shuffles whole column.
 * turncolumn: turns column over first card becoming the last.
 * movecard: moves one card.
 * movepile: moves more cards.
 * faceup: turns card around.
 * trymovepile: calculates if move of more cards instead of one is possible 
to destination column acording to all its properties (alternate, suit, ...)
If move is possible and max parameter in not exceded a pile is moved.
Max parameter could be any number or "parameterXX". 
  Source column can be column's id or "selected" to use selected column
to move pile from (useful when alowing piling from any column). 
  Function trymovepile supposes that cards in source column are allready
in certain order (alternate etc). So if a pile of 4 cards is movable by
matching fourth card with destination column's top card, a pile is moved.
This is why this function is not so appropriate for game like Free Cell
but is for many other.

	  More on parameters:

	  Parameters are numeric values that get set during a game. They may be used
	to count how many empty columns there is or something like that. You can store 
	about 20 such parameters (parameter00, parameter01, ...) during a game. When 
	you need those values you can use them in functions like trymovepile.
	This function is useful as it can be specified to be called after player
	tries to move a card to certain column (see columns behaviour). In this case,
	instead of players intended card move, a pile is moved.

	  Functions you can use when seting parameters:

	 * you can of course specify any numeric value to parameter (like 
	parameter19=52)

	 * countempty(listed columns):  this functions returns how many of listed
	columns are empty.

	 * cardsrowed(column):  this functions returns how many upper cards in column
	matches column's alternate, suit, ... (Useful when you want only those
	cards when moving pile.). Parameter can be column number or "selected".

	 * source_column:  this function returns currently selected column. You
	might want to store returned numeric value in parameter for later use.

	 * weight_of(listed columns):  this functions returns how many cards are there.


 * ifduringaction: works like if function but doesnt get fired every time card moves. It
accepts parameters:

	 * destination_card=listed cards:  checks if card where move was intended
	is in the list.
	 * parameterXX=value, parameterXX=>value, parameterXX=<value: checks if one of 
	the 20 parameters has specified	value.

	EXAMPLE:
		[action_move_pile_to_column_8]
		setparameter=parameter01=countempty(9,10,11)
		increase(parameter01)
		ifduringaction(destination_card=d11,h11)thenparameter01=52
		trymovepile=parameter01,selected-8
		[]


 * turntopcard: if top card in specified column is face down this action turns
card up.




	1.1.5.  Finish section

  This section describes winning (or loosing) situation.

--Example:--------------------------
[FINISH]
[VICTORY]
empty_columns=8,9,10,11,12,13,14,15
[DEFEAT]
empty_columns=0
------------------------------------
  This example defines that "You win" happens when 8 columns are empty.
And "you loose" when first column has no more cards. 

empty_columns: specify column id (columns start from 0)






	2. CUSTOMISING CARD GAMES FOR ONE



  To customize the game you can modify "CardGame.ini" file.
Be carefull to keep all sections in predefined order.

--- Example: -----
[LOADPICTURES]
no
[ANIMATE]
no
[LOADWHATPICTURES]
.jpg
[ZOOM]
0.9
[CARDSIZE]
1365
2010
[CARDGAPX]
120
[CARDGAPY]
120
[SCREEN_RESOLUTION_FACTOR]
1
[LOADWHATPICTURESPREFIX]
800x600
[PICTURESRESIZEABLE]
no
[LANGUAGE]
slo
multilanguage=yes
askforlanguage=yes
[SHAREWARE]
SerialNumber=AMFHEBNEBFLPENFHGBMN
[SETUPCARDSIZE]
yes
------------------

  You can set loadpictures to yes if you want new card deck. 
In this case you would need 52+1 picture files named "c01.bmp",
"c02.bmp", ... , "s013.bmp" and "face.bmp". (where Clubs=c, 
Diamonds=d, Hearts=h, Spade=s). Might also be jpg picture format.

  Set animation to yes to enable tutorial animation.

[LOADWHATPICTURES] and [LOADWHATPICTURESPREFIX] define file name that 
can be for example "800x600h03.jpg" in your \deck folder. What pictures 
in this case would be .jpg and prefix in this case is "800x600".

[ZOOM] is 1 (100%) when you play at full screen.

[CARDSIZE],[CARDGAPX],[CARDGAPY] also define card size and inbetween space.
You can use default640x480, default800x600, default1024x768 as card size
parameters. They match included card set sizes. If you use included jpg
set of pictures, use loadpictures=yes, loadwhatpictures=.jpg, card size=
1365 and 2012.

[SCREEN_RESOLUTION_FACTOR] is 1 when you play at full screen and 
defines card positions on your screen.

[PICTURESRESIZEABLE] set to no can speed up game performance.
First line after [LANGUAGE] defines file name of described language. Don't 
specify it (leave the line empty) if you want English. For example: type slo
if you wish to play considering "CardGame - slo.txt" and "slo.txt".
Switches multilanguage=yes and askforlanguage=yes defines weather switching 
between languages are allowed and weather CardGames ask for language at the 
beginning of the game.

[SHAREWARE] section restricts some games to unregistered users.
When you register, first letter of serial number is set to "R".
When you register to certain games (+Free Cell) first letter is "P",
and other 18 letters are "J" for registered game, "A" for unregistered.
Letter 20 is anything.
When you are not registered you get serial number starting with "A" and
any other 19 letters. Not all of the games will be available at start.

[SETUPCARDSIZE]
Is "yes" to adapt to right screen resolution. Used only once at first run.





