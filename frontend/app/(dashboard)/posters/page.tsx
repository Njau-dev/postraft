'use client';

import EmptyState from '@/components/shared/EmptyState';
import { Image } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function PostersPage() {
  const router = useRouter();

  return (
    <div className="flex flex-col h-full">

      <main className="flex-1 overflow-y-auto p-6">
        <EmptyState
          icon={Image}
          title="No posters yet"
          description="Generate your first poster using products and templates"
          action={{
            label: 'Generate Posters',
            onClick: () => router.push('/posters/generate'),
          }}
        />
      </main>
    </div>
  );
}
