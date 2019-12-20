# cardpacks

```py

f = Deck() #Standard, uses standard Playing Card pack

#Also included is other packs (limited for now, more to come)

f = Deck(pack=FrenchStrippedPlayingPack) #0-9 numbered cards only
# Also available is TarotNouveauPack and TarotArcanaPack

# Once you have a deck, you can

f.shuffle()

#and

card = f.pull()
# card is now a randomly drawn card from the deck, it has various values based on the pack itself
# But the default packs try to be consistent, they have a .name, .value, and when represented as string, they show a format of "the VALUE of CLASS" or something similar.
