'use client';

import { Layout } from 'lucide-react';

export default function TemplatesPage() {
  return (
    <div className="flex flex-col h-full">
      <main className="flex-1 overflow-y-auto p-6">
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <Layout className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <p className="text-muted-foreground">Templates page - Coming in Day 9</p>
          </div>
        </div>
      </main>
    </div>
  );
}
