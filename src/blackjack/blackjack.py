from .statehandling import state, draw_logo
from .gamelogic import Standing, print_standing

def game_loop():
    is_play_again = True
    while is_play_again:
        state.shuffle()
        state.initial_deal()

        draw_logo()

        state.bet()

        # print(f"Debug: { state.standing() }")
        is_hit = True

        state.draw_board(conceal_dealer=True)

        while state.standing() != Standing.PlayerBlackjack and state.standing() != Standing.PlayerBust and is_hit:
            if is_hit := input("Hit? (enter 'y' to draw another card): ") == "y":
                state.hit_player()
                state.draw_board(conceal_dealer=True)

        # NOTE: No need for dealer to play if Player is bust
        if state.standing() != Standing.PlayerBust:
            while state.standing() != Standing.DealerBlackjack and state.standing() != Standing.DealerBust and state.dealer_hand_value() < 17:
                state.hit_dealer()

        state.maybe_payout()
        state.draw_board(conceal_dealer=False)
        # print(f"Debug: { state.standing() }") 

        print_standing(state.standing())
        
        is_play_again = False if state.player_wallet <= 0 else True if input("Do you want keep going? (enter 'y' to continue): ") == 'y' else False
    if state.player_wallet <= 0:
        print("Game's Over! You have nothing left to bet with.")

def main():
    try:
        game_loop()

        if (state.player_wallet > 25):
            print(f"You've earned ${ state.player_wallet - 25 }. Congratulations! Bye!")
        else:
            print(f"You've lost ${ 25 - state.player_wallet }. Very unfortunate. Bye!")

    except KeyboardInterrupt:
        print(f"\nGame's Over.")

if __name__ == "__main__":
    main()
