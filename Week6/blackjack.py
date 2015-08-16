# Mini-project #6 - Blackjack

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cardlist = []

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for card in self.cardlist:
            ans += str(card) + " "
        return "Hand Contains "+ ans.strip()

    def add_card(self, card):
        # add a card object to a hand
        self.cardlist.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        total = 0
        aces = 0
        for card in self.cardlist:
            rank = card.get_rank()
            value = VALUES.get(rank)
            if value == 1:
                aces += 1
            total += value
        while aces > 0 and total + 10 <= 21:
            total += 10
            aces -= 1
        return total
                           
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        count = 0
        for card in self.cardlist:
            card.draw(canvas, [pos[0] + count*(CARD_SIZE[0]+15), pos[1]])
            count += 1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cardlist = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cardlist.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cardlist)

    def deal_card(self):
        # deal a card object from the deck
        return self.cardlist.pop()
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for card in self.cardlist:
            ans += str(card) + " "
        return ans.strip()


#define event handlers for buttons
def deal():
    global outcome, score, in_play, curr_deck, player_hand, dealer_hand
    if in_play:
        outcome = "Quitter. You lose."
        score -= 1
        in_play = False
    else :
        outcome = ""
        curr_deck = Deck()
        curr_deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(curr_deck.deal_card())
        dealer_hand.add_card(curr_deck.deal_card())
        player_hand.add_card(curr_deck.deal_card())
        dealer_hand.add_card(curr_deck.deal_card())
        in_play = True

def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global outcome, score, in_play
    if in_play:
        player_hand.add_card(curr_deck.deal_card())
        val = player_hand.get_value()
        if val > 21:
            outcome = "You went bust and lose"
            in_play = False
            score -= 1
       
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global outcome, in_play, score
    if in_play:
        dealer_value = dealer_hand.get_value()
        player_value = player_hand.get_value()
        while dealer_value < 17:
            dealer_hand.add_card(curr_deck.deal_card())
            dealer_value = dealer_hand.get_value()
        in_play = False
        if dealer_value >= player_value:
            if dealer_value > 21:
                outcome = "Dealer went bust. You win"
                score += 1
            else:
                outcome = "Dealer has higher hand. You lose"
                score -= 1
        else:
            outcome = "You have a higher hand. You win"
            score += 1

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome
    canvas.draw_text("BlackJack", [225, 50], 40, "Cyan")
    canvas.draw_text("Dealer", [50, 120], 30, "Black")
    dealer_hand.draw(canvas, [50, 160])
    canvas.draw_text("Player", [50, 350], 30, "Black")
    player_hand.draw(canvas, [50, 390])
    canvas.draw_text(outcome, [180, 120], 30, "Black")
    canvas.draw_text("Score : "+str(score), [450, 80], 30, "Black")
    if in_play:
        canvas.draw_text("Hit or Stand ?", [180, 350], 30, "Black")
        source_center = CARD_BACK_CENTER
        canvas.draw_image(card_back, source_center, CARD_BACK_SIZE, [50 + CARD_BACK_SIZE[0]/2, 160 + CARD_BACK_SIZE[1]/2], CARD_BACK_SIZE)
    else:
        canvas.draw_text("New Deal ?", [180, 350], 30, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric