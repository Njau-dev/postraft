'use client';

import { useEffect, useState } from 'react';
import { Product } from '@/types';
import { useCreateProduct, useUpdateProduct, useUploadProductImage } from '@/hooks/useProducts';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Upload,
  X,
  Image as ImageIcon,
  Package,
  Tag,
  DollarSign,
  Hash,
  FileText,
  Loader2,
  Sparkles
} from 'lucide-react';
import Image from 'next/image';
import { Card, CardContent } from '@/components/ui/card';

interface ProductFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  product?: Product | null;
}

export default function ProductFormDialog({
  open,
  onOpenChange,
  product,
}: ProductFormDialogProps) {
  const isEdit = !!product;
  const createProduct = useCreateProduct();
  const updateProduct = useUpdateProduct();
  const uploadImage = useUploadProductImage();

  const [formData, setFormData] = useState({
    name: '',
    price: '',
    category: '',
    sku: '',
    description: '',
  });
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  // Populate form when editing
  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name,
        price: product.price.toString(),
        category: product.category || '',
        sku: product.sku || '',
        description: product.description || '',
      });
      setImagePreview(product.image_url || null);
    } else {
      setFormData({
        name: '',
        price: '',
        category: '',
        sku: '',
        description: '',
      });
      setImagePreview(null);
    }
    setImageFile(null);
  }, [product, open]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        setImageFile(file);
        const reader = new FileReader();
        reader.onloadend = () => {
          setImagePreview(reader.result as string);
        };
        reader.readAsDataURL(file);
      }
    }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = {
        name: formData.name,
        price: parseFloat(formData.price),
        category: formData.category || undefined,
        sku: formData.sku || undefined,
        description: formData.description || undefined,
      };

      if (isEdit && product) {
        // Update product
        await updateProduct.mutateAsync({ id: product.id, data });

        // Upload image if changed
        if (imageFile) {
          await uploadImage.mutateAsync({ id: product.id, file: imageFile });
        }
      } else {
        // Create product
        const newProduct = await createProduct.mutateAsync(data);

        // Upload image if provided
        if (imageFile && newProduct.id) {
          await uploadImage.mutateAsync({ id: newProduct.id, file: imageFile });
        }
      }

      onOpenChange(false);
    } catch (error) {
      // Error handled by mutations
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl border-2 border-primary/20">
        <DialogHeader className="space-y-3">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-primary/10 p-2">
              {isEdit ? (
                <Package className="h-6 w-6 text-primary" />
              ) : (
                <Sparkles className="h-6 w-6 text-primary" />
              )}
            </div>
            <div>
              <DialogTitle className="text-2xl">
                {isEdit ? 'Edit Product' : 'Add New Product'}
              </DialogTitle>
              <DialogDescription>
                {isEdit
                  ? 'Update product details and regenerate designs'
                  : 'Add a new product to generate social media designs'}
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Image Upload Section */}
          <Card className="border-2">
            <CardContent className="p-6">
              <Label className="text-lg font-semibold">Product Image</Label>
              <p className="mb-4 text-sm text-muted-foreground">
                Upload a high-quality image for better design generation
              </p>

              <div
                className={`relative rounded-xl border-2 border-dashed p-8 text-center transition-colors ${dragActive
                  ? 'border-primary bg-primary/10'
                  : 'border-muted-foreground/25 hover:border-primary/50'
                  }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  id="image"
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  className="hidden"
                />

                {imagePreview ? (
                  <div className="relative mx-auto max-w-xs">
                    <div className="relative h-48 w-full overflow-hidden rounded-lg">
                      <Image
                        src={imagePreview}
                        alt="Preview"
                        fill
                        className="object-cover"
                      />
                    </div>
                    <div className="mt-4 flex items-center justify-center gap-3">
                      <Label
                        htmlFor="image"
                        className="cursor-pointer rounded-md border border-input bg-background px-4 py-2 hover:bg-accent hover:text-accent-foreground"
                      >
                        Change Image
                      </Label>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setImageFile(null);
                          setImagePreview(product?.image_url || null);
                        }}
                        className="text-destructive hover:text-destructive"
                      >
                        <X className="mr-2 h-4 w-4" />
                        Remove
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-secondary">
                      <Upload className="h-10 w-10 text-muted-foreground" />
                    </div>
                    <div className="space-y-2">
                      <Label
                        htmlFor="image"
                          className="cursor-pointer text-primary hover:underline"
                        >
                          Click to upload
                        </Label>
                        <p className="text-sm text-muted-foreground">or drag and drop</p>
                        <p className="text-xs text-muted-foreground">
                          PNG, JPG, WEBP up to 10MB
                        </p>
                      </div>
                    </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Product Details Section */}
          <Card className="border-2">
            <CardContent className="p-6">
              <Label className="text-lg font-semibold">Product Details</Label>
              <p className="mb-6 text-sm text-muted-foreground">
                Fill in the product information
              </p>

              <div className="space-y-6">
                {/* Product Name */}
                <div className="space-y-2">
                  <Label htmlFor="name" className="flex items-center gap-2">
                    <Package className="h-4 w-4" />
                    Product Name *
                  </Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="e.g., Premium Coffee Beans 500g"
                    className="border-2"
                    required
                  />
                </div>

                {/* Price & Category */}
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="price" className="flex items-center gap-2">
                      <DollarSign className="h-4 w-4" />
                      Price (KES) *
                    </Label>
                    <Input
                      id="price"
                      type="number"
                      step="0.01"
                      min="0"
                      value={formData.price}
                      onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                      placeholder="0.00"
                      className="border-2"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="category" className="flex items-center gap-2">
                      <Tag className="h-4 w-4" />
                      Category
                    </Label>
                    <Input
                      id="category"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      placeholder="e.g., Beverages, Groceries"
                      className="border-2"
                    />
                  </div>
                </div>

                {/* SKU */}
                <div className="space-y-2">
                  <Label htmlFor="sku" className="flex items-center gap-2">
                    <Hash className="h-4 w-4" />
                    SKU (Stock Keeping Unit)
                  </Label>
                  <Input
                    id="sku"
                    value={formData.sku}
                    onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                    placeholder="e.g., COFFEE-500G-PREM"
                    className="border-2"
                  />
                </div>

                {/* Description */}
                <div className="space-y-2">
                  <Label htmlFor="description" className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    Description
                  </Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) =>
                      setFormData({ ...formData, description: e.target.value })
                    }
                    placeholder="Describe your product for better AI design generation..."
                    className="min-h-32 border-2"
                  />
                  <p className="text-xs text-muted-foreground">
                    Detailed descriptions help generate better designs
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Footer */}
          <DialogFooter className="gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={loading}
              className="border-2"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={loading}
              className="gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : isEdit ? (
                <>
                  <Sparkles className="h-4 w-4" />
                  Update & Regenerate Designs
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" />
                  Create Product
                </>
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}