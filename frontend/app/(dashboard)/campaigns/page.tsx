'use client';

import { Megaphone } from 'lucide-react';

export default function CampaignsPage() {
  return (
    <div className="flex flex-col h-full">
      <main className="flex-1 overflow-y-auto p-6">
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <Megaphone className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <p className="text-muted-foreground">Campaigns page - Coming later</p>
          </div>
        </div>
      </main>
    </div>
  );
}
