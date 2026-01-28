import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import { Template } from '@/types';
import { toast } from 'sonner';

// Get all templates
export function useTemplates(format?: string) {
    return useQuery<Template[]>({
        queryKey: ['templates', format],
        queryFn: async () => {
            const params = format ? `?format=${format}` : '';
            const response = await api.get(`/templates${params}`);
            return response.data.data.templates;
        },
    });
}
// Get single template
export function useTemplate(id: number) {
    return useQuery<Template>({
        queryKey: ['template', id],
        queryFn: async () => {
            const response = await api.get(`/templates/${id}`);
            return response.data.data;
        },
        enabled: !!id,
    });
}
// Create template
export function useCreateTemplate() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (data: Partial<Template>) => {
            const response = await api.post('/templates', data);
            return response.data.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['templates'] });
            toast.success('Template created successfully');
        },
        onError: (error: any) => {
            const message = error.response?.data?.error || 'Failed to create template';
            toast.error(message);
        },
    });
}
// Update template
export function useUpdateTemplate() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async ({ id, data }: { id: number; data: Partial<Template> }) => {
            const response = await api.put(`/templates/${id}`, data);
            return response.data.data;
        },
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: ['templates'] });
            queryClient.invalidateQueries({ queryKey: ['template', variables.id] });
            toast.success('Template updated successfully');
        },
        onError: (error: any) => {
            const message = error.response?.data?.error || 'Failed to update template';
            toast.error(message);
        },
    });
}
// Delete template
export function useDeleteTemplate() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (id: number) => {
            await api.delete(`/templates/${id}`);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['templates'] });
            toast.success('Template deleted successfully');
        },
        onError: (error: any) => {
            const message = error.response?.data?.error || 'Failed to delete template';
            toast.error(message);
        },
    });
}
// Duplicate template
export function useDuplicateTemplate() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (id: number) => {
            const response = await api.post(`/templates/${id}/duplicate`);
            return response.data.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['templates'] });
            toast.success('Template duplicated successfully');
        },
        onError: (error: any) => {
            const message = error.response?.data?.error || 'Failed to duplicate template';
            toast.error(message);
        },
    });
}