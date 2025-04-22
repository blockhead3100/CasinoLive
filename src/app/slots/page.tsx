
import { Card } from "@/components/ui/card";

export default function SlotsPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-4xl font-bold mb-4">Virtual Slots</h1>
      <Card className="w-full max-w-md">
        <div className="p-4">
          <p className="text-muted-foreground">
            Spin the reels and test your luck! (Feature coming soon)
          </p>
        </div>
      </Card>
    </div>
  );
}
