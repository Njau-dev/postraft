import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import { Product } from '@/types';
import { toast } from 'sonner';

interface ProductsResponse {
  products: Product[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

interface ProductFilters {
  category?: string;
  search?: string;
  page?: number;
  per_page?: number;
}

// Get all products
export function useProducts(filters?: ProductFilters) {
  return useQuery<ProductsResponse>({
    queryKey: ['products', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters?.category) params.append('category', filters.category);
      if (filters?.search) params.append('search', filters.search);
      if (filters?.page) params.append('page', filters.page.toString());
      if (filters?.per_page) params.append('per_page', filters.per_page.toString());

      const response = await api.get(`/products?${params.toString()}`);
      return response.data.data;
    },
  });
}

// Get single product
export function useProduct(id: number) {
  return useQuery<Product>({
    queryKey: ['product', id],
    queryFn: async () => {
      const response = await api.get(`/products/${id}`);
      return response.data.data;
    },
    enabled: !!id,
  });
}

// Get categories
export function useCategories() {
  return useQuery<string[]>({
    queryKey: ['product-categories'],
    queryFn: async () => {
      const response = await api.get('/products/categories');
      return response.data.data.categories;
    },
  });
}

// Create product
export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: Partial<Product>) => {
      const response = await api.post('/products', data);
      return response.data.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['product-categories'] });
      toast.success('Product created successfully');
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Failed to create product';
      toast.error(message);
    },
  });
}

// Update product
export function useUpdateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Product> }) => {
      const response = await api.put(`/products/${id}`, data);
      return response.data.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['product', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['product-categories'] });
      toast.success('Product updated successfully');
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Failed to update product';
      toast.error(message);
    },
  });
}

// Delete product
export function useDeleteProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/products/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['product-categories'] });
      toast.success('Product deleted successfully');
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Failed to delete product';
      toast.error(message);
    },
  });
}

// Upload product image
export function useUploadProductImage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, file }: { id: number; file: File }) => {
      const formData = new FormData();
      formData.append('image', file);

      const response = await api.post(`/products/${id}/image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
      queryClient.invalidateQueries({ queryKey: ['product', variables.id] });
      toast.success('Image uploaded successfully');
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Failed to upload image';
      toast.error(message);
    },
  });
}
