
import { Card } from "@/components/ui/card";

export default function CardGamesPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-4xl font-bold mb-4">Digital Card Games</h1>
      <Card className="w-full max-w-md">
        <div className="p-4">
          <p className="text-muted-foreground">
            Play Blackjack, Poker, and more! (Feature coming soon)
          </p>
        </div>
      </Card>
    </div>
  );
}
