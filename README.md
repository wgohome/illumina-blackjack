# Blackjack Application (Question 8)

Prepared for "Illumina Coding Challenge: 31516-JOB Informatics Software Engineer"

By [William Goh](mailto:wirriamm@gmail.com)

## Running the code

Requires `Python >= 3.10` (for the updated type hint support)

This is a CLI application. To enter, from the root directory of this repository, run

```bash
python main.py
```

To run the tests written,

- Install `pytest` with `pip`
- Run `pytest` from the root of the repository

If you do not have `Python >= 3.10` on your local, I have pushed a docker image from this app. You can pull a docker image from dockerhub and run:

```bash
docker pull wirriamm/illumina-blackjack
docker run -it wirriamm/illumina-blackjack
```

## Given Requirements

a. Graphics are not necessary

b. Support at least a dealer and one player

c. Figure out a simple way to display the players’ hands (e.g. text)

d. Correctly deal cards and keep track of the remaining cards in the deck (or decks)

e. The idea of Blackjack is to score higher than a Dealer’s hand without exceeding twenty-one. Cards count their value, except face cards (jacks, queens, kings) count for ten, and aces count for one. If you beat the Dealer, you get 10 points. If you get Blackjack (21 with just two cards) and beat the Dealer, you get 15 points.

f. The game starts by giving two cards (from a standard 52 card deck) to the Dealer (one face down) and two cards to the player. The player decides whether to Hit (get another card) or Stay. The player can continue to hit as many if desired. If the player exceeds 21 before staying, it is a loss (-10 points). If the player does not exceed 21, it becomes the dealer’s turn. The Dealer adds cards until 16 is exceeded. When this occurs, if the dealer also exceeds 21 or if his total is less than the player’s, he loses. If the dealer total is greater than the player total (and under 21), the dealer wins. If the dealer and player have the same total, it is a Push (no points added or subtracted).

g. Add the rule that says aces count for either one or eleven, whichever benefits the player.

h. Reshuffle the cards whenever there are fewer than fifteen (or so) cards remaining in the
deck.

## Interpretation and Implementation

Participants can refer to both the dealer and the players. Each game must have exactly one dealer and at least one other player.

For each player's turn, the logic goes like this:

![image](https://user-images.githubusercontent.com/59186927/171618234-431bf0b3-8f91-4053-82e0-56621d232a6c.png)

For the dealer's turn, the logic goes like this:

![image](https://user-images.githubusercontent.com/59186927/171619055-df3da711-7d12-4c24-a785-de70538c44ab.png)

## Assumptions

- When a player (not dealer) exceeds 21 at their own turn (before the dealer gets to play), the player will immediately be considered to have lost this round, lose 10 points, and surrender their card to the discard pile.

- Aces can only take values of 1 or 11, and it depends on whichever benefits the participant the most. We ignore the actual additional constraints in the real life game of Blackjack.

- Valid scores are within: `16 < score <= 21`

- Does not consider the rules of the Chinese Blackjack, where they would consider 5 cards unbusted is a special win. We do not take into account the 5 card limit in this program.

- The requirements specifies 2 participants, but the application can accomodate more than 2 participants. This leads to several further assumptions:

  - When the dealer's hand is busted (>21), then they loses points to as many surviving players, losing 10 points for each such player.

  - When the dealer gets blackjack, they get only 15 points once. All other players who got blackjack, and already collected their 15 points will still keep them.

  - If the `16 < dealer score <= 21`, then the dealer will duel with each surviving player and earn the 10 points for each player the dealer wins.

## Areas for improvement

- Can build into a GUI next

- Can further refactor to decouple the behaviour in Table class

- Can persist user name and scores to pick up where they left

- Requirements point (h) requires reshuffling when there is less than 15 cards. But since decks are reset and shuffled at the start of each round. This might not be expected unless the number of players get very huge - at which stage there could possibly be not enough cards to reshuffle too. I might have misunderstood the point and have left this out for now, and could work on it on further clarifications.
