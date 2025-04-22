import { Card } from "@/components/ui/card";

export default function FundsPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-4xl font-bold mb-4">Funds Management</h1>
      <Card className="w-full max-w-md">
        <div className="p-4">
          <p className="text-muted-foreground">
            Deposit or withdraw funds.(Feature coming soon)
          </p>
        </div>
      </Card>
    </div>
  );
}
