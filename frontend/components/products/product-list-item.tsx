'use client';

import { Product } from '@/types';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Edit, Trash2, Image as ImageIcon } from 'lucide-react';
import { formatPrice, formatDate } from '@/lib/utils';
import Image from 'next/image';

interface ProductListItemProps {
  product: Product;
  onEdit: (product: Product) => void;
  onDelete: (product: Product) => void;
}

export default function ProductListItem({
  product,
  onEdit,
  onDelete,
}: ProductListItemProps) {
  return (
    <div className="flex items-center gap-4 rounded-lg border p-4 transition-colors hover:bg-muted/50">
      {/* Image */}
      <div className="relative h-16 w-16 flex-shrink-0 overflow-hidden rounded-md bg-muted">
        {product.image_url ? (
          <Image
            src={product.image_url}
            alt={product.name}
            fill
            className="object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center">
            <ImageIcon className="h-6 w-6 text-muted-foreground" />
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 space-y-1">
        <h3 className="font-semibold">{product.name}</h3>
        <div className="flex items-center gap-2">
          <p className="text-lg font-bold">{formatPrice(product.price)}</p>
          {product.category && (
            <Badge variant="secondary" className="text-xs">
              {product.category}
            </Badge>
          )}
          {product.sku && (
            <span className="text-xs text-muted-foreground">
              SKU: {product.sku}
            </span>
          )}
        </div>
        {product.description && (
          <p className="line-clamp-1 text-sm text-muted-foreground">
            {product.description}
          </p>
        )}
      </div>

      {/* Date */}
      <div className="hidden text-sm text-muted-foreground lg:block">
        {formatDate(product.created_at)}
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        <Button
          size="sm"
          variant="outline"
          onClick={() => onEdit(product)}
        >
          <Edit className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          variant="outline"
          onClick={() => onDelete(product)}
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
