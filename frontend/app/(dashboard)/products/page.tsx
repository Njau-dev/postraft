'use client';

import { useState } from 'react';
import { useProducts, useCategories, useDeleteProduct } from '@/hooks/useProducts';
import EmptyState from '@/components/shared/empty-state';
import ProductFormDialog from '@/components/products/product-form-dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import {
  Package,
  Plus,
  Search,
  Loader2,
  MoreHorizontal,
  Edit,
  Trash2,
  Image as ImageIcon,
  Filter,
  Download,
  Sparkles
} from 'lucide-react';
import { Product } from '@/types';
import Image from 'next/image';
import { formatCurrency } from '@/lib/utils';

export default function ProductsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [page, setPage] = useState(1);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [productToDelete, setProductToDelete] = useState<Product | null>(null);

  // Fetch data
  const { data, isLoading, isError } = useProducts({
    search: searchQuery || undefined,
    category: selectedCategory !== 'all' ? selectedCategory : undefined,
    page,
    per_page: 20,
  });

  const { data: categories } = useCategories();
  const deleteProduct = useDeleteProduct();

  const handleEdit = (product: Product) => {
    setEditingProduct(product);
    setDialogOpen(true);
  };

  const handleDelete = (product: Product) => {
    setProductToDelete(product);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (productToDelete) {
      await deleteProduct.mutateAsync(productToDelete.id);
      setDeleteDialogOpen(false);
      setProductToDelete(null);
    }
  };

  const handleAddNew = () => {
    setEditingProduct(null);
    setDialogOpen(true);
  };

  const handleGenerateDesign = (product: Product) => {
    // TODO: Implement design generation
    console.log('Generate design for:', product);
  };

  return (
    <div className="min-h-screen bg-linear-to-b from-background to-secondary/10 p-6">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Products</h1>
              <p className="text-muted-foreground">
                Manage your products and generate stunning social media designs
              </p>
            </div>
            <Button onClick={handleAddNew} size="lg" className="gap-2">
              <Plus className="h-4 w-4" />
              Add Product
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="mb-8 grid gap-4 md:grid-cols-3">
          <Card className="border-2 border-primary/10">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Products</p>
                  <p className="text-3xl font-bold">{data?.total || 0}</p>
                </div>
                <div className="rounded-lg bg-primary/10 p-3">
                  <Package className="h-6 w-6 text-primary" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-2 border-blue-500/10">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Ready for Design</p>
                  <p className="text-3xl font-bold">{data?.products?.filter(p => p.image_url).length || 0}</p>
                </div>
                <div className="rounded-lg bg-blue-500/10 p-3">
                  <Sparkles className="h-6 w-6 text-blue-500" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-2 border-green-500/10">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Categories</p>
                  <p className="text-3xl font-bold">{categories?.length || 0}</p>
                </div>
                <div className="rounded-lg bg-green-500/10 p-3">
                  <Filter className="h-6 w-6 text-green-500" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters Card */}
        <Card className="mb-6 border-2">
          <CardHeader className="pb-3">
            <CardTitle>Filters</CardTitle>
            <CardDescription>
              Search and filter your products
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              {/* Search */}
              <div className="relative flex-1 md:max-w-md">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search products by name, SKU, or category..."
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setPage(1);
                  }}
                  className="pl-10 border-2"
                />
              </div>

              {/* Category Filter */}
              <div className="flex items-center gap-3">
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger className="w-48 border-2">
                    <SelectValue placeholder="All Categories" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    {categories?.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {cat}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Products Table Card */}
        <Card className="border-2 overflow-hidden">
          <CardHeader className="bg-secondary/50">
            <CardTitle>Product Catalog</CardTitle>
            <CardDescription>
              {data ? `Showing ${data.products.length} of ${data.total} products` : 'Loading products...'}
            </CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            {/* Loading State */}
            {isLoading && (
              <div className="p-6">
                {Array.from({ length: 5 }).map((_, i) => (
                  <div key={i} className="flex items-center space-x-4 p-4 border-b">
                    <Skeleton className="h-12 w-12 rounded-lg" />
                    <div className="space-y-2 flex-1">
                      <Skeleton className="h-4 w-1/4" />
                      <Skeleton className="h-4 w-1/2" />
                    </div>
                    <Skeleton className="h-10 w-24" />
                  </div>
                ))}
              </div>
            )}

            {/* Error State */}
            {isError && (
              <div className="p-6 text-center">
                <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-8">
                  <p className="text-destructive font-semibold">
                    Failed to load products. Please try again.
                  </p>
                </div>
              </div>
            )}

            {/* Empty State */}
            {!isLoading && data && data.total === 0 && !searchQuery && (
              <div className="p-12">
                <EmptyState
                  icon={Package}
                  title="No products yet"
                  description="Add your first product to start generating beautiful social media designs"
                  action={{
                    label: 'Add Your First Product',
                    onClick: handleAddNew,
                    icon: Plus,
                  }}
                />
              </div>
            )}

            {/* No Results */}
            {!isLoading && data && data.total === 0 && searchQuery && (
              <div className="p-12">
                <EmptyState
                  icon={Search}
                  title="No products found"
                  description={`No products match "${searchQuery}"`}
                  action={{
                    label: 'Clear Search',
                    onClick: () => setSearchQuery(''),
                    variant: 'outline',
                  }}
                />
              </div>
            )}

            {/* Products Table */}
            {!isLoading && data && data.total > 0 && (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader className="bg-secondary/30">
                    <TableRow>
                      <TableHead className="w-12">#</TableHead>
                      <TableHead className="w-24">Image</TableHead>
                      <TableHead>Product Details</TableHead>
                      <TableHead className="w-32">Price</TableHead>
                      <TableHead className="w-32">Category</TableHead>
                      <TableHead className="w-48">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {data.products.map((product, index) => (
                      <TableRow key={product.id} className="hover:bg-secondary/20">
                        <TableCell className="font-medium">
                          {((page - 1) * data.per_page) + index + 1}
                        </TableCell>
                        <TableCell>
                          <div className="relative h-16 w-16 overflow-hidden rounded-lg border">
                            {product.image_url ? (
                              <Image
                                src={product.image_url}
                                alt={product.name}
                                fill
                                className="object-cover"
                              />
                            ) : (
                              <div className="flex h-full items-center justify-center bg-secondary">
                                <ImageIcon className="h-6 w-6 text-muted-foreground" />
                              </div>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div>
                            <p className="font-semibold">{product.name}</p>
                            {product.sku && (
                              <p className="text-sm text-muted-foreground">SKU: {product.sku}</p>
                            )}
                            {product.description && (
                              <p className="text-sm text-muted-foreground line-clamp-1">
                                {product.description}
                              </p>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="font-semibold text-base">
                            {formatCurrency(product.price)}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {product.category ? (
                            <Badge variant="secondary">{product.category}</Badge>
                          ) : (
                            <span className="text-muted-foreground">—</span>
                          )}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Button
                              size="sm"
                              variant="outline"
                              className="gap-1"
                              onClick={() => handleGenerateDesign(product)}
                            >
                              <Sparkles className="h-3 w-3" />
                              Generate
                            </Button>
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="icon">
                                  <MoreHorizontal className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end">
                                <DropdownMenuLabel>Actions</DropdownMenuLabel>
                                <DropdownMenuSeparator />
                                <DropdownMenuItem onClick={() => handleEdit(product)}>
                                  <Edit className="mr-2 h-4 w-4" />
                                  Edit Product
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleGenerateDesign(product)}>
                                  <Sparkles className="mr-2 h-4 w-4" />
                                  Generate Design
                                </DropdownMenuItem>
                                <DropdownMenuItem>
                                  <Download className="mr-2 h-4 w-4" />
                                  Export Data
                                </DropdownMenuItem>
                                <DropdownMenuSeparator />
                                <DropdownMenuItem
                                  onClick={() => handleDelete(product)}
                                  className="text-destructive"
                                >
                                  <Trash2 className="mr-2 h-4 w-4" />
                                  Delete
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>

          {/* Pagination */}
          {data && data.pages > 1 && (
            <div className="border-t p-4">
              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">
                  Showing {((page - 1) * data.per_page) + 1} to{' '}
                  {Math.min(page * data.per_page, data.total)} of {data.total} products
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    onClick={() => setPage(page - 1)}
                    disabled={!data.has_prev}
                    size="sm"
                  >
                    Previous
                  </Button>
                  <span className="text-sm font-medium">
                    Page {page} of {data.pages}
                  </span>
                  <Button
                    variant="outline"
                    onClick={() => setPage(page + 1)}
                    disabled={!data.has_next}
                    size="sm"
                  >
                    Next
                  </Button>
                </div>
              </div>
            </div>
          )}
        </Card>
      </div>

      {/* Enhanced Product Form Dialog */}
      <ProductFormDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        product={editingProduct}
      />

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent className="border-2 border-destructive/20">
          <AlertDialogHeader>
            <div className="flex items-center gap-3">
              <div className="rounded-full bg-destructive/10 p-2">
                <Trash2 className="h-6 w-6 text-destructive" />
              </div>
              <div>
                <AlertDialogTitle>Delete Product</AlertDialogTitle>
                <AlertDialogDescription>
                  This action cannot be undone. This will permanently delete the product
                  and all associated designs.
                </AlertDialogDescription>
              </div>
            </div>
          </AlertDialogHeader>
          <div className="my-4 rounded-lg bg-secondary/50 p-4">
            <p className="font-semibold">{productToDelete?.name}</p>
            <p className="text-sm text-muted-foreground">
              {productToDelete?.sku && `SKU: ${productToDelete.sku} • `}
              Price: {formatCurrency(productToDelete?.price || 0)}
            </p>
          </div>
          <AlertDialogFooter>
            <AlertDialogCancel variant="outline">Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={confirmDelete}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete Product
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}