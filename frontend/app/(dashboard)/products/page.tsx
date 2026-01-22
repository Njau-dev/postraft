'use client';

import EmptyState from '@/components/shared/EmptyState';
import { Package } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function ProductsPage() {
  const router = useRouter();

  return (
    <div className="flex flex-col h-full">
      <main className="flex-1 overflow-y-auto p-6">
        <EmptyState
          icon={Package}
          title="No products yet"
          description="Add your first product to start generating posters"
          action={{
            label: 'Add Product',
            onClick: () => router.push('/products/add'),
          }}
        />
      </main>
    </div>
  );
}
