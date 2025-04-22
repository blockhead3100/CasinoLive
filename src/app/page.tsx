import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Coins } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-4xl font-bold mb-4">Welcome to Lucky Ace</h1>
      <div className="flex flex-wrap justify-center gap-4">
        <Card className="w-80">
          <div className="p-4">
            <h2 className="text-2xl font-semibold mb-2">Virtual Slots</h2>
            <p className="text-muted-foreground">Experience the thrill of spinning reels.</p>
            <Button asChild>
              <a href="/slots">
                Play Slots
              </a>
            </Button>
          </div>
        </Card>
        <Card className="w-80">
          <div className="p-4">
            <h2 className="text-2xl font-semibold mb-2">Digital Card Games</h2>
            <p className="text-muted-foreground">Test your skills in card games like Blackjack and Poker.</p>
            <Button asChild>
              <a href="/card-games">
                Play Card Games
              </a>
            </Button>
          </div>
        </Card>
        <Card className="w-80">
          <div className="p-4">
            <h2 className="text-2xl font-semibold mb-2">Manage your funds</h2>
            <p className="text-muted-foreground">Deposit or withdraw Funds.</p>
            <Button asChild>
              <a href="/funds">
                <Coins className="mr-2 h-4 w-4" />
                Funds
              </a>
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
}
