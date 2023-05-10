import pandas as pd

User = pd.read_csv("Phase_3/demo_data/Demo Data/Users.tsv",sep="\t")
User["postal_code"]=User["postal_code"].astype(str)
User["postal_code"]=User["postal_code"].apply(lambda x:x.zfill(5))
User = User.rename(columns={"postal_code":"fk_postal_code"})
User.to_csv("Phase_3/demo_data/User.csv",index=False)

Trade = pd.read_csv("Phase_3/demo_data/Demo Data/Trades.tsv",sep="\t")
Trade = Trade.rename(columns={"item_proposed":"proposedItemNum","item_desired":"desiredItemNum","date_proposed":"proposedDate","date_reviewed":"decisionDate","accepted":"status"})
Trade["status"]=Trade["status"].apply(lambda x: "Accepted" if x==1 else "Rejected" if x==0 else "Pending")
Trade.to_csv("Phase_3/demo_data/Trade.csv",index=False)

Item = pd.read_csv("Phase_3/demo_data/Demo Data/Items.tsv",sep="\t")
Item = Item.rename(columns={"item_number":"itemNumber","email":"fk_email"})

BoardGame = Item.loc[Item["type"]=="Board Game",]
BoardGame = BoardGame[["itemNumber"]].rename(columns={"itemNumber":"fk_itemNumber"})
BoardGame.to_csv("Phase_3/demo_data/BoardGame.csv",index=False)

CollectiveCardGame = Item.loc[Item["type"]=="Collectible Card Game",]
CollectiveCardGame = CollectiveCardGame[["itemNumber","card_count"]].rename(columns={"itemNumber":"fk_itemNumber","card_count":"cardsOffered"})
CollectiveCardGame.to_csv("Phase_3/demo_data/CollectiveCardGame.csv",index=False)

ComputerGame = Item.loc[Item["type"]=="Computer Game",]
ComputerGame = ComputerGame[["itemNumber","platform"]].rename(columns={"itemNumber":"fk_itemNumber","platform":"computerPlatform"})
ComputerGame.to_csv("Phase_3/demo_data/ComputerGame.csv",index=False)

PlayingCardGame = Item.loc[Item["type"]=="Playing Card Game",]
PlayingCardGame = PlayingCardGame[["itemNumber"]].rename(columns={"itemNumber":"fk_itemNumber"})
PlayingCardGame.to_csv("Phase_3/demo_data/PlayingCardGame.csv",index=False)

VideoGame = Item.loc[Item["type"]=="Video Game",]
VideoGame = VideoGame[["itemNumber","media"]].rename(columns={"itemNumber":"fk_itemNumber"})
VideoGame.to_csv("Phase_3/demo_data/VideoGame.csv",index=False)

VideoGamePlatform = Item.loc[Item["type"]=="Video Game",]
VideoGamePlatform = VideoGamePlatform[["itemNumber","platform"]].rename(columns={"itemNumber":"fk_VideoGame_itemNumber"})
VideoGamePlatform.to_csv("Phase_3/demo_data/VideoGamePlatform.csv",index=False)


Item = Item[["itemNumber","fk_email","title","condition","description"]]
Item.to_csv("Phase_3/demo_data/Item.csv",index=False)
